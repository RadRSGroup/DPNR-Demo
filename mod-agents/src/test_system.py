#!/usr/bin/env python3
"""
Comprehensive Agent Library Test Suite
Validates all components and performance criteria
"""

import asyncio
import logging
import sys
import time
import json
from pathlib import Path
from typing import Dict, Any, List, Tuple
import traceback

# Add the agent library to the path
sys.path.append(str(Path(__file__).parent))

# Import test modules
sys.path.append(str(Path(__file__).parent / "tests"))

# Import all components to test
from agent_library.core.base_agent import AgentMessage, AgentResponse, AgentStatus
from agent_library.agents.language.translation_agent import TranslationAgent
from agent_library.agents.language.nlp_analyzer_agent import NLPAnalyzerAgent
from agent_library.agents.assessment.enneagram_agent import EnneagramAgent
from agent_library.orchestration.chain_builder import ChainBuilder
from agent_library.orchestration.workflow_engine import WorkflowEngine

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SystemTestSuite:
    """Comprehensive test suite for the agent library"""
    
    def __init__(self):
        self.test_results = {
            "unit_tests": {},
            "integration_tests": {},
            "performance_tests": {},
            "hebrew_specific_tests": {},
            "summary": {}
        }
        self.agents = {}
        self.chain_builder = ChainBuilder()
        self.workflow_engine = None
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """Run the complete test suite"""
        logger.info("🧪 Starting Comprehensive Agent Library Test Suite")
        logger.info("=" * 70)
        
        start_time = time.time()
        
        try:
            # 1. Unit Tests
            logger.info("1️⃣ Running Unit Tests...")
            unit_results = await self.run_unit_tests()
            self.test_results["unit_tests"] = unit_results
            
            # 2. Integration Tests
            logger.info("\n2️⃣ Running Integration Tests...")
            integration_results = await self.run_integration_tests()
            self.test_results["integration_tests"] = integration_results
            
            # 3. Performance Tests
            logger.info("\n3️⃣ Running Performance Tests...")
            performance_results = await self.run_performance_tests()
            self.test_results["performance_tests"] = performance_results
            
            # 4. Hebrew-Specific Tests
            logger.info("\n4️⃣ Running Hebrew-Specific Tests...")
            hebrew_results = await self.run_hebrew_tests()
            self.test_results["hebrew_specific_tests"] = hebrew_results
            
            # 5. Generate Summary
            total_time = time.time() - start_time
            self.test_results["summary"] = self.generate_summary(total_time)
            
            logger.info(f"\n✅ Test Suite Completed in {total_time:.2f} seconds")
            
            return self.test_results
            
        except Exception as e:
            logger.error(f"❌ Test suite failed: {str(e)}")
            logger.error(traceback.format_exc())
            return {"error": str(e), "results": self.test_results}
    
    async def run_unit_tests(self) -> Dict[str, Any]:
        """Run unit tests for individual agents"""
        results = {}
        
        # Test Translation Agent
        logger.info("   🔄 Testing Translation Agent...")
        results["translation_agent"] = await self.test_translation_agent()
        
        # Test NLP Analyzer Agent
        logger.info("   📊 Testing NLP Analyzer Agent...")
        results["nlp_analyzer_agent"] = await self.test_nlp_analyzer_agent()
        
        # Test Enneagram Agent
        logger.info("   🧠 Testing Enneagram Agent...")
        results["enneagram_agent"] = await self.test_enneagram_agent()
        
        # Test Chain Builder
        logger.info("   🔗 Testing Chain Builder...")
        results["chain_builder"] = await self.test_chain_builder()
        
        return results
    
    async def test_translation_agent(self) -> Dict[str, Any]:
        """Test translation agent functionality"""
        results = {"passed": 0, "failed": 0, "tests": []}
        
        try:
            # Initialize agent
            agent = TranslationAgent("test_translation_agent")
            await agent.initialize()
            self.agents["translation"] = agent
            
            # Test 1: Basic English to Hebrew translation
            message = AgentMessage(
                id="test_1",
                source_agent="test",
                payload={
                    "action": "translate",
                    "text": "Hello, how are you today?",
                    "target_language": "he"
                }
            )
            
            response = await agent.handle_message(message)
            test_passed = response.success and "translated_text" in response.data
            results["tests"].append({
                "name": "English to Hebrew translation",
                "passed": test_passed,
                "response_time": response.processing_time,
                "confidence": response.confidence
            })
            if test_passed:
                results["passed"] += 1
            else:
                results["failed"] += 1
            
            # Test 2: Language detection
            message = AgentMessage(
                id="test_2",
                source_agent="test",
                payload={
                    "action": "detect_language",
                    "text": "שלום, איך אתה היום?"
                }
            )
            
            response = await agent.handle_message(message)
            test_passed = response.success and response.data.get("detected_language") == "he"
            results["tests"].append({
                "name": "Hebrew language detection",
                "passed": test_passed,
                "detected_language": response.data.get("detected_language") if response.success else None
            })
            if test_passed:
                results["passed"] += 1
            else:
                results["failed"] += 1
            
            # Test 3: Input validation
            message = AgentMessage(
                id="test_3",
                source_agent="test",
                payload={
                    "action": "translate",
                    "text": "",  # Empty text should fail
                    "target_language": "he"
                }
            )
            
            response = await agent.handle_message(message)
            test_passed = not response.success  # Should fail validation
            results["tests"].append({
                "name": "Input validation (empty text)",
                "passed": test_passed,
                "expected_failure": True
            })
            if test_passed:
                results["passed"] += 1
            else:
                results["failed"] += 1
            
        except Exception as e:
            results["error"] = str(e)
            results["failed"] += 1
        
        return results
    
    async def test_nlp_analyzer_agent(self) -> Dict[str, Any]:
        """Test NLP analyzer functionality"""
        results = {"passed": 0, "failed": 0, "tests": []}
        
        try:
            # Initialize agent
            agent = NLPAnalyzerAgent("test_nlp_agent")
            await agent.initialize()
            self.agents["nlp"] = agent
            
            # Test 1: Sentiment analysis
            message = AgentMessage(
                id="test_1",
                source_agent="test",
                payload={
                    "action": "analyze_text",
                    "text": "I am extremely happy and excited about this amazing opportunity!",
                    "features": ["sentiment", "emotion"]
                }
            )
            
            response = await agent.handle_message(message)
            test_passed = (response.success and 
                          "sentiment" in response.data and
                          "emotion" in response.data)
            results["tests"].append({
                "name": "Sentiment and emotion analysis",
                "passed": test_passed,
                "sentiment": response.data.get("sentiment") if response.success else None,
                "response_time": response.processing_time
            })
            if test_passed:
                results["passed"] += 1
            else:
                results["failed"] += 1
            
            # Test 2: Text statistics
            message = AgentMessage(
                id="test_2",
                source_agent="test",
                payload={
                    "action": "analyze_text",
                    "text": "This is a sample text for testing. It contains multiple sentences and various words.",
                    "features": ["stats", "linguistic"]
                }
            )
            
            response = await agent.handle_message(message)
            test_passed = (response.success and 
                          "stats" in response.data and
                          response.data["stats"]["word_count"] > 0)
            results["tests"].append({
                "name": "Text statistics extraction",
                "passed": test_passed,
                "word_count": response.data.get("stats", {}).get("word_count") if response.success else None
            })
            if test_passed:
                results["passed"] += 1
            else:
                results["failed"] += 1
            
            # Test 3: Keyword extraction
            message = AgentMessage(
                id="test_3",
                source_agent="test",
                payload={
                    "action": "extract_keywords",
                    "text": "Natural language processing is an important field in artificial intelligence research.",
                    "top_k": 5
                }
            )
            
            response = await agent.handle_message(message)
            test_passed = (response.success and 
                          "keywords" in response.data and
                          len(response.data["keywords"]) > 0)
            results["tests"].append({
                "name": "Keyword extraction",
                "passed": test_passed,
                "keyword_count": len(response.data.get("keywords", [])) if response.success else 0
            })
            if test_passed:
                results["passed"] += 1
            else:
                results["failed"] += 1
            
        except Exception as e:
            results["error"] = str(e)
            results["failed"] += 1
        
        return results
    
    async def test_enneagram_agent(self) -> Dict[str, Any]:
        """Test Enneagram assessment functionality"""
        results = {"passed": 0, "failed": 0, "tests": []}
        
        try:
            # Initialize agent
            agent = EnneagramAgent("test_enneagram_agent")
            await agent.initialize()
            self.agents["enneagram"] = agent
            
            # Test 1: Type 7 (Enthusiast) assessment
            message = AgentMessage(
                id="test_1",
                source_agent="test",
                payload={
                    "action": "assess_enneagram",
                    "text": "I love exploring new opportunities and having fun experiences. I'm always looking for the next exciting adventure and I tend to be optimistic about everything. Sometimes I have trouble focusing on one thing for too long because there are so many interesting options out there.",
                }
            )
            
            response = await agent.handle_message(message)
            test_passed = (response.success and 
                          "primary_type" in response.data and
                          response.data["confidence"] > 0.5)
            results["tests"].append({
                "name": "Type 7 assessment",
                "passed": test_passed,
                "primary_type": response.data.get("primary_type") if response.success else None,
                "confidence": response.data.get("confidence") if response.success else 0,
                "response_time": response.processing_time
            })
            if test_passed:
                results["passed"] += 1
            else:
                results["failed"] += 1
            
            # Test 2: Type comparison
            message = AgentMessage(
                id="test_2",
                source_agent="test",
                payload={
                    "action": "compare_types",
                    "text": "I really care about helping others and making sure everyone is comfortable. I often put other people's needs before my own.",
                    "candidate_types": [2, 6, 9]  # Helper, Loyalist, Peacemaker
                }
            )
            
            response = await agent.handle_message(message)
            test_passed = (response.success and 
                          "type_comparison" in response.data)
            results["tests"].append({
                "name": "Type comparison",
                "passed": test_passed,
                "most_likely": response.data.get("most_likely") if response.success else None
            })
            if test_passed:
                results["passed"] += 1
            else:
                results["failed"] += 1
            
            # Test 3: Detailed analysis
            message = AgentMessage(
                id="test_3",
                source_agent="test",
                payload={
                    "action": "detailed_analysis",
                    "text": "I strive for perfection in everything I do. I have high standards and I get frustrated when things aren't done correctly.",
                    "include_wings": True
                }
            )
            
            response = await agent.handle_message(message)
            test_passed = (response.success and 
                          "basic_assessment" in response.data and
                          "wing_analysis" in response.data)
            results["tests"].append({
                "name": "Detailed analysis with wings",
                "passed": test_passed,
                "has_wing_analysis": "wing_analysis" in response.data if response.success else False
            })
            if test_passed:
                results["passed"] += 1
            else:
                results["failed"] += 1
            
        except Exception as e:
            results["error"] = str(e)
            results["failed"] += 1
        
        return results
    
    async def test_chain_builder(self) -> Dict[str, Any]:
        """Test chain builder functionality"""
        results = {"passed": 0, "failed": 0, "tests": []}
        
        try:
            # Test 1: Create simple chain
            chain = self.chain_builder.create_chain("test_chain", "Test Chain")
            test_passed = chain is not None and chain.chain_id == "test_chain"
            results["tests"].append({
                "name": "Create simple chain",
                "passed": test_passed
            })
            if test_passed:
                results["passed"] += 1
            else:
                results["failed"] += 1
            
            # Test 2: Add agents to chain
            self.chain_builder.add_agent("test_chain", "agent1", "TestAgent")
            self.chain_builder.add_agent("test_chain", "agent2", "TestAgent")
            
            chain = self.chain_builder.chains["test_chain"]
            test_passed = len(chain.nodes) == 2
            results["tests"].append({
                "name": "Add agents to chain",
                "passed": test_passed,
                "node_count": len(chain.nodes)
            })
            if test_passed:
                results["passed"] += 1
            else:
                results["failed"] += 1
            
            # Test 3: Connect agents
            self.chain_builder.connect_agents("test_chain", "agent1", "agent2")
            
            chain = self.chain_builder.chains["test_chain"]
            test_passed = len(chain.connections) == 1
            results["tests"].append({
                "name": "Connect agents",
                "passed": test_passed,
                "connection_count": len(chain.connections)
            })
            if test_passed:
                results["passed"] += 1
            else:
                results["failed"] += 1
            
            # Test 4: Export/import chain
            exported = self.chain_builder.export_chain("test_chain", "json")
            imported_chain = self.chain_builder.import_chain(exported, "json")
            
            test_passed = (imported_chain.chain_id == "test_chain" and
                          len(imported_chain.nodes) == 2)
            results["tests"].append({
                "name": "Export/import chain",
                "passed": test_passed
            })
            if test_passed:
                results["passed"] += 1
            else:
                results["failed"] += 1
            
        except Exception as e:
            results["error"] = str(e)
            results["failed"] += 1
        
        return results
    
    async def run_integration_tests(self) -> Dict[str, Any]:
        """Run integration tests between agents"""
        results = {"passed": 0, "failed": 0, "tests": []}
        
        try:
            # Create workflow engine
            self.workflow_engine = WorkflowEngine(self.chain_builder)
            
            # Register agents
            for agent in self.agents.values():
                self.workflow_engine.register_agent(agent)
            
            # Register agent types
            self.chain_builder.register_agent(TranslationAgent, "TranslationAgent")
            self.chain_builder.register_agent(NLPAnalyzerAgent, "NLPAnalyzerAgent")
            self.chain_builder.register_agent(EnneagramAgent, "EnneagramAgent")
            
            # Test 1: Translation + NLP chain
            logger.info("     🔄 Testing Translation → NLP chain...")
            chain = self.chain_builder.create_chain("trans_nlp_chain", "Translation + NLP")
            
            self.chain_builder.add_agent("trans_nlp_chain", "test_translation_agent", "TranslationAgent")
            self.chain_builder.add_agent("trans_nlp_chain", "test_nlp_agent", "NLPAnalyzerAgent")
            self.chain_builder.connect_agents("trans_nlp_chain", "test_translation_agent", "test_nlp_agent",
                                             {"translated_text": "text"})
            
            execution = await self.workflow_engine.execute_chain(
                "trans_nlp_chain",
                {
                    "action": "translate",
                    "text": "I am very happy today!",
                    "target_language": "he"
                },
                timeout=30
            )
            
            test_passed = execution.status.value == "completed"
            results["tests"].append({
                "name": "Translation → NLP chain",
                "passed": test_passed,
                "execution_status": execution.status.value,
                "error": execution.error
            })
            if test_passed:
                results["passed"] += 1
            else:
                results["failed"] += 1
            
            # Test 2: Full assessment chain
            logger.info("     🧠 Testing full assessment chain...")
            chain = self.chain_builder.create_chain("full_assessment", "Full Assessment")
            
            self.chain_builder.add_agent("full_assessment", "test_translation_agent", "TranslationAgent")
            self.chain_builder.add_agent("full_assessment", "test_nlp_agent", "NLPAnalyzerAgent") 
            self.chain_builder.add_agent("full_assessment", "test_enneagram_agent", "EnneagramAgent")
            
            self.chain_builder.connect_agents("full_assessment", "test_translation_agent", "test_nlp_agent",
                                             {"translated_text": "text"})
            self.chain_builder.connect_agents("full_assessment", "test_nlp_agent", "test_enneagram_agent",
                                             {"sentiment": "emotional_context"})
            
            execution = await self.workflow_engine.execute_chain(
                "full_assessment",
                {
                    "action": "translate", 
                    "text": "I love helping others and making sure everyone feels included and valued.",
                    "target_language": "he"
                },
                timeout=45
            )
            
            test_passed = execution.status.value == "completed"
            results["tests"].append({
                "name": "Full assessment chain",
                "passed": test_passed,
                "execution_status": execution.status.value,
                "node_count": len(execution.node_executions),
                "completed_nodes": len([n for n in execution.node_executions.values() 
                                      if n.status.value == "completed"])
            })
            if test_passed:
                results["passed"] += 1
            else:
                results["failed"] += 1
            
        except Exception as e:
            results["error"] = str(e)
            results["failed"] += 1
            logger.error(f"Integration test error: {str(e)}")
        
        return results
    
    async def run_performance_tests(self) -> Dict[str, Any]:
        """Run performance tests to validate SLAs"""
        results = {"passed": 0, "failed": 0, "tests": [], "metrics": {}}
        
        try:
            # Test 1: Translation agent response time
            logger.info("     ⚡ Testing translation response time...")
            agent = self.agents["translation"]
            
            response_times = []
            for i in range(10):
                start_time = time.time()
                message = AgentMessage(
                    id=f"perf_test_{i}",
                    source_agent="test",
                    payload={
                        "action": "translate",
                        "text": "This is a test message for performance testing.",
                        "target_language": "he"
                    }
                )
                response = await agent.handle_message(message)
                response_times.append(time.time() - start_time)
            
            avg_response_time = sum(response_times) / len(response_times)
            max_response_time = max(response_times)
            
            # SLA: < 2s for translation
            test_passed = avg_response_time < 2.0 and max_response_time < 3.0
            results["tests"].append({
                "name": "Translation response time SLA",
                "passed": test_passed,
                "avg_response_time": avg_response_time,
                "max_response_time": max_response_time,
                "sla_requirement": "< 2s average, < 3s max"
            })
            if test_passed:
                results["passed"] += 1
            else:
                results["failed"] += 1
            
            # Test 2: NLP analyzer response time
            logger.info("     📊 Testing NLP analyzer response time...")
            agent = self.agents["nlp"]
            
            response_times = []
            for i in range(10):
                start_time = time.time()
                message = AgentMessage(
                    id=f"nlp_perf_test_{i}",
                    source_agent="test",
                    payload={
                        "action": "analyze_text",
                        "text": "This is a sample text for analyzing sentiment, emotions, and linguistic features.",
                        "features": ["sentiment", "emotion", "stats"]
                    }
                )
                response = await agent.handle_message(message)
                response_times.append(time.time() - start_time)
            
            avg_response_time = sum(response_times) / len(response_times)
            max_response_time = max(response_times)
            
            # SLA: < 1s for NLP analysis
            test_passed = avg_response_time < 1.0 and max_response_time < 2.0
            results["tests"].append({
                "name": "NLP analyzer response time SLA",
                "passed": test_passed,
                "avg_response_time": avg_response_time,
                "max_response_time": max_response_time,
                "sla_requirement": "< 1s average, < 2s max"
            })
            if test_passed:
                results["passed"] += 1
            else:
                results["failed"] += 1
            
            # Test 3: Concurrent processing
            logger.info("     🔄 Testing concurrent processing...")
            start_time = time.time()
            
            tasks = []
            for i in range(20):
                message = AgentMessage(
                    id=f"concurrent_test_{i}",
                    source_agent="test",
                    payload={
                        "action": "translate",
                        "text": f"Concurrent test message number {i}",
                        "target_language": "he"
                    }
                )
                tasks.append(self.agents["translation"].handle_message(message))
            
            responses = await asyncio.gather(*tasks)
            total_time = time.time() - start_time
            
            successful = sum(1 for r in responses if r.success)
            throughput = len(tasks) / total_time
            
            # Target: > 10 requests/second
            test_passed = throughput > 10 and successful == len(tasks)
            results["tests"].append({
                "name": "Concurrent processing throughput",
                "passed": test_passed,
                "total_requests": len(tasks),
                "successful": successful,
                "total_time": total_time,
                "throughput": throughput,
                "target_throughput": "> 10 req/s"
            })
            if test_passed:
                results["passed"] += 1
            else:
                results["failed"] += 1
            
            results["metrics"] = {
                "translation_avg_time": avg_response_time,
                "nlp_avg_time": avg_response_time,
                "concurrent_throughput": throughput
            }
            
        except Exception as e:
            results["error"] = str(e)
            results["failed"] += 1
        
        return results
    
    async def run_hebrew_tests(self) -> Dict[str, Any]:
        """Run Hebrew-specific functionality tests"""
        results = {"passed": 0, "failed": 0, "tests": []}
        
        try:
            # Test 1: Hebrew text detection
            logger.info("     🇮🇱 Testing Hebrew text detection...")
            agent = self.agents["translation"]
            
            message = AgentMessage(
                id="hebrew_detect_test",
                source_agent="test",
                payload={
                    "action": "detect_language",
                    "text": "שלום, זה טקסט בעברית לבדיקת המערכת"
                }
            )
            
            response = await agent.handle_message(message)
            detected_lang = response.data.get("detected_language") if response.success else None
            
            test_passed = response.success and detected_lang == "he"
            results["tests"].append({
                "name": "Hebrew text detection",
                "passed": test_passed,
                "detected_language": detected_lang,
                "confidence": response.data.get("confidence") if response.success else None
            })
            if test_passed:
                results["passed"] += 1
            else:
                results["failed"] += 1
            
            # Test 2: Hebrew to English translation
            logger.info("     🔄 Testing Hebrew to English translation...")
            message = AgentMessage(
                id="hebrew_translation_test",
                source_agent="test",
                payload={
                    "action": "translate",
                    "text": "אני אדם אופטימי שאוהב לעזור לאחרים ולחקור הזדמנויות חדשות",
                    "target_language": "en"
                }
            )
            
            response = await agent.handle_message(message)
            
            test_passed = (response.success and 
                          "translated_text" in response.data and
                          len(response.data["translated_text"]) > 0)
            results["tests"].append({
                "name": "Hebrew to English translation",
                "passed": test_passed,
                "original_text": "אני אדם אופטימי שאוהב לעזור לאחרים...",
                "translated_text": response.data.get("translated_text", "")[:100] if response.success else None,
                "confidence": response.data.get("confidence") if response.success else None
            })
            if test_passed:
                results["passed"] += 1
            else:
                results["failed"] += 1
            
            # Test 3: Hebrew psychological assessment
            logger.info("     🧠 Testing Hebrew psychological assessment chain...")
            
            if self.workflow_engine:
                execution = await self.workflow_engine.execute_chain(
                    "full_assessment",
                    {
                        "action": "translate",
                        "text": "אני אוהב לעזור לאנשים ולוודא שכולם מרגישים בנוח. לפעמים אני שם את הצרכים של אחרים לפני הצרכים שלי.",
                        "target_language": "en"
                    },
                    timeout=60
                )
                
                test_passed = execution.status.value == "completed"
                
                # Extract assessment results if available
                assessment_result = None
                if test_passed and "test_enneagram_agent" in execution.node_executions:
                    enneagram_result = execution.node_executions["test_enneagram_agent"].output_data
                    assessment_result = enneagram_result.get("primary_type")
                
                results["tests"].append({
                    "name": "Hebrew psychological assessment chain",
                    "passed": test_passed,
                    "execution_status": execution.status.value,
                    "primary_type_detected": assessment_result,
                    "execution_time": (execution.end_time - execution.start_time).total_seconds() if execution.end_time else None
                })
                if test_passed:
                    results["passed"] += 1
                else:
                    results["failed"] += 1
            
        except Exception as e:
            results["error"] = str(e)
            results["failed"] += 1
        
        return results
    
    def generate_summary(self, total_time: float) -> Dict[str, Any]:
        """Generate test summary"""
        total_tests = 0
        total_passed = 0
        total_failed = 0
        
        for category, category_results in self.test_results.items():
            if category != "summary" and isinstance(category_results, dict):
                if "passed" in category_results and "failed" in category_results:
                    total_passed += category_results["passed"]
                    total_failed += category_results["failed"]
                    total_tests += category_results["passed"] + category_results["failed"]
                else:
                    # Handle nested test categories
                    for subcategory, subcategory_results in category_results.items():
                        if isinstance(subcategory_results, dict) and "passed" in subcategory_results:
                            total_passed += subcategory_results["passed"]
                            total_failed += subcategory_results["failed"]
                            total_tests += subcategory_results["passed"] + subcategory_results["failed"]
        
        success_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
        
        return {
            "total_execution_time": total_time,
            "total_tests": total_tests,
            "total_passed": total_passed,
            "total_failed": total_failed,
            "success_rate": success_rate,
            "performance_summary": {
                "all_slas_met": total_failed == 0,
                "hebrew_support": "functional" if self.test_results.get("hebrew_specific_tests", {}).get("passed", 0) > 0 else "needs_attention",
                "integration_status": "working" if self.test_results.get("integration_tests", {}).get("passed", 0) > 0 else "needs_attention"
            }
        }


async def main():
    """Main test runner"""
    print("🧪 Agent Library Comprehensive Test Suite")
    print("=" * 60)
    
    test_suite = SystemTestSuite()
    results = await test_suite.run_all_tests()
    
    # Print summary
    summary = results.get("summary", {})
    print(f"\n📊 TEST SUMMARY")
    print(f"=" * 30)
    print(f"Total tests: {summary.get('total_tests', 0)}")
    print(f"Passed: {summary.get('total_passed', 0)}")
    print(f"Failed: {summary.get('total_failed', 0)}")
    print(f"Success rate: {summary.get('success_rate', 0):.1f}%")
    print(f"Execution time: {summary.get('total_execution_time', 0):.2f}s")
    
    # Performance summary
    perf_summary = summary.get("performance_summary", {})
    print(f"\n🎯 PERFORMANCE STATUS")
    print(f"All SLAs met: {'✅' if perf_summary.get('all_slas_met') else '❌'}")
    print(f"Hebrew support: {'✅' if perf_summary.get('hebrew_support') == 'functional' else '❌'}")
    print(f"Integration: {'✅' if perf_summary.get('integration_status') == 'working' else '❌'}")
    
    # Save detailed results
    results_file = "test_results.json"
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"\n💾 Detailed results saved to: {results_file}")
    
    # Return appropriate exit code
    return 0 if summary.get("total_failed", 1) == 0 else 1


if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n👋 Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Test suite crashed: {str(e)}")
        sys.exit(1)