#!/usr/bin/env python3
"""
Simple HTTP API Server for Agent System
No heavy dependencies - uses built-in http.server
"""

import asyncio
import json
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import our production system
sys.path.insert(0, str(Path(__file__).parent))
from run_production import ProductionSystem, assess_text

# Global system instance
system = None

class AgentAPIHandler(BaseHTTPRequestHandler):
    """Simple HTTP handler for agent API"""
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            html = """
            <html>
            <head><title>Agent Library API</title></head>
            <body>
                <h1>🤖 Agent Library API</h1>
                <p>Endpoints:</p>
                <ul>
                    <li>GET /health - System health check</li>
                    <li>POST /assess - Assess text</li>
                    <li>GET /test - Run test suite</li>
                </ul>
                <h2>Quick Test</h2>
                <form action="/assess" method="get">
                    <input type="text" name="text" placeholder="Enter text to assess" style="width: 400px;">
                    <button type="submit">Assess</button>
                </form>
            </body>
            </html>
            """
            self.wfile.write(html.encode())
            
        elif parsed_path.path == '/health':
            # Health check endpoint
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            if system and system.initialized:
                health = loop.run_until_complete(system.health_check())
                self.send_json_response(200, health)
            else:
                self.send_json_response(503, {"status": "unhealthy", "error": "System not initialized"})
                
        elif parsed_path.path == '/assess' and parsed_path.query:
            # Simple GET-based assessment for testing
            params = parse_qs(parsed_path.query)
            text = params.get('text', [''])[0]
            
            if text:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(assess_text(text))
                self.send_json_response(200, result)
            else:
                self.send_json_response(400, {"error": "Missing 'text' parameter"})
                
        elif parsed_path.path == '/test':
            # Run built-in tests
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            
            test_results = "Running tests...\n\n"
            
            # Test cases
            tests = [
                ("Hebrew: שלום עולם", "Basic Hebrew"),
                ("English: I love helping others", "Helper personality"),
                ("Mixed: Hello שלום", "Mixed language")
            ]
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            for text, description in tests:
                test_results += f"Test: {description}\n"
                test_results += f"Input: {text}\n"
                
                try:
                    result = loop.run_until_complete(assess_text(text))
                    if "summary" in result:
                        test_results += f"Result: {json.dumps(result['summary'], indent=2)}\n"
                    else:
                        test_results += f"Error: {result.get('error', 'Unknown error')}\n"
                except Exception as e:
                    test_results += f"Exception: {str(e)}\n"
                
                test_results += "-" * 40 + "\n"
            
            self.wfile.write(test_results.encode())
            
        else:
            self.send_error(404, "Not Found")
    
    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/assess':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                text = data.get('text', '')
                
                if not text:
                    self.send_json_response(400, {"error": "Missing 'text' field"})
                    return
                
                # Process assessment
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(assess_text(text))
                
                self.send_json_response(200, result)
                
            except json.JSONDecodeError:
                self.send_json_response(400, {"error": "Invalid JSON"})
            except Exception as e:
                logger.error(f"Assessment error: {e}")
                self.send_json_response(500, {"error": str(e)})
        else:
            self.send_error(404, "Not Found")
    
    def send_json_response(self, code, data):
        """Send JSON response"""
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())
    
    def log_message(self, format, *args):
        """Override to use logger"""
        logger.info(f"{self.client_address[0]} - {format % args}")

async def initialize_system():
    """Initialize the global system"""
    global system
    system = ProductionSystem()
    success = await system.initialize()
    if success:
        logger.info("✅ System initialized successfully")
    else:
        logger.error("❌ System initialization failed")
    return success

def run_server(port=8000):
    """Run the HTTP server"""
    logger.info(f"🚀 Starting Agent API Server on port {port}")
    
    # Initialize system
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    if not loop.run_until_complete(initialize_system()):
        logger.error("Failed to initialize system")
        sys.exit(1)
    
    # Start HTTP server
    server_address = ('', port)
    httpd = HTTPServer(server_address, AgentAPIHandler)
    
    logger.info(f"✅ Server ready at http://0.0.0.0:{port}")
    logger.info("Available endpoints:")
    logger.info("  - GET  /        - Web interface")
    logger.info("  - GET  /health  - Health check")
    logger.info("  - POST /assess  - Assess text (JSON)")
    logger.info("  - GET  /test    - Run test suite")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("👋 Shutting down server")
        httpd.shutdown()

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8000))
    run_server(port)