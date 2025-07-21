"""
Frontend API Server

Integrates the comprehensive assessment system with a web frontend
for user-friendly psychological assessments.
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

from comprehensive_assessment_system import ComprehensiveAssessmentSystem


class FrontendAPIHandler(BaseHTTPRequestHandler):
    """HTTP request handler for frontend API"""
    
    def __init__(self, *args, **kwargs):
        # Initialize assessment system (shared across requests)
        if not hasattr(FrontendAPIHandler, '_assessment_system'):
            FrontendAPIHandler._assessment_system = ComprehensiveAssessmentSystem()
        super().__init__(*args, **kwargs)
    
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
        query_params = parse_qs(parsed_path.query)
        
        if path == '/':
            # Serve main assessment interface
            self._send_html_response(self._get_main_interface())
        
        elif path == '/health':
            # Health check
            self._send_json_response({
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat(),
                "available_assessments": self._assessment_system.get_available_assessments()
            })
        
        elif path == '/assessments':
            # List available assessments
            self._send_json_response({
                "assessments": self._assessment_system.get_available_assessments()
            })
        
        elif path.startswith('/session/'):
            # Get session status
            session_id = path.split('/')[-1]
            if session_id in self._assessment_system.active_sessions:
                session_data = self._assessment_system.active_sessions[session_id]
                self._send_json_response({
                    "session_id": session_id,
                    "status": "active",
                    "responses_count": len(session_data["responses"]),
                    "partial_results": session_data.get("partial_results", {})
                })
            else:
                self._send_json_response({"error": "Session not found"}, 404)
        
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
                
                # Run assessment (in a new event loop for this thread)
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                try:
                    result = loop.run_until_complete(
                        self._assessment_system.assess_complete(text, user_id)
                    )
                    serialized_result = self._assessment_system._serialize_assessment_result(result)
                    self._send_json_response(serialized_result)
                finally:
                    loop.close()
            
            elif path == '/assess/quick':
                # Quick assessment
                text = request_data.get('text', '')
                
                if not text or len(text.strip()) < 10:
                    self._send_json_response({"error": "Text too short (minimum 10 characters)"}, 400)
                    return
                
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                try:
                    result = loop.run_until_complete(
                        self._assessment_system.assess_quick(text)
                    )
                    self._send_json_response(result)
                finally:
                    loop.close()
            
            elif path == '/session/start':
                # Start interactive session
                text = request_data.get('text', '')
                user_id = request_data.get('user_id', f'user_{uuid.uuid4().hex[:8]}')
                
                if not text or len(text.strip()) < 10:
                    self._send_json_response({"error": "Text too short (minimum 10 characters)"}, 400)
                    return
                
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                try:
                    result = loop.run_until_complete(
                        self._assessment_system.start_interactive_session(user_id, text)
                    )
                    self._send_json_response(result)
                finally:
                    loop.close()
            
            elif path.startswith('/session/') and path.endswith('/respond'):
                # Continue interactive session
                session_id = path.split('/')[-2]
                response_text = request_data.get('response', '')
                
                if not response_text:
                    self._send_json_response({"error": "Response text required"}, 400)
                    return
                
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                try:
                    result = loop.run_until_complete(
                        self._assessment_system.continue_interactive_session(session_id, response_text)
                    )
                    self._send_json_response(result)
                finally:
                    loop.close()
            
            else:
                self._send_json_response({"error": "Endpoint not found"}, 404)
        
        except Exception as e:
            print(f"Error processing request: {e}")
            self._send_json_response({"error": f"Internal server error: {str(e)}"}, 500)
    
    def _get_main_interface(self):
        """Generate main assessment interface HTML"""
        return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Comprehensive Psychological Assessment</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
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
        
        .header h1 {
            font-size: 28px;
            margin-bottom: 10px;
        }
        
        .header p {
            opacity: 0.9;
            font-size: 16px;
        }
        
        .content {
            padding: 40px;
        }
        
        .assessment-types {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .assessment-card {
            border: 2px solid #e1e5e9;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            transition: all 0.3s;
            cursor: pointer;
        }
        
        .assessment-card:hover {
            border-color: #4CAF50;
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        }
        
        .assessment-card.selected {
            border-color: #4CAF50;
            background: #f8fff8;
        }
        
        .assessment-card h3 {
            color: #333;
            margin-bottom: 8px;
            font-size: 16px;
        }
        
        .assessment-card p {
            color: #666;
            font-size: 13px;
            line-height: 1.4;
        }
        
        .form-section {
            margin: 30px 0;
        }
        
        .form-section h3 {
            color: #333;
            margin-bottom: 15px;
            font-size: 18px;
        }
        
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
        
        textarea:focus {
            outline: none;
            border-color: #4CAF50;
        }
        
        .input-help {
            font-size: 14px;
            color: #666;
            margin-top: 8px;
        }
        
        button {
            background: linear-gradient(45deg, #4CAF50, #45a049);
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
            min-width: 200px;
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
        
        .results.show {
            display: block;
        }
        
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
        
        .recommendations {
            list-style: none;
        }
        
        .recommendations li {
            padding: 8px 0;
            border-bottom: 1px solid #eee;
        }
        
        .recommendations li:last-child {
            border-bottom: none;
        }
        
        .language-detected {
            background: #e3f2fd;
            padding: 10px;
            border-radius: 6px;
            margin-bottom: 15px;
            font-size: 14px;
            color: #1565c0;
        }
        
        .loading {
            text-align: center;
            padding: 40px;
        }
        
        .spinner {
            border: 3px solid #f3f3f3;
            border-top: 3px solid #4CAF50;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .error {
            background: #ffebee;
            color: #c62828;
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
            border-left: 4px solid #f44336;
        }
        
        .session-mode {
            background: #e8f5e8;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
            border-left: 4px solid #4CAF50;
        }
        
        .question-section {
            background: #f0f8ff;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
            border-left: 4px solid #2196f3;
        }
        
        .mode-selector {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            justify-content: center;
        }
        
        .mode-btn {
            padding: 10px 20px;
            border: 2px solid #e1e5e9;
            background: white;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
            min-width: auto;
            margin: 0;
        }
        
        .mode-btn.active {
            border-color: #4CAF50;
            background: #f8fff8;
            color: #2e7d32;
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
            <!-- Assessment Mode Selection -->
            <div class="form-section">
                <h3>Assessment Mode</h3>
                <div class="mode-selector">
                    <button class="mode-btn active" onclick="selectMode('complete')">Complete Assessment</button>
                    <button class="mode-btn" onclick="selectMode('quick')">Quick Assessment</button>
                    <button class="mode-btn" onclick="selectMode('interactive')">Interactive Session</button>
                </div>
            </div>
            
            <!-- Available Assessment Types -->
            <div class="form-section">
                <h3>Assessment Frameworks</h3>
                <div class="assessment-types" id="assessmentTypes">
                    <!-- Will be populated by JavaScript -->
                </div>
            </div>
            
            <!-- Text Input -->
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
            
            <!-- Action Buttons -->
            <button id="assessBtn" onclick="startAssessment()">Start Assessment</button>
            
            <!-- Progress Bar -->
            <div class="progress-bar" id="progressBar" style="display: none;">
                <div class="progress-fill" id="progressFill"></div>
            </div>
            
            <!-- Results -->
            <div class="results" id="results"></div>
        </div>
    </div>

    <script>
        let currentMode = 'complete';
        let currentSession = null;
        
        // Initialize page
        document.addEventListener('DOMContentLoaded', function() {
            loadAssessmentTypes();
        });
        
        function selectMode(mode) {
            currentMode = mode;
            
            // Update button states
            document.querySelectorAll('.mode-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            event.target.classList.add('active');
            
            // Update UI based on mode
            const assessBtn = document.getElementById('assessBtn');
            if (mode === 'interactive') {
                assessBtn.textContent = 'Start Interactive Session';
            } else if (mode === 'quick') {
                assessBtn.textContent = 'Quick Assessment';
            } else {
                assessBtn.textContent = 'Complete Assessment';
            }
        }
        
        async function loadAssessmentTypes() {
            try {
                const response = await fetch('/assessments');
                const data = await response.json();
                
                const container = document.getElementById('assessmentTypes');
                container.innerHTML = '';
                
                data.assessments.forEach(assessment => {
                    const card = document.createElement('div');
                    card.className = 'assessment-card selected';
                    card.innerHTML = `
                        <h3>${assessment.name}</h3>
                        <p>${assessment.description}</p>
                    `;
                    container.appendChild(card);
                });
            } catch (error) {
                console.error('Error loading assessment types:', error);
            }
        }
        
        async function startAssessment() {
            const text = document.getElementById('inputText').value.trim();
            
            if (text.length < 50) {
                showError('Please provide at least 50 characters of text for accurate assessment.');
                return;
            }
            
            // Clear previous results
            document.getElementById('results').classList.remove('show');
            
            // Show progress
            showProgress();
            
            try {
                let result;
                
                if (currentMode === 'interactive') {
                    result = await startInteractiveSession(text);
                } else if (currentMode === 'quick') {
                    result = await quickAssessment(text);
                } else {
                    result = await completeAssessment(text);
                }
                
                hideProgress();
                displayResults(result);
                
            } catch (error) {
                hideProgress();
                showError('Assessment failed: ' + error.message);
            }
        }
        
        async function completeAssessment(text) {
            const response = await fetch('/assess/complete', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    text: text,
                    user_id: 'web_user_' + Date.now()
                })
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Assessment failed');
            }
            
            return await response.json();
        }
        
        async function quickAssessment(text) {
            const response = await fetch('/assess/quick', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: text })
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Assessment failed');
            }
            
            return await response.json();
        }
        
        async function startInteractiveSession(text) {
            const response = await fetch('/session/start', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    text: text,
                    user_id: 'web_user_' + Date.now()
                })
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Session start failed');
            }
            
            const result = await response.json();
            currentSession = result.session_id;
            return result;
        }
        
        async function continueSession(response) {
            if (!currentSession) {
                throw new Error('No active session');
            }
            
            const apiResponse = await fetch(`/session/${currentSession}/respond`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ response: response })
            });
            
            if (!apiResponse.ok) {
                const error = await apiResponse.json();
                throw new Error(error.error || 'Session continue failed');
            }
            
            return await apiResponse.json();
        }
        
        function displayResults(result) {
            const resultsDiv = document.getElementById('results');
            let html = '';
            
            // Language detection
            if (result.detected_language && result.detected_language !== 'en') {
                html += `
                    <div class="language-detected">
                        🌐 Language detected: ${result.detected_language.toUpperCase()} → Translated to English for analysis
                    </div>
                `;
            }
            
            if (currentMode === 'interactive') {
                html += displayInteractiveResults(result);
            } else {
                html += displayAssessmentResults(result);
            }
            
            resultsDiv.innerHTML = html;
            resultsDiv.classList.add('show');
            
            // Scroll to results
            resultsDiv.scrollIntoView({ behavior: 'smooth' });
        }
        
        function displayInteractiveResults(result) {
            if (result.status === 'completed') {
                return displayAssessmentResults(result.final_assessment);
            }
            
            let html = `
                <div class="session-mode">
                    <h4>📝 Interactive Assessment Session</h4>
                    <p><strong>Progress:</strong> ${result.progress || 'In progress'}</p>
                </div>
            `;
            
            if (result.current_assessment) {
                html += `
                    <div class="result-section">
                        <h4>Current Assessment Preview</h4>
                        ${displayQuickResults(result.current_assessment)}
                    </div>
                `;
            }
            
            if (result.next_question) {
                html += `
                    <div class="question-section">
                        <h4>📋 Next Question</h4>
                        <p><strong>${result.next_question}</strong></p>
                        <textarea id="sessionResponse" placeholder="Your response..." style="margin-top: 15px; min-height: 80px;"></textarea>
                        <button onclick="submitSessionResponse()" style="margin-top: 10px;">Submit Response</button>
                    </div>
                `;
            }
            
            return html;
        }
        
        function displayAssessmentResults(result) {
            let html = `
                <div class="result-section">
                    <h4>🎯 Assessment Summary</h4>
                    <p><strong>${result.insights?.personality_summary || 'Assessment completed successfully'}</strong></p>
                    <div class="confidence-score">Overall Confidence: ${Math.round((result.metadata?.overall_confidence || 0) * 100)}%</div>
                </div>
            `;
            
            // Individual assessments
            if (result.assessments) {
                Object.entries(result.assessments).forEach(([key, assessment]) => {
                    if (assessment && !assessment.error) {
                        html += formatAssessmentSection(key, assessment);
                    }
                });
            } else if (result.enneagram || result.big_five) {
                // Quick assessment format
                html += displayQuickResults(result);
            }
            
            // Insights and recommendations
            if (result.insights?.cross_framework_insights) {
                html += `
                    <div class="result-section">
                        <h4>🔗 Cross-Framework Insights</h4>
                        ${result.insights.cross_framework_insights.map(insight => `<p>• ${insight}</p>`).join('')}
                    </div>
                `;
            }
            
            if (result.insights?.development_recommendations) {
                html += `
                    <div class="result-section">
                        <h4>🚀 Development Recommendations</h4>
                        <ul class="recommendations">
                            ${result.insights.development_recommendations.map(rec => `<li>• ${rec}</li>`).join('')}
                        </ul>
                    </div>
                `;
            }
            
            return html;
        }
        
        function displayQuickResults(result) {
            let html = '';
            
            if (result.enneagram && !result.enneagram.error) {
                const enneagram = result.enneagram;
                if (enneagram.assessment) {
                    html += `
                        <div class="result-section">
                            <h4>🔴 Enneagram Type</h4>
                            <p><strong>${enneagram.assessment.top_type}</strong></p>
                            <p>${enneagram.assessment.description}</p>
                        </div>
                    `;
                }
            }
            
            if (result.big_five && !result.big_five.error) {
                html += `
                    <div class="result-section">
                        <h4>🌟 Big Five Traits</h4>
                        <p>${result.big_five.summary || 'Big Five assessment completed'}</p>
                    </div>
                `;
            }
            
            return html;
        }
        
        function formatAssessmentSection(key, assessment) {
            const titles = {
                'enneagram': '🔴 Enneagram Type',
                'big_five': '🌟 Big Five Personality',
                'values': '💎 Personal Values',
                'emotional_intelligence': '💝 Emotional Intelligence',
                'cognitive_style': '🧩 Cognitive Style',
                'clinical_language': '🔬 Clinical Analysis'
            };
            
            const title = titles[key] || key.replace('_', ' ').toUpperCase();
            
            let content = '';
            
            if (assessment.summary) {
                content += `<p><strong>${assessment.summary}</strong></p>`;
            }
            
            if (assessment.assessment?.top_type) {
                content += `<p><strong>Type:</strong> ${assessment.assessment.top_type}</p>`;
            }
            
            if (assessment.assessment?.description) {
                content += `<p>${assessment.assessment.description}</p>`;
            }
            
            if (assessment.strengths && Array.isArray(assessment.strengths)) {
                content += `<p><strong>Strengths:</strong> ${assessment.strengths.slice(0, 3).join(', ')}</p>`;
            }
            
            return `
                <div class="result-section">
                    <h4>${title}</h4>
                    ${content || '<p>Assessment completed</p>'}
                </div>
            `;
        }
        
        async function submitSessionResponse() {
            const response = document.getElementById('sessionResponse').value.trim();
            
            if (!response) {
                showError('Please provide a response before continuing.');
                return;
            }
            
            showProgress();
            
            try {
                const result = await continueSession(response);
                hideProgress();
                displayResults(result);
            } catch (error) {
                hideProgress();
                showError('Session error: ' + error.message);
            }
        }
        
        function showProgress() {
            document.getElementById('progressBar').style.display = 'block';
            document.getElementById('assessBtn').disabled = true;
            
            // Animate progress
            let progress = 0;
            const interval = setInterval(() => {
                progress += Math.random() * 15;
                if (progress > 90) progress = 90;
                document.getElementById('progressFill').style.width = progress + '%';
            }, 200);
            
            // Store interval ID for cleanup
            window.progressInterval = interval;
        }
        
        function hideProgress() {
            if (window.progressInterval) {
                clearInterval(window.progressInterval);
            }
            document.getElementById('progressFill').style.width = '100%';
            setTimeout(() => {
                document.getElementById('progressBar').style.display = 'none';
                document.getElementById('assessBtn').disabled = false;
            }, 500);
        }
        
        function showError(message) {
            const resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = `<div class="error">❌ ${message}</div>`;
            resultsDiv.classList.add('show');
        }
    </script>
</body>
</html>
        '''


class ThreadedHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    """HTTP Server that handles requests in separate threads"""
    allow_reuse_address = True


def start_frontend_server(port=8000, host='0.0.0.0'):
    """Start the frontend API server"""
    server_address = (host, port)
    httpd = ThreadedHTTPServer(server_address, FrontendAPIHandler)
    
    print(f"🌐 Frontend Assessment Server starting on http://{host}:{port}")
    print(f"📊 Available endpoints:")
    print(f"   GET  /           - Main assessment interface")
    print(f"   GET  /health     - Health check")
    print(f"   POST /assess/complete - Complete assessment")
    print(f"   POST /assess/quick    - Quick assessment")
    print(f"   POST /session/start   - Start interactive session")
    print(f"   POST /session/{{id}}/respond - Continue session")
    print(f"")
    print(f"🚀 Ready for psychological assessments!")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\\n🛑 Server shutting down...")
        httpd.shutdown()


if __name__ == "__main__":
    # Start the server
    start_frontend_server()