#!/usr/bin/env python3
"""
Enhanced API Server with Interactive Assessment Support
Supports multi-step assessments with follow-up questions
"""

import asyncio
import json
import sys
import os
import uuid
from datetime import datetime
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import urllib.parse

# Add paths for imports
sys.path.insert(0, str(Path(__file__).parent))
from run_production import ProductionSystem

class AssessmentSession:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.created_at = datetime.now()
        self.conversation_history = []
        self.current_step = 0
        self.confidence_scores = []
        self.preliminary_results = None
        self.needs_followup = False
        self.total_steps = 3  # Initial + 2 potential follow-ups
        
    def add_response(self, text: str, result: dict):
        self.conversation_history.append({
            "step": self.current_step,
            "user_input": text,
            "result": result,
            "timestamp": datetime.now().isoformat()
        })
        
        if result.get("success"):
            confidence = result["result"]["summary"]["confidence"]
            self.confidence_scores.append(confidence)
            
            # Check if we need follow-up
            if confidence < 0.8 and self.current_step < 2:
                self.needs_followup = True
            else:
                self.needs_followup = False
        
        self.current_step += 1

class EnhancedAPIHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.sessions = {}
        self.system = None
        super().__init__(*args, **kwargs)
    
    def log_message(self, format, *args):
        # Reduce server log noise
        pass
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == '/':
            self.serve_main_page()
        elif path == '/health':
            self.handle_health()
        elif path == '/session':
            self.handle_new_session()
        elif path.startswith('/session/'):
            session_id = path.split('/')[-1]
            self.handle_session_status(session_id)
        else:
            self.send_404()
    
    def do_POST(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == '/assess':
            self.handle_simple_assess()
        elif path == '/interactive':
            self.handle_interactive_assess()
        elif path.startswith('/session/'):
            session_id = path.split('/')[-1].split('/')[0]
            if path.endswith('/respond'):
                self.handle_session_response(session_id)
            elif path.endswith('/finalize'):
                self.handle_session_finalize(session_id)
        else:
            self.send_404()
    
    def serve_main_page(self):
        """Serve the interactive assessment page"""
        html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interactive Personality Assessment</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .subtitle { opacity: 0.9; font-size: 1.1em; }
        
        .content {
            padding: 30px;
        }
        
        .assessment-area {
            display: none;
        }
        
        .assessment-area.active {
            display: block;
        }
        
        .question {
            margin-bottom: 20px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 12px;
            border-left: 4px solid #667eea;
        }
        
        .question h3 {
            color: #333;
            margin-bottom: 10px;
            font-size: 1.2em;
        }
        
        .question p {
            color: #666;
            line-height: 1.6;
        }
        
        textarea {
            width: 100%;
            min-height: 120px;
            padding: 15px;
            border: 2px solid #e1e5e9;
            border-radius: 12px;
            font-size: 16px;
            font-family: inherit;
            resize: vertical;
            transition: border-color 0.3s;
        }
        
        textarea:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        .language-note {
            font-size: 14px;
            color: #666;
            margin: 10px 0;
            text-align: center;
        }
        
        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 12px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            display: block;
            margin: 20px auto;
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
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            transition: width 0.5s ease;
            width: 0%;
        }
        
        .step-indicator {
            text-align: center;
            margin: 20px 0;
            color: #666;
            font-size: 14px;
        }
        
        .results {
            padding: 20px;
            background: #f8f9fa;
            border-radius: 12px;
            margin: 20px 0;
            display: none;
        }
        
        .results.show {
            display: block;
        }
        
        .personality-type {
            text-align: center;
            padding: 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 12px;
            margin: 20px 0;
        }
        
        .personality-type h2 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .personality-description {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .confidence-meter {
            margin: 20px 0;
            text-align: center;
        }
        
        .confidence-bar {
            width: 100%;
            height: 20px;
            background: #e1e5e9;
            border-radius: 10px;
            overflow: hidden;
            margin: 10px 0;
        }
        
        .confidence-fill {
            height: 100%;
            background: linear-gradient(90deg, #ff6b6b, #ffd93d, #6bcf7f);
            transition: width 1s ease;
        }
        
        .insights {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        
        .insight-card {
            padding: 15px;
            background: white;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }
        
        .insight-card h4 {
            color: #333;
            margin-bottom: 5px;
        }
        
        .insight-card p {
            color: #666;
            font-size: 14px;
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            display: none;
        }
        
        .loading.show {
            display: block;
        }
        
        .spinner {
            display: inline-block;
            width: 40px;
            height: 40px;
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .hebrew {
            direction: rtl;
            text-align: right;
        }
        
        .welcome {
            text-align: center;
            padding: 40px 20px;
        }
        
        .welcome h2 {
            color: #333;
            margin-bottom: 20px;
        }
        
        .welcome p {
            color: #666;
            line-height: 1.6;
            margin-bottom: 30px;
        }
        
        .start-btn {
            font-size: 18px;
            padding: 20px 40px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧠 Interactive Personality Assessment</h1>
            <p class="subtitle">Comprehensive multi-step evaluation with personalized insights</p>
        </div>
        
        <div class="content">
            <!-- Welcome Screen -->
            <div id="welcome" class="assessment-area active">
                <div class="welcome">
                    <h2>Welcome to Your Personality Journey</h2>
                    <p>This assessment will help you understand your personality type through the Enneagram framework. The process is interactive - I'll ask follow-up questions based on your responses to provide the most accurate results.</p>
                    <p><strong>What to expect:</strong></p>
                    <ul style="text-align: left; max-width: 500px; margin: 20px auto; color: #666;">
                        <li>3-5 personalized questions</li>
                        <li>Hebrew and English support</li>
                        <li>Detailed personality insights</li>
                        <li>Growth recommendations</li>
                    </ul>
                    <button onclick="startAssessment()" class="start-btn">🚀 Begin Assessment</button>
                </div>
            </div>
            
            <!-- Assessment Screen -->
            <div id="assessment" class="assessment-area">
                <div class="step-indicator">
                    <span id="stepText">Step 1 of 3</span>
                </div>
                
                <div class="progress-bar">
                    <div class="progress-fill" id="progressFill"></div>
                </div>
                
                <div class="question" id="currentQuestion">
                    <h3>Tell me about yourself</h3>
                    <p>Please describe your personality, how you approach relationships and work, what motivates you, and how you handle challenges. Be as detailed as you can - this helps me understand you better.</p>
                </div>
                
                <textarea 
                    id="responseText" 
                    placeholder="Share your thoughts here... You can write in English or Hebrew (עברית)"
                ></textarea>
                
                <div class="language-note">
                    💡 Write freely - I'll understand both languages and ask relevant follow-up questions
                </div>
                
                <button onclick="submitResponse()" id="submitBtn">Continue →</button>
            </div>
            
            <!-- Loading Screen -->
            <div id="loading" class="loading">
                <div class="spinner"></div>
                <h3>Analyzing your response...</h3>
                <p>This may take a moment as I process your unique personality patterns</p>
            </div>
            
            <!-- Results Screen -->
            <div id="results" class="assessment-area">
                <div class="personality-type" id="personalityResult">
                    <h2 id="typeNumber">Type ?</h2>
                    <p class="personality-description" id="typeDescription">Loading...</p>
                </div>
                
                <div class="confidence-meter">
                    <h3>Assessment Confidence</h3>
                    <div class="confidence-bar">
                        <div class="confidence-fill" id="confidenceFill"></div>
                    </div>
                    <p id="confidenceText">Calculating...</p>
                </div>
                
                <div class="insights" id="insightsContainer">
                    <!-- Insights will be populated here -->
                </div>
                
                <button onclick="startOver()" style="background: #28a745;">🔄 Take Another Assessment</button>
                <button onclick="downloadResults()" style="background: #17a2b8;">📄 Download Results</button>
            </div>
        </div>
    </div>
    
    <script>
        let sessionId = null;
        let currentStep = 0;
        let maxSteps = 3;
        let assessmentData = {};
        
        const typeDescriptions = {
            1: "The Perfectionist - Principled, purposeful, self-controlled, and perfectionistic",
            2: "The Helper - Demonstrative, generous, people-pleasing, and possessive",
            3: "The Achiever - Adaptive, excelling, driven, and image-conscious",
            4: "The Individualist - Expressive, dramatic, self-absorbed, and temperamental",
            5: "The Investigator - Perceptive, innovative, secretive, and isolated",
            6: "The Loyalist - Engaging, responsible, anxious, and suspicious",
            7: "The Enthusiast - Spontaneous, versatile, distractible, and scattered",
            8: "The Challenger - Self-confident, decisive, willful, and confrontational",
            9: "The Peacemaker - Receptive, reassuring, agreeable, and complacent"
        };
        
        const followUpQuestions = {
            1: "You seem to value doing things correctly. Can you describe a situation where you had to choose between following rules and being flexible? How did you handle it?",
            2: "You appear to care deeply about helping others. What happens when your own needs conflict with someone else's? How do you typically handle that tension?",
            3: "Achievement seems important to you. Can you tell me about a time when you had to choose between looking successful and being authentic? What did you do?",
            4: "You value authenticity and being unique. Describe a moment when you felt truly understood by someone. What made that interaction special?",
            5: "You seem to prefer understanding before acting. Can you think of a time when you had to make a quick decision without all the information? How did that feel?",
            6: "Security appears to be important to you. Tell me about how you build trust with new people or in uncertain situations.",
            7: "You enjoy possibilities and new experiences. What helps you stay focused when you need to complete something that isn't exciting?",
            8: "You value being in control and direct. Can you describe a situation where you had to let someone else take the lead? How was that for you?",
            9: "You seem to value harmony and peace. Tell me about a time when you had to speak up despite potential conflict. What motivated you to do that?"
        };
        
        async function startAssessment() {
            try {
                const response = await fetch('/session');
                const data = await response.json();
                sessionId = data.session_id;
                
                showScreen('assessment');
                updateProgress(1);
            } catch (error) {
                alert('Failed to start assessment: ' + error.message);
            }
        }
        
        async function submitResponse() {
            const text = document.getElementById('responseText').value.trim();
            
            if (text.length < 20) {
                alert('Please provide a more detailed response (at least 20 characters)');
                return;
            }
            
            showLoading(true);
            
            try {
                const response = await fetch(`/session/${sessionId}/respond`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({text: text})
                });
                
                const data = await response.json();
                
                if (data.needs_followup && currentStep < maxSteps - 1) {
                    // Show follow-up question
                    currentStep++;
                    updateProgress(currentStep + 1);
                    showFollowUp(data.personality_type, data.confidence);
                } else {
                    // Show final results
                    await showFinalResults();
                }
                
                assessmentData = data;
                
            } catch (error) {
                alert('Assessment failed: ' + error.message);
            } finally {
                showLoading(false);
            }
        }
        
        function showFollowUp(preliminaryType, confidence) {
            const question = followUpQuestions[preliminaryType] || 
                "Can you tell me more about how you handle challenging situations and what motivates you in difficult times?";
            
            document.getElementById('currentQuestion').innerHTML = `
                <h3>Follow-up Question</h3>
                <p>${question}</p>
                <small style="color: #666; display: block; margin-top: 10px;">
                    Based on your previous response, I detected Type ${preliminaryType} traits with ${Math.round(confidence * 100)}% confidence. 
                    This question will help me provide a more accurate assessment.
                </small>
            `;
            
            document.getElementById('responseText').value = '';
            document.getElementById('stepText').textContent = `Step ${currentStep + 1} of ${maxSteps}`;
            
            showScreen('assessment');
        }
        
        async function showFinalResults() {
            try {
                const response = await fetch(`/session/${sessionId}/finalize`, {
                    method: 'POST'
                });
                
                const data = await response.json();
                const result = data.final_result;
                
                // Update personality type display
                document.getElementById('typeNumber').textContent = `Type ${result.personality_type}`;
                document.getElementById('typeDescription').textContent = 
                    typeDescriptions[result.personality_type] || "Unknown type";
                
                // Update confidence meter
                const confidence = result.confidence;
                document.getElementById('confidenceFill').style.width = `${confidence * 100}%`;
                document.getElementById('confidenceText').textContent = 
                    `${Math.round(confidence * 100)}% confident in this assessment`;
                
                // Show insights
                showInsights(result);
                
                showScreen('results');
                
            } catch (error) {
                alert('Failed to get final results: ' + error.message);
            }
        }
        
        function showInsights(result) {
            const container = document.getElementById('insightsContainer');
            const insights = [
                {
                    title: "Language Processing",
                    content: `Detected: ${result.source_language === 'he' ? 'Hebrew' : 'English'}`
                },
                {
                    title: "Emotional Tone", 
                    content: `${result.sentiment}`
                },
                {
                    title: "Assessment Steps",
                    content: `Completed ${currentStep + 1} steps`
                },
                {
                    title: "Growth Areas",
                    content: "Self-awareness and mindfulness practices recommended"
                }
            ];
            
            container.innerHTML = insights.map(insight => `
                <div class="insight-card">
                    <h4>${insight.title}</h4>
                    <p>${insight.content}</p>
                </div>
            `).join('');
        }
        
        function showScreen(screenId) {
            document.querySelectorAll('.assessment-area').forEach(area => {
                area.classList.remove('active');
            });
            document.getElementById(screenId).classList.add('active');
        }
        
        function showLoading(show) {
            document.getElementById('loading').classList.toggle('show', show);
            document.getElementById('assessment').style.display = show ? 'none' : 'block';
        }
        
        function updateProgress(step) {
            const progress = (step / maxSteps) * 100;
            document.getElementById('progressFill').style.width = `${progress}%`;
        }
        
        function startOver() {
            sessionId = null;
            currentStep = 0;
            assessmentData = {};
            document.getElementById('responseText').value = '';
            showScreen('welcome');
            updateProgress(0);
        }
        
        function downloadResults() {
            const results = {
                session_id: sessionId,
                personality_type: assessmentData.personality_type,
                confidence: assessmentData.confidence,
                timestamp: new Date().toISOString(),
                responses: assessmentData.conversation_history || []
            };
            
            const blob = new Blob([JSON.stringify(results, null, 2)], {type: 'application/json'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `personality-assessment-${sessionId}.json`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }
        
        // Auto-detect Hebrew text direction
        document.getElementById('responseText').addEventListener('input', function(e) {
            const text = e.target.value;
            const hebrewRegex = /[\u0590-\u05FF]/;
            if (hebrewRegex.test(text)) {
                e.target.classList.add('hebrew');
            } else {
                e.target.classList.remove('hebrew');
            }
        });
    </script>
</body>
</html>
        """
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))
    
    def handle_health(self):
        """Health check endpoint"""
        health_data = {
            "status": "healthy",
            "sessions_active": len(self.sessions),
            "system_ready": self.system is not None
        }
        self.send_json_response(health_data)
    
    def handle_new_session(self):
        """Create new assessment session"""
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = AssessmentSession(session_id)
        
        self.send_json_response({
            "session_id": session_id,
            "status": "created",
            "steps_total": 3
        })
    
    def handle_session_status(self, session_id: str):
        """Get session status"""
        if session_id not in self.sessions:
            self.send_error(404, "Session not found")
            return
        
        session = self.sessions[session_id]
        self.send_json_response({
            "session_id": session_id,
            "current_step": session.current_step,
            "total_steps": session.total_steps,
            "conversation_history": session.conversation_history,
            "needs_followup": session.needs_followup
        })
    
    def handle_simple_assess(self):
        """Simple single-step assessment"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            text = data.get('text', '').strip()
            if len(text) < 10:
                self.send_error(400, "Text too short")
                return
            
            # Run assessment
            result = asyncio.run(self._assess_text(text))
            self.send_json_response(result)
            
        except Exception as e:
            self.send_error(500, str(e))
    
    def handle_interactive_assess(self):
        """Interactive multi-step assessment"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            session_id = data.get('session_id')
            text = data.get('text', '').strip()
            
            if not session_id or session_id not in self.sessions:
                self.send_error(404, "Session not found")
                return
            
            if len(text) < 10:
                self.send_error(400, "Response too short")
                return
            
            session = self.sessions[session_id]
            
            # Process the response
            result = asyncio.run(self._assess_text(text))
            session.add_response(text, result)
            
            # Determine next step
            response_data = {
                "session_id": session_id,
                "step": session.current_step,
                "result": result,
                "needs_followup": session.needs_followup,
                "conversation_history": session.conversation_history
            }
            
            if result.get("success"):
                summary = result["result"]["summary"]
                response_data.update({
                    "personality_type": summary["personality_type"],
                    "confidence": summary["confidence"],
                    "source_language": summary["source_language"]
                })
            
            self.send_json_response(response_data)
            
        except Exception as e:
            self.send_error(500, str(e))
    
    def handle_session_response(self, session_id: str):
        """Handle response in interactive session"""
        self.handle_interactive_assess()
    
    def handle_session_finalize(self, session_id: str):
        """Finalize assessment and return comprehensive results"""
        if session_id not in self.sessions:
            self.send_error(404, "Session not found")
            return
        
        session = self.sessions[session_id]
        
        if not session.conversation_history:
            self.send_error(400, "No assessment data available")
            return
        
        # Get the most recent/best result
        final_result = session.conversation_history[-1]["result"]["result"]["summary"]
        
        # Calculate overall confidence from all steps
        if session.confidence_scores:
            overall_confidence = sum(session.confidence_scores) / len(session.confidence_scores)
            final_result["confidence"] = overall_confidence
        
        comprehensive_result = {
            "session_id": session_id,
            "total_steps": len(session.conversation_history),
            "final_result": final_result,
            "conversation_history": session.conversation_history,
            "assessment_quality": "high" if overall_confidence > 0.8 else "medium"
        }
        
        self.send_json_response(comprehensive_result)
    
    async def _assess_text(self, text: str) -> dict:
        """Run assessment through the production system"""
        try:
            if not self.system:
                self.system = ProductionSystem()
                await self.system.initialize()
            
            result = await self.system.process_chain(text)
            return {"success": True, "result": result}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def send_json_response(self, data):
        """Send JSON response"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def send_404(self):
        """Send 404 response"""
        self.send_error(404, "Not found")

# Global variables to share state
global_sessions = {}
global_system = None

def run_server(port=8090):
    """Run the enhanced API server"""
    
    class HandlerClass(EnhancedAPIHandler):
        def __init__(self, *args, **kwargs):
            global global_sessions, global_system
            self.sessions = global_sessions
            self.system = global_system
            super().__init__(*args, **kwargs)
    
    try:
        server = HTTPServer(('0.0.0.0', port), HandlerClass)
        print(f"🚀 Enhanced Interactive Assessment Server running on http://localhost:{port}")
        print(f"📊 Visit http://localhost:{port} to take the full interactive assessment")
        print(f"🔍 API endpoints available:")
        print(f"   GET  /health - System health")
        print(f"   GET  /session - Create new session") 
        print(f"   POST /assess - Simple assessment")
        print(f"   POST /interactive - Interactive assessment")
        print("Press Ctrl+C to stop...")
        
        server.serve_forever()
        
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    except Exception as e:
        print(f"❌ Server error: {e}")

if __name__ == "__main__":
    run_server()