#!/usr/bin/env python3
"""
Simple Docker-compatible server for agent library
"""

import json
import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime


class SimpleAgentHandler(BaseHTTPRequestHandler):
    """Simple HTTP handler for Docker deployment"""
    
    def _send_cors_headers(self):
        """Send CORS headers"""
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
        if self.path == '/health':
            self._send_json_response({
                "status": "healthy",
                "message": "Agent Library Docker Container Running",
                "timestamp": datetime.utcnow().isoformat(),
                "version": "1.0.0",
                "features": [
                    "Enneagram Assessment",
                    "Big Five Personality", 
                    "Values Assessment",
                    "Emotional Intelligence",
                    "Cognitive Style",
                    "Clinical Language Analysis",
                    "Hebrew-English Translation"
                ]
            })
        elif self.path == '/':
            # Serve simple assessment interface
            html = '''
<!DOCTYPE html>
<html>
<head>
    <title>Agent Library - Docker</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        .container { background: #f5f5f5; padding: 30px; border-radius: 10px; }
        h1 { color: #333; text-align: center; }
        textarea { width: 100%; height: 120px; padding: 10px; margin: 10px 0; }
        button { background: #4CAF50; color: white; padding: 15px 30px; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background: #45a049; }
        .result { margin-top: 20px; padding: 15px; background: white; border-radius: 5px; }
        .status { text-align: center; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧠 Agent Library System</h1>
        <div class="status">
            <p>✅ <strong>Docker Container Running Successfully!</strong></p>
            <p>🎯 Ready for Psychological Assessment</p>
        </div>
        
        <h3>Quick Assessment Test</h3>
        <textarea id="inputText" placeholder="Write about yourself (English or Hebrew supported):

Example: 'I am a very organized person who likes to plan everything carefully. I value achievement and success, but I also care about helping others.'

Hebrew example: 'אני אדם מאוד מאורגן שאוהב לתכנן הכל בקפידה. חשוב לי הצלחה והישגים, אבל גם אכפת לי לעזור לאחרים.'"></textarea>
        
        <button onclick="runAssessment()">Run Assessment</button>
        
        <div id="result" class="result" style="display: none;">
            <h4>Assessment Result:</h4>
            <div id="resultContent"></div>
        </div>
    </div>

    <script>
        async function runAssessment() {
            const text = document.getElementById('inputText').value.trim();
            
            if (text.length < 20) {
                alert('Please provide at least 20 characters of text.');
                return;
            }
            
            try {
                const response = await fetch('/assess', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: text })
                });
                
                const result = await response.json();
                
                document.getElementById('resultContent').innerHTML = `
                    <p><strong>Assessment Type:</strong> ${result.assessment_type || 'Enneagram'}</p>
                    <p><strong>Result:</strong> ${result.result || result.message}</p>
                    <p><strong>Confidence:</strong> ${result.confidence || 'N/A'}</p>
                    <p><strong>Language:</strong> ${result.detected_language || 'en'}</p>
                `;
                
                document.getElementById('result').style.display = 'block';
                
            } catch (error) {
                document.getElementById('resultContent').innerHTML = `
                    <p style="color: red;"><strong>Error:</strong> ${error.message}</p>
                `;
                document.getElementById('result').style.display = 'block';
            }
        }
    </script>
</body>
</html>
            '''
            
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))
        else:
            self._send_json_response({"error": "Endpoint not found"}, 404)
    
    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/assess':
            request_data = self._get_request_body()
            text = request_data.get('text', '').strip()
            
            if len(text) < 10:
                self._send_json_response({"error": "Text too short (minimum 10 characters)"}, 400)
                return
            
            # Simple assessment simulation
            result = self.simulate_assessment(text)
            self._send_json_response(result)
        else:
            self._send_json_response({"error": "Endpoint not found"}, 404)
    
    def simulate_assessment(self, text):
        """Simulate basic assessment for Docker demo"""
        text_lower = text.lower()
        
        # Detect language
        detected_language = "he" if any(char in text for char in "אבגדהוזחטיכלמנסעפצקרשת") else "en"
        
        # Simple keyword-based Enneagram assessment
        patterns = {
            "Type 1 - The Perfectionist": ["perfect", "right", "correct", "should", "organized", "systematic", "proper"],
            "Type 2 - The Helper": ["help", "others", "support", "care", "relationships", "family", "love"],
            "Type 3 - The Achiever": ["success", "goal", "achieve", "accomplish", "recognition", "ambitious", "win"],
            "Type 4 - The Individualist": ["unique", "different", "authentic", "creative", "feelings", "special", "artistic"],
            "Type 5 - The Investigator": ["understand", "knowledge", "analyze", "observe", "independent", "think", "learn"],
            "Type 6 - The Loyalist": ["security", "safe", "loyal", "responsible", "worry", "support", "trust"],
            "Type 7 - The Enthusiast": ["exciting", "fun", "adventure", "possibilities", "explore", "new", "variety"],
            "Type 8 - The Challenger": ["control", "power", "strong", "challenge", "direct", "leader", "confident"],
            "Type 9 - The Peacemaker": ["peace", "harmony", "calm", "comfortable", "avoid", "conflict", "easy"]
        }
        
        scores = {}
        for type_name, keywords in patterns.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                scores[type_name] = score
        
        if scores:
            top_type = max(scores.keys(), key=scores.get)
            confidence = min(0.95, scores[top_type] / 7.0)
        else:
            top_type = "Type 9 - The Peacemaker"  # Default
            confidence = 0.3
        
        return {
            "assessment_type": "Enneagram",
            "result": top_type,
            "confidence": round(confidence, 2),
            "detected_language": detected_language,
            "patterns_found": len(scores),
            "message": f"Assessment complete! Based on your text, you align most with {top_type}.",
            "timestamp": datetime.utcnow().isoformat()
        }


def start_server(port=8000):
    """Start the simple Docker server"""
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, SimpleAgentHandler)
    
    print(f"🐳 Agent Library Docker Server starting on http://0.0.0.0:{port}")
    print(f"🌐 Access the assessment interface at: http://localhost:{port}")
    print(f"🔍 Health check available at: http://localhost:{port}/health")
    print(f"🚀 Ready for psychological assessments!")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\\n🛑 Server shutting down...")
        httpd.shutdown()


if __name__ == "__main__":
    start_server()