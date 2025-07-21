#!/bin/bash

echo "🎯 Personality Assessment Test Script"
echo "===================================="

# Check if Docker API is running
echo "🔍 Checking if assessment system is running..."
if curl -s http://localhost:8080/health > /dev/null; then
    echo "✅ System is ready!"
else
    echo "❌ System not running. Please start with: docker run -p 8080:8000 agent-library"
    exit 1
fi

echo ""
echo "📝 Please describe yourself in 2-3 sentences."
echo "Include: relationships, work style, motivations, values"
echo "You can write in English or Hebrew"
echo ""
echo "Paste your text and press Enter:"
read -r user_input

if [ ${#user_input} -lt 20 ]; then
    echo "⚠️  Please provide more detail (at least 20 characters)"
    exit 1
fi

echo ""
echo "📊 Analyzing your personality..."
echo "⏳ Processing..."

# Make the API call and format the result
response=$(curl -s -X POST http://localhost:8080/assess \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"$user_input\"}")

if [ $? -eq 0 ]; then
    echo ""
    echo "============================================================"
    echo "🧠 YOUR PERSONALITY ASSESSMENT RESULTS"
    echo "============================================================"
    
    # Extract key information using jq if available, otherwise show raw JSON
    if command -v jq &> /dev/null; then
        personality_type=$(echo "$response" | jq -r '.summary.personality_type')
        confidence=$(echo "$response" | jq -r '.summary.confidence')
        language=$(echo "$response" | jq -r '.summary.source_language')
        sentiment=$(echo "$response" | jq -r '.summary.sentiment')
        steps=$(echo "$response" | jq '.steps | length')
        
        case $personality_type in
            1) description="The Perfectionist - Principled, purposeful, self-controlled" ;;
            2) description="The Helper - Generous, people-pleasing, demonstrates care" ;;
            3) description="The Achiever - Adaptive, excelling, driven, image-conscious" ;;
            4) description="The Individualist - Expressive, dramatic, temperamental" ;;
            5) description="The Investigator - Perceptive, innovative, secretive" ;;
            6) description="The Loyalist - Engaging, responsible, anxious" ;;
            7) description="The Enthusiast - Spontaneous, versatile, scattered" ;;
            8) description="The Challenger - Self-confident, decisive, willful" ;;
            9) description="The Peacemaker - Receptive, reassuring, agreeable" ;;
            *) description="Unknown type" ;;
        esac
        
        echo "🎯 Personality Type: $personality_type"
        echo "📝 Description: $description"
        echo "💪 Confidence: $(echo "$confidence * 100" | bc -l | cut -d. -f1)%"
        echo "🌐 Language: $language"
        echo "😊 Sentiment: $sentiment"
        echo "⚙️  Processing Steps: $steps"
    else
        echo "Raw response (install jq for formatted output):"
        echo "$response" | python3 -m json.tool
    fi
    
    echo "============================================================"
    
    # Save result
    echo "$response" > "assessment_result_$(date +%Y%m%d_%H%M%S).json"
    echo "💾 Detailed results saved to: assessment_result_$(date +%Y%m%d_%H%M%S).json"
    
else
    echo "❌ Failed to get assessment. Check if the system is running."
fi

echo ""
echo "🔄 Run this script again to take another assessment!"