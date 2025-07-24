#!/usr/bin/env python3
"""
System Comparison Test: New Agent Library vs Original psychological_assessment_system.py
Tests English and Hebrew samples to compare assessment quality
"""

import asyncio
import sys
import os
import json
import time
import urllib.request
import urllib.parse
from pathlib import Path
from typing import Dict, Any, List
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add paths for imports
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import new agent system
from run_production import ProductionSystem, assess_text

# Test samples for comparison
TEST_SAMPLES = {
    "english_helper": {
        "text": "I genuinely care about helping others and making sure everyone around me feels comfortable and valued. I often put other people's needs before my own and get great satisfaction from being needed and appreciated. Sometimes I worry that I'm not doing enough for others, and I can become resentful if my efforts aren't recognized.",
        "language": "English",
        "expected_type": 2,  # Helper/Giver
        "description": "Clear Type 2 (Helper) personality traits"
    },
    "hebrew_helper": {
        "text": "אני באמת אכפת לי לעזור לאחרים ולוודא שכולם סביבי מרגישים בנוח ומוערכים. לעתים קרובות אני שם את הצרכים של אנשים אחרים לפני שלי ומקבל סיפוק גדול מהיות נחוץ ומוערך. לפעמים אני דואג שאני לא עושה מספיק עבור אחרים.",
        "language": "Hebrew",
        "expected_type": 2,  # Helper/Giver
        "description": "Hebrew translation of Type 2 traits"
    },
    "english_achiever": {
        "text": "I am very driven to succeed and achieve my goals. I work hard to maintain a successful image and I'm always focused on being efficient and productive. I like to be seen as competent and accomplished by others. Sometimes I worry about whether I'm truly being myself or just playing a role.",
        "language": "English", 
        "expected_type": 3,  # Achiever
        "description": "Clear Type 3 (Achiever) personality traits"
    },
    "hebrew_achiever": {
        "text": "אני מאוד נמרץ להצליח ולהשיג את המטרות שלי. אני עובד קשה כדי לשמור על תדמית מוצלחת ותמיד מתמקד בלהיות יעיל ופרודוקטיבי. אני אוהב שרואים אותי כמוכשר ומוצלח על ידי אחרים. לפעמים אני דואג אם אני באמת אני עצמי או רק משחק תפקיד.",
        "language": "Hebrew",
        "expected_type": 3,  # Achiever  
        "description": "Hebrew translation of Type 3 traits"
    },
    "english_enthusiast": {
        "text": "I love exploring new opportunities and having exciting experiences. I'm always looking for the next adventure and I tend to be very optimistic about life. I have lots of interests and sometimes struggle to focus on just one thing because there are so many fascinating possibilities out there.",
        "language": "English",
        "expected_type": 7,  # Enthusiast
        "description": "Clear Type 7 (Enthusiast) personality traits"
    },
    "hebrew_enthusiast": {
        "text": "אני אוהב לחקור הזדמנויות חדשות ולחוות חוויות מרגשות. אני תמיד מחפש את ההרפתקה הבאה ונוטה להיות מאוד אופטימי לגבי החיים. יש לי הרבה תחומי עניין ולפעמים נאבק להתמקד רק בדבר אחד כי יש כל כך הרבה אפשרויות מרתקות בחוץ.",
        "language": "Hebrew",
        "expected_type": 7,  # Enthusiast
        "description": "Hebrew translation of Type 7 traits"
    }
}

class SystemComparisonTest:
    """Comprehensive comparison test between systems"""
    
    def __init__(self):
        self.new_system = None
        self.original_system_available = False
        self.results = {
            "new_system": {},
            "original_system": {},
            "comparison": {}
        }
        
    async def initialize(self):
        """Initialize both systems"""
        logger.info("🔄 Initializing systems for comparison...")
        
        # Initialize new agent system
        self.new_system = ProductionSystem()
        new_system_ready = await self.new_system.initialize()
        
        if not new_system_ready:
            logger.error("❌ Failed to initialize new agent system")
            return False
        
        logger.info("✅ New agent system initialized")
        
        # Check if original system is available
        try:
            # This would require the original system dependencies
            # For now, we'll test against the Docker API
            response = urllib.request.urlopen("http://localhost:8080/health", timeout=5)
            if response.status == 200:
                logger.info("✅ New system Docker API available")
            else:
                logger.warning("⚠️  Docker API not responding correctly")
        except Exception as e:
            logger.info("ℹ️  Docker API not available for comparison")
        
        return True
    
    async def test_new_system(self, sample_id: str, sample: Dict[str, Any]) -> Dict[str, Any]:
        """Test sample against new agent system"""
        logger.info(f"Testing new system with {sample_id}...")
        
        start_time = time.time()
        
        try:
            # Test through production system
            result = await self.new_system.process_chain(sample["text"])
            processing_time = time.time() - start_time
            
            if "error" in result:
                return {
                    "success": False,
                    "error": result["error"],
                    "processing_time": processing_time
                }
            
            # Extract assessment data
            assessment_data = {
                "success": True,
                "processing_time": processing_time,
                "source_language": result["summary"]["source_language"],
                "sentiment": result["summary"]["sentiment"],
                "personality_type": result["summary"]["personality_type"],
                "confidence": result["summary"]["confidence"],
                "steps": len(result["steps"]),
                "raw_result": result
            }
            
            return assessment_data
            
        except Exception as e:
            logger.error(f"Error testing new system: {e}")
            return {
                "success": False,
                "error": str(e),
                "processing_time": time.time() - start_time
            }
    
    async def test_docker_api(self, sample_id: str, sample: Dict[str, Any]) -> Dict[str, Any]:
        """Test sample against Docker API"""
        logger.info(f"Testing Docker API with {sample_id}...")
        
        start_time = time.time()
        
        try:
            # Prepare request data
            data = json.dumps({"text": sample["text"]}).encode('utf-8')
            req = urllib.request.Request(
                "http://localhost:8080/assess",
                data=data,
                headers={'Content-Type': 'application/json'}
            )
            
            response = urllib.request.urlopen(req, timeout=30)
            processing_time = time.time() - start_time
            
            if response.status != 200:
                return {
                    "success": False,
                    "error": f"HTTP {response.status}: {response.read().decode()}",
                    "processing_time": processing_time
                }
            
            result = json.loads(response.read().decode())
            
            return {
                "success": True,
                "processing_time": processing_time,
                "source_language": result["summary"]["source_language"],
                "sentiment": result["summary"]["sentiment"], 
                "personality_type": result["summary"]["personality_type"],
                "confidence": result["summary"]["confidence"],
                "steps": len(result["steps"]),
                "raw_result": result
            }
            
        except Exception as e:
            logger.error(f"Error testing Docker API: {e}")
            return {
                "success": False,
                "error": str(e),
                "processing_time": time.time() - start_time
            }
    
    def analyze_assessment_accuracy(self, sample_id: str, sample: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze assessment accuracy"""
        if not result["success"]:
            return {"accuracy_score": 0, "issues": ["Assessment failed"]}
        
        issues = []
        accuracy_factors = []
        
        # Check personality type accuracy
        predicted_type = result.get("personality_type")
        expected_type = sample["expected_type"]
        
        if predicted_type == expected_type:
            accuracy_factors.append(1.0)  # Perfect match
        elif isinstance(predicted_type, int) and 1 <= predicted_type <= 9:
            # Partial credit for valid type prediction
            accuracy_factors.append(0.5)
            issues.append(f"Expected Type {expected_type}, got Type {predicted_type}")
        else:
            accuracy_factors.append(0.0)
            issues.append(f"Invalid type prediction: {predicted_type}")
        
        # Check language detection (for Hebrew samples)
        if sample["language"] == "Hebrew":
            detected_lang = result.get("source_language", "")
            if detected_lang == "he":
                accuracy_factors.append(1.0)
            elif detected_lang in ["hebrew", "iw"]:
                accuracy_factors.append(0.8)
            else:
                accuracy_factors.append(0.0)
                issues.append(f"Hebrew not detected, got: {detected_lang}")
        else:
            # English detection
            detected_lang = result.get("source_language", "")
            if detected_lang == "en":
                accuracy_factors.append(1.0)
            else:
                accuracy_factors.append(0.5)
                issues.append(f"English detection unclear: {detected_lang}")
        
        # Check confidence level
        confidence = result.get("confidence", 0)
        if confidence >= 0.7:
            accuracy_factors.append(1.0)
        elif confidence >= 0.5:
            accuracy_factors.append(0.7)
        else:
            accuracy_factors.append(0.3)
            issues.append(f"Low confidence: {confidence}")
        
        # Calculate overall accuracy
        accuracy_score = sum(accuracy_factors) / len(accuracy_factors) if accuracy_factors else 0
        
        return {
            "accuracy_score": accuracy_score,
            "personality_match": predicted_type == expected_type,
            "language_detection": result.get("source_language"),
            "confidence_level": confidence,
            "issues": issues
        }
    
    async def run_comparison_test(self):
        """Run complete comparison test"""
        logger.info("🧪 Starting comprehensive system comparison...")
        
        if not await self.initialize():
            logger.error("❌ System initialization failed")
            return None
        
        # Test all samples
        for sample_id, sample in TEST_SAMPLES.items():
            logger.info(f"\n--- Testing Sample: {sample_id} ---")
            logger.info(f"Language: {sample['language']}")
            logger.info(f"Expected: Type {sample['expected_type']} ({sample['description']})")
            logger.info(f"Text: {sample['text'][:100]}...")
            
            # Test new system (direct)
            new_result = await self.test_new_system(sample_id, sample)
            self.results["new_system"][sample_id] = new_result
            
            # Test Docker API
            docker_result = await self.test_docker_api(sample_id, sample)
            self.results["original_system"][sample_id] = docker_result
            
            # Analyze accuracy
            if new_result["success"]:
                new_accuracy = self.analyze_assessment_accuracy(sample_id, sample, new_result)
                self.results["new_system"][sample_id]["accuracy"] = new_accuracy
                logger.info(f"New System: Type {new_result.get('personality_type')}, Accuracy: {new_accuracy['accuracy_score']:.1%}")
            
            if docker_result["success"]:
                docker_accuracy = self.analyze_assessment_accuracy(sample_id, sample, docker_result)
                self.results["original_system"][sample_id]["accuracy"] = docker_accuracy
                logger.info(f"Docker API: Type {docker_result.get('personality_type')}, Accuracy: {docker_accuracy['accuracy_score']:.1%}")
        
        # Generate comparison summary
        self.generate_comparison_summary()
        
        return self.results
    
    def generate_comparison_summary(self):
        """Generate summary comparison"""
        logger.info("\n📊 Generating Comparison Summary...")
        
        new_system_stats = self.calculate_system_stats("new_system")
        docker_stats = self.calculate_system_stats("original_system")
        
        self.results["comparison"] = {
            "new_system_stats": new_system_stats,
            "docker_api_stats": docker_stats,
            "summary": self.create_summary_report(new_system_stats, docker_stats)
        }
    
    def calculate_system_stats(self, system_key: str) -> Dict[str, Any]:
        """Calculate statistics for a system"""
        system_results = self.results[system_key]
        
        stats = {
            "total_tests": len(system_results),
            "successful_tests": 0,
            "failed_tests": 0,
            "average_accuracy": 0,
            "average_processing_time": 0,
            "hebrew_accuracy": 0,
            "english_accuracy": 0,
            "type_predictions": {}
        }
        
        total_accuracy = 0
        total_time = 0
        hebrew_tests = 0
        english_tests = 0
        hebrew_accuracy_sum = 0
        english_accuracy_sum = 0
        
        for sample_id, result in system_results.items():
            if result["success"]:
                stats["successful_tests"] += 1
                
                if "accuracy" in result:
                    accuracy = result["accuracy"]["accuracy_score"]
                    total_accuracy += accuracy
                    
                    # Track by language
                    if "hebrew" in sample_id:
                        hebrew_tests += 1
                        hebrew_accuracy_sum += accuracy
                    else:
                        english_tests += 1
                        english_accuracy_sum += accuracy
                    
                    # Track type predictions
                    predicted_type = result.get("personality_type")
                    if predicted_type:
                        stats["type_predictions"][sample_id] = predicted_type
                
                total_time += result.get("processing_time", 0)
            else:
                stats["failed_tests"] += 1
        
        # Calculate averages
        if stats["successful_tests"] > 0:
            stats["average_accuracy"] = total_accuracy / stats["successful_tests"]
            stats["average_processing_time"] = total_time / stats["successful_tests"]
        
        if hebrew_tests > 0:
            stats["hebrew_accuracy"] = hebrew_accuracy_sum / hebrew_tests
        
        if english_tests > 0:
            stats["english_accuracy"] = english_accuracy_sum / english_tests
        
        return stats
    
    def create_summary_report(self, new_stats: Dict[str, Any], docker_stats: Dict[str, Any]) -> str:
        """Create human-readable summary report"""
        report = []
        
        report.append("=" * 60)
        report.append("SYSTEM COMPARISON SUMMARY")
        report.append("=" * 60)
        
        # Overall performance
        report.append(f"\n📊 OVERALL PERFORMANCE:")
        report.append(f"New System:  {new_stats['successful_tests']}/{new_stats['total_tests']} tests passed ({new_stats['average_accuracy']:.1%} accuracy)")
        report.append(f"Docker API:  {docker_stats['successful_tests']}/{docker_stats['total_tests']} tests passed ({docker_stats['average_accuracy']:.1%} accuracy)")
        
        # Language-specific performance
        report.append(f"\n🌐 LANGUAGE PERFORMANCE:")
        report.append(f"Hebrew - New: {new_stats['hebrew_accuracy']:.1%}, Docker: {docker_stats['hebrew_accuracy']:.1%}")
        report.append(f"English - New: {new_stats['english_accuracy']:.1%}, Docker: {docker_stats['english_accuracy']:.1%}")
        
        # Performance metrics
        report.append(f"\n⚡ PERFORMANCE METRICS:")
        report.append(f"New System Avg Time: {new_stats['average_processing_time']:.3f}s")
        report.append(f"Docker API Avg Time: {docker_stats['average_processing_time']:.3f}s")
        
        # Detailed results
        report.append(f"\n🎯 DETAILED RESULTS:")
        for sample_id in TEST_SAMPLES.keys():
            expected_type = TEST_SAMPLES[sample_id]['expected_type']
            new_type = new_stats['type_predictions'].get(sample_id, 'FAILED')
            docker_type = docker_stats['type_predictions'].get(sample_id, 'FAILED')
            
            report.append(f"{sample_id:20} | Expected: {expected_type} | New: {new_type} | Docker: {docker_type}")
        
        # Conclusions
        report.append(f"\n🏆 CONCLUSIONS:")
        
        if new_stats['average_accuracy'] > docker_stats['average_accuracy']:
            report.append("✅ New system shows higher overall accuracy")
        elif new_stats['average_accuracy'] == docker_stats['average_accuracy']:
            report.append("➡️ Both systems show equivalent accuracy")
        else:
            report.append("⚠️ Docker API shows higher accuracy")
        
        if new_stats['average_processing_time'] < docker_stats['average_processing_time']:
            report.append("✅ New system is faster")
        else:
            report.append("⚠️ Docker API is faster")
        
        report.append("=" * 60)
        
        return "\n".join(report)

async def main():
    """Run the comparison test"""
    print("🔬 System Comparison Test: New Agent Library vs Original")
    print("=" * 70)
    
    test = SystemComparisonTest()
    results = await test.run_comparison_test()
    
    if results:
        # Print summary
        print(results["comparison"]["summary"])
        
        # Save detailed results
        results_file = "system_comparison_results.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\n💾 Detailed results saved to: {results_file}")
        
        return 0
    else:
        print("❌ Comparison test failed")
        return 1

if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n👋 Test interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Test failed: {e}", exc_info=True)
        sys.exit(1)