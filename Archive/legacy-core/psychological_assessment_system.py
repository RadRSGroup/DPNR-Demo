# Multi-Model Psychological Assessment System
# Production-ready implementation using CrewAI, PostgreSQL, and modern Python patterns

import asyncio
import json
import uuid
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass
from enum import Enum
import numpy as np
from pydantic import BaseModel, Field, validator
import asyncpg
import openai
import cohere
from crewai import Agent, Task, Crew, Process
from transformers import pipeline
import websockets
from contextlib import asynccontextmanager
import hashlib
import redis.asyncio as redis
from sentence_transformers import SentenceTransformer

# ===============================================================================
# CONFIGURATION AND SETUP
# ===============================================================================

@dataclass
class Config:
    openai_api_key: str
    cohere_api_key: str
    database_url: str
    redis_url: str
    embedding_model: str = "text-embedding-3-large"
    max_concurrent_assessments: int = 100
    confidence_threshold: float = 0.75
    recursive_max_depth: int = 3

config = Config(
    openai_api_key="your-openai-key",
    cohere_api_key="your-cohere-key", 
    database_url="postgresql://user:pass@localhost/psych_db",
    redis_url="redis://localhost:6379"
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ===============================================================================
# CORE DATA MODELS
# ===============================================================================

class AssessmentType(str, Enum):
    ENNEAGRAM = "enneagram"
    BIG_FIVE = "big_five"
    EMOTIONAL_INTELLIGENCE = "emotional_intelligence"
    VALUES = "values"
    COGNITIVE_STYLE = "cognitive_style"

class ConfidenceLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class UserInput(BaseModel):
    user_id: str = Field(..., min_length=5, max_length=50)
    text: str = Field(..., min_length=10, max_length=5000)
    assessment_types: List[AssessmentType] = Field(default_factory=lambda: list(AssessmentType))
    context: Optional[Dict[str, Any]] = Field(default_factory=dict)
    
    @validator('text')
    def validate_meaningful_content(cls, v):
        if v.strip().count(' ') < 3:
            raise ValueError('Response must contain meaningful content')
        return v

class PersonalityScore(BaseModel):
    trait: str
    score: float = Field(..., ge=0.0, le=1.0)
    confidence: float = Field(..., ge=0.0, le=1.0)
    evidence: List[str] = Field(default_factory=list)

class AssessmentResult(BaseModel):
    assessment_id: str
    user_id: str
    assessment_type: AssessmentType
    scores: List[PersonalityScore]
    overall_confidence: float
    requires_followup: bool
    followup_questions: List[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    processing_time_ms: int

class RecursivePrompt(BaseModel):
    question: str
    context: str
    expected_insights: List[str]
    confidence_threshold: float = 0.75

# ===============================================================================
# DATABASE LAYER
# ===============================================================================

class DatabaseManager:
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.pool = None
    
    async def initialize(self):
        self.pool = await asyncpg.create_pool(
            self.database_url,
            min_size=5,
            max_size=20,
            command_timeout=30
        )
        await self._create_tables()
        logger.info("Database initialized successfully")
    
    async def _create_tables(self):
        async with self.pool.acquire() as conn:
            # Enable pgvector extension
            await conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
            
            # Users table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    user_id VARCHAR(50) UNIQUE NOT NULL,
                    created_at TIMESTAMPTZ DEFAULT NOW(),
                    metadata JSONB DEFAULT '{}',
                    gdpr_consent BOOLEAN DEFAULT FALSE,
                    data_retention_end TIMESTAMPTZ
                )
            """)
            
            # Assessments table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS assessments (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    user_id VARCHAR(50) REFERENCES users(user_id),
                    assessment_type VARCHAR(50) NOT NULL,
                    input_text TEXT NOT NULL,
                    scores JSONB NOT NULL,
                    confidence FLOAT NOT NULL,
                    embedding VECTOR(1536),
                    requires_followup BOOLEAN DEFAULT FALSE,
                    followup_questions JSONB DEFAULT '[]',
                    processing_time_ms INTEGER,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                )
            """)
            
            # Create indexes
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_assessments_user_type 
                ON assessments(user_id, assessment_type)
            """)
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_assessments_embedding 
                ON assessments USING hnsw (embedding vector_l2_ops)
            """)
    
    async def save_assessment(self, result: AssessmentResult, embedding: List[float]):
        async with self.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO assessments (
                    user_id, assessment_type, input_text, scores, confidence,
                    embedding, requires_followup, followup_questions, processing_time_ms
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            """, 
                result.user_id,
                result.assessment_type.value,
                "",  # Store separately if needed
                json.dumps([score.dict() for score in result.scores]),
                result.overall_confidence,
                embedding,
                result.requires_followup,
                json.dumps(result.followup_questions),
                result.processing_time_ms
            )
    
    async def find_similar_profiles(self, embedding: List[float], assessment_type: str, limit: int = 5):
        async with self.pool.acquire() as conn:
            rows = await conn.fetch("""
                SELECT user_id, scores, confidence,
                       1 - (embedding <=> $1) as similarity
                FROM assessments 
                WHERE assessment_type = $2
                ORDER BY embedding <=> $1 
                LIMIT $3
            """, embedding, assessment_type, limit)
            return [dict(row) for row in rows]

# ===============================================================================
# NLP PROCESSING PIPELINE
# ===============================================================================

class NLPPipeline:
    def __init__(self):
        self.sentiment_analyzer = pipeline(
            "sentiment-analysis",
            model="cardiffnlp/twitter-roberta-base-sentiment-latest"
        )
        self.emotion_analyzer = pipeline(
            "text-classification",
            model="j-hartmann/emotion-english-distilroberta-base"
        )
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    
    async def analyze_text(self, text: str) -> Dict[str, Any]:
        # Run analyses in parallel
        sentiment_task = asyncio.create_task(self._analyze_sentiment(text))
        emotion_task = asyncio.create_task(self._analyze_emotions(text))
        embedding_task = asyncio.create_task(self._generate_embedding(text))
        
        sentiment, emotions, embedding = await asyncio.gather(
            sentiment_task, emotion_task, embedding_task
        )
        
        return {
            "sentiment": sentiment,
            "emotions": emotions,
            "embedding": embedding,
            "text_stats": self._extract_text_stats(text)
        }
    
    async def _analyze_sentiment(self, text: str) -> Dict[str, float]:
        result = self.sentiment_analyzer(text)[0]
        return {"label": result["label"], "score": result["score"]}
    
    async def _analyze_emotions(self, text: str) -> List[Dict[str, float]]:
        results = self.emotion_analyzer(text)
        return [{"emotion": r["label"], "score": r["score"]} for r in results]
    
    async def _generate_embedding(self, text: str) -> List[float]:
        embedding = self.embedding_model.encode(text)
        return embedding.tolist()
    
    def _extract_text_stats(self, text: str) -> Dict[str, Any]:
        words = text.split()
        return {
            "word_count": len(words),
            "avg_word_length": sum(len(w) for w in words) / len(words) if words else 0,
            "sentence_count": text.count('.') + text.count('!') + text.count('?'),
            "complexity_score": len(set(words)) / len(words) if words else 0
        }

# ===============================================================================
# PSYCHOLOGICAL ASSESSMENT PROCESSORS
# ===============================================================================

class BaseProcessor:
    def __init__(self, nlp_pipeline: NLPPipeline):
        self.nlp = nlp_pipeline
        self.confidence_threshold = 0.75
    
    async def process(self, text: str, context: Dict[str, Any]) -> Tuple[List[PersonalityScore], float]:
        raise NotImplementedError
    
    def calculate_confidence(self, scores: List[PersonalityScore]) -> float:
        if not scores:
            return 0.0
        return sum(score.confidence for score in scores) / len(scores)

class EnneagramProcessor(BaseProcessor):
    def __init__(self, nlp_pipeline: NLPPipeline):
        super().__init__(nlp_pipeline)
        self.type_patterns = {
            "type_1": ["perfect", "correct", "should", "must", "proper", "right", "wrong"],
            "type_2": ["help", "care", "love", "need", "support", "others", "giving"],
            "type_3": ["success", "achieve", "win", "goal", "efficient", "image", "best"],
            "type_4": ["unique", "special", "different", "deep", "missing", "authentic"],
            "type_5": ["understand", "knowledge", "private", "observe", "analyze"],
            "type_6": ["security", "safe", "trust", "loyal", "doubt", "authority"],
            "type_7": ["fun", "exciting", "options", "adventure", "positive", "avoid"],
            "type_8": ["control", "power", "strong", "direct", "justice", "protect"],
            "type_9": ["peace", "harmony", "conflict", "comfortable", "agree", "merge"]
        }
    
    async def process(self, text: str, context: Dict[str, Any]) -> Tuple[List[PersonalityScore], float]:
        nlp_analysis = await self.nlp.analyze_text(text)
        text_lower = text.lower()
        
        scores = []
        for type_name, patterns in self.type_patterns.items():
            pattern_matches = sum(1 for pattern in patterns if pattern in text_lower)
            score = min(pattern_matches / len(patterns), 1.0)
            
            # Adjust based on sentiment and emotions
            sentiment_boost = 0.1 if nlp_analysis["sentiment"]["score"] > 0.8 else 0
            confidence = min(score + sentiment_boost, 1.0)
            
            evidence = [pattern for pattern in patterns if pattern in text_lower]
            
            scores.append(PersonalityScore(
                trait=type_name,
                score=score,
                confidence=confidence,
                evidence=evidence
            ))
        
        overall_confidence = self.calculate_confidence(scores)
        return scores, overall_confidence

class BigFiveProcessor(BaseProcessor):
    def __init__(self, nlp_pipeline: NLPPipeline):
        super().__init__(nlp_pipeline)
        self.trait_patterns = {
            "openness": ["creative", "imaginative", "curious", "artistic", "novel"],
            "conscientiousness": ["organized", "disciplined", "careful", "thorough"],
            "extraversion": ["outgoing", "social", "energetic", "talkative", "assertive"],
            "agreeableness": ["kind", "cooperative", "trusting", "helpful", "sympathetic"],
            "neuroticism": ["anxious", "worried", "stressed", "moody", "emotional"]
        }
    
    async def process(self, text: str, context: Dict[str, Any]) -> Tuple[List[PersonalityScore], float]:
        nlp_analysis = await self.nlp.analyze_text(text)
        text_lower = text.lower()
        
        scores = []
        for trait, patterns in self.trait_patterns.items():
            pattern_matches = sum(1 for pattern in patterns if pattern in text_lower)
            base_score = pattern_matches / len(patterns)
            
            # Adjust based on text complexity for openness
            if trait == "openness":
                complexity_boost = nlp_analysis["text_stats"]["complexity_score"] * 0.2
                base_score += complexity_boost
            
            score = min(base_score, 1.0)
            confidence = 0.8 if score > 0.3 else 0.5
            evidence = [pattern for pattern in patterns if pattern in text_lower]
            
            scores.append(PersonalityScore(
                trait=trait,
                score=score,
                confidence=confidence,
                evidence=evidence
            ))
        
        overall_confidence = self.calculate_confidence(scores)
        return scores, overall_confidence

class EmotionalIntelligenceProcessor(BaseProcessor):
    def __init__(self, nlp_pipeline: NLPPipeline):
        super().__init__(nlp_pipeline)
        self.domains = {
            "self_awareness": ["feel", "emotion", "recognize", "aware", "understand myself"],
            "self_regulation": ["control", "manage", "calm", "adapt", "regulate"],
            "social_awareness": ["others", "empathy", "read", "understand people"],
            "relationship_management": ["communicate", "influence", "resolve", "collaborate"]
        }
    
    async def process(self, text: str, context: Dict[str, Any]) -> Tuple[List[PersonalityScore], float]:
        nlp_analysis = await self.nlp.analyze_text(text)
        text_lower = text.lower()
        
        scores = []
        emotion_diversity = len(nlp_analysis["emotions"])
        
        for domain, patterns in self.domains.items():
            pattern_matches = sum(1 for pattern in patterns if pattern in text_lower)
            base_score = pattern_matches / len(patterns)
            
            # Boost for emotional vocabulary diversity
            emotion_boost = min(emotion_diversity * 0.1, 0.3)
            score = min(base_score + emotion_boost, 1.0)
            
            confidence = 0.9 if emotion_diversity > 3 else 0.6
            evidence = [pattern for pattern in patterns if pattern in text_lower]
            
            scores.append(PersonalityScore(
                trait=domain,
                score=score,
                confidence=confidence,
                evidence=evidence
            ))
        
        overall_confidence = self.calculate_confidence(scores)
        return scores, overall_confidence

# ===============================================================================
# CONFIDENCE SCORING AND RECURSIVE PROMPTING
# ===============================================================================

class ConfidenceScorer:
    def __init__(self):
        self.min_confidence = 0.5
        self.high_confidence = 0.8
    
    def assess_overall_confidence(self, assessment_results: Dict[str, Tuple[List[PersonalityScore], float]]) -> float:
        if not assessment_results:
            return 0.0
        
        confidences = [conf for _, conf in assessment_results.values()]
        return sum(confidences) / len(confidences)
    
    def identify_low_confidence_areas(self, assessment_results: Dict[str, Tuple[List[PersonalityScore], float]]) -> List[str]:
        low_confidence_areas = []
        for assessment_type, (scores, confidence) in assessment_results.items():
            if confidence < self.min_confidence:
                low_confidence_areas.append(assessment_type)
        return low_confidence_areas
    
    def calculate_entropy(self, scores: List[PersonalityScore]) -> float:
        if not scores:
            return 1.0
        
        values = [score.score for score in scores]
        # Normalize to probabilities
        total = sum(values) if sum(values) > 0 else 1
        probs = [v/total for v in values]
        
        # Calculate entropy
        entropy = -sum(p * np.log2(p + 1e-10) for p in probs if p > 0)
        return entropy / np.log2(len(probs))  # Normalize

class RecursivePromptGenerator:
    def __init__(self, openai_client):
        self.client = openai_client
        self.max_depth = 3
        
        self.recursive_prompts = {
            "enneagram": {
                "type_1": "You mention valuing structure. When do you choose flexibility over rules?",
                "type_2": "You seem focused on helping others. What happens when your needs aren't met?",
                "type_3": "Achievement appears important to you. How do you define success?",
                "type_4": "You value authenticity. What makes you feel most understood?",
                "type_5": "You prefer understanding before acting. When do you trust your gut?",
                "type_6": "Security seems important. How do you build confidence in uncertainty?",
                "type_7": "You enjoy possibilities. What helps you stay focused when needed?",
                "type_8": "You value control. When is it hardest to let others lead?",
                "type_9": "You seek harmony. When do you speak up despite potential conflict?"
            },
            "big_five": {
                "openness": "How do you typically respond to completely new experiences?",
                "conscientiousness": "Describe your approach to long-term goals versus immediate desires.",
                "extraversion": "What energizes you more: social interaction or solitude?",
                "agreeableness": "How do you handle situations where you disagree with others?",
                "neuroticism": "What strategies do you use when feeling overwhelmed?"
            }
        }
    
    async def generate_followup_questions(self, assessment_type: str, low_confidence_traits: List[str]) -> List[str]:
        questions = []
        
        if assessment_type in self.recursive_prompts:
            for trait in low_confidence_traits:
                if trait in self.recursive_prompts[assessment_type]:
                    questions.append(self.recursive_prompts[assessment_type][trait])
        
        # Generate additional dynamic questions using LLM
        if len(questions) < 3:
            dynamic_questions = await self._generate_dynamic_questions(assessment_type, low_confidence_traits)
            questions.extend(dynamic_questions)
        
        return questions[:3]  # Limit to 3 questions max
    
    async def _generate_dynamic_questions(self, assessment_type: str, traits: List[str]) -> List[str]:
        prompt = f"""
        Generate 2-3 insightful follow-up questions for a {assessment_type} personality assessment.
        Focus on these areas where confidence is low: {', '.join(traits)}
        
        Questions should be:
        - Personal but not invasive
        - Focused on behavior and preferences
        - Designed to reveal personality patterns
        - Clear and easy to understand
        
        Format as a simple list, one question per line.
        """
        
        try:
            response = await self.client.chat.completions.acreate(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.7
            )
            
            content = response.choices[0].message.content.strip()
            questions = [q.strip() for q in content.split('\n') if q.strip()]
            return questions[:2]
            
        except Exception as e:
            logger.error(f"Error generating dynamic questions: {e}")
            return []

# ===============================================================================
# CREWAI AGENTS
# ===============================================================================

class PsychologicalAssessmentCrew:
    def __init__(self, db_manager: DatabaseManager, nlp_pipeline: NLPPipeline):
        self.db = db_manager
        self.nlp = nlp_pipeline
        self.processors = {
            AssessmentType.ENNEAGRAM: EnneagramProcessor(nlp_pipeline),
            AssessmentType.BIG_FIVE: BigFiveProcessor(nlp_pipeline),
            AssessmentType.EMOTIONAL_INTELLIGENCE: EmotionalIntelligenceProcessor(nlp_pipeline)
        }
        self.confidence_scorer = ConfidenceScorer()
        self.prompt_generator = RecursivePromptGenerator(openai.AsyncOpenAI())
        
        # Create agents
        self.diagnostic_agent = self._create_diagnostic_agent()
        self.validation_agent = self._create_validation_agent()
        self.empathy_agent = self._create_empathy_agent()
    
    def _create_diagnostic_agent(self) -> Agent:
        return Agent(
            role="Clinical Diagnostic Specialist",
            goal="Conduct comprehensive psychological assessment across multiple frameworks",
            backstory="Expert in psychological evaluation with focus on evidence-based assessment and multi-model validation",
            memory=True,
            allow_delegation=True,
            verbose=True
        )
    
    def _create_validation_agent(self) -> Agent:
        return Agent(
            role="Assessment Validator",
            goal="Ensure assessment quality and identify areas requiring follow-up",
            backstory="Specialist in psychological test validation and confidence scoring",
            memory=True,
            verbose=True
        )
    
    def _create_empathy_agent(self) -> Agent:
        return Agent(
            role="Empathetic Response Coordinator",
            goal="Provide compassionate and contextually appropriate responses",
            backstory="Expert in therapeutic communication and emotional support",
            memory=True,
            verbose=True
        )
    
    async def process_assessment(self, user_input: UserInput) -> AssessmentResult:
        start_time = asyncio.get_event_loop().time()
        
        # Run all requested assessments in parallel
        assessment_tasks = {}
        for assessment_type in user_input.assessment_types:
            if assessment_type in self.processors:
                task = asyncio.create_task(
                    self.processors[assessment_type].process(
                        user_input.text, 
                        user_input.context
                    )
                )
                assessment_tasks[assessment_type] = task
        
        # Wait for all assessments to complete
        assessment_results = {}
        for assessment_type, task in assessment_tasks.items():
            try:
                scores, confidence = await task
                assessment_results[assessment_type] = (scores, confidence)
            except Exception as e:
                logger.error(f"Error processing {assessment_type}: {e}")
                assessment_results[assessment_type] = ([], 0.0)
        
        # Calculate overall confidence and determine if follow-up needed
        overall_confidence = self.confidence_scorer.assess_overall_confidence(assessment_results)
        low_confidence_areas = self.confidence_scorer.identify_low_confidence_areas(assessment_results)
        
        requires_followup = overall_confidence < 0.7 or len(low_confidence_areas) > 0
        followup_questions = []
        
        if requires_followup:
            # Generate follow-up questions for low confidence areas
            for area in low_confidence_areas[:2]:  # Limit to 2 areas
                questions = await self.prompt_generator.generate_followup_questions(
                    area, [score.trait for score, _ in assessment_results.get(area, ([], 0))[0] if score.confidence < 0.6]
                )
                followup_questions.extend(questions)
        
        # Combine all scores
        all_scores = []
        for scores, _ in assessment_results.values():
            all_scores.extend(scores)
        
        # Create result
        end_time = asyncio.get_event_loop().time()
        processing_time_ms = int((end_time - start_time) * 1000)
        
        result = AssessmentResult(
            assessment_id=str(uuid.uuid4()),
            user_id=user_input.user_id,
            assessment_type=user_input.assessment_types[0] if user_input.assessment_types else AssessmentType.BIG_FIVE,
            scores=all_scores,
            overall_confidence=overall_confidence,
            requires_followup=requires_followup,
            followup_questions=followup_questions,
            processing_time_ms=processing_time_ms
        )
        
        # Save to database
        nlp_analysis = await self.nlp.analyze_text(user_input.text)
        await self.db.save_assessment(result, nlp_analysis["embedding"])
        
        return result

# ===============================================================================
# REAL-TIME WEBSOCKET HANDLER
# ===============================================================================

class WebSocketHandler:
    def __init__(self, assessment_crew: PsychologicalAssessmentCrew):
        self.crew = assessment_crew
        self.active_sessions = {}
        self.redis_client = None
    
    async def initialize(self):
        self.redis_client = await redis.from_url(config.redis_url)
        logger.info("WebSocket handler initialized")
    
    async def handle_connection(self, websocket, path):
        session_id = str(uuid.uuid4())
        self.active_sessions[session_id] = {
            'websocket': websocket,
            'user_id': None,
            'conversation_history': [],
            'assessment_state': {}
        }
        
        logger.info(f"New WebSocket connection: {session_id}")
        
        try:
            await websocket.send(json.dumps({
                'type': 'connection_established',
                'session_id': session_id,
                'message': 'Welcome to the psychological assessment system'
            }))
            
            async for message in websocket:
                await self._process_message(session_id, message)
                
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"WebSocket connection closed: {session_id}")
        except Exception as e:
            logger.error(f"WebSocket error for session {session_id}: {e}")
        finally:
            if session_id in self.active_sessions:
                del self.active_sessions[session_id]
    
    async def _process_message(self, session_id: str, message: str):
        try:
            data = json.loads(message)
            session = self.active_sessions[session_id]
            
            if data['type'] == 'start_assessment':
                await self._handle_start_assessment(session, data)
            elif data['type'] == 'user_response':
                await self._handle_user_response(session, data)
            elif data['type'] == 'get_results':
                await self._handle_get_results(session, data)
            
        except Exception as e:
            logger.error(f"Error processing message for session {session_id}: {e}")
            await self._send_error(session_id, str(e))
    
    async def _handle_start_assessment(self, session: Dict, data: Dict):
        session['user_id'] = data.get('user_id', str(uuid.uuid4()))
        session['assessment_types'] = data.get('assessment_types', ['big_five'])
        
        await session['websocket'].send(json.dumps({
            'type': 'assessment_started',
            'message': 'Please describe yourself, your preferences, and how you typically behave in various situations.',
            'prompt': 'Tell me about yourself - how do you approach relationships, work, challenges, and what motivates you?'
        }))
    
    async def _handle_user_response(self, session: Dict, data: Dict):
        user_text = data.get('text', '')
        session['conversation_history'].append(user_text)
        
        # Create assessment input
        user_input = UserInput(
            user_id=session['user_id'],
            text=user_text,
            assessment_types=[AssessmentType(t) for t in session['assessment_types']],
            context={'conversation_history': session['conversation_history']}
        )
        
        # Process assessment
        result = await self.crew.process_assessment(user_input)
        session['assessment_state']['last_result'] = result
        
        # Send results and follow-up if needed
        response = {
            'type': 'assessment_result',
            'confidence': result.overall_confidence,
            'requires_followup': result.requires_followup,
            'processing_time_ms': result.processing_time_ms
        }
        
        if result.requires_followup and result.followup_questions:
            response['type'] = 'followup_needed'
            response['questions'] = result.followup_questions
            response['message'] = 'I need a bit more information to provide accurate results.'
        else:
            response['scores'] = [score.dict() for score in result.scores]
            response['message'] = 'Assessment complete! Here are your results.'
        
        await session['websocket'].send(json.dumps(response))
    
    async def _handle_get_results(self, session: Dict, data: Dict):
        if 'last_result' not in session['assessment_state']:
            await session['websocket'].send(json.dumps({
                'type': 'error',
                'message': 'No assessment results available. Please complete an assessment first.'
            }))
            return
        
        result = session['assessment_state']['last_result']
        response = {
            'type': 'final_results',
            'assessment_id': result.assessment_id,
            'scores': [score.dict() for score in result.scores],
            'overall_confidence': result.overall_confidence,
            'processing_time_ms': result.processing_time_ms,
            'timestamp': result.timestamp.isoformat()
        }
        
        await session['websocket'].send(json.dumps(response))
    
    async def _send_error(self, session_id: str, error_message: str):
        if session_id in self.active_sessions:
            await self.active_sessions[session_id]['websocket'].send(json.dumps({
                'type': 'error',
                'message': error_message
            }))

# ===============================================================================
# MAIN APPLICATION
# ===============================================================================

class PsychologicalAssessmentSystem:
    def __init__(self, config: Config):
        self.config = config
        self.db_manager = DatabaseManager(config.database_url)
        self.nlp_pipeline = NLPPipeline()
        self.assessment_crew = None
        self.websocket_handler = None
    
    async def initialize(self):
        await self.db_manager.initialize()
        
        self.assessment_crew = PsychologicalAssessmentCrew(
            self.db_manager, 
            self.nlp_pipeline
        )
        
        self.websocket_handler = WebSocketHandler(self.assessment_crew)
        await self.websocket_handler.initialize()
        
        logger.info("Psychological Assessment System initialized successfully")
    
    async def start_websocket_server(self, host: str = "localhost", port: int = 8765):
        logger.info(f"Starting WebSocket server on {host}:{port}")
        
        async def handler(websocket, path):
            await self.websocket_handler.handle_connection(websocket, path)
        
        start_server = websockets.serve(handler, host, port)
        await start_server
        logger.info("WebSocket server started")
    
    async def process_single_assessment(self, user_input: UserInput) -> AssessmentResult:
        return await self.assessment_crew.process_assessment(user_input)

# ===============================================================================
# EXAMPLE USAGE AND TESTING
# ===============================================================================

async def main():
    # Initialize system
    system = PsychologicalAssessmentSystem(config)
    await system.initialize()
    
    # Example single assessment
    user_input = UserInput(
        user_id="test_user_001",
        text="I'm someone who really values getting things done correctly. I pay attention to details and often notice when things aren't quite right. I prefer having clear structure and guidelines to follow. When working in groups, I sometimes get frustrated when others are careless or don't follow proper procedures.",
        assessment_types=[AssessmentType.ENNEAGRAM, AssessmentType.BIG_FIVE],
        context={"source": "api_test"}
    )
    
    result = await system.process_single_assessment(user_input)
    
    print("Assessment Results:")
    print(f"Assessment ID: {result.assessment_id}")
    print(f"Overall Confidence: {result.overall_confidence:.2f}")
    print(f"Processing Time: {result.processing_time_ms}ms")
    print(f"Requires Follow-up: {result.requires_followup}")
    
    if result.followup_questions:
        print("\nFollow-up Questions:")
        for i, question in enumerate(result.followup_questions, 1):
            print(f"{i}. {question}")
    
    print("\nDetailed Scores:")
    for score in result.scores:
        print(f"- {score.trait}: {score.score:.2f} (confidence: {score.confidence:.2f})")
        if score.evidence:
            print(f"  Evidence: {', '.join(score.evidence)}")
    
    # Start WebSocket server for real-time assessments
    print("\nStarting WebSocket server...")
    await system.start_websocket_server()

if __name__ == "__main__":
    asyncio.run(main())