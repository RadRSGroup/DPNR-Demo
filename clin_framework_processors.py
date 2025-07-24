# Enhanced Framework-Specific Processors with Clinical-Grade Models and Advanced Linguistic Analysis

from typing import Dict, List, Tuple, Any, Optional
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch
import spacy
from collections import Counter
import re
from textstat import flesch_reading_ease, flesch_kincaid_grade
import nltk
from nltk import pos_tag, word_tokenize
from nltk.corpus import stopwords
from sentence_transformers import SentenceTransformer

class ClinicalLinguisticAnalyzer:
    """Advanced linguistic feature extraction for clinical assessment"""
    
    def __init__(self):
        # Load spaCy model for advanced NLP
        self.nlp = spacy.load("en_core_web_lg")
        
        # Clinical-grade models
        self.clinical_pipeline = pipeline(
            "text-classification",
            model="mental-health/mental-roberta-base",
            device=0 if torch.cuda.is_available() else -1
        )
        
        self.therapy_sentiment = pipeline(
            "sentiment-analysis",
            model="j-hartmann/therapy-sentiment-roberta-base",
            device=0 if torch.cuda.is_available() else -1
        )
        
        # Initialize LIWC-style categories
        self._initialize_liwc_categories()
        
    def _initialize_liwc_categories(self):
        """Initialize LIWC-style word categories for psychological assessment"""
        self.liwc_categories = {
            "i_words": ["i", "me", "my", "mine", "myself"],
            "we_words": ["we", "us", "our", "ours", "ourselves"],
            "negation": ["no", "not", "never", "nothing", "nowhere", "neither", "nobody", "none"],
            "anxiety_words": ["nervous", "anxious", "worried", "scared", "afraid", "panic", "stress"],
            "anger_words": ["angry", "mad", "frustrated", "annoyed", "furious", "rage", "hate"],
            "sadness_words": ["sad", "depressed", "lonely", "miserable", "hopeless", "grief", "sorrow"],
            "cognitive_words": ["think", "know", "believe", "understand", "realize", "remember", "forget"],
            "certainty_words": ["always", "never", "definitely", "certainly", "absolutely", "surely"],
            "tentative_words": ["maybe", "perhaps", "possibly", "might", "could", "probably", "guess"],
            "achievement_words": ["accomplish", "achieve", "success", "goal", "win", "best", "proud"],
            "power_words": ["control", "influence", "lead", "manage", "dominate", "authority", "command"],
            "affiliation_words": ["friend", "together", "share", "companion", "ally", "partner", "team"]
        }
    
    def extract_clinical_features(self, text: str) -> Dict[str, Any]:
        """Extract comprehensive clinical and linguistic features"""
        doc = self.nlp(text)
        
        # Basic text statistics
        words = [token.text.lower() for token in doc if not token.is_punct]
        sentences = list(doc.sents)
        
        # Clinical risk assessment
        clinical_results = self.clinical_pipeline(text)
        therapy_sentiment = self.therapy_sentiment(text)
        
        # Linguistic complexity
        complexity_features = self._extract_complexity_features(text, doc)
        
        # Syntactic patterns
        syntactic_features = self._extract_syntactic_features(doc)
        
        # Semantic coherence
        semantic_features = self._extract_semantic_features(doc)
        
        # Emotional and cognitive markers
        psycholinguistic_features = self._extract_psycholinguistic_features(words, doc)
        
        # Temporal orientation
        temporal_features = self._extract_temporal_features(doc)
        
        return {
            "clinical_indicators": {
                "risk_assessment": clinical_results,
                "therapy_sentiment": therapy_sentiment,
                "overall_risk_score": self._calculate_risk_score(clinical_results)
            },
            "complexity": complexity_features,
            "syntactic": syntactic_features,
            "semantic": semantic_features,
            "psycholinguistic": psycholinguistic_features,
            "temporal": temporal_features,
            "text_statistics": {
                "word_count": len(words),
                "sentence_count": len(sentences),
                "avg_word_length": np.mean([len(w) for w in words]) if words else 0,
                "avg_sentence_length": np.mean([len(sent.text.split()) for sent in sentences]) if sentences else 0
            }
        }
    
    def _extract_complexity_features(self, text: str, doc) -> Dict[str, float]:
        """Extract text complexity features"""
        return {
            "flesch_reading_ease": flesch_reading_ease(text) if len(text) > 100 else 0,
            "flesch_kincaid_grade": flesch_kincaid_grade(text) if len(text) > 100 else 0,
            "lexical_diversity": len(set([t.lemma_ for t in doc if not t.is_punct])) / len(doc) if len(doc) > 0 else 0,
            "avg_syllables_per_word": self._calculate_avg_syllables(doc),
            "complex_word_ratio": self._calculate_complex_word_ratio(doc)
        }
    
    def _extract_syntactic_features(self, doc) -> Dict[str, Any]:
        """Extract syntactic patterns relevant to psychological assessment"""
        pos_counts = Counter([token.pos_ for token in doc])
        dep_counts = Counter([token.dep_ for token in doc])
        
        # Passive voice detection
        passive_count = sum(1 for sent in doc.sents if self._is_passive(sent))
        
        # Subordinate clauses
        subordinate_count = dep_counts.get('mark', 0) + dep_counts.get('ccomp', 0)
        
        return {
            "pos_distribution": dict(pos_counts),
            "dependency_patterns": dict(dep_counts),
            "passive_voice_ratio": passive_count / len(list(doc.sents)) if doc.sents else 0,
            "subordinate_clause_ratio": subordinate_count / len(list(doc.sents)) if doc.sents else 0,
            "noun_verb_ratio": pos_counts.get('NOUN', 0) / (pos_counts.get('VERB', 0) + 1),
            "adjective_ratio": pos_counts.get('ADJ', 0) / len(doc) if len(doc) > 0 else 0
        }
    
    def _extract_semantic_features(self, doc) -> Dict[str, float]:
        """Extract semantic coherence and topic consistency"""
        sentences = list(doc.sents)
        if len(sentences) < 2:
            return {"coherence_score": 1.0, "topic_consistency": 1.0}
        
        # Calculate sentence embeddings
        embedder = SentenceTransformer('all-MiniLM-L6-v2')
        sentence_texts = [sent.text for sent in sentences]
        embeddings = embedder.encode(sentence_texts)
        
        # Coherence: average similarity between consecutive sentences
        coherence_scores = []
        for i in range(len(embeddings) - 1):
            similarity = np.dot(embeddings[i], embeddings[i+1]) / (np.linalg.norm(embeddings[i]) * np.linalg.norm(embeddings[i+1]))
            coherence_scores.append(similarity)
        
        # Topic consistency: average similarity to document centroid
        centroid = np.mean(embeddings, axis=0)
        consistency_scores = [
            np.dot(emb, centroid) / (np.linalg.norm(emb) * np.linalg.norm(centroid))
            for emb in embeddings
        ]
        
        return {
            "coherence_score": np.mean(coherence_scores) if coherence_scores else 1.0,
            "topic_consistency": np.mean(consistency_scores) if consistency_scores else 1.0,
            "coherence_variance": np.var(coherence_scores) if coherence_scores else 0.0
        }
    
    def _extract_psycholinguistic_features(self, words: List[str], doc) -> Dict[str, Any]:
        """Extract LIWC-style psycholinguistic features"""
        features = {}
        total_words = len(words) if words else 1
        
        # Calculate category frequencies
        for category, word_list in self.liwc_categories.items():
            count = sum(1 for word in words if word in word_list)
            features[f"{category}_ratio"] = count / total_words
        
        # Emotion word density
        emotion_words = self.liwc_categories["anxiety_words"] + self.liwc_categories["anger_words"] + self.liwc_categories["sadness_words"]
        emotion_count = sum(1 for word in words if word in emotion_words)
        features["emotion_density"] = emotion_count / total_words
        
        # Cognitive processing indicators
        features["cognitive_complexity"] = features["cognitive_words_ratio"] + features["tentative_words_ratio"]
        
        # Self-focus vs other-focus
        features["self_focus"] = features["i_words_ratio"]
        features["collective_focus"] = features["we_words_ratio"]
        
        # Absolutist thinking
        features["absolutist_thinking"] = features["certainty_words_ratio"]
        
        return features
    
    def _extract_temporal_features(self, doc) -> Dict[str, float]:
        """Extract temporal orientation features"""
        past_tense = sum(1 for token in doc if token.tag_ in ['VBD', 'VBN'])
        present_tense = sum(1 for token in doc if token.tag_ in ['VB', 'VBP', 'VBZ', 'VBG'])
        future_markers = sum(1 for token in doc if token.text.lower() in ['will', 'shall', 'going to', 'gonna'])
        
        total_verbs = past_tense + present_tense + future_markers + 1
        
        return {
            "past_focus": past_tense / total_verbs,
            "present_focus": present_tense / total_verbs,
            "future_focus": future_markers / total_verbs,
            "temporal_balance": 1 - abs(past_tense - future_markers) / total_verbs
        }
    
    def _is_passive(self, sentence) -> bool:
        """Detect passive voice in a sentence"""
        for token in sentence:
            if token.dep_ == "nsubjpass" or token.dep_ == "auxpass":
                return True
        return False
    
    def _calculate_avg_syllables(self, doc) -> float:
        """Calculate average syllables per word"""
        syllable_count = 0
        word_count = 0
        
        for token in doc:
            if token.is_alpha:
                syllable_count += self._count_syllables(token.text)
                word_count += 1
        
        return syllable_count / word_count if word_count > 0 else 0
    
    def _count_syllables(self, word: str) -> int:
        """Count syllables in a word"""
        word = word.lower()
        count = 0
        vowels = "aeiouy"
        if word[0] in vowels:
            count += 1
        for index in range(1, len(word)):
            if word[index] in vowels and word[index - 1] not in vowels:
                count += 1
        if word.endswith("e"):
            count -= 1
        if count == 0:
            count += 1
        return count
    
    def _calculate_complex_word_ratio(self, doc) -> float:
        """Calculate ratio of complex words (3+ syllables)"""
        complex_count = 0
        total_words = 0
        
        for token in doc:
            if token.is_alpha:
                if self._count_syllables(token.text) >= 3:
                    complex_count += 1
                total_words += 1
        
        return complex_count / total_words if total_words > 0 else 0
    
    def _calculate_risk_score(self, clinical_results: List[Dict]) -> float:
        """Calculate overall clinical risk score"""
        risk_labels = ['depression', 'anxiety', 'stress', 'suicide', 'self-harm']
        
        risk_score = 0
        for result in clinical_results:
            if any(risk in result.get('label', '').lower() for risk in risk_labels):
                risk_score += result.get('score', 0)
        
        return min(risk_score, 1.0)


class EnhancedEnneagramProcessor:
    """Advanced Enneagram processor with clinical-grade analysis"""
    
    def __init__(self, clinical_analyzer: ClinicalLinguisticAnalyzer):
        self.clinical_analyzer = clinical_analyzer
        
        # Comprehensive type profiles with clinical correlates
        self.type_profiles = {
            "type_1": {
                "name": "The Perfectionist",
                "core_motivation": "To be good, right, accurate, and perfect",
                "core_fear": "Being corrupt, evil, or defective",
                "keywords": ["perfect", "correct", "should", "must", "proper", "right", "wrong", "improve", "fix", "standard"],
                "behavioral_markers": {
                    "primary": ["self-criticism", "attention to detail", "rule-following"],
                    "stress": ["rigidity", "criticality", "anger suppression"],
                    "growth": ["spontaneity", "self-acceptance", "flexibility"]
                },
                "linguistic_patterns": {
                    "modal_verbs": ["should", "must", "ought to", "need to"],
                    "judgment_language": ["right", "wrong", "correct", "incorrect", "proper", "improper"],
                    "perfectionism_markers": ["always", "never", "completely", "totally", "perfectly"],
                    "self_criticism": ["I should have", "I failed to", "I must do better"]
                },
                "clinical_correlates": {
                    "anxiety_indicators": ["perfectionistic anxiety", "fear of mistakes"],
                    "mood_patterns": ["suppressed anger", "frustration", "guilt"],
                    "cognitive_style": ["black-and-white thinking", "high standards", "detail-oriented"]
                }
            },
            "type_2": {
                "name": "The Helper",
                "core_motivation": "To feel loved and needed",
                "core_fear": "Being unwanted or unworthy of love",
                "keywords": ["help", "care", "love", "need", "support", "others", "giving", "serve", "appreciate"],
                "behavioral_markers": {
                    "primary": ["people-pleasing", "anticipating needs", "emotional attunement"],
                    "stress": ["manipulation", "resentment", "possessiveness"],
                    "growth": ["self-care", "authenticity", "receiving help"]
                },
                "linguistic_patterns": {
                    "other_focus": ["you", "they", "them", "others", "people"],
                    "helping_language": ["help", "assist", "support", "care for", "take care of"],
                    "emotional_expression": ["feel", "love", "care", "need", "appreciate"],
                    "indirect_needs": ["It would be nice if", "Don't worry about me", "I'm fine"]
                },
                "clinical_correlates": {
                    "anxiety_indicators": ["relationship anxiety", "fear of abandonment"],
                    "mood_patterns": ["hidden resentment", "pride", "emotional volatility"],
                    "cognitive_style": ["emotional reasoning", "other-directed thinking", "intuitive"]
                }
            },
            "type_3": {
                "name": "The Achiever",
                "core_motivation": "To feel valuable and worthwhile",
                "core_fear": "Being worthless or without value",
                "keywords": ["success", "achieve", "goal", "win", "best", "efficient", "accomplish", "perform", "excel"],
                "behavioral_markers": {
                    "primary": ["goal-oriented", "competitive", "image-conscious"],
                    "stress": ["workaholism", "deception", "burnout"],
                    "growth": ["authenticity", "collaboration", "being vs doing"]
                },
                "linguistic_patterns": {
                    "achievement_language": ["accomplish", "achieve", "succeed", "win", "best"],
                    "efficiency_focus": ["optimize", "maximize", "efficient", "productive", "results"],
                    "comparison": ["better than", "top", "leading", "outperform", "excel"],
                    "image_management": ["appear", "seem", "look like", "present as"]
                },
                "clinical_correlates": {
                    "anxiety_indicators": ["performance anxiety", "imposter syndrome"],
                    "mood_patterns": ["hidden emptiness", "burnout", "emotional disconnection"],
                    "cognitive_style": ["strategic thinking", "results-focused", "adaptive"]
                }
            },
            "type_4": {
                "name": "The Individualist",
                "core_motivation": "To find themselves and their significance",
                "core_fear": "Having no identity or significance",
                "keywords": ["unique", "special", "different", "authentic", "deep", "missing", "melancholy", "creative"],
                "behavioral_markers": {
                    "primary": ["emotional intensity", "self-awareness", "creativity"],
                    "stress": ["envy", "melancholy", "withdrawal"],
                    "growth": ["equanimity", "objectivity", "action-oriented"]
                },
                "linguistic_patterns": {
                    "uniqueness_language": ["different", "unique", "special", "unlike others"],
                    "emotional_depth": ["deeply", "intensely", "profoundly", "truly"],
                    "longing_language": ["missing", "lacking", "yearning", "searching"],
                    "authenticity": ["real", "authentic", "genuine", "true self"]
                },
                "clinical_correlates": {
                    "anxiety_indicators": ["identity anxiety", "fear of ordinariness"],
                    "mood_patterns": ["melancholy", "mood swings", "emotional sensitivity"],
                    "cognitive_style": ["introspective", "symbolic thinking", "aesthetic focus"]
                }
            },
            "type_5": {
                "name": "The Investigator",
                "core_motivation": "To be competent and understanding",
                "core_fear": "Being overwhelmed or invaded",
                "keywords": ["understand", "analyze", "research", "knowledge", "observe", "think", "privacy", "competent"],
                "behavioral_markers": {
                    "primary": ["observation", "analysis", "knowledge-seeking"],
                    "stress": ["isolation", "stinginess", "detachment"],
                    "growth": ["engagement", "generosity", "confidence"]
                },
                "linguistic_patterns": {
                    "analytical_language": ["analyze", "understand", "research", "investigate"],
                    "cognitive_focus": ["think", "consider", "observe", "study", "examine"],
                    "detachment": ["objective", "rational", "logical", "factual"],
                    "privacy_language": ["alone", "space", "private", "independent"]
                },
                "clinical_correlates": {
                    "anxiety_indicators": ["social anxiety", "fear of incompetence"],
                    "mood_patterns": ["emotional detachment", "intellectualization"],
                    "cognitive_style": ["analytical", "compartmentalized", "theoretical"]
                }
            },
            "type_6": {
                "name": "The Loyalist",
                "core_motivation": "To have security and support",
                "core_fear": "Being without support or guidance",
                "keywords": ["safe", "secure", "loyal", "responsible", "anxious", "doubt", "authority", "trust"],
                "behavioral_markers": {
                    "primary": ["loyalty", "responsibility", "vigilance"],
                    "stress": ["anxiety", "suspicion", "reactivity"],
                    "growth": ["courage", "self-trust", "independence"]
                },
                "linguistic_patterns": {
                    "security_language": ["safe", "secure", "stable", "reliable", "trustworthy"],
                    "doubt_expression": ["but what if", "I'm not sure", "maybe", "possibly"],
                    "authority_reference": ["they say", "according to", "the rules", "supposed to"],
                    "loyalty_language": ["committed", "dedicated", "faithful", "responsible"]
                },
                "clinical_correlates": {
                    "anxiety_indicators": ["generalized anxiety", "catastrophic thinking"],
                    "mood_patterns": ["worry", "skepticism", "ambivalence"],
                    "cognitive_style": ["vigilant", "questioning", "scenario planning"]
                }
            },
            "type_7": {
                "name": "The Enthusiast",
                "core_motivation": "To maintain happiness and avoid pain",
                "core_fear": "Being trapped in pain or deprivation",
                "keywords": ["fun", "exciting", "adventure", "options", "positive", "plan", "future", "opportunity"],
                "behavioral_markers": {
                    "primary": ["enthusiasm", "versatility", "spontaneity"],
                    "stress": ["scattered", "impulsive", "escapist"],
                    "growth": ["focus", "depth", "presence"]
                },
                "linguistic_patterns": {
                    "positive_language": ["exciting", "fun", "amazing", "great", "wonderful"],
                    "future_focus": ["will", "going to", "plan", "next", "tomorrow"],
                    "options_language": ["could", "might", "maybe we can", "what about"],
                    "avoidance": ["let's not", "instead", "better idea", "move on"]
                },
                "clinical_correlates": {
                    "anxiety_indicators": ["FOMO", "restlessness", "avoidance"],
                    "mood_patterns": ["forced positivity", "underlying anxiety", "scattered energy"],
                    "cognitive_style": ["associative", "quick thinking", "reframing"]
                }
            },
            "type_8": {
                "name": "The Challenger",
                "core_motivation": "To be self-reliant and in control",
                "core_fear": "Being controlled or vulnerable",
                "keywords": ["control", "power", "strong", "justice", "direct", "protect", "lead", "fight"],
                "behavioral_markers": {
                    "primary": ["assertiveness", "leadership", "protectiveness"],
                    "stress": ["domination", "vengeance", "ruthlessness"],
                    "growth": ["vulnerability", "compassion", "collaboration"]
                },
                "linguistic_patterns": {
                    "power_language": ["control", "dominate", "lead", "command", "direct"],
                    "intensity": ["absolutely", "definitely", "obviously", "clearly"],
                    "confrontational": ["fight", "battle", "stand up", "push back"],
                    "protective": ["defend", "protect", "shield", "guard"]
                },
                "clinical_correlates": {
                    "anxiety_indicators": ["vulnerability anxiety", "control issues"],
                    "mood_patterns": ["anger", "intensity", "emotional suppression"],
                    "cognitive_style": ["black-and-white", "action-oriented", "strategic"]
                }
            },
            "type_9": {
                "name": "The Peacemaker",
                "core_motivation": "To maintain inner and outer peace",
                "core_fear": "Loss of connection and fragmentation",
                "keywords": ["peace", "harmony", "comfortable", "agree", "fine", "okay", "whatever", "calm"],
                "behavioral_markers": {
                    "primary": ["accommodating", "agreeable", "calming presence"],
                    "stress": ["passive-aggressive", "stubborn", "dissociated"],
                    "growth": ["assertiveness", "engagement", "self-priority"]
                },
                "linguistic_patterns": {
                    "harmony_language": ["peace", "calm", "comfortable", "easy-going"],
                    "agreement": ["sure", "okay", "fine", "whatever works", "no problem"],
                    "minimizing": ["it's not a big deal", "doesn't matter", "either way"],
                    "inclusive": ["we", "us", "together", "everyone"]
                },
                "clinical_correlates": {
                    "anxiety_indicators": ["conflict avoidance", "decision anxiety"],
                    "mood_patterns": ["suppressed anger", "numbness", "disengagement"],
                    "cognitive_style": ["holistic", "inclusive", "synthesizing"]
                }
            }
        }
    
    async def process(self, text: str, clinical_features: Dict[str, Any]) -> Tuple[List[Dict], float, Dict]:
        """Process text for Enneagram type identification with clinical insights"""
        
        # Extract type scores using multiple methods
        keyword_scores = self._analyze_keywords(text)
        linguistic_scores = self._analyze_linguistic_patterns(text, clinical_features)
        behavioral_scores = self._analyze_behavioral_indicators(text, clinical_features)
        clinical_correlation_scores = self._analyze_clinical_correlates(clinical_features)
        
        # Combine scores with weighted average
        combined_scores = self._combine_scores(
            keyword_scores,
            linguistic_scores,
            behavioral_scores,
            clinical_correlation_scores
        )
        
        # Calculate confidence based on feature consistency
        confidence = self._calculate_confidence(
            combined_scores,
            clinical_features
        )
        
        # Generate detailed results
        results = []
        for type_key, score in combined_scores.items():
            if score > 0.1:  # Only include types with meaningful scores
                profile = self.type_profiles[type_key]
                results.append({
                    "type": type_key,
                    "name": profile["name"],
                    "score": float(score),
                    "confidence": float(confidence * score),
                    "evidence": self._gather_evidence(text, type_key, clinical_features),
                    "clinical_insights": self._generate_clinical_insights(type_key, clinical_features),
                    "growth_recommendations": self._generate_growth_recommendations(type_key, score)
                })
        
        # Sort by score
        results.sort(key=lambda x: x["score"], reverse=True)
        
        # Additional analysis
        additional_insights = {
            "primary_types": [r["type"] for r in results[:3]],
            "triadic_analysis": self._analyze_triads(combined_scores),
            "instinctual_variants": self._analyze_instinctual_variants(text, clinical_features),
            "integration_direction": self._suggest_integration_path(results),
            "clinical_considerations": self._clinical_considerations(clinical_features)
        }
        
        return results, confidence, additional_insights
    
    def _analyze_keywords(self, text: str) -> Dict[str, float]:
        """Analyze keyword frequency for each type"""
        text_lower = text.lower()
        words = text_lower.split()
        scores = {}
        
        for type_key, profile in self.type_profiles.items():
            keywords = profile["keywords"]
            matches = sum(1 for word in words if word in keywords)
            scores[type_key] = matches / len(words) if words else 0
        
        return scores
    
    def _analyze_linguistic_patterns(self, text: str, clinical_features: Dict) -> Dict[str, float]:
        """Analyze linguistic patterns specific to each type"""
        scores = {}
        text_lower = text.lower()
        
        # Use clinical linguistic features
        ling_features = clinical_features.get("psycholinguistic", {})
        
        for type_key, profile in self.type_profiles.items():
            pattern_score = 0
            pattern_count = 0
            
            for pattern_type, patterns in profile["linguistic_patterns"].items():
                for pattern in patterns:
                    if pattern in text_lower:
                        pattern_score += 1
                pattern_count += len(patterns)
            
            # Adjust based on clinical linguistic features
            if type_key == "type_1" and ling_features.get("certainty_words_ratio", 0) > 0.05:
                pattern_score += 0.2
            elif type_key == "type_2" and ling_features.get("we_words_ratio", 0) > 0.03:
                pattern_score += 0.2
            elif type_key == "type_3" and ling_features.get("achievement_words_ratio", 0) > 0.04:
                pattern_score += 0.2
            elif type_key == "type_4" and ling_features.get("i_words_ratio", 0) > 0.06:
                pattern_score += 0.2
            elif type_key == "type_5" and ling_features.get("cognitive_words_ratio", 0) > 0.05:
                pattern_score += 0.2
            elif type_key == "type_6" and ling_features.get("tentative_words_ratio", 0) > 0.04:
                pattern_score += 0.2
            elif type_key == "type_7" and clinical_features.get("temporal", {}).get("future_focus", 0) > 0.4:
                pattern_score += 0.2
            elif type_key == "type_8" and ling_features.get("power_words_ratio", 0) > 0.03:
                pattern_score += 0.2
            elif type_key == "type_9" and ling_features.get("collective_focus", 0) > 0.04:
                pattern_score += 0.2
            
            scores[type_key] = pattern_score / (pattern_count + 1)
        
        return scores
    
    def _analyze_behavioral_indicators(self, text: str, clinical_features: Dict) -> Dict[str, float]:
        """Analyze behavioral indicators from text and clinical features"""
        scores = {}
        
        # Use clinical indicators for behavioral analysis
        clinical_indicators = clinical_features.get("clinical_indicators", {})
        risk_assessment = clinical_indicators.get("risk_assessment", [])
        
        for type_key, profile in self.type_profiles.items():
            behavioral_score = 0
            
            # Check for behavioral markers in text
            for marker_type, markers in profile["behavioral_markers"].items():
                for marker in markers:
                    if marker.lower() in text.lower():
                        behavioral_score += 0.3 if marker_type == "primary" else 0.2
            
            # Adjust based on clinical risk patterns
            if type_key == "type_1" and any("anxiety" in r.get("label", "") for r in risk_assessment):
                behavioral_score += 0.15
            elif type_key == "type_4" and any("depression" in r.get("label", "") for r in risk_assessment):
                behavioral_score += 0.15
            elif type_key == "type_6" and clinical_indicators.get("overall_risk_score", 0) > 0.5:
                behavioral_score += 0.15
            
            scores[type_key] = min(behavioral_score, 1.0)
        
        return scores
    
    def _analyze_clinical_correlates(self, clinical_features: Dict) -> Dict[str, float]:
        """Analyze clinical correlates for each type"""
        scores = {}
        
        clinical_indicators = clinical_features.get("clinical_indicators", {})
        complexity = clinical_features.get("complexity", {})
        syntactic = clinical_features.get("syntactic", {})
        
        for type_key, profile in self.type_profiles.items():
            clinical_score = 0
            
            # Type-specific clinical patterns
            if type_key == "type_1":
                # Perfectionists show high complexity and formal language
                if complexity.get("flesch_kincaid_grade", 0) > 10:
                    clinical_score += 0.2
                if syntactic.get("passive_voice_ratio", 0) < 0.1:
                    clinical_score += 0.1
                    
            elif type_key == "type_2":
                # Helpers show other-focused language
                if syntactic.get("noun_verb_ratio", 1) < 0.8:
                    clinical_score += 0.2
                    
            elif type_key == "type_3":
                # Achievers show action-oriented language
                if syntactic.get("noun_verb_ratio", 1) > 1.2:
                    clinical_score += 0.2
                    
            elif type_key == "type_4":
                # Individualists show emotional complexity
                if syntactic.get("adjective_ratio", 0) > 0.15:
                    clinical_score += 0.2
                if clinical_features.get("semantic", {}).get("coherence_variance", 0) > 0.2:
                    clinical_score += 0.1
                    
            elif type_key == "type_5":
                # Investigators show analytical language
                if complexity.get("complex_word_ratio", 0) > 0.2:
                    clinical_score += 0.2
                if syntactic.get("subordinate_clause_ratio", 0) > 0.3:
                    clinical_score += 0.1
                    
            elif type_key == "type_6":
                # Loyalists show uncertainty
                if clinical_features.get("psycholinguistic", {}).get("tentative_words_ratio", 0) > 0.04:
                    clinical_score += 0.2
                    
            elif type_key == "type_7":
                # Enthusiasts show positive, future-focused language
                if clinical_features.get("temporal", {}).get("future_focus", 0) > 0.4:
                    clinical_score += 0.2
                    
            elif type_key == "type_8":
                # Challengers show direct, assertive language
                if syntactic.get("passive_voice_ratio", 0) < 0.05:
                    clinical_score += 0.2
                    
            elif type_key == "type_9":
                # Peacemakers show balanced, inclusive language
                if clinical_features.get("semantic", {}).get("coherence_score", 0) > 0.8:
                    clinical_score += 0.2
            
            scores[type_key] = clinical_score
        
        return scores
    
    def _combine_scores(self, *score_dicts) -> Dict[str, float]:
        """Combine multiple scoring methods with weights"""
        weights = [0.25, 0.35, 0.25, 0.15]  # Keyword, linguistic, behavioral, clinical
        combined = {}
        
        for type_key in self.type_profiles.keys():
            weighted_sum = sum(
                scores.get(type_key, 0) * weight 
                for scores, weight in zip(score_dicts, weights)
            )
            combined[type_key] = weighted_sum
        
        # Normalize scores
        total = sum(combined.values())
        if total > 0:
            combined = {k: v/total for k, v in combined.items()}
        
        return combined
    
    def _calculate_confidence(self, scores: Dict[str, float], clinical_features: Dict) -> float:
        """Calculate overall confidence in the assessment"""
        # Base confidence on score distribution
        sorted_scores = sorted(scores.values(), reverse=True)
        
        if len(sorted_scores) >= 2:
            # Clear primary type
            if sorted_scores[0] > 0.3 and sorted_scores[0] - sorted_scores[1] > 0.1:
                confidence = 0.8
            # Moderate clarity
            elif sorted_scores[0] > 0.2:
                confidence = 0.6
            # Low clarity
            else:
                confidence = 0.4
        else:
            confidence = 0.3
        
        # Adjust based on text quality
        text_stats = clinical_features.get("text_statistics", {})
        if text_stats.get("word_count", 0) < 50:
            confidence *= 0.7
        elif text_stats.get("word_count", 0) > 200:
            confidence *= 1.1
        
        # Adjust based on clinical clarity
        if clinical_features.get("semantic", {}).get("coherence_score", 0) > 0.8:
            confidence *= 1.1
        
        return min(confidence, 0.95)
    
    def _gather_evidence(self, text: str, type_key: str, clinical_features: Dict) -> List[str]:
        """Gather specific evidence for a type assignment"""
        evidence = []
        profile = self.type_profiles[type_key]
        
        # Find keyword matches
        for keyword in profile["keywords"]:
            if keyword in text.lower():
                evidence.append(f"Uses keyword '{keyword}'")
        
        # Find linguistic pattern matches
        for pattern_type, patterns in profile["linguistic_patterns"].items():
            for pattern in patterns:
                if pattern in text.lower():
                    evidence.append(f"Shows {pattern_type}: '{pattern}'")
        
        # Add clinical evidence
        if type_key == "type_1" and clinical_features.get("psycholinguistic", {}).get("certainty_words_ratio", 0) > 0.05:
            evidence.append("High use of certainty language")
        
        return evidence[:5]  # Limit to top 5 pieces of evidence
    
    def _generate_clinical_insights(self, type_key: str, clinical_features: Dict) -> Dict[str, Any]:
        """Generate clinical insights for the identified type"""
        profile = self.type_profiles[type_key]
        clinical_indicators = clinical_features.get("clinical_indicators", {})
        
        insights = {
            "risk_level": clinical_indicators.get("overall_risk_score", 0),
            "primary_concerns": [],
            "strengths": [],
            "therapeutic_considerations": []
        }
        
        # Type-specific clinical insights
        if type_key == "type_1":
            if clinical_indicators.get("overall_risk_score", 0) > 0.5:
                insights["primary_concerns"].append("Perfectionistic anxiety may be elevated")
            insights["strengths"].append("High standards and attention to detail")
            insights["therapeutic_considerations"].append("Focus on self-compassion and flexibility")
            
        elif type_key == "type_2":
            if clinical_features.get("psycholinguistic", {}).get("i_words_ratio", 0) < 0.02:
                insights["primary_concerns"].append("May be neglecting personal needs")
            insights["strengths"].append("Strong empathy and interpersonal awareness")
            insights["therapeutic_considerations"].append("Develop healthy boundaries")
            
        # Add more type-specific insights...
        
        return insights
    
    def _generate_growth_recommendations(self, type_key: str, score: float) -> List[str]:
        """Generate personalized growth recommendations"""
        profile = self.type_profiles[type_key]
        recommendations = []
        
        if score > 0.3:  # Strong type identification
            # Add growth direction from profile
            growth_behaviors = profile["behavioral_markers"].get("growth", [])
            for behavior in growth_behaviors[:2]:
                recommendations.append(f"Practice {behavior}")
        
        return recommendations
    
    def _analyze_triads(self, scores: Dict[str, float]) -> Dict[str, float]:
        """Analyze Enneagram triads (gut, heart, head)"""
        triads = {
            "gut": ["type_8", "type_9", "type_1"],
            "heart": ["type_2", "type_3", "type_4"],
            "head": ["type_5", "type_6", "type_7"]
        }
        
        triad_scores = {}
        for triad_name, types in triads.items():
            triad_scores[triad_name] = sum(scores.get(t, 0) for t in types) / 3
        
        return triad_scores
    
    def _analyze_instinctual_variants(self, text: str, clinical_features: Dict) -> Dict[str, float]:
        """Analyze instinctual variants (self-preservation, social, sexual)"""
        # Simplified analysis - would be more complex in production
        variants = {
            "self_preservation": 0.33,
            "social": 0.33,
            "sexual_intimate": 0.33
        }
        
        # Adjust based on linguistic features
        if "safety" in text.lower() or "secure" in text.lower():
            variants["self_preservation"] += 0.1
        if clinical_features.get("psycholinguistic", {}).get("we_words_ratio", 0) > 0.04:
            variants["social"] += 0.1
        if clinical_features.get("psycholinguistic", {}).get("i_words_ratio", 0) > 0.06:
            variants["sexual_intimate"] += 0.1
        
        # Normalize
        total = sum(variants.values())
        return {k: v/total for k, v in variants.items()}
    
    def _suggest_integration_path(self, results: List[Dict]) -> Dict[str, Any]:
        """Suggest integration path based on Enneagram theory"""
        if not results:
            return {}
        
        primary_type = results[0]["type"]
        
        # Simplified integration paths
        integration_paths = {
            "type_1": {"integration": "type_7", "disintegration": "type_4"},
            "type_2": {"integration": "type_4", "disintegration": "type_8"},
            "type_3": {"integration": "type_6", "disintegration": "type_9"},
            "type_4": {"integration": "type_1", "disintegration": "type_2"},
            "type_5": {"integration": "type_8", "disintegration": "type_7"},
            "type_6": {"integration": "type_9", "disintegration": "type_3"},
            "type_7": {"integration": "type_5", "disintegration": "type_1"},
            "type_8": {"integration": "type_2", "disintegration": "type_5"},
            "type_9": {"integration": "type_3", "disintegration": "type_6"}
        }
        
        return integration_paths.get(primary_type, {})
    
    def _clinical_considerations(self, clinical_features: Dict) -> List[str]:
        """Generate clinical considerations based on assessment"""
        considerations = []
        
        risk_score = clinical_features.get("clinical_indicators", {}).get("overall_risk_score", 0)
        if risk_score > 0.7:
            considerations.append("High clinical risk indicators present - consider professional support")
        elif risk_score > 0.4:
            considerations.append("Moderate clinical indicators - monitor for changes")
        
        coherence = clinical_features.get("semantic", {}).get("coherence_score", 1)
        if coherence < 0.5:
            considerations.append("Low semantic coherence may indicate emotional distress")
        
        return considerations


class EnhancedBigFiveProcessor:
    """Advanced Big Five processor with clinical-grade analysis"""
    
    def __init__(self, clinical_analyzer: ClinicalLinguisticAnalyzer):
        self.clinical_analyzer = clinical_analyzer
        
        # Comprehensive trait profiles with facets
        self.trait_profiles = {
            "openness": {
                "name": "Openness to Experience",
                "facets": {
                    "imagination": ["imagine", "fantasy", "dream", "creative", "visualize"],
                    "artistic_interests": ["art", "music", "poetry", "beauty", "aesthetic"],
                    "emotionality": ["feel", "emotion", "moved", "touched", "sensitive"],
                    "adventurousness": ["try", "new", "adventure", "explore", "experiment"],
                    "intellect": ["think", "analyze", "understand", "complex", "abstract"],
                    "liberalism": ["challenge", "tradition", "change", "progressive", "question"]
                },
                "high_indicators": {
                    "keywords": ["creative", "curious", "imaginative", "artistic", "unconventional"],
                    "linguistic_markers": ["what if", "imagine", "suppose", "wonder", "possibility"],
                    "complexity_threshold": 0.7
                },
                "low_indicators": {
                    "keywords": ["practical", "traditional", "routine", "conventional", "realistic"],
                    "linguistic_markers": ["always done", "proven", "standard", "normal", "usual"],
                    "complexity_threshold": 0.3
                },
                "clinical_correlates": {
                    "positive": ["creativity", "cognitive flexibility", "aesthetic sensitivity"],
                    "negative": ["fantasy proneness", "impracticality", "emotional overwhelm"]
                }
            },
            "conscientiousness": {
                "name": "Conscientiousness",
                "facets": {
                    "self_efficacy": ["capable", "competent", "handle", "manage", "accomplish"],
                    "orderliness": ["organize", "plan", "schedule", "systematic", "neat"],
                    "dutifulness": ["duty", "obligation", "responsible", "reliable", "promise"],
                    "achievement_striving": ["goal", "achieve", "succeed", "strive", "excel"],
                    "self_discipline": ["discipline", "persist", "finish", "complete", "follow through"],
                    "cautiousness": ["careful", "think before", "consider", "deliberate", "cautious"]
                },
                "high_indicators": {
                    "keywords": ["organized", "disciplined", "responsible", "thorough", "reliable"],
                    "linguistic_markers": ["plan to", "schedule", "must", "should", "deadline"],
                    "modal_verb_ratio": 0.05
                },
                "low_indicators": {
                    "keywords": ["spontaneous", "flexible", "carefree", "relaxed", "adaptable"],
                    "linguistic_markers": ["whatever", "maybe later", "go with flow", "see what happens"],
                    "modal_verb_ratio": 0.01
                },
                "clinical_correlates": {
                    "positive": ["achievement", "health behaviors", "job performance"],
                    "negative": ["perfectionism", "rigidity", "workaholic tendencies"]
                }
            },
            "extraversion": {
                "name": "Extraversion",
                "facets": {
                    "friendliness": ["friend", "people", "social", "warm", "affectionate"],
                    "gregariousness": ["party", "group", "crowd", "gathering", "socialize"],
                    "assertiveness": ["lead", "charge", "direct", "assert", "speak up"],
                    "activity_level": ["busy", "active", "energy", "fast-paced", "on the go"],
                    "excitement_seeking": ["thrill", "excitement", "adventure", "stimulation", "rush"],
                    "cheerfulness": ["happy", "joy", "laugh", "fun", "enthusiastic"]
                },
                "high_indicators": {
                    "keywords": ["outgoing", "social", "energetic", "talkative", "assertive"],
                    "linguistic_markers": ["we", "us", "party", "fun", "exciting"],
                    "exclamation_ratio": 0.1
                },
                "low_indicators": {
                    "keywords": ["quiet", "reserved", "solitary", "calm", "independent"],
                    "linguistic_markers": ["alone", "peaceful", "quiet time", "prefer not", "rather stay"],
                    "exclamation_ratio": 0.02
                },
                "clinical_correlates": {
                    "positive": ["social support", "positive affect", "leadership"],
                    "negative": ["attention-seeking", "impulsivity", "social exhaustion"]
                }
            },
            "agreeableness": {
                "name": "Agreeableness",
                "facets": {
                    "trust": ["trust", "believe", "faith", "honest", "sincere"],
                    "morality": ["fair", "cheat", "honest", "ethical", "principled"],
                    "altruism": ["help", "assist", "support", "care", "generous"],
                    "cooperation": ["cooperate", "work together", "compromise", "agree", "harmony"],
                    "modesty": ["humble", "modest", "simple", "unpretentious", "down to earth"],
                    "sympathy": ["concern", "sympathy", "compassion", "feel for", "empathy"]
                },
                "high_indicators": {
                    "keywords": ["kind", "cooperative", "trusting", "helpful", "compassionate"],
                    "linguistic_markers": ["understand", "appreciate", "together", "share", "support"],
                    "other_focus_ratio": 0.06
                },
                "low_indicators": {
                    "keywords": ["competitive", "skeptical", "critical", "demanding", "tough"],
                    "linguistic_markers": ["don't trust", "compete", "win", "skeptical", "prove it"],
                    "other_focus_ratio": 0.02
                },
                "clinical_correlates": {
                    "positive": ["relationship quality", "teamwork", "social harmony"],
                    "negative": ["exploitation vulnerability", "conflict avoidance", "dependency"]
                }
            },
            "neuroticism": {
                "name": "Neuroticism (Emotional Stability)",
                "facets": {
                    "anxiety": ["anxious", "worried", "nervous", "tense", "stressed"],
                    "anger": ["angry", "irritated", "frustrated", "annoyed", "mad"],
                    "depression": ["sad", "depressed", "down", "hopeless", "empty"],
                    "self_consciousness": ["embarrassed", "shy", "awkward", "self-conscious", "uncomfortable"],
                    "immoderation": ["resist", "control", "temptation", "indulge", "excess"],
                    "vulnerability": ["panic", "helpless", "overwhelmed", "break down", "fall apart"]
                },
                "high_indicators": {
                    "keywords": ["anxious", "worried", "stressed", "emotional", "sensitive"],
                    "linguistic_markers": ["can't handle", "too much", "overwhelmed", "worried about", "stressed"],
                    "negative_emotion_ratio": 0.15
                },
                "low_indicators": {
                    "keywords": ["calm", "relaxed", "stable", "composed", "unflappable"],
                    "linguistic_markers": ["no worries", "calm", "handle it", "stable", "fine"],
                    "negative_emotion_ratio": 0.03
                },
                "clinical_correlates": {
                    "positive": ["emotional sensitivity", "empathy", "self-awareness"],
                    "negative": ["anxiety disorders", "depression", "stress vulnerability"]
                }
            }
        }
    
    async def process(self, text: str, clinical_features: Dict[str, Any]) -> Tuple[List[Dict], float, Dict]:
        """Process text for Big Five trait assessment with clinical insights"""
        
        # Extract trait scores using multiple methods
        trait_scores = {}
        trait_details = {}
        
        for trait_name, profile in self.trait_profiles.items():
            # Analyze each trait with multiple methods
            facet_scores = self._analyze_facets(text, profile["facets"])
            indicator_scores = self._analyze_indicators(text, profile, clinical_features)
            clinical_scores = self._analyze_clinical_markers(trait_name, clinical_features)
            
            # Combine scores
            combined_score = self._combine_trait_scores(
                facet_scores,
                indicator_scores,
                clinical_scores
            )
            
            trait_scores[trait_name] = combined_score
            trait_details[trait_name] = {
                "facet_scores": facet_scores,
                "clinical_insights": self._generate_trait_insights(trait_name, combined_score, clinical_features)
            }
        
        # Calculate overall confidence
        confidence = self._calculate_confidence(trait_scores, clinical_features)
        
        # Generate results
        results = []
        for trait_name, score in trait_scores.items():
            profile = self.trait_profiles[trait_name]
            results.append({
                "trait": trait_name,
                "name": profile["name"],
                "score": float(score),
                "percentile": self._score_to_percentile(score),
                "level": self._score_to_level(score),
                "confidence": float(confidence),
                "facets": trait_details[trait_name]["facet_scores"],
                "clinical_insights": trait_details[trait_name]["clinical_insights"],
                "evidence": self._gather_evidence(text, trait_name, clinical_features)
            })
        
        # Additional insights
        additional_insights = {
            "personality_profile": self._generate_personality_profile(trait_scores),
            "clinical_implications": self._analyze_clinical_implications(trait_scores, clinical_features),
            "interpersonal_style": self._analyze_interpersonal_style(trait_scores),
            "vocational_implications": self._analyze_vocational_fit(trait_scores),
            "therapeutic_considerations": self._generate_therapeutic_considerations(trait_scores, clinical_features)
        }
        
        return results, confidence, additional_insights
    
    def _analyze_facets(self, text: str, facets: Dict[str, List[str]]) -> Dict[str, float]:
        """Analyze facet-level scores for a trait"""
        text_lower = text.lower()
        words = text_lower.split()
        facet_scores = {}
        
        for facet_name, keywords in facets.items():
            matches = sum(1 for word in words if word in keywords)
            facet_scores[facet_name] = min(matches / (len(words) * 0.01), 1.0) if words else 0
        
        return facet_scores
    
    def _analyze_indicators(self, text: str, profile: Dict, clinical_features: Dict) -> Dict[str, float]:
        """Analyze high/low indicators for a trait"""
        text_lower = text.lower()
        
        # High indicator score
        high_score = 0
        high_keywords = profile["high_indicators"]["keywords"]
        high_markers = profile["high_indicators"]["linguistic_markers"]
        
        for keyword in high_keywords:
            if keyword in text_lower:
                high_score += 0.1
        
        for marker in high_markers:
            if marker in text_lower:
                high_score += 0.15
        
        # Low indicator score
        low_score = 0
        low_keywords = profile["low_indicators"]["keywords"]
        low_markers = profile["low_indicators"]["linguistic_markers"]
        
        for keyword in low_keywords:
            if keyword in text_lower:
                low_score += 0.1
        
        for marker in low_markers:
            if marker in text_lower:
                low_score += 0.15
        
        # Additional checks based on trait
        if "complexity_threshold" in profile["high_indicators"]:
            complexity = clinical_features.get("complexity", {}).get("lexical_diversity", 0.5)
            if complexity > profile["high_indicators"]["complexity_threshold"]:
                high_score += 0.2
            elif complexity < profile["low_indicators"]["complexity_threshold"]:
                low_score += 0.2
        
        return {
            "high": min(high_score, 1.0),
            "low": min(low_score, 1.0)
        }
    
    def _analyze_clinical_markers(self, trait_name: str, clinical_features: Dict) -> float:
        """Analyze clinical markers relevant to each trait"""
        score = 0.5  # Neutral baseline
        
        psycholinguistic = clinical_features.get("psycholinguistic", {})
        complexity = clinical_features.get("complexity", {})
        temporal = clinical_features.get("temporal", {})
        clinical = clinical_features.get("clinical_indicators", {})
        
        if trait_name == "openness":
            # High lexical diversity and complexity indicate openness
            if complexity.get("lexical_diversity", 0) > 0.7:
                score += 0.2
            if complexity.get("flesch_kincaid_grade", 8) > 12:
                score += 0.1
            if psycholinguistic.get("cognitive_words_ratio", 0) > 0.05:
                score += 0.1
                
        elif trait_name == "conscientiousness":
            # Modal verbs and future planning indicate conscientiousness
            if psycholinguistic.get("certainty_words_ratio", 0) > 0.04:
                score += 0.2
            if temporal.get("future_focus", 0) > 0.3:
                score += 0.15
            if psycholinguistic.get("achievement_words_ratio", 0) > 0.03:
                score += 0.15
                
        elif trait_name == "extraversion":
            # Social words and positive emotion indicate extraversion
            if psycholinguistic.get("we_words_ratio", 0) > 0.03:
                score += 0.2
            if psycholinguistic.get("affiliation_words_ratio", 0) > 0.03:
                score += 0.15
            # Check for exclamation marks (simplified)
            if text.count('!') > len(text.split('.')) * 0.1:
                score += 0.1
                
        elif trait_name == "agreeableness":
            # Other-focus and positive sentiment indicate agreeableness
            collective_focus = psycholinguistic.get("collective_focus", 0)
            self_focus = psycholinguistic.get("self_focus", 0)
            if collective_focus > self_focus:
                score += 0.2
            if psycholinguistic.get("affiliation_words_ratio", 0) > 0.04:
                score += 0.15
                
        elif trait_name == "neuroticism":
            # Negative emotions and clinical risk indicate neuroticism
            if clinical.get("overall_risk_score", 0) > 0.5:
                score += 0.3
            if psycholinguistic.get("anxiety_words_ratio", 0) > 0.02:
                score += 0.2
            if psycholinguistic.get("negation_ratio", 0) > 0.03:
                score += 0.1
        
        return max(0, min(1, score))
    
    def _combine_trait_scores(self, facet_scores: Dict, indicator_scores: Dict, clinical_score: float) -> float:
        """Combine different scoring methods for final trait score"""
        # Average facet scores
        avg_facet_score = np.mean(list(facet_scores.values())) if facet_scores else 0.5
        
        # Calculate indicator balance
        high_indicator = indicator_scores.get("high", 0)
        low_indicator = indicator_scores.get("low", 0)
        
        # Weighted combination
        if high_indicator > low_indicator:
            indicator_contribution = 0.5 + (high_indicator - low_indicator) * 0.5
        else:
            indicator_contribution = 0.5 - (low_indicator - high_indicator) * 0.5
        
        # Combine all scores
        final_score = (
            avg_facet_score * 0.3 +
            indicator_contribution * 0.4 +
            clinical_score * 0.3
        )
        
        return max(0.1, min(0.9, final_score))  # Keep scores in reasonable range
    
    def _calculate_confidence(self, trait_scores: Dict, clinical_features: Dict) -> float:
        """Calculate confidence in Big Five assessment"""
        base_confidence = 0.7
        
        # Adjust based on text length
        word_count = clinical_features.get("text_statistics", {}).get("word_count", 0)
        if word_count < 50:
            base_confidence *= 0.6
        elif word_count > 200:
            base_confidence *= 1.2
        
        # Adjust based on coherence
        coherence = clinical_features.get("semantic", {}).get("coherence_score", 0.5)
        base_confidence *= (0.5 + coherence)
        
        # Adjust based on trait score consistency
        trait_variance = np.var(list(trait_scores.values()))
        if trait_variance > 0.1:  # High variance suggests clear personality profile
            base_confidence *= 1.1
        
        return min(0.95, base_confidence)
    
    def _score_to_percentile(self, score: float) -> int:
        """Convert trait score to population percentile"""
        # Simplified - would use normative data in production
        return int(score * 100)
    
    def _score_to_level(self, score: float) -> str:
        """Convert score to descriptive level"""
        if score >= 0.7:
            return "High"
        elif score >= 0.3:
            return "Average"
        else:
            return "Low"
    
    def _gather_evidence(self, text: str, trait_name: str, clinical_features: Dict) -> List[str]:
        """Gather evidence for trait scoring"""
        evidence = []
        profile = self.trait_profiles[trait_name]
        
        # Check for keyword matches
        for keyword in profile["high_indicators"]["keywords"]:
            if keyword in text.lower():
                evidence.append(f"Uses '{keyword}' suggesting high {trait_name}")
        
        # Add clinical evidence
        if trait_name == "openness" and clinical_features.get("complexity", {}).get("lexical_diversity", 0) > 0.7:
            evidence.append("High lexical diversity indicates intellectual curiosity")
        
        return evidence[:5]
    
    def _generate_trait_insights(self, trait_name: str, score: float, clinical_features: Dict) -> Dict:
        """Generate clinical insights for a specific trait"""
        profile = self.trait_profiles[trait_name]
        level = self._score_to_level(score)
        
        insights = {
            "level": level,
            "description": f"{level} {profile['name']}",
            "strengths": [],
            "challenges": [],
            "clinical_relevance": []
        }
        
        # Add level-specific insights
        if level == "High":
            insights["strengths"].extend(profile["clinical_correlates"]["positive"])
            if trait_name == "neuroticism":
                insights["challenges"].extend(profile["clinical_correlates"]["negative"])
                insights["clinical_relevance"].append("May benefit from stress management techniques")
        elif level == "Low":
            if trait_name == "neuroticism":
                insights["strengths"].append("Emotional stability and resilience")
            elif trait_name == "conscientiousness":
                insights["challenges"].append("May struggle with organization and follow-through")
        
        return insights
    
    def _generate_personality_profile(self, trait_scores: Dict) -> str:
        """Generate a narrative personality profile"""
        high_traits = [t for t, s in trait_scores.items() if s >= 0.7]
        low_traits = [t for t, s in trait_scores.items() if s <= 0.3]
        
        profile_parts = []
        
        if high_traits:
            profile_parts.append(f"High in {', '.join(high_traits)}")
        if low_traits:
            profile_parts.append(f"Low in {', '.join(low_traits)}")
        
        if not profile_parts:
            return "Balanced across all five traits"
        
        return "; ".join(profile_parts)
    
    def _analyze_clinical_implications(self, trait_scores: Dict, clinical_features: Dict) -> List[str]:
        """Analyze clinical implications of personality profile"""
        implications = []
        
        # High neuroticism with clinical risk
        if trait_scores.get("neuroticism", 0) > 0.7:
            risk_score = clinical_features.get("clinical_indicators", {}).get("overall_risk_score", 0)
            if risk_score > 0.5:
                implications.append("Elevated neuroticism with clinical risk indicators - consider mental health support")
            else:
                implications.append("High neuroticism - monitor for stress-related concerns")
        
        # Low conscientiousness with high neuroticism
        if trait_scores.get("conscientiousness", 0) < 0.3 and trait_scores.get("neuroticism", 0) > 0.6:
            implications.append("Low conscientiousness + high neuroticism may impact daily functioning")
        
        # Very low agreeableness
        if trait_scores.get("agreeableness", 0) < 0.2:
            implications.append("Very low agreeableness may impact interpersonal relationships")
        
        # High openness with low conscientiousness
        if trait_scores.get("openness", 0) > 0.7 and trait_scores.get("conscientiousness", 0) < 0.3:
            implications.append("Creative potential may be hindered by low organization")
        
        return implications
    
    def _analyze_interpersonal_style(self, trait_scores: Dict) -> Dict[str, Any]:
        """Analyze interpersonal style based on Big Five profile"""
        style = {
            "social_approach": "",
            "conflict_style": "",
            "relationship_patterns": [],
            "communication_style": ""
        }
        
        # Social approach
        extraversion = trait_scores.get("extraversion", 0.5)
        agreeableness = trait_scores.get("agreeableness", 0.5)
        
        if extraversion > 0.6 and agreeableness > 0.6:
            style["social_approach"] = "Warm and outgoing"
        elif extraversion > 0.6 and agreeableness < 0.4:
            style["social_approach"] = "Assertive and competitive"
        elif extraversion < 0.4 and agreeableness > 0.6:
            style["social_approach"] = "Reserved but kind"
        else:
            style["social_approach"] = "Independent and selective"
        
        # Conflict style
        if agreeableness > 0.7:
            style["conflict_style"] = "Accommodating and peace-seeking"
        elif agreeableness < 0.3 and extraversion > 0.6:
            style["conflict_style"] = "Direct and confrontational"
        else:
            style["conflict_style"] = "Balanced and situational"
        
        # Communication style
        openness = trait_scores.get("openness", 0.5)
        if openness > 0.7 and extraversion > 0.6:
            style["communication_style"] = "Expressive and abstract"
        elif conscientiousness = trait_scores.get("conscientiousness", 0.5) > 0.7:
            style["communication_style"] = "Clear and structured"
        else:
            style["communication_style"] = "Adaptive and pragmatic"
        
        return style
    
    def _analyze_vocational_fit(self, trait_scores: Dict) -> Dict[str, List[str]]:
        """Suggest vocational areas based on personality profile"""
        suggestions = {
            "ideal_environments": [],
            "potential_strengths": [],
            "areas_to_develop": []
        }
        
        # High openness
        if trait_scores.get("openness", 0) > 0.7:
            suggestions["ideal_environments"].append("Creative and innovative fields")
            suggestions["potential_strengths"].append("Problem-solving and innovation")
        
        # High conscientiousness
        if trait_scores.get("conscientiousness", 0) > 0.7:
            suggestions["ideal_environments"].append("Structured and goal-oriented roles")
            suggestions["potential_strengths"].append("Project management and execution")
        
        # High extraversion
        if trait_scores.get("extraversion", 0) > 0.7:
            suggestions["ideal_environments"].append("Team-based and social environments")
            suggestions["potential_strengths"].append("Leadership and communication")
        
        # High agreeableness
        if trait_scores.get("agreeableness", 0) > 0.7:
            suggestions["ideal_environments"].append("Collaborative and helping professions")
            suggestions["potential_strengths"].append("Teamwork and mentoring")
        
        # Low neuroticism
        if trait_scores.get("neuroticism", 0) < 0.3:
            suggestions["ideal_environments"].append("High-pressure or crisis management")
            suggestions["potential_strengths"].append("Stress management and resilience")
        
        return suggestions
    
    def _generate_therapeutic_considerations(self, trait_scores: Dict, clinical_features: Dict) -> List[str]:
        """Generate therapeutic considerations based on personality and clinical features"""
        considerations = []
        
        # Personality-informed therapeutic approaches
        if trait_scores.get("openness", 0) > 0.7:
            considerations.append("May respond well to insight-oriented and creative therapeutic approaches")
        
        if trait_scores.get("conscientiousness", 0) > 0.7:
            considerations.append("Likely to benefit from structured, goal-oriented interventions")
        elif trait_scores.get("conscientiousness", 0) < 0.3:
            considerations.append("May need support with treatment adherence and goal-setting")
        
        if trait_scores.get("extraversion", 0) > 0.7:
            considerations.append("Group therapy or social support interventions may be beneficial")
        elif trait_scores.get("extraversion", 0) < 0.3:
            considerations.append("Individual therapy with gradual social exposure may be preferred")
        
        if trait_scores.get("neuroticism", 0) > 0.7:
            considerations.append("Focus on emotion regulation and stress management techniques")
            if clinical_features.get("clinical_indicators", {}).get("overall_risk_score", 0) > 0.5:
                considerations.append("Consider evidence-based treatments for anxiety/mood concerns")
        
        return considerations


class ClinicalIntegrationProcessor:
    """Integrates multiple assessment frameworks with clinical-grade analysis"""
    
    def __init__(self, 
                 enneagram_processor: EnhancedEnneagramProcessor,
                 bigfive_processor: EnhancedBigFiveProcessor,
                 clinical_analyzer: ClinicalLinguisticAnalyzer):
        self.enneagram = enneagram_processor
        self.bigfive = bigfive_processor
        self.clinical = clinical_analyzer
        
    async def integrated_assessment(self, text: str) -> Dict[str, Any]:
        """Perform integrated multi-framework assessment with clinical insights"""
        
        # Extract clinical features first
        clinical_features = self.clinical.extract_clinical_features(text)
        
        # Run framework assessments in parallel
        enneagram_task = asyncio.create_task(
            self.enneagram.process(text, clinical_features)
        )
        bigfive_task = asyncio.create_task(
            self.bigfive.process(text, clinical_features)
        )
        
        # Wait for results
        enneagram_results, enneagram_confidence, enneagram_insights = await enneagram_task
        bigfive_results, bigfive_confidence, bigfive_insights = await bigfive_task
        
        # Cross-framework analysis
        cross_framework_insights = self._analyze_cross_framework_patterns(
            enneagram_results,
            bigfive_results,
            clinical_features
        )
        
        # Clinical synthesis
        clinical_synthesis = self._synthesize_clinical_picture(
            enneagram_results,
            bigfive_results,
            clinical_features
        )
        
        # Risk assessment
        risk_assessment = self._comprehensive_risk_assessment(
            clinical_features,
            enneagram_results,
            bigfive_results
        )
        
        # Treatment recommendations
        treatment_recommendations = self._generate_treatment_recommendations(
            enneagram_results,
            bigfive_results,
            clinical_features,
            risk_assessment
        )
        
        return {
            "clinical_features": clinical_features,
            "enneagram": {
                "results": enneagram_results,
                "confidence": enneagram_confidence,
                "insights": enneagram_insights
            },
            "big_five": {
                "results": bigfive_results,
                "confidence": bigfive_confidence,
                "insights": bigfive_insights
            },
            "cross_framework_insights": cross_framework_insights,
            "clinical_synthesis": clinical_synthesis,
            "risk_assessment": risk_assessment,
            "treatment_recommendations": treatment_recommendations,
            "overall_confidence": self._calculate_overall_confidence(
                enneagram_confidence,
                bigfive_confidence,
                clinical_features
            )
        }
    
    def _analyze_cross_framework_patterns(self, 
                                        enneagram_results: List[Dict],
                                        bigfive_results: List[Dict],
                                        clinical_features: Dict) -> Dict[str, Any]:
        """Analyze patterns across assessment frameworks"""
        patterns = {
            "convergent_findings": [],
            "divergent_findings": [],
            "personality_integration": "",
            "behavioral_predictions": []
        }
        
        # Extract primary types/traits
        primary_enneagram = enneagram_results[0] if enneagram_results else None
        bigfive_profile = {r["trait"]: r["score"] for r in bigfive_results}
        
        # Look for convergent patterns
        if primary_enneagram and primary_enneagram["type"] == "type_1":
            if bigfive_profile.get("conscientiousness", 0) > 0.7:
                patterns["convergent_findings"].append(
                    "High conscientiousness aligns with Type 1 perfectionism"
                )
            if bigfive_profile.get("neuroticism", 0) > 0.6:
                patterns["convergent_findings"].append(
                    "Elevated neuroticism consistent with Type 1 anxiety patterns"
                )
        
        # Personality integration narrative
        if primary_enneagram:
            patterns["personality_integration"] = self._create_integration_narrative(
                primary_enneagram,
                bigfive_profile
            )
        
        # Behavioral predictions
        patterns["behavioral_predictions"] = self._predict_behaviors(
            primary_enneagram,
            bigfive_profile,
            clinical_features
        )
        
        return patterns
    
    def _synthesize_clinical_picture(self,
                                   enneagram_results: List[Dict],
                                   bigfive_results: List[Dict],
                                   clinical_features: Dict) -> Dict[str, Any]:
        """Synthesize comprehensive clinical picture"""
        synthesis = {
            "clinical_formulation": "",
            "strengths": [],
            "vulnerabilities": [],
            "protective_factors": [],
            "risk_factors": [],
            "clinical_priorities": []
        }
        
        # Analyze strengths
        bigfive_profile = {r["trait"]: r["score"] for r in bigfive_results}
        
        if bigfive_profile.get("conscientiousness", 0) > 0.7:
            synthesis["strengths"].append("Strong organizational skills and self-discipline")
            synthesis["protective_factors"].append("High conscientiousness as resilience factor")
        
        if bigfive_profile.get("openness", 0) > 0.7:
            synthesis["strengths"].append("Cognitive flexibility and creativity")
            synthesis["protective_factors"].append("Openness to therapeutic interventions")
        
        # Analyze vulnerabilities
        if bigfive_profile.get("neuroticism", 0) > 0.7:
            synthesis["vulnerabilities"].append("Emotional reactivity and stress sensitivity")
            synthesis["risk_factors"].append("High neuroticism increases mental health risks")
        
        # Clinical priorities based on risk
        risk_score = clinical_features.get("clinical_indicators", {}).get("overall_risk_score", 0)
        if risk_score > 0.7:
            synthesis["clinical_priorities"].append("Immediate mental health intervention recommended")
        elif risk_score > 0.4:
            synthesis["clinical_priorities"].append("Preventive mental health support advised")
        
        # Create formulation
        synthesis["clinical_formulation"] = self._create_clinical_formulation(
            enneagram_results,
            bigfive_results,
            clinical_features
        )
        
        return synthesis
    
    def _comprehensive_risk_assessment(self,
                                     clinical_features: Dict,
                                     enneagram_results: List[Dict],
                                     bigfive_results: List[Dict]) -> Dict[str, Any]:
        """Comprehensive risk assessment across all data"""
        risk_assessment = {
            "overall_risk_level": "low",
            "risk_domains": {},
            "immediate_concerns": [],
            "monitoring_recommendations": [],
            "protective_factors": []
        }
        
        # Clinical risk indicators
        clinical_risk = clinical_features.get("clinical_indicators", {}).get("overall_risk_score", 0)
        
        # Personality-based risk factors
        bigfive_profile = {r["trait"]: r["score"] for r in bigfive_results}
        
        # Calculate domain-specific risks
        # Mood/Anxiety risk
        mood_risk = clinical_risk * 0.4
        if bigfive_profile.get("neuroticism", 0) > 0.7:
            mood_risk += 0.3
        if primary_enneagram := (enneagram_results[0] if enneagram_results else None):
            if primary_enneagram["type"] in ["type_4", "type_6"]:
                mood_risk += 0.2
        
        risk_assessment["risk_domains"]["mood_anxiety"] = min(mood_risk, 1.0)
        
        # Interpersonal risk
        interpersonal_risk = 0
        if bigfive_profile.get("agreeableness", 0) < 0.3:
            interpersonal_risk += 0.4
        if bigfive_profile.get("extraversion", 0) < 0.2:
            interpersonal_risk += 0.3
        
        risk_assessment["risk_domains"]["interpersonal"] = interpersonal_risk
        
        # Self-harm risk (requires careful clinical judgment)
        if clinical_risk > 0.8 and bigfive_profile.get("neuroticism", 0) > 0.8:
            risk_assessment["immediate_concerns"].append(
                "Elevated clinical indicators warrant professional evaluation"
            )
        
        # Overall risk level
        max_risk = max(risk_assessment["risk_domains"].values())
        if max_risk > 0.7:
            risk_assessment["overall_risk_level"] = "high"
        elif max_risk > 0.4:
            risk_assessment["overall_risk_level"] = "moderate"
        
        # Protective factors
        if bigfive_profile.get("conscientiousness", 0) > 0.6:
            risk_assessment["protective_factors"].append("Good self-regulation abilities")
        if bigfive_profile.get("extraversion", 0) > 0.6:
            risk_assessment["protective_factors"].append("Social support seeking")
        
        return risk_assessment
    
    def _generate_treatment_recommendations(self,
                                          enneagram_results: List[Dict],
                                          bigfive_results: List[Dict],
                                          clinical_features: Dict,
                                          risk_assessment: Dict) -> Dict[str, Any]:
        """Generate comprehensive treatment recommendations"""
        recommendations = {
            "therapeutic_approaches": [],
            "specific_interventions": [],
            "self_help_strategies": [],
            "lifestyle_modifications": [],
            "follow_up_timeline": "",
            "referral_recommendations": []
        }
        
        bigfive_profile = {r["trait"]: r["score"] for r in bigfive_results}
        primary_enneagram = enneagram_results[0] if enneagram_results else None
        
        # Therapeutic approach recommendations
        if bigfive_profile.get("openness", 0) > 0.7:
            recommendations["therapeutic_approaches"].append(
                "Insight-oriented therapy (e.g., psychodynamic, existential)"
            )
        
        if bigfive_profile.get("conscientiousness", 0) > 0.6:
            recommendations["therapeutic_approaches"].append(
                "Structured approaches (e.g., CBT, DBT skills training)"
            )
        
        if risk_assessment["risk_domains"].get("mood_anxiety", 0) > 0.6:
            recommendations["therapeutic_approaches"].append(
                "Evidence-based treatments for anxiety/depression"
            )
            recommendations["specific_interventions"].append(
                "Cognitive restructuring for negative thought patterns"
            )
        
        # Enneagram-specific recommendations
        if primary_enneagram:
            if primary_enneagram["type"] == "type_1":
                recommendations["specific_interventions"].append(
                    "Self-compassion exercises for perfectionism"
                )
                recommendations["self_help_strategies"].append(
                    "Mindfulness practices to reduce self-criticism"
                )
            elif primary_enneagram["type"] == "type_2":
                recommendations["specific_interventions"].append(
                    "Boundary setting and assertiveness training"
                )
                recommendations["self_help_strategies"].append(
                    "Self-care planning and needs identification"
                )
            # Add more type-specific recommendations...
        
        # Risk-based timeline
        if risk_assessment["overall_risk_level"] == "high":
            recommendations["follow_up_timeline"] = "Immediate professional consultation recommended"
            recommendations["referral_recommendations"].append(
                "Mental health professional with crisis intervention experience"
            )
        elif risk_assessment["overall_risk_level"] == "moderate":
            recommendations["follow_up_timeline"] = "Professional consultation within 2-4 weeks"
        else:
            recommendations["follow_up_timeline"] = "Routine mental health check-in recommended"
        
        # Lifestyle modifications based on personality
        if bigfive_profile.get("neuroticism", 0) > 0.6:
            recommendations["lifestyle_modifications"].extend([
                "Regular stress management practices",
                "Consistent sleep schedule",
                "Limit caffeine and stimulants"
            ])
        
        if bigfive_profile.get("extraversion", 0) < 0.3:
            recommendations["lifestyle_modifications"].append(
                "Gradual increase in social activities"
            )
        
        return recommendations
    
    def _calculate_overall_confidence(self,
                                    enneagram_confidence: float,
                                    bigfive_confidence: float,
                                    clinical_features: Dict) -> float:
        """Calculate overall assessment confidence"""
        # Weighted average of framework confidences
        framework_confidence = (enneagram_confidence * 0.4 + bigfive_confidence * 0.6)
        
        # Adjust based on text quality
        text_quality_multiplier = 1.0
        word_count = clinical_features.get("text_statistics", {}).get("word_count", 0)
        
        if word_count < 100:
            text_quality_multiplier = 0.7
        elif word_count > 300:
            text_quality_multiplier = 1.1
        
        # Adjust based on clinical clarity
        coherence = clinical_features.get("semantic", {}).get("coherence_score", 0.5)
        clarity_multiplier = 0.7 + (coherence * 0.6)
        
        overall_confidence = framework_confidence * text_quality_multiplier * clarity_multiplier
        
        return min(0.95, max(0.3, overall_confidence))
    
    def _create_integration_narrative(self,
                                    primary_enneagram: Dict,
                                    bigfive_profile: Dict) -> str:
        """Create narrative integrating Enneagram and Big Five findings"""
        narrative_parts = []
        
        # Start with Enneagram type
        narrative_parts.append(
            f"Primary Enneagram {primary_enneagram['name']} pattern"
        )
        
        # Add Big Five modifiers
        if bigfive_profile.get("extraversion", 0) > 0.7:
            narrative_parts.append("with extraverted expression")
        elif bigfive_profile.get("extraversion", 0) < 0.3:
            narrative_parts.append("with introverted expression")
        
        if bigfive_profile.get("neuroticism", 0) > 0.7:
            narrative_parts.append("and heightened emotional sensitivity")
        
        return " ".join(narrative_parts)
    
    def _predict_behaviors(self,
                         primary_enneagram: Optional[Dict],
                         bigfive_profile: Dict,
                         clinical_features: Dict) -> List[str]:
        """Predict likely behaviors based on integrated assessment"""
        predictions = []
        
        # Stress response predictions
        if bigfive_profile.get("neuroticism", 0) > 0.7:
            if primary_enneagram and primary_enneagram["type"] == "type_1":
                predictions.append("Under stress: Increased self-criticism and rigidity")
            elif primary_enneagram and primary_enneagram["type"] == "type_2":
                predictions.append("Under stress: May become demanding or manipulative")
        
        # Social behavior predictions
        if bigfive_profile.get("extraversion", 0) > 0.7 and bigfive_profile.get("agreeableness", 0) > 0.7:
            predictions.append("Social situations: Warm, engaging, seeks harmony")
        
        return predictions
    
    def _create_clinical_formulation(self,
                                   enneagram_results: List[Dict],
                                   bigfive_results: List[Dict],
                                   clinical_features: Dict) -> str:
        """Create comprehensive clinical formulation"""
        formulation_parts = []
        
        # Personality structure
        primary_enneagram = enneagram_results[0] if enneagram_results else None
        bigfive_profile = {r["trait"]: r["score"] for r in bigfive_results}
        
        if primary_enneagram:
            formulation_parts.append(
                f"Presents with {primary_enneagram['name']} personality organization"
            )
        
        # Add Big Five descriptors
        high_traits = [k for k, v in bigfive_profile.items() if v > 0.7]
        if high_traits:
            formulation_parts.append(
                f"characterized by high {', '.join(high_traits)}"
            )
        
        # Clinical features
        risk_score = clinical_features.get("clinical_indicators", {}).get("overall_risk_score", 0)
        if risk_score > 0.5:
            formulation_parts.append(
                "with elevated clinical risk indicators"
            )
        
        # Linguistic patterns
        if clinical_features.get("psycholinguistic", {}).get("self_focus", 0) > 0.08:
            formulation_parts.append(
                "showing heightened self-referential processing"
            )
        
        return ". ".join(formulation_parts) + "."


# Example usage
async def demonstrate_clinical_assessment():
    """Demonstrate the enhanced clinical assessment system"""
    
    # Initialize components
    clinical_analyzer = ClinicalLinguisticAnalyzer()
    enneagram_processor = EnhancedEnneagramProcessor(clinical_analyzer)
    bigfive_processor = EnhancedBigFiveProcessor(clinical_analyzer)
    integrator = ClinicalIntegrationProcessor(
        enneagram_processor,
        bigfive_processor,
        clinical_analyzer
    )
    
    # Sample text for assessment
    sample_text = """
    I find myself constantly worrying about whether I'm doing things correctly. 
    I have very high standards for myself and others, and it frustrates me when 
    people are careless or don't follow proper procedures. I tend to be quite 
    organized and detail-oriented, but sometimes I feel overwhelmed by all the 
    things that need to be fixed or improved. I don't have many close friends 
    because I find it hard to relax and just enjoy social situations - I'm always 
    noticing what could be better. Recently, I've been feeling more anxious than 
    usual, and I can't seem to turn off my critical inner voice.
    """
    
    # Run integrated assessment
    results = await integrator.integrated_assessment(sample_text)
    
    # Display results
    print("=== CLINICAL LINGUISTIC FEATURES ===")
    print(f"Word count: {results['clinical_features']['text_statistics']['word_count']}")
    print(f"Complexity score: {results['clinical_features']['complexity']['lexical_diversity']:.2f}")
    print(f"Clinical risk: {results['clinical_features']['clinical_indicators']['overall_risk_score']:.2f}")
    
    print("\n=== ENNEAGRAM ASSESSMENT ===")
    for i, etype in enumerate(results['enneagram']['results'][:3]):
        print(f"{i+1}. {etype['name']}: {etype['score']:.2f} (confidence: {etype['confidence']:.2f})")
    
    print("\n=== BIG FIVE PROFILE ===")
    for trait in results['big_five']['results']:
        print(f"{trait['name']}: {trait['level']} ({trait['score']:.2f})")
    
    print("\n=== CLINICAL SYNTHESIS ===")
    print(f"Clinical Formulation: {results['clinical_synthesis']['clinical_formulation']}")
    print(f"Risk Level: {results['risk_assessment']['overall_risk_level']}")
    
    print("\n=== TREATMENT RECOMMENDATIONS ===")
    for approach in results['treatment_recommendations']['therapeutic_approaches'][:2]:
        print(f"- {approach}")
    
    print(f"\nOverall Assessment Confidence: {results['overall_confidence']:.2%}")


if __name__ == "__main__":
    # Run demonstration
    asyncio.run(demonstrate_clinical_assessment())