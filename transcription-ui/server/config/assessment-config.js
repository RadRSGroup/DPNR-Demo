// Configuration file for the Emotional Persona Assessment System
// This file centralizes config values used throughout the application

const ASSESSMENT_CONFIG = {
  // LLM service configuration
  llm: {
    provider: 'ollama',                  // Use 'ollama' instead of 'openai'
    endpoint: 'http://localhost:11434',  // Base URL for Ollama API
    apiPath: '/api/generate',            // API endpoint path
    model: 'llama3',                     // Default model to use
    fallbackModel: 'llama2',             // Fallback model if primary not available
    timeout: 300000,                     // Timeout in milliseconds (5 minutes)
    
    // Generation parameters
    params: {
      temperature: 0.3,                  // Lower for more deterministic outputs
      top_p: 0.9,                        // Nucleus sampling parameter
      top_k: 40,                         // Limits vocab to top K tokens
      num_predict: 2048                  // Max tokens to generate
    }
  },
  
  // Score weighting and calculation settings
  scoring: {
    // Phase weights for different question types
    phaseWeights: {
      initialSegmentation: { weight: 0.3, maxScore: 30 },
      detailedDifferentiation: { weight: 0.4, maxScore: 40 },
      typeConfirmation: { weight: 0.3, maxScore: 30 }
    },
    
    // Weight balance between multiple choice and text responses
    multipleChoiceWeight: 0.6,           // 60% weight for multiple choice
    textAnalysisWeight: 0.4,             // 40% weight for text analysis
    
    // Secondary persona threshold (% of primary persona score)
    secondaryThreshold: 0.7
  },
  
  // Question configuration
  questions: {
    // Types of questions supported
    types: ['single-select', 'multi-select', 'text-input'],
    
    // Default validation requirements
    validation: {
      textInput: {
        minLength: 50,                   // Minimum character count
        maxLength: 1000,                 // Maximum character count
      },
      multiSelect: {
        minSelections: 1,                // Minimum number of selections
        maxSelections: 3                 // Maximum number of selections
      }
    }
  },
  
  // UI/UX configuration
  ui: {
    showDebugInfo: false,                // Show scoring debug info in console
    showPersonaScores: true,             // Show numeric scores in results
    maxTextInsights: 5,                  // Maximum number of text insights to show
    maxCoreValues: 5,                    // Maximum number of core values to show
    animateTransitions: true             // Use animations between screens
  }
};

// Text analysis prompts
const ANALYSIS_PROMPTS = {
  // Main emotional persona analysis prompt
  emotionalPersonaAnalysis: `
# Emotional Persona Analysis

You are a specialized emotional intelligence system designed to analyze text and identify patterns related to the 9 Emotional Personas framework. Your task is to carefully analyze the provided text to identify traits, values, needs, and behavioral patterns that align with each of the emotional personas.

## Context

The 9 Emotional Personas framework identifies distinct emotional and behavioral patterns that shape how individuals perceive the world, make decisions, and interact with others. Each persona has characteristic traits, core values, emotional needs, and typical patterns across different life domains.

## Personas Overview

1. **The Upholder (Type 1)** 
   - Traits: Ethical, responsible, improvement-oriented, structured
   - Fears: Being wrong, flawed, or irresponsible
   - Values: Integrity, justice, self-discipline, moral clarity
   - Needs: Certainty, significance, contribution

2. **The Giver (Type 2)**
   - Traits: Generous, supportive, relationship-focused, caring
   - Fears: Being unloved, unwanted, or forgotten
   - Values: Generosity, loyalty, compassion, service
   - Needs: Love/connection, significance, contribution

3. **The Driver (Type 3)**
   - Traits: Achievement-oriented, efficient, image-conscious, adaptable
   - Fears: Being seen as a failure or worthless
   - Values: Excellence, efficiency, recognition, ambition
   - Needs: Significance, growth, love/connection

4. **The Seeker (Type 4)**
   - Traits: Authentic, creative, emotionally deep, individualistically-minded
   - Fears: Being emotionally abandoned, unseen, or insignificant
   - Values: Authenticity, depth, individuality, emotional truth
   - Needs: Love/connection, significance, growth

5. **The Observer (Type 5)**
   - Traits: Analytical, perceptive, private, knowledge-seeking
   - Fears: Being depleted, invaded, or emotionally exposed
   - Values: Knowledge, autonomy, competence, objectivity
   - Needs: Certainty, growth, significance

6. **The Guardian (Type 6)**
   - Traits: Loyal, vigilant, prepared, supportive
   - Fears: Being unsafe, betrayed, or left unprepared
   - Values: Security, preparedness, loyalty, honesty
   - Needs: Certainty, love/connection, contribution

7. **The Explorer (Type 7)**
   - Traits: Enthusiastic, optimistic, adventurous, possibility-focused
   - Fears: Being trapped in emotional pain, boredom, or limitation
   - Values: Freedom, adventure, optimism, flexibility
   - Needs: Variety, growth, love/connection

8. **The Protector (Type 8)**
   - Traits: Powerful, assertive, protective, justice-focused
   - Fears: Being controlled, betrayed, or emotionally weak
   - Values: Strength, justice, protection, leadership
   - Needs: Certainty, significance, love/connection

9. **The Harmonizer (Type 9)**
   - Traits: Peaceful, accepting, supportive, conflict-avoidant
   - Fears: Conflict, disconnection, or being overlooked
   - Values: Peace, harmony, acceptance, stability
   - Needs: Certainty, love/connection, growth

## Analysis Tasks

For the provided text, you will:

1. **Identify Persona Markers**
   - Note language, themes, and patterns that align with each persona
   - Consider both explicit statements and implicit patterns
   - Look for recurring emotional themes and responses to challenges

2. **Score Each Persona**
   - Provide a numerical score (0-100) for each persona based on evidence in the text
   - Higher scores indicate stronger alignment with that persona's traits

3. **Identify Core Values and Needs**
   - Extract the most prominent values and needs expressed in the text
   - Connect these to the corresponding personas

4. **Analyze Life Domain Patterns**
   - Identify how the dominant personas influence each life domain
   - Note strengths and potential challenges in each area

## Output Format

\`\`\`
## Persona Scores
- The Upholder (Type 1): [score]
- The Giver (Type 2): [score]
- The Driver (Type 3): [score]
- The Seeker (Type 4): [score]
- The Observer (Type 5): [score]
- The Guardian (Type 6): [score]
- The Explorer (Type 7): [score]
- The Protector (Type 8): [score]
- The Harmonizer (Type 9): [score]

## Core Values Expressed
[List 5-7 core values evident in the text]

## Key Insights
[List 3-5 key insights about emotional patterns]
\`\`\`
  `
};

module.exports = { ASSESSMENT_CONFIG, ANALYSIS_PROMPTS }; 