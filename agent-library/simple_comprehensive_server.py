"""
Simple Comprehensive Assessment Server

A simplified version of the comprehensive assessment system that runs the 
interactive frontend without complex orchestration dependencies.
"""

import asyncio
import json
import uuid
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import socketserver
from datetime import datetime
import threading
import logging
from typing import Dict, List, Any, Optional

# Mock assessment results for demonstration
def mock_enneagram_assessment(text: str) -> Dict[str, Any]:
    """Mock Enneagram assessment"""
    # Simple keyword-based assessment for demo
    if "creative" in text.lower() or "artistic" in text.lower():
        return {
            "assessment": {
                "top_type": "Type 4 - The Individualist",
                "description": "Creative, emotionally honest, and unique. You seek authenticity and meaning.",
                "confidence": 0.8
            },
            "strengths": ["Creative expression", "Emotional depth", "Authenticity"],
            "recommendations": ["Channel creativity constructively", "Practice emotional regulation"]
        }
    elif "organized" in text.lower() or "plan" in text.lower():
        return {
            "assessment": {
                "top_type": "Type 1 - The Perfectionist",
                "description": "Organized, principled, and improvement-oriented. You strive for excellence.",
                "confidence": 0.85
            },
            "strengths": ["High standards", "Organization", "Attention to detail"],
            "recommendations": ["Practice self-compassion", "Embrace flexibility"]
        }
    elif "help" in text.lower() or "others" in text.lower():
        return {
            "assessment": {
                "top_type": "Type 2 - The Helper",
                "description": "Caring, generous, and people-pleasing. You focus on others' needs.",
                "confidence": 0.8
            },
            "strengths": ["Empathy", "Generosity", "Interpersonal skills"],
            "recommendations": ["Set healthy boundaries", "Practice self-care"]
        }
    else:
        return {
            "assessment": {
                "top_type": "Type 7 - The Enthusiast",
                "description": "Spontaneous, versatile, and optimistic. You seek variety and excitement.",
                "confidence": 0.7
            },
            "strengths": ["Enthusiasm", "Adaptability", "Optimism"],
            "recommendations": ["Practice focus and commitment", "Develop patience"]
        }

def mock_big_five_assessment(text: str) -> Dict[str, Any]:
    """Mock Big Five assessment"""
    return {
        "big_five_profile": {
            "openness": {"score": 0.75, "description": "High openness to experience"},
            "conscientiousness": {"score": 0.65, "description": "Moderate conscientiousness"},
            "extraversion": {"score": 0.55, "description": "Moderate extraversion"},
            "agreeableness": {"score": 0.7, "description": "High agreeableness"},
            "neuroticism": {"score": 0.4, "description": "Low neuroticism"}
        },
        "summary": "Creative and agreeable personality with good emotional stability",
        "confidence": 0.8
    }

def mock_values_assessment(text: str) -> Dict[str, Any]:
    """Mock Values assessment"""
    return {
        "values_profile": {
            "individual_values": {
                "achievement": {"score": 0.7, "description": "Values accomplishment and success"},
                "benevolence": {"score": 0.8, "description": "Values helping and caring for others"},
                "creativity": {"score": 0.75, "description": "Values innovation and self-expression"}
            }
        },
        "value_priorities": [
            ("Benevolence", 0.8),
            ("Creativity", 0.75),
            ("Achievement", 0.7)
        ],
        "confidence": 0.75
    }

def mock_emotional_intelligence_assessment(text: str) -> Dict[str, Any]:
    """Mock Emotional Intelligence assessment"""
    return {
        "eq_profile": {
            "self_awareness": {"score": 0.7, "description": "Good understanding of own emotions"},
            "self_regulation": {"score": 0.65, "description": "Moderate emotional control"},
            "motivation": {"score": 0.8, "description": "High intrinsic motivation"},
            "empathy": {"score": 0.75, "description": "Strong ability to understand others"}
        },
        "overall_score": 0.725,
        "confidence": 0.8
    }

def mock_cognitive_style_assessment(text: str) -> Dict[str, Any]:
    """Mock Cognitive Style assessment"""
    return {
        "cognitive_profile": {
            "analytical": {"score": 0.7, "description": "Strong analytical thinking"},
            "creative": {"score": 0.8, "description": "High creative thinking"},
            "practical": {"score": 0.6, "description": "Moderate practical orientation"},
            "intuitive": {"score": 0.75, "description": "Strong intuitive processing"}
        },
        "thinking_style": "Creative-Analytical blend",
        "confidence": 0.75
    }

def mock_clinical_assessment(text: str) -> Dict[str, Any]:
    """Mock Clinical Language assessment"""
    return {
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

def detect_language(text: str) -> str:
    """Simple language detection"""
    hebrew_chars = set("אבגדהוזחטיכלמנסעפצקרשת")
    if any(char in hebrew_chars for char in text):
        return "he"
    return "en"

def translate_text(text: str, target_lang: str = "en") -> str:
    """Simple translation placeholder"""
    if detect_language(text) == "he" and target_lang == "en":
        # Simple Hebrew-English translation mapping for demo
        translations = {
            "אני יוצרת": "I am creative",
            "אני אוהב": "I love",
            "אני מאורגן": "I am organized"
        }
        for he, en in translations.items():
            text = text.replace(he, en)
    return text

class SimpleFrontendAPIHandler(BaseHTTPRequestHandler):
    """HTTP request handler for simplified comprehensive assessment"""
    
    def _send_cors_headers(self):
        """Send CORS headers for frontend access"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
    
    def _send_json_response(self, data, status_code=200):
        """Send JSON response"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self._send_cors_headers()
        self.end_headers()
        
        response = json.dumps(data, indent=2, default=str)
        self.wfile.write(response.encode('utf-8'))
    
    def _send_html_response(self, html_content):
        """Send HTML response"""
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self._send_cors_headers()
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))
    
    def _get_request_body(self):
        """Get JSON request body"""
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
        """Handle preflight CORS requests"""
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == '/':
            # Serve main assessment interface
            self._send_html_response(self._get_main_interface())
        
        elif path == '/health':
            # Health check
            self._send_json_response({
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat(),
                "system": "Simple Comprehensive Assessment System",
                "available_assessments": [
                    {"id": "enneagram", "name": "Enneagram Types", "description": "9 personality types focused on core motivations"},
                    {"id": "big_five", "name": "Big Five Traits", "description": "Five-factor model with personality dimensions"},
                    {"id": "values", "name": "Personal Values", "description": "Schwartz's universal human values"},
                    {"id": "emotional_intelligence", "name": "Emotional Intelligence", "description": "Four-domain EQ assessment"},
                    {"id": "cognitive_style", "name": "Cognitive Style", "description": "Thinking patterns and information processing"},
                    {"id": "clinical_language", "name": "Clinical Language Analysis", "description": "Psycholinguistic markers and risk assessment"}
                ]
            })
        
        elif path == '/assessments':
            # List available assessments
            self._send_json_response({
                "assessments": [
                    {"id": "enneagram", "name": "Enneagram Types", "description": "9 personality types focused on core motivations"},
                    {"id": "big_five", "name": "Big Five Traits", "description": "Five-factor model with personality dimensions"},
                    {"id": "values", "name": "Personal Values", "description": "Schwartz's universal human values"},
                    {"id": "emotional_intelligence", "name": "Emotional Intelligence", "description": "Four-domain EQ assessment"},
                    {"id": "cognitive_style", "name": "Cognitive Style", "description": "Thinking patterns and information processing"},
                    {"id": "clinical_language", "name": "Clinical Language Analysis", "description": "Psycholinguistic markers and risk assessment"}
                ]
            })
        
        else:
            # 404 for unknown paths
            self._send_json_response({"error": "Endpoint not found"}, 404)
    
    def do_POST(self):
        """Handle POST requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # Get request body
        request_data = self._get_request_body()
        
        try:
            if path == '/assess/complete':
                # Complete assessment
                text = request_data.get('text', '')
                user_id = request_data.get('user_id')
                
                if not text or len(text.strip()) < 10:
                    self._send_json_response({"error": "Text too short (minimum 10 characters)"}, 400)
                    return
                
                # Detect language and translate if needed
                detected_language = detect_language(text)
                translated_text = translate_text(text) if detected_language != "en" else text
                
                # Run all mock assessments
                enneagram_result = mock_enneagram_assessment(translated_text)
                big_five_result = mock_big_five_assessment(translated_text)
                values_result = mock_values_assessment(translated_text)
                eq_result = mock_emotional_intelligence_assessment(translated_text)
                cognitive_result = mock_cognitive_style_assessment(translated_text)
                clinical_result = mock_clinical_assessment(translated_text)
                
                # Generate insights
                cross_insights = [
                    f"Your {enneagram_result['assessment']['top_type']} personality aligns well with your values",
                    "Strong emotional intelligence supports your interpersonal relationships",
                    "Creative thinking style matches your openness to experience"
                ]
                
                personality_summary = f"{enneagram_result['assessment']['top_type']} | {big_five_result['summary']}"
                
                development_recommendations = (
                    enneagram_result.get('recommendations', []) + 
                    ["Practice mindfulness for emotional regulation", "Set specific goals for personal growth"]
                )[:6]
                
                # Calculate overall confidence
                confidences = [
                    enneagram_result.get('confidence', 0),
                    big_five_result.get('confidence', 0),
                    values_result.get('confidence', 0),
                    eq_result.get('confidence', 0),
                    cognitive_result.get('confidence', 0),
                    clinical_result.get('confidence', 0)
                ]
                overall_confidence = sum(confidences) / len(confidences)
                
                result = {
                    "assessment_id": f"assessment_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                    "user_input": text,
                    "detected_language": detected_language,
                    "translated_text": translated_text if detected_language != "en" else None,
                    "assessments": {
                        "enneagram": enneagram_result,
                        "big_five": big_five_result,
                        "values": values_result,
                        "emotional_intelligence": eq_result,
                        "cognitive_style": cognitive_result,
                        "clinical_language": clinical_result
                    },
                    "insights": {
                        "cross_framework_insights": cross_insights,
                        "personality_summary": personality_summary,
                        "development_recommendations": development_recommendations
                    },
                    "metadata": {
                        "overall_confidence": overall_confidence,
                        "processing_time_seconds": 1.5,
                        "timestamp": datetime.utcnow().isoformat()
                    }
                }
                
                self._send_json_response(result)
            
            elif path == '/assess/quick':
                # Quick assessment
                text = request_data.get('text', '')
                
                if not text or len(text.strip()) < 10:
                    self._send_json_response({"error": "Text too short (minimum 10 characters)"}, 400)
                    return
                
                detected_language = detect_language(text)
                translated_text = translate_text(text) if detected_language != "en" else text
                
                result = {
                    "enneagram": mock_enneagram_assessment(translated_text),
                    "big_five": mock_big_five_assessment(translated_text),
                    "detected_language": detected_language,
                    "assessment_type": "quick"
                }
                
                self._send_json_response(result)
            
            elif path == '/session/start':
                # Start interactive session
                text = request_data.get('text', '')
                user_id = request_data.get('user_id', f'user_{uuid.uuid4().hex[:8]}')
                
                if not text or len(text.strip()) < 10:
                    self._send_json_response({"error": "Text too short (minimum 10 characters)"}, 400)
                    return
                
                session_id = f"session_{user_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
                
                # Initial assessment
                detected_language = detect_language(text)
                translated_text = translate_text(text) if detected_language != "en" else text
                initial_result = {
                    "enneagram": mock_enneagram_assessment(translated_text),
                    "big_five": mock_big_five_assessment(translated_text)
                }
                
                # Generate follow-up question
                follow_up_questions = [
                    "How do you typically handle stress or challenging situations?",
                    "What motivates you most in life - personal achievement, relationships, or making a difference?",
                    "When making important decisions, do you rely more on logic or intuition?",
                    "How do you prefer to work - independently or as part of a team?",
                    "What would others say is your greatest strength and your biggest growth area?"
                ]
                
                result = {
                    "session_id": session_id,
                    "initial_assessment": initial_result,
                    "next_question": follow_up_questions[0],
                    "progress": "1/5"
                }
                
                self._send_json_response(result)
            
            elif path.startswith('/session/') and path.endswith('/respond'):
                # Continue interactive session
                session_id = path.split('/')[-2]
                response_text = request_data.get('response', '')
                
                if not response_text:
                    self._send_json_response({"error": "Response text required"}, 400)
                    return
                
                # Mock continuation - in real system this would track session state
                follow_up_questions = [
                    "What motivates you most in life - personal achievement, relationships, or making a difference?",
                    "When making important decisions, do you rely more on logic or intuition?",
                    "How do you prefer to work - independently or as part of a team?",
                    "What would others say is your greatest strength and your biggest growth area?"
                ]
                
                # Simulate session progress
                import random
                question_index = random.randint(0, len(follow_up_questions) - 1)
                progress_num = random.randint(2, 4)
                
                if progress_num >= 4:
                    # Session complete - return full assessment
                    combined_text = f"Initial response plus follow-up: {response_text}"
                    detected_language = detect_language(combined_text)
                    translated_text = translate_text(combined_text) if detected_language != "en" else combined_text
                    
                    # Full assessment
                    enneagram_result = mock_enneagram_assessment(translated_text)
                    big_five_result = mock_big_five_assessment(translated_text)
                    values_result = mock_values_assessment(translated_text)
                    eq_result = mock_emotional_intelligence_assessment(translated_text)
                    cognitive_result = mock_cognitive_style_assessment(translated_text)
                    clinical_result = mock_clinical_assessment(translated_text)
                    
                    final_assessment = {
                        "assessment_id": f"session_{session_id}_final",
                        "assessments": {
                            "enneagram": enneagram_result,
                            "big_five": big_five_result,
                            "values": values_result,
                            "emotional_intelligence": eq_result,
                            "cognitive_style": cognitive_result,
                            "clinical_language": clinical_result
                        },
                        "insights": {
                            "personality_summary": f"{enneagram_result['assessment']['top_type']} with strong emotional intelligence",
                            "development_recommendations": ["Continue self-reflection", "Practice mindfulness", "Set clear goals"]
                        }
                    }
                    
                    result = {
                        "session_id": session_id,
                        "status": "completed",
                        "final_assessment": final_assessment
                    }
                else:
                    # Continue session
                    result = {
                        "session_id": session_id,
                        "status": "continuing",
                        "current_assessment": {
                            "enneagram": mock_enneagram_assessment(response_text),
                            "big_five": mock_big_five_assessment(response_text)
                        },
                        "next_question": follow_up_questions[question_index],
                        "progress": f"{progress_num}/5"
                    }
                
                self._send_json_response(result)
            
            else:
                self._send_json_response({"error": "Endpoint not found"}, 404)
        
        except Exception as e:
            print(f"Error processing request: {e}")
            self._send_json_response({"error": f"Internal server error: {str(e)}"}, 500)
    
    def _get_main_interface(self):
        """Generate main assessment interface HTML"""
        # Read the HTML from the frontend_api_server.py since it's already well-designed
        try:
            with open('frontend_api_server.py', 'r') as f:
                content = f.read()
            
            # Extract HTML content between the triple quotes
            start_marker = "return '''"
            end_marker = "        '''"
            
            start_index = content.find(start_marker)
            if start_index != -1:
                start_index += len(start_marker)
                end_index = content.find(end_marker, start_index)
                if end_index != -1:
                    html_content = content[start_index:end_index].strip()
                    return html_content
        except:
            pass
        
        # Fallback simple HTML
        return '''
<!DOCTYPE html>
<html>
<head>
    <title>Comprehensive Psychological Assessment</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
        h1 { color: #2c3e50; text-align: center; }
        textarea { width: 100%; height: 120px; margin: 10px 0; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
        button { background: #3498db; color: white; padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer; margin: 10px 5px; }
        button:hover { background: #2980b9; }
        .results { margin-top: 20px; padding: 20px; background: #ecf0f1; border-radius: 5px; display: none; }
        .assessment-card { background: white; margin: 10px 0; padding: 15px; border-radius: 5px; border-left: 4px solid #3498db; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧠 Comprehensive Psychological Assessment</h1>
        <p style="text-align: center; color: #666;">AI-powered personality analysis using multiple psychological frameworks</p>
        
        <div style="margin: 20px 0;">
            <h3>Tell us about yourself</h3>
            <textarea id="inputText" placeholder="Write about yourself, your personality, values, how you handle challenges, what motivates you, etc. Both English and Hebrew are supported."></textarea>
        </div>
        
        <div style="text-align: center;">
            <button onclick="completeAssessment()">Complete Assessment</button>
            <button onclick="quickAssessment()">Quick Assessment</button>
            <button onclick="startInteractive()">Interactive Session</button>
        </div>
        
        <div id="results" class="results"></div>
    </div>

    <script>
        async function completeAssessment() {
            const text = document.getElementById('inputText').value;
            if (text.length < 10) {
                alert('Please provide at least 10 characters of text.');
                return;
            }
            
            showLoading();
            try {
                const response = await fetch('/assess/complete', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: text })
                });
                
                const result = await response.json();
                displayResults(result);
            } catch (error) {
                showError('Assessment failed: ' + error.message);
            }
        }
        
        async function quickAssessment() {
            const text = document.getElementById('inputText').value;
            if (text.length < 10) {
                alert('Please provide at least 10 characters of text.');
                return;
            }
            
            showLoading();
            try {
                const response = await fetch('/assess/quick', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: text })
                });
                
                const result = await response.json();
                displayQuickResults(result);
            } catch (error) {
                showError('Assessment failed: ' + error.message);
            }
        }
        
        async function startInteractive() {
            const text = document.getElementById('inputText').value;
            if (text.length < 10) {
                alert('Please provide at least 10 characters of text.');
                return;
            }
            
            showLoading();
            try {
                const response = await fetch('/session/start', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: text })
                });
                
                const result = await response.json();
                displayInteractiveSession(result);
            } catch (error) {
                showError('Session failed: ' + error.message);
            }
        }
        
        function displayResults(result) {
            const resultsDiv = document.getElementById('results');
            let html = '<h3>🎯 Complete Assessment Results</h3>';
            
            if (result.detected_language && result.detected_language !== 'en') {
                html += `<p style="background: #e3f2fd; padding: 10px; border-radius: 5px;">🌐 Language detected: ${result.detected_language.toUpperCase()} → Translated to English</p>`;
            }
            
            html += `<div class="assessment-card"><h4>Summary</h4><p><strong>${result.insights.personality_summary}</strong></p></div>`;
            
            // Show individual assessments
            Object.entries(result.assessments).forEach(([key, assessment]) => {
                const title = key.replace('_', ' ').toUpperCase();
                html += `<div class="assessment-card"><h4>${title}</h4>`;
                
                if (assessment.assessment) {
                    html += `<p><strong>${assessment.assessment.top_type || assessment.assessment.description}</strong></p>`;
                    if (assessment.assessment.description && assessment.assessment.top_type) {
                        html += `<p>${assessment.assessment.description}</p>`;
                    }
                } else if (assessment.summary) {
                    html += `<p>${assessment.summary}</p>`;
                }
                
                html += `</div>`;
            });
            
            // Show insights and recommendations
            html += `<div class="assessment-card"><h4>🔗 Cross-Framework Insights</h4>`;
            result.insights.cross_framework_insights.forEach(insight => {
                html += `<p>• ${insight}</p>`;
            });
            html += `</div>`;
            
            html += `<div class="assessment-card"><h4>🚀 Development Recommendations</h4>`;
            result.insights.development_recommendations.forEach(rec => {
                html += `<p>• ${rec}</p>`;
            });
            html += `</div>`;
            
            html += `<p style="text-align: center; color: #666; margin-top: 20px;">Overall Confidence: ${Math.round(result.metadata.overall_confidence * 100)}%</p>`;
            
            resultsDiv.innerHTML = html;
            resultsDiv.style.display = 'block';
        }
        
        function displayQuickResults(result) {
            const resultsDiv = document.getElementById('results');
            let html = '<h3>⚡ Quick Assessment Results</h3>';
            
            if (result.detected_language !== 'en') {
                html += `<p style="background: #e3f2fd; padding: 10px; border-radius: 5px;">🌐 Language detected: ${result.detected_language.toUpperCase()}</p>`;
            }
            
            if (result.enneagram && result.enneagram.assessment) {
                html += `<div class="assessment-card"><h4>🔴 Enneagram Type</h4><p><strong>${result.enneagram.assessment.top_type}</strong></p><p>${result.enneagram.assessment.description}</p></div>`;
            }
            
            if (result.big_five && result.big_five.summary) {
                html += `<div class="assessment-card"><h4>🌟 Big Five Profile</h4><p>${result.big_five.summary}</p></div>`;
            }
            
            resultsDiv.innerHTML = html;
            resultsDiv.style.display = 'block';
        }
        
        function displayInteractiveSession(result) {
            const resultsDiv = document.getElementById('results');
            let html = '<h3>📝 Interactive Assessment Session</h3>';
            html += `<p><strong>Progress:</strong> ${result.progress}</p>`;
            
            if (result.status === 'completed') {
                displayResults(result.final_assessment);
                return;
            }
            
            if (result.next_question) {
                html += `<div style="background: #f0f8ff; padding: 15px; border-radius: 5px; margin: 15px 0; border-left: 4px solid #2196f3;">`;
                html += `<h4>📋 Next Question</h4><p><strong>${result.next_question}</strong></p>`;
                html += `<textarea id="sessionResponse" placeholder="Your response..." style="margin-top: 10px; height: 80px;"></textarea>`;
                html += `<button onclick="continueSession('${result.session_id}')" style="margin-top: 10px;">Submit Response</button>`;
                html += `</div>`;
            }
            
            resultsDiv.innerHTML = html;
            resultsDiv.style.display = 'block';
        }
        
        async function continueSession(sessionId) {
            const response = document.getElementById('sessionResponse').value;
            if (!response) {
                alert('Please provide a response before continuing.');
                return;
            }
            
            showLoading();
            try {
                const apiResponse = await fetch(`/session/${sessionId}/respond`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ response: response })
                });
                
                const result = await apiResponse.json();
                displayInteractiveSession(result);
            } catch (error) {
                showError('Session error: ' + error.message);
            }
        }
        
        function showLoading() {
            document.getElementById('results').innerHTML = '<p style="text-align: center;">⏳ Processing assessment...</p>';
            document.getElementById('results').style.display = 'block';
        }
        
        function showError(message) {
            document.getElementById('results').innerHTML = `<p style="color: red; text-align: center;">❌ ${message}</p>`;
            document.getElementById('results').style.display = 'block';
        }
    </script>
</body>
</html>
        '''

class ThreadedHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    """HTTP Server that handles requests in separate threads"""
    allow_reuse_address = True

def start_simple_comprehensive_server(port=8000, host='0.0.0.0'):
    """Start the simple comprehensive assessment server"""
    server_address = (host, port)
    httpd = ThreadedHTTPServer(server_address, SimpleFrontendAPIHandler)
    
    print(f"🌐 Simple Comprehensive Assessment Server starting on http://{host}:{port}")
    print(f"📊 Available endpoints:")
    print(f"   GET  /           - Main assessment interface")
    print(f"   GET  /health     - Health check")
    print(f"   POST /assess/complete - Complete assessment")
    print(f"   POST /assess/quick    - Quick assessment")
    print(f"   POST /session/start   - Start interactive session")
    print(f"   POST /session/{{id}}/respond - Continue session")
    print(f"")
    print(f"🚀 Ready for comprehensive psychological assessments!")
    print(f"📝 Features:")
    print(f"   ✅ All 6 assessment frameworks (mock implementations)")
    print(f"   ✅ Hebrew-English language detection and translation")
    print(f"   ✅ Interactive sessions with follow-up questions")
    print(f"   ✅ Cross-framework insights and recommendations")
    print(f"   ✅ Complete 'digital twin' personality profiling")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\\n🛑 Server shutting down...")
        httpd.shutdown()

if __name__ == "__main__":
    # Start the simple comprehensive server
    start_simple_comprehensive_server()