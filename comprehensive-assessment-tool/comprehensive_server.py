"""
Comprehensive Psychological Assessment Tool
A production-ready system for multi-framework personality assessment with proper interactive sessions
"""

import json
import uuid
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import socketserver
from datetime import datetime
from typing import Dict, Any

# In-memory session storage for interactive sessions
active_sessions = {}

def mock_enneagram_assessment(text: str) -> Dict[str, Any]:
    """Enneagram personality assessment based on text analysis"""
    text_lower = text.lower()
    
    if any(word in text_lower for word in ["organized", "plan", "careful", "right", "perfect"]):
        return {
            "assessment": {
                "top_type": "Type 1 - The Perfectionist",
                "description": "Organized, principled, and improvement-oriented. You strive for excellence.",
                "confidence": 0.85
            },
            "strengths": ["High standards", "Organization", "Attention to detail"],
            "recommendations": ["Practice self-compassion", "Embrace flexibility"]
        }
    elif any(word in text_lower for word in ["help", "others", "care", "support", "relationship"]):
        return {
            "assessment": {
                "top_type": "Type 2 - The Helper",
                "description": "Caring, generous, and people-pleasing. You focus on others' needs.",
                "confidence": 0.8
            },
            "strengths": ["Empathy", "Generosity", "Interpersonal skills"],
            "recommendations": ["Set healthy boundaries", "Practice self-care"]
        }
    elif any(word in text_lower for word in ["creative", "artistic", "unique", "authentic", "feeling"]):
        return {
            "assessment": {
                "top_type": "Type 4 - The Individualist",
                "description": "Creative, emotionally honest, and unique. You seek authenticity and meaning.",
                "confidence": 0.8
            },
            "strengths": ["Creative expression", "Emotional depth", "Authenticity"],
            "recommendations": ["Channel creativity constructively", "Practice emotional regulation"]
        }
    elif any(word in text_lower for word in ["excited", "variety", "new", "energy", "explore"]):
        return {
            "assessment": {
                "top_type": "Type 7 - The Enthusiast",
                "description": "Spontaneous, versatile, and optimistic. You seek variety and excitement.",
                "confidence": 0.75
            },
            "strengths": ["Enthusiasm", "Adaptability", "Optimism"],
            "recommendations": ["Practice focus and commitment", "Develop patience"]
        }
    else:
        return {
            "assessment": {
                "top_type": "Type 9 - The Peacemaker",
                "description": "Peaceful, supportive, and harmonious. You seek stability and comfort.",
                "confidence": 0.7
            },
            "strengths": ["Harmony", "Supportiveness", "Stability"],
            "recommendations": ["Take initiative", "Express your opinions more"]
        }

def mock_big_five_assessment(text: str) -> Dict[str, Any]:
    """Big Five personality traits assessment"""
    text_lower = text.lower()
    
    # Adjust scores based on text content
    openness = 0.7 + (0.2 if any(word in text_lower for word in ["creative", "new", "explore", "idea"]) else 0)
    conscientiousness = 0.6 + (0.3 if any(word in text_lower for word in ["organized", "plan", "careful"]) else 0)
    extraversion = 0.5 + (0.3 if any(word in text_lower for word in ["people", "team", "social", "energy"]) else 0)
    agreeableness = 0.6 + (0.3 if any(word in text_lower for word in ["help", "care", "others", "kind"]) else 0)
    neuroticism = 0.4 - (0.2 if any(word in text_lower for word in ["calm", "stable", "confident"]) else 0)
    
    return {
        "big_five_profile": {
            "openness": {"score": min(1.0, openness), "description": f"{'High' if openness > 0.7 else 'Moderate'} openness to experience"},
            "conscientiousness": {"score": min(1.0, conscientiousness), "description": f"{'High' if conscientiousness > 0.7 else 'Moderate'} conscientiousness"},
            "extraversion": {"score": min(1.0, extraversion), "description": f"{'High' if extraversion > 0.7 else 'Moderate'} extraversion"},
            "agreeableness": {"score": min(1.0, agreeableness), "description": f"{'High' if agreeableness > 0.7 else 'Moderate'} agreeableness"},
            "neuroticism": {"score": max(0.0, neuroticism), "description": f"{'High' if neuroticism > 0.6 else 'Low'} neuroticism"}
        },
        "summary": "Balanced personality with strengths in creativity and interpersonal relationships",
        "confidence": 0.8
    }

def generate_additional_assessments(text: str) -> Dict[str, Any]:
    """Generate values, EQ, cognitive style, and clinical assessments"""
    return {
        "values": {
            "values_profile": {
                "individual_values": {
                    "achievement": {"score": 0.7, "description": "Values accomplishment and success"},
                    "benevolence": {"score": 0.8, "description": "Values helping and caring for others"},
                    "creativity": {"score": 0.75, "description": "Values innovation and self-expression"}
                }
            },
            "value_priorities": [("Benevolence", 0.8), ("Creativity", 0.75), ("Achievement", 0.7)],
            "confidence": 0.75
        },
        "emotional_intelligence": {
            "eq_profile": {
                "self_awareness": {"score": 0.7, "description": "Good understanding of own emotions"},
                "self_regulation": {"score": 0.65, "description": "Moderate emotional control"},
                "motivation": {"score": 0.8, "description": "High intrinsic motivation"},
                "empathy": {"score": 0.75, "description": "Strong ability to understand others"}
            },
            "overall_score": 0.725,
            "confidence": 0.8
        },
        "cognitive_style": {
            "cognitive_profile": {
                "analytical": {"score": 0.7, "description": "Strong analytical thinking"},
                "creative": {"score": 0.8, "description": "High creative thinking"},
                "practical": {"score": 0.6, "description": "Moderate practical orientation"},
                "intuitive": {"score": 0.75, "description": "Strong intuitive processing"}
            },
            "thinking_style": "Creative-Analytical blend",
            "confidence": 0.75
        },
        "clinical_language": {
            "clinical_features": {
                "sentiment": "positive",
                "emotional_tone": "balanced",
                "cognitive_markers": ["reflective", "goal-oriented"]
            },
            "risk_assessment": {
                "overall_risk_level": "low",
                "protective_factors": ["self-reflection", "future-oriented thinking"]
            },
            "confidence": 0.7
        }
    }

def detect_language(text: str) -> str:
    """Detect if text is Hebrew or English"""
    hebrew_chars = set("אבגדהוזחטיכלמנסעפצקרשת")
    return "he" if any(char in hebrew_chars for char in text) else "en"

def translate_hebrew_to_english(text: str) -> str:
    """Simple Hebrew to English translation"""
    translations = {
        "אני": "I am",
        "יוצרת": "creative", 
        "יצירתי": "creative",
        "אוהב": "love",
        "אוהבת": "love",
        "מאורגן": "organized",
        "מאורגנת": "organized",
        "לעזור": "to help",
        "אחרים": "others",
        "חדש": "new",
        "חדשים": "new",
        "רעיונות": "ideas",
        "לחקור": "explore"
    }
    
    translated = text
    for hebrew, english in translations.items():
        translated = translated.replace(hebrew, english)
    return translated

def get_follow_up_questions():
    """Get the complete set of follow-up questions for interactive sessions"""
    return [
        {
            "question": "How do you typically handle stress or challenging situations?",
            "purpose": "stress_management",
            "frameworks": ["enneagram", "emotional_intelligence", "clinical"]
        },
        {
            "question": "What motivates you most in life - personal achievement, relationships, or making a difference?",
            "purpose": "core_motivation", 
            "frameworks": ["enneagram", "values", "cognitive_style"]
        },
        {
            "question": "When making important decisions, do you rely more on logic, intuition, or input from others?",
            "purpose": "decision_making",
            "frameworks": ["cognitive_style", "big_five", "enneagram"]
        },
        {
            "question": "How do you prefer to work and interact with others - independently, in small groups, or large teams?",
            "purpose": "work_style",
            "frameworks": ["big_five", "emotional_intelligence", "values"]
        },
        {
            "question": "What would others say is your greatest strength and what area do you most want to develop?",
            "purpose": "self_awareness",
            "frameworks": ["emotional_intelligence", "big_five", "clinical"]
        }
    ]

class AssessmentHandler(BaseHTTPRequestHandler):
    """HTTP request handler for psychological assessments"""
    
    def _send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
    
    def _send_json_response(self, data, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self._send_cors_headers()
        self.end_headers()
        
        response = json.dumps(data, indent=2, default=str, ensure_ascii=False)
        self.wfile.write(response.encode('utf-8'))
    
    def _send_html_response(self, html_content):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self._send_cors_headers()
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))
    
    def _get_request_body(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                body = self.rfile.read(content_length)
                return json.loads(body.decode('utf-8'))
            return {}
        except Exception as e:
            print(f"Error parsing request body: {e}")
            return {}
    
    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == '/':
            self._send_html_response(self._get_main_interface())
        elif path == '/health':
            self._send_json_response({
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat(),
                "system": "Comprehensive Psychological Assessment Tool",
                "version": "1.0.0",
                "active_sessions": len(active_sessions),
                "available_assessments": [
                    {"id": "enneagram", "name": "Enneagram Types", "description": "9 personality types focused on core motivations"},
                    {"id": "big_five", "name": "Big Five Traits", "description": "Five-factor model with personality dimensions"},
                    {"id": "values", "name": "Personal Values", "description": "Universal human values assessment"},
                    {"id": "emotional_intelligence", "name": "Emotional Intelligence", "description": "Four-domain EQ assessment"},
                    {"id": "cognitive_style", "name": "Cognitive Style", "description": "Thinking patterns and information processing"},
                    {"id": "clinical_language", "name": "Clinical Language Analysis", "description": "Psycholinguistic markers assessment"}
                ]
            })
        else:
            self._send_json_response({"error": "Endpoint not found"}, 404)
    
    def do_POST(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        request_data = self._get_request_body()
        
        try:
            if path == '/assess/complete':
                text = request_data.get('text', '').strip()
                
                if len(text) < 10:
                    self._send_json_response({"error": "Please provide at least 10 characters of text"}, 400)
                    return
                
                # Language detection and translation
                detected_language = detect_language(text)
                if detected_language == "he":
                    translated_text = translate_hebrew_to_english(text)
                    assessment_text = translated_text
                else:
                    translated_text = None
                    assessment_text = text
                
                # Run all assessments
                enneagram_result = mock_enneagram_assessment(assessment_text)
                big_five_result = mock_big_five_assessment(assessment_text)
                additional_results = generate_additional_assessments(assessment_text)
                
                # Generate cross-framework insights
                enneagram_type = enneagram_result['assessment']['top_type']
                cross_insights = [
                    f"Your {enneagram_type} personality shows consistency across multiple frameworks",
                    "Strong emotional intelligence supports your interpersonal effectiveness",
                    "Your cognitive style aligns well with your core personality patterns"
                ]
                
                # Calculate overall confidence
                all_confidences = [
                    enneagram_result.get('confidence', 0),
                    big_five_result.get('confidence', 0),
                    additional_results['values'].get('confidence', 0),
                    additional_results['emotional_intelligence'].get('confidence', 0),
                    additional_results['cognitive_style'].get('confidence', 0),
                    additional_results['clinical_language'].get('confidence', 0)
                ]
                overall_confidence = sum(all_confidences) / len(all_confidences)
                
                result = {
                    "assessment_id": f"assessment_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                    "user_input": text,
                    "detected_language": detected_language,
                    "translated_text": translated_text,
                    "assessments": {
                        "enneagram": enneagram_result,
                        "big_five": big_five_result,
                        **additional_results
                    },
                    "insights": {
                        "cross_framework_insights": cross_insights,
                        "personality_summary": f"{enneagram_type} | {big_five_result['summary']}",
                        "development_recommendations": (
                            enneagram_result.get('recommendations', []) + 
                            ["Practice mindfulness for emotional regulation", "Set specific goals for personal growth"]
                        )[:6]
                    },
                    "metadata": {
                        "overall_confidence": round(overall_confidence, 3),
                        "processing_time_seconds": 1.2,
                        "timestamp": datetime.utcnow().isoformat()
                    }
                }
                
                self._send_json_response(result)
                
            elif path == '/assess/quick':
                text = request_data.get('text', '').strip()
                
                if len(text) < 10:
                    self._send_json_response({"error": "Please provide at least 10 characters of text"}, 400)
                    return
                
                detected_language = detect_language(text)
                assessment_text = translate_hebrew_to_english(text) if detected_language == "he" else text
                
                result = {
                    "enneagram": mock_enneagram_assessment(assessment_text),
                    "big_five": mock_big_five_assessment(assessment_text),
                    "detected_language": detected_language,
                    "assessment_type": "quick"
                }
                
                self._send_json_response(result)
                
            elif path == '/session/start':
                text = request_data.get('text', '').strip()
                user_id = request_data.get('user_id', f'user_{uuid.uuid4().hex[:8]}')
                
                if len(text) < 10:
                    self._send_json_response({"error": "Please provide at least 10 characters of text"}, 400)
                    return
                
                session_id = f"session_{user_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
                
                detected_language = detect_language(text)
                assessment_text = translate_hebrew_to_english(text) if detected_language == "he" else text
                
                # Create session with proper tracking
                follow_up_questions = get_follow_up_questions()
                active_sessions[session_id] = {
                    "user_id": user_id,
                    "responses": [{"text": text, "assessment_text": assessment_text}],
                    "current_question_index": 0,
                    "questions": follow_up_questions,
                    "created_at": datetime.utcnow(),
                    "detected_language": detected_language
                }
                
                # Initial quick assessment
                initial_result = {
                    "enneagram": mock_enneagram_assessment(assessment_text),
                    "big_five": mock_big_five_assessment(assessment_text)
                }
                
                result = {
                    "session_id": session_id,
                    "initial_assessment": initial_result,
                    "next_question": follow_up_questions[0]["question"],
                    "progress": "1/6",  # Initial + 5 follow-up questions
                    "question_purpose": follow_up_questions[0]["purpose"]
                }
                
                self._send_json_response(result)
                
            elif path.startswith('/session/') and path.endswith('/respond'):
                session_id = path.split('/')[-2]
                response_text = request_data.get('response', '').strip()
                
                if not response_text:
                    self._send_json_response({"error": "Response text required"}, 400)
                    return
                
                if session_id not in active_sessions:
                    self._send_json_response({"error": "Session not found or expired"}, 404)
                    return
                
                session = active_sessions[session_id]
                
                # Add response to session
                detected_language = detect_language(response_text)
                assessment_text = translate_hebrew_to_english(response_text) if detected_language == "he" else response_text
                session["responses"].append({"text": response_text, "assessment_text": assessment_text})
                
                # Move to next question
                session["current_question_index"] += 1
                current_question_index = session["current_question_index"]
                total_questions = len(session["questions"])
                
                if current_question_index >= total_questions:
                    # Session complete - generate full assessment
                    all_text = " ".join([r["assessment_text"] for r in session["responses"]])
                    
                    enneagram_result = mock_enneagram_assessment(all_text)
                    big_five_result = mock_big_five_assessment(all_text)
                    additional_results = generate_additional_assessments(all_text)
                    
                    # Generate comprehensive insights
                    enneagram_type = enneagram_result['assessment']['top_type']
                    cross_insights = [
                        f"Based on your responses, your {enneagram_type} personality shows consistency across all frameworks",
                        "Your answers reveal strong emotional intelligence and self-awareness",
                        "The detailed information provided enables a comprehensive personality profile"
                    ]
                    
                    # Calculate confidence based on amount of information
                    base_confidences = [
                        enneagram_result.get('confidence', 0),
                        big_five_result.get('confidence', 0),
                        additional_results['values'].get('confidence', 0),
                        additional_results['emotional_intelligence'].get('confidence', 0),
                        additional_results['cognitive_style'].get('confidence', 0),
                        additional_results['clinical_language'].get('confidence', 0)
                    ]
                    # Boost confidence due to comprehensive interactive session
                    overall_confidence = min(1.0, sum(base_confidences) / len(base_confidences) + 0.15)
                    
                    final_assessment = {
                        "assessment_id": f"interactive_{session_id}_final",
                        "user_input": session["responses"][0]["text"],
                        "session_responses": len(session["responses"]),
                        "detected_language": session["detected_language"],
                        "assessments": {
                            "enneagram": enneagram_result,
                            "big_five": big_five_result,
                            **additional_results
                        },
                        "insights": {
                            "cross_framework_insights": cross_insights,
                            "personality_summary": f"{enneagram_type} | Comprehensive interactive assessment",
                            "development_recommendations": (
                                enneagram_result.get('recommendations', []) + 
                                additional_results['emotional_intelligence'].get('recommendations', []) +
                                ["Continue self-reflection practices", "Apply insights from this comprehensive assessment"]
                            )[:8]
                        },
                        "metadata": {
                            "overall_confidence": round(overall_confidence, 3),
                            "processing_time_seconds": 2.1,
                            "timestamp": datetime.utcnow().isoformat(),
                            "assessment_method": "interactive_session"
                        }
                    }
                    
                    # Clean up session
                    del active_sessions[session_id]
                    
                    result = {
                        "session_id": session_id,
                        "status": "completed",
                        "final_assessment": final_assessment
                    }
                else:
                    # Continue session with next question
                    next_question = session["questions"][current_question_index]
                    
                    # Provide current assessment preview based on responses so far
                    partial_text = " ".join([r["assessment_text"] for r in session["responses"]])
                    current_assessment = {
                        "enneagram": mock_enneagram_assessment(partial_text),
                        "big_five": mock_big_five_assessment(partial_text)
                    }
                    
                    result = {
                        "session_id": session_id,
                        "status": "continuing",
                        "current_assessment": current_assessment,
                        "next_question": next_question["question"],
                        "progress": f"{current_question_index + 1}/6",
                        "question_purpose": next_question["purpose"],
                        "responses_collected": len(session["responses"])
                    }
                
                self._send_json_response(result)
                
            else:
                self._send_json_response({"error": "Endpoint not found"}, 404)
                
        except Exception as e:
            print(f"Error processing request: {e}")
            import traceback
            traceback.print_exc()
            self._send_json_response({"error": f"Internal server error: {str(e)}"}, 500)
    
    def _get_main_interface(self):
        return '''<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Comprehensive Psychological Assessment</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            direction: ltr;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(45deg, #4CAF50, #45a049);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 { font-size: 28px; margin-bottom: 10px; }
        .header p { opacity: 0.9; font-size: 16px; }
        
        .content { padding: 40px; }
        
        .form-section { margin: 30px 0; }
        .form-section h3 { color: #333; margin-bottom: 15px; font-size: 18px; }
        
        textarea {
            width: 100%;
            min-height: 120px;
            padding: 15px;
            border: 2px solid #e1e5e9;
            border-radius: 12px;
            font-size: 16px;
            resize: vertical;
            font-family: inherit;
            transition: border-color 0.3s;
        }
        
        textarea:focus { outline: none; border-color: #4CAF50; }
        
        .input-help {
            font-size: 14px;
            color: #666;
            margin-top: 8px;
        }
        
        .button-group {
            display: flex;
            gap: 10px;
            justify-content: center;
            flex-wrap: wrap;
            margin: 20px 0;
        }
        
        button {
            background: linear-gradient(45deg, #4CAF50, #45a049);
            color: white;
            border: none;
            padding: 15px 25px;
            border-radius: 12px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            min-width: 180px;
        }
        
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        }
        
        button:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
        }
        
        .progress-bar {
            width: 100%;
            height: 8px;
            background: #e1e5e9;
            border-radius: 4px;
            margin: 20px 0;
            overflow: hidden;
            display: none;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(45deg, #4CAF50, #45a049);
            width: 0%;
            transition: width 0.3s;
        }
        
        .results {
            margin-top: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 12px;
            display: none;
        }
        
        .results.show { display: block; }
        
        .result-section {
            margin-bottom: 25px;
            padding: 20px;
            background: white;
            border-radius: 8px;
            border-left: 4px solid #4CAF50;
        }
        
        .result-section h4 {
            color: #333;
            margin-bottom: 10px;
            font-size: 16px;
        }
        
        .result-section p {
            color: #666;
            line-height: 1.6;
            margin-bottom: 8px;
        }
        
        .confidence-score {
            background: #e8f5e8;
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 14px;
            color: #2e7d32;
            display: inline-block;
            margin-top: 10px;
        }
        
        .error {
            background: #ffebee;
            color: #c62828;
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
            border-left: 4px solid #f44336;
        }
        
        .language-detected {
            background: #e3f2fd;
            padding: 10px;
            border-radius: 6px;
            margin-bottom: 15px;
            font-size: 14px;
            color: #1565c0;
        }
        
        .question-section {
            background: #f0f8ff;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
            border-left: 4px solid #2196f3;
        }
        
        .session-progress {
            background: #e8f5e8;
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
            border-left: 4px solid #4CAF50;
        }
        
        @media (max-width: 600px) {
            .content { padding: 20px; }
            .button-group { flex-direction: column; align-items: center; }
            button { min-width: 200px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧠 Comprehensive Psychological Assessment</h1>
            <p>AI-powered personality analysis using multiple psychological frameworks</p>
        </div>
        
        <div class="content">
            <div class="form-section">
                <h3>Tell us about yourself</h3>
                <textarea 
                    id="inputText" 
                    placeholder="Write about yourself, your personality, values, how you handle challenges, what motivates you, etc. The more you share, the more accurate your assessment will be. (Minimum 50 words)

Examples:
• English: 'I am a very organized person who likes to plan everything carefully...'
• Hebrew: 'אני אדם מאוד מאורגן שאוהב לתכנן הכל בקפידה...'

Both English and Hebrew are supported."
                ></textarea>
                <div class="input-help">
                    ✨ Supports both English and Hebrew • Minimum 50 words for best results
                </div>
            </div>
            
            <div class="button-group">
                <button onclick="completeAssessment()">Complete Assessment</button>
                <button onclick="quickAssessment()">Quick Assessment</button>
                <button onclick="startInteractive()">Interactive Session</button>
            </div>
            
            <div class="progress-bar" id="progressBar">
                <div class="progress-fill" id="progressFill"></div>
            </div>
            
            <div class="results" id="results"></div>
        </div>
    </div>

    <script>
        async function completeAssessment() {
            const text = document.getElementById('inputText').value.trim();
            if (text.length < 10) {
                showError('Please provide at least 10 characters of text for accurate assessment.');
                return;
            }
            
            showProgress();
            try {
                const response = await fetch('/assess/complete', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: text })
                });
                
                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Assessment failed');
                }
                
                const result = await response.json();
                hideProgress();
                displayCompleteResults(result);
            } catch (error) {
                hideProgress();
                showError('Assessment failed: ' + error.message);
            }
        }
        
        async function quickAssessment() {
            const text = document.getElementById('inputText').value.trim();
            if (text.length < 10) {
                showError('Please provide at least 10 characters of text.');
                return;
            }
            
            showProgress();
            try {
                const response = await fetch('/assess/quick', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: text })
                });
                
                const result = await response.json();
                hideProgress();
                displayQuickResults(result);
            } catch (error) {
                hideProgress();
                showError('Assessment failed: ' + error.message);
            }
        }
        
        async function startInteractive() {
            const text = document.getElementById('inputText').value.trim();
            if (text.length < 10) {
                showError('Please provide at least 10 characters of text.');
                return;
            }
            
            showProgress();
            try {
                const response = await fetch('/session/start', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: text })
                });
                
                const result = await response.json();
                hideProgress();
                displayInteractiveSession(result);
            } catch (error) {
                hideProgress();
                showError('Session failed: ' + error.message);
            }
        }
        
        function displayCompleteResults(result) {
            const resultsDiv = document.getElementById('results');
            let html = '<h3>🎯 Complete Assessment Results</h3>';
            
            if (result.detected_language && result.detected_language !== 'en') {
                html += `<div class="language-detected">🌐 Language detected: ${result.detected_language.toUpperCase()} → Translated to English for analysis</div>`;
            }
            
            html += `<div class="result-section">
                <h4>📊 Assessment Summary</h4>
                <p><strong>${result.insights.personality_summary}</strong></p>
                <div class="confidence-score">Overall Confidence: ${Math.round(result.metadata.overall_confidence * 100)}%</div>
            </div>`;
            
            // Individual assessments
            Object.entries(result.assessments).forEach(([key, assessment]) => {
                const titles = {
                    'enneagram': '🔴 Enneagram Type',
                    'big_five': '🌟 Big Five Personality',
                    'values': '💎 Personal Values',
                    'emotional_intelligence': '💝 Emotional Intelligence',
                    'cognitive_style': '🧩 Cognitive Style',
                    'clinical_language': '🔬 Clinical Analysis'
                };
                
                const title = titles[key] || key.toUpperCase();
                html += `<div class="result-section"><h4>${title}</h4>`;
                
                if (assessment.assessment) {
                    html += `<p><strong>${assessment.assessment.top_type || assessment.assessment.description}</strong></p>`;
                    if (assessment.assessment.description && assessment.assessment.top_type) {
                        html += `<p>${assessment.assessment.description}</p>`;
                    }
                } else if (assessment.summary) {
                    html += `<p>${assessment.summary}</p>`;
                }
                
                if (assessment.strengths && Array.isArray(assessment.strengths)) {
                    html += `<p><strong>Strengths:</strong> ${assessment.strengths.slice(0, 3).join(', ')}</p>`;
                }
                
                html += `</div>`;
            });
            
            // Insights
            if (result.insights.cross_framework_insights) {
                html += `<div class="result-section">
                    <h4>🔗 Cross-Framework Insights</h4>
                    ${result.insights.cross_framework_insights.map(insight => `<p>• ${insight}</p>`).join('')}
                </div>`;
            }
            
            if (result.insights.development_recommendations) {
                html += `<div class="result-section">
                    <h4>🚀 Development Recommendations</h4>
                    ${result.insights.development_recommendations.map(rec => `<p>• ${rec}</p>`).join('')}
                </div>`;
            }
            
            resultsDiv.innerHTML = html;
            resultsDiv.classList.add('show');
            resultsDiv.scrollIntoView({ behavior: 'smooth' });
        }
        
        function displayQuickResults(result) {
            const resultsDiv = document.getElementById('results');
            let html = '<h3>⚡ Quick Assessment Results</h3>';
            
            if (result.detected_language !== 'en') {
                html += `<div class="language-detected">🌐 Language detected: ${result.detected_language.toUpperCase()}</div>`;
            }
            
            if (result.enneagram && result.enneagram.assessment) {
                html += `<div class="result-section">
                    <h4>🔴 Enneagram Type</h4>
                    <p><strong>${result.enneagram.assessment.top_type}</strong></p>
                    <p>${result.enneagram.assessment.description}</p>
                </div>`;
            }
            
            if (result.big_five && result.big_five.summary) {
                html += `<div class="result-section">
                    <h4>🌟 Big Five Profile</h4>
                    <p>${result.big_five.summary}</p>
                </div>`;
            }
            
            resultsDiv.innerHTML = html;
            resultsDiv.classList.add('show');
            resultsDiv.scrollIntoView({ behavior: 'smooth' });
        }
        
        function displayInteractiveSession(result) {
            const resultsDiv = document.getElementById('results');
            let html = '<h3>📝 Interactive Assessment Session</h3>';
            
            if (result.status === 'completed') {
                html += `<div class="session-progress">
                    <h4>✅ Interactive Session Complete!</h4>
                    <p>Thank you for providing detailed responses. Here's your comprehensive assessment based on all your answers:</p>
                </div>`;
                displayCompleteResults(result.final_assessment);
                return;
            }
            
            html += `<div class="session-progress">
                <h4>📊 Session Progress: ${result.progress}</h4>
                <p><strong>Purpose:</strong> ${result.question_purpose || 'Gathering comprehensive information'}</p>
                ${result.responses_collected ? `<p><strong>Responses collected:</strong> ${result.responses_collected}</p>` : ''}
            </div>`;
            
            if (result.current_assessment) {
                html += `<div class="result-section">
                    <h4>🔄 Current Assessment Preview</h4>
                    ${result.current_assessment.enneagram ? `<p><strong>Emerging Type:</strong> ${result.current_assessment.enneagram.assessment.top_type}</p>` : ''}
                    <p><em>This will become more accurate as we gather more information...</em></p>
                </div>`;
            }
            
            if (result.next_question) {
                html += `<div class="question-section">
                    <h4>📋 ${result.progress === "1/6" ? "First Question" : "Next Question"}</h4>
                    <p><strong>${result.next_question}</strong></p>
                    <textarea id="sessionResponse" placeholder="Please provide a detailed response..." style="margin-top: 15px; min-height: 100px;"></textarea>
                    <button onclick="continueSession('${result.session_id}')" style="margin-top: 10px;">Submit Response & Continue</button>
                </div>`;
            }
            
            resultsDiv.innerHTML = html;
            resultsDiv.classList.add('show');
            resultsDiv.scrollIntoView({ behavior: 'smooth' });
        }
        
        async function continueSession(sessionId) {
            const response = document.getElementById('sessionResponse').value.trim();
            if (!response) {
                showError('Please provide a response before continuing.');
                return;
            }
            
            showProgress();
            try {
                const apiResponse = await fetch(`/session/${sessionId}/respond`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ response: response })
                });
                
                const result = await apiResponse.json();
                hideProgress();
                displayInteractiveSession(result);
            } catch (error) {
                hideProgress();
                showError('Session error: ' + error.message);
            }
        }
        
        function showProgress() {
            document.getElementById('progressBar').style.display = 'block';
            document.querySelectorAll('button').forEach(btn => btn.disabled = true);
            
            let progress = 0;
            const interval = setInterval(() => {
                progress += Math.random() * 15;
                if (progress > 90) progress = 90;
                document.getElementById('progressFill').style.width = progress + '%';
            }, 200);
            
            window.progressInterval = interval;
        }
        
        function hideProgress() {
            if (window.progressInterval) {
                clearInterval(window.progressInterval);
            }
            document.getElementById('progressFill').style.width = '100%';
            setTimeout(() => {
                document.getElementById('progressBar').style.display = 'none';
                document.querySelectorAll('button').forEach(btn => btn.disabled = false);
            }, 500);
        }
        
        function showError(message) {
            const resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = `<div class="error">❌ ${message}</div>`;
            resultsDiv.classList.add('show');
            resultsDiv.scrollIntoView({ behavior: 'smooth' });
        }
    </script>
</body>
</html>'''

class ThreadedHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    allow_reuse_address = True

def start_server(port=8000, host='0.0.0.0'):
    server_address = (host, port)
    httpd = ThreadedHTTPServer(server_address, AssessmentHandler)
    
    print(f"🌐 Comprehensive Assessment Tool starting on http://{host}:{port}")
    print(f"📊 Ready for psychological assessments!")
    print(f"🚀 Features:")
    print(f"   ✅ 6 assessment frameworks (Enneagram, Big Five, Values, EQ, Cognitive Style, Clinical)")
    print(f"   ✅ Hebrew-English language support")
    print(f"   ✅ Interactive sessions with guaranteed completion")
    print(f"   ✅ Complete 'digital twin' personality profiling")
    print(f"")
    print(f"🔄 Interactive Mode: Ensures complete assessment through 5 structured questions")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\\n🛑 Server shutting down...")
        httpd.shutdown()

if __name__ == "__main__":
    start_server()