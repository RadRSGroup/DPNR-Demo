
const axios = require('axios');
const { ASSESSMENT_CONFIG, ANALYSIS_PROMPTS } = require('../config/assessment-config');
const express = require('express');

// Define Ollama configuration using centralized config
const OLLAMA_URL = (process.env.OLLAMA_URL || ASSESSMENT_CONFIG.llm.endpoint).replace(/\/$/, '');
const OLLAMA_MODEL = process.env.OLLAMA_MODEL || ASSESSMENT_CONFIG.llm.model;
const OLLAMA_API_PATH = ASSESSMENT_CONFIG.llm.apiPath || '/api/generate';

// Define persona information
const personaInfo = {
  'observer': {
    name: 'The Observer (Type 5)',
    description: 'You are analytical, perceptive, and value knowledge. You prefer to gather information before acting and often need space to process your thoughts. Your methodical approach to life and problem-solving allows you to see patterns others might miss.',
    values: ['Knowledge', 'Autonomy', 'Competence', 'Objectivity', 'Privacy']
  },
  'giver': {
    name: 'The Giver (Type 2)',
    description: 'You are generous, empathetic, and relationship-focused. Your natural inclination is to support others and anticipate their needs. You find fulfillment in making meaningful connections and being appreciated for your contributions.',
    values: ['Generosity', 'Compassion', 'Connection', 'Recognition', 'Harmony']
  },
  'driver': {
    name: 'The Driver (Type 3)',
    description: 'You are achievement-oriented, efficient, and adaptable. You focus on goals and outcomes, often excelling in competitive environments. Your ability to adapt to situations and present yourself effectively helps you succeed in various contexts.',
    values: ['Success', 'Efficiency', 'Progress', 'Recognition', 'Excellence']
  },
  'seeker': {
    name: 'The Seeker (Type 4)',
    description: 'You are authentic, emotionally deep, and creative. You value personal meaning and seek to express your unique identity. Your sensitivity to emotions and desire for depth creates rich experiences and meaningful connections.',
    values: ['Authenticity', 'Meaning', 'Creativity', 'Depth', 'Individuality']
  },
  'upholder': {
    name: 'The Upholder (Type 1)',
    description: 'You are principled, responsible, and improvement-oriented. You have high standards for yourself and others, with a strong sense of right and wrong. Your dedication to integrity and doing things correctly creates order and reliability.',
    values: ['Integrity', 'Responsibility', 'Improvement', 'Order', 'Correctness']
  },
  'guardian': {
    name: 'The Guardian (Type 6)',
    description: 'You are loyal, prepared, and security-focused. You anticipate problems and work to create safety for yourself and others. Your ability to identify risks and plan accordingly makes you a dependable ally and thoughtful decision-maker.',
    values: ['Security', 'Loyalty', 'Preparation', 'Responsibility', 'Community']
  },
  'explorer': {
    name: 'The Explorer (Type 7)',
    description: 'You are enthusiastic, optimistic, and versatile. You seek variety and positive experiences, bringing energy to any situation. Your ability to see possibilities and maintain optimism helps you navigate life with flexibility and joy.',
    values: ['Freedom', 'Joy', 'Variety', 'Adventure', 'Possibility']
  },
  'protector': {
    name: 'The Protector (Type 8)',
    description: 'You are strong, decisive, and justice-oriented. You naturally take charge in situations and stand up for yourself and others. Your directness and willingness to confront challenges makes you a powerful advocate and leader.',
    values: ['Strength', 'Justice', 'Independence', 'Protection', 'Truth']
  },
  'harmonizer': {
    name: 'The Harmonizer (Type 9)',
    description: 'You are peaceful, accepting, and supportive. You seek harmony and find common ground between different perspectives. Your ability to see multiple viewpoints and mediate conflicts creates stability and unity in relationships.',
    values: ['Peace', 'Harmony', 'Unity', 'Stability', 'Inclusion']
  }
};

// Main analysis handler
async function analyzeAssessment(req, res) {
  try {
    const { responses } = req.body;
    
    if (!responses) {
      return res.status(400).json({ error: 'No responses provided' });
    }
    
    // Collect all responses and format them for analysis
    const formattedResponses = formatResponsesForAnalysis(responses);
    
    // Calculate scores based on multiple-choice questions
    const personaScores = calculatePersonaScores(responses);
    
    // Get text inputs for LLM analysis
    const textInputs = extractTextInputs(responses);
    
    // Combine all text inputs into one document for analysis
    const combinedText = textInputs.join('\n\n');
    
    // Only send to LLM if there's text to analyze
    let textAnalysisResults = {};
    if (combinedText.trim().length > 0) {
      // Send to Ollama for text analysis
      textAnalysisResults = await analyzeTextWithLLM(combinedText);
    }
    
    // Combine multiple-choice results with text analysis
    const finalResults = combineResults(personaScores, textAnalysisResults);
    
    // Format final output
    const outputResults = formatOutputResults(finalResults);
    
    return res.status(200).json(outputResults);
  } catch (error) {
    console.error('Analysis error:', error);
    return res.status(500).json({ error: 'Analysis failed: ' + error.message });
  }
}

// Format responses for readability in logs/analysis
function formatResponsesForAnalysis(responses) {
  const formatted = {};
  
  // Group responses by question ID
  Object.entries(responses).forEach(([questionId, response]) => {
    // Check if response is array (multiple/single choice) or string (text input)
    if (Array.isArray(response)) {
      formatted[questionId] = response;
    } else {
      formatted[questionId] = response; // Text input
    }
  });
  
  return formatted;
}

// Calculate persona scores based on multiple-choice responses
function calculatePersonaScores(responses) {
  // Initialize scores for each persona
  const scores = {
    observer: 0,
    giver: 0,
    driver: 0,
    seeker: 0,
    upholder: 0,
    guardian: 0,
    explorer: 0,
    protector: 0,
    harmonizer: 0
  };
  
  // Count how many options we've processed for each persona
  const counts = { ...scores };
  
  // Process each response
  Object.entries(responses).forEach(([questionId, response]) => {
    // Skip text input questions (they're strings, not arrays)
    if (!Array.isArray(response)) return;
    
    // For questions where we have the answer key mapping
    if (questionId.startsWith('qQ')) {
      // Get question type based on number of selected options
      const isMultiSelect = response.length > 1;
      
      // Process each selected option
      response.forEach(optionId => {
        // This is where you'd normally look up which persona this option maps to
        // For this example, we're assuming the option already has a persona tag
        // In a real implementation, you'd have a mapping of optionId -> persona
        
        // Example logic - replace with your actual mapping logic
        // For demonstration purposes, assuming options follow pattern from the UI code
        // where each option has a persona property
        const optionPersona = getPersonaForOption(optionId);
        
        if (optionPersona && scores.hasOwnProperty(optionPersona)) {
          // For multi-select questions, we give less weight to each selection
          // since the user can choose multiple options
          const weight = isMultiSelect ? (1 / response.length) : 1;
          scores[optionPersona] += weight;
          counts[optionPersona]++;
        }
      });
    }
  });
  
  // Normalize scores (divide by count to get average)
  Object.keys(scores).forEach(persona => {
    if (counts[persona] > 0) {
      scores[persona] = (scores[persona] / counts[persona]) * 100; // Convert to 0-100 scale
    }
  });
  
  return scores;
}

// Mock function to map option IDs to personas
// In a real implementation, this would use your actual option -> persona mapping
function getPersonaForOption(optionId) {
  // This is a simplified example - you would replace this with your actual mapping
  // For this example, we're extracting the last digit and mapping it to a persona
  const lastDigit = parseInt(optionId.slice(-1));
  
  const personaMap = {
    1: 'observer',
    2: 'giver',
    3: 'driver',
    4: 'seeker',
    5: 'upholder',
    6: 'guardian',
    7: 'explorer',
    8: 'protector',
    9: 'harmonizer'
  };
  
  return personaMap[lastDigit] || null;
}

// Extract text inputs for LLM analysis
function extractTextInputs(responses) {
  const textInputs = [];
  
  Object.entries(responses).forEach(([questionId, response]) => {
    // Only process text inputs (not arrays)
    if (typeof response === 'string') {
      // Add some context about which question this was
      const questionText = getQuestionText(questionId);
      textInputs.push(`Question: ${questionText}\nResponse: ${response}`);
    }
  });
  
  return textInputs;
}

// Mock function to get question text
// In a real implementation, you would look this up from your questions database/config
function getQuestionText(questionId) {
  // Example mapping - replace with your actual questions
  const questionMap = {
    'qQ103': 'Describe a challenging situation you faced recently and how you handled it',
    'qQ106': 'What are your most important goals in life right now?'
  };
  
  return questionMap[questionId] || 'Unknown question';
}

// Analyze text inputs with LLM
async function analyzeTextWithLLM(text) {
  try {
    // Create the LLM prompt based on the prompt content in llm_prompt.txt
    const prompt = createEmotionalPersonaPrompt(text);
    
    console.log(`Analyzing text with Ollama model ${OLLAMA_MODEL}...`);
    
    // Call Ollama API instead of OpenAI
    const response = await axios.post(`${OLLAMA_URL}${OLLAMA_API_PATH}`, {
      model: OLLAMA_MODEL,
      prompt: prompt,
      stream: false,
      options: {
        temperature: 0.3,
        top_p: 0.9,
        top_k: 40,
        num_predict: 2048
      }
    }, {
      timeout: 300000 // 5 minute timeout
    });
    
    if (!response.data || !response.data.response) {
      throw new Error('Invalid response from Ollama service');
    }
    
    // Parse the response to extract structured data
    return parsePersonaAnalysisResponse(response.data.response);
  } catch (error) {
    console.error('LLM analysis error:', error);
    return {
      personaScores: {},
      coreValues: [],
      textInsights: ['Error analyzing text input.']
    };
  }
}

// Create the emotional persona analysis prompt
function createEmotionalPersonaPrompt(userText) {
  // This would contain the full prompt from llm_prompt.txt
  // For brevity, this is simplified here
  return `
# Emotional Persona Analysis

You are a specialized emotional intelligence system designed to analyze text and identify patterns related to the 9 Emotional Personas framework. 

Please analyze the following text according to the 9 Emotional Personas framework:

${userText}

Provide the following:
1. Persona scores (0-100) for each of the 9 types (Upholder, Giver, Driver, Seeker, Observer, Guardian, Explorer, Protector, Harmonizer)
2. Core values expressed in the text (list 5-7 values)
3. Key insights about the person's emotional patterns (list 3-5 insights)

Format your answer as follows:

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
[List of 5-7 values]

## Key Insights
[List of 3-5 insights about emotional patterns]
`;
}

// Parse the LLM response into structured data
function parsePersonaAnalysisResponse(response) {
  try {
    console.log('Parsing Ollama response...');
    
    // Initialize default values
    const result = {
      personaScores: {
        upholder: 0,
        giver: 0,
        driver: 0,
        seeker: 0,
        observer: 0,
        guardian: 0,
        explorer: 0,
        protector: 0,
        harmonizer: 0
      },
      coreValues: [],
      textInsights: []
    };
    
    // Extract scores using regex patterns
    const scoreMatches = response.matchAll(/The (Upholder|Giver|Driver|Seeker|Observer|Guardian|Explorer|Protector|Harmonizer).*?(\d+)/gi);
    for (const match of scoreMatches) {
      const personaType = match[1].toLowerCase();
      const score = parseInt(match[2], 10);
      
      if (!isNaN(score) && result.personaScores.hasOwnProperty(personaType)) {
        result.personaScores[personaType] = score;
      }
    }
    
    // Extract core values
    const valuesSection = response.match(/## Core Values Expressed\s+([\s\S]*?)(?=##|$)/i);
    if (valuesSection && valuesSection[1]) {
      const valuesList = valuesSection[1].trim()
        .split(/\n+/)
        .map(line => line.replace(/^-\s*|\s*$/, '').trim())
        .filter(value => value.length > 0);
      
      result.coreValues = valuesList.slice(0, 7); // Take up to 7 values
    }
    
    // Extract insights
    const insightsSection = response.match(/## Key Insights\s+([\s\S]*?)(?=##|$)/i);
    if (insightsSection && insightsSection[1]) {
      const insightsList = insightsSection[1].trim()
        .split(/\n+/)
        .map(line => line.replace(/^-\s*|\s*$/, '').trim())
        .filter(insight => insight.length > 0);
      
      result.textInsights = insightsList.slice(0, 5); // Take up to 5 insights
    }
    
    // If we couldn't extract structured data, use some fallback logic
    if (Object.values(result.personaScores).every(score => score === 0)) {
      console.warn('Could not extract structured persona scores from LLM response');
      
      // Use a simple fallback method - look for persona names and assign rough scores
      const personaTypes = ['upholder', 'giver', 'driver', 'seeker', 'observer', 'guardian', 'explorer', 'protector', 'harmonizer'];
      
      personaTypes.forEach(persona => {
        // Count mentions and weight by patterns
        const regex = new RegExp(persona, 'gi');
        const mentions = (response.match(regex) || []).length;
        result.personaScores[persona] = Math.min(mentions * 20, 100); // Simple heuristic
      });
    }
    
    // Use fallbacks for missing values and insights
    if (result.coreValues.length === 0) {
      result.coreValues = ['Growth', 'Achievement', 'Autonomy', 'Understanding', 'Connection'];
    }
    
    if (result.textInsights.length === 0) {
      result.textInsights = [
        'Shows a pattern of analytical problem-solving',
        'Values independence while seeking meaningful connections',
        'Demonstrates curiosity and openness to new experiences'
      ];
    }
    
    return result;
  } catch (error) {
    console.error('Error parsing LLM response:', error);
    return {
      personaScores: {
        upholder: 30,
        giver: 40,
        driver: 70,
        seeker: 55,
        observer: 65,
        guardian: 45,
        explorer: 60,
        protector: 50,
        harmonizer: 35
      },
      coreValues: ['Growth', 'Achievement', 'Autonomy', 'Understanding', 'Connection'],
      textInsights: [
        'Shows a pattern of analytical problem-solving and self-reflection',
        'Exhibits strong drive for personal achievement and recognition',
        'Values independence but also seeks meaningful connections',
        'Demonstrates curiosity and openness to new experiences',
        'May struggle with perfectionism and self-criticism'
      ]
    };
  }
}

// Combine multiple-choice scores with text analysis results
function combineResults(mcScores, textResults) {
  // Initialize with multiple-choice scores
  const combinedScores = { ...mcScores };
  
  // If we have text analysis results, combine the scores
  if (textResults.personaScores && Object.keys(textResults.personaScores).length > 0) {
    // Weight between multiple-choice (60%) and text analysis (40%)
    const mcWeight = 0.6;
    const textWeight = 0.4;
    
    Object.keys(combinedScores).forEach(persona => {
      if (textResults.personaScores[persona] !== undefined) {
        // Weighted average of both scores
        combinedScores[persona] = (
          mcScores[persona] * mcWeight + 
          textResults.personaScores[persona] * textWeight
        );
      }
    });
  }
  
  return {
    personaScores: combinedScores,
    coreValues: textResults.coreValues || [],
    textInsights: textResults.textInsights || []
  };
}

// Format the final output results
function formatOutputResults(results) {
  // Find primary persona (highest score)
  const sortedPersonas = Object.entries(results.personaScores)
    .sort((a, b) => b[1] - a[1])
    .map(([persona, score]) => ({ 
      persona, 
      score,
      info: personaInfo[persona] 
    }));
    
  const primaryPersona = sortedPersonas[0];
  
  // Get secondary personas (next two highest scores that are at least 70% of primary score)
  const secondaryPersonas = sortedPersonas
    .slice(1, 4)
    .filter(p => p.score >= primaryPersona.score * 0.7)
    .map(p => p.info);
  
  // Create life domain analysis
  const lifeDomains = createLifeDomainAnalysis(primaryPersona.persona, secondaryPersonas.map(p => p.name));
  
  return {
    primaryPersona: primaryPersona.info,
    secondaryPersonas: secondaryPersonas,
    coreValues: results.coreValues,
    lifeDomains: lifeDomains,
    textInsights: results.textInsights
  };
}

// Create life domain analysis based on persona types
function createLifeDomainAnalysis(primaryPersona, secondaryPersonas) {
  // This is where you would generate personalized domain analysis
  // This is simplified for this example
  
  // Example domain analyses for each persona
  const domainPatterns = {
    observer: {
      relationships: "You tend to value deep but limited connections, preferring quality over quantity in relationships. You may need more space than others and appreciate partners who respect your need for privacy and independence.",
      career: "You excel in roles requiring analytical thinking, research, or specialized expertise. Your methodical approach and attention to detail are strengths, though you may need to work on collaborative skills.",
      health: "You take an informed approach to health, researching before making decisions. Consider balancing intellectual pursuits with physical activity and social connection for overall wellbeing."
    },
    // Add entries for other personas here
    giver: {
      relationships: "You naturally attune to others' needs and create deep emotional connections. Be mindful of maintaining healthy boundaries and ensuring your own needs are met alongside supporting others.",
      career: "You thrive in supportive, helping roles and team environments where your interpersonal skills shine. Your ability to build relationships is a professional asset.",
      health: "Your tendency to prioritize others may lead to neglecting your own wellbeing. Creating self-care routines and learning to receive support are important for your health."
    },
    driver: {
      relationships: "You may focus on achievements more than emotional connections. Learning to be present and vulnerable can deepen your relationships beyond surface-level interactions.",
      career: "Your drive for success and efficiency makes you a valuable team member. Be mindful of burnout and remember that sustainable success includes periods of rest.",
      health: "You approach health goals with determination but may ignore warning signs when focused on other achievements. Balance is key to long-term wellbeing."
    },
    seeker: {
      relationships: "You crave authentic, deep connections and may be disappointed by superficial interactions. Your emotional awareness brings depth to relationships but can lead to intensity.",
      career: "You need work that aligns with your values and offers creative expression. Routine tasks may feel draining unless connected to a meaningful purpose.",
      health: "Your emotional awareness can be a strength in holistic health approaches, but mood fluctuations may affect consistency in self-care routines."
    },
    upholder: {
      relationships: "You bring reliability and clarity to relationships but may be critical of yourself and others. Practicing acceptance can enhance your connections.",
      career: "Your strong work ethic and attention to detail make you a valuable contributor. Remember that perfect is the enemy of good—sometimes done is better than perfect.",
      health: "You likely maintain disciplined health routines but may struggle with rigidity. Allowing flexibility in your approach can reduce stress."
    },
    guardian: {
      relationships: "You are loyal and supportive, creating safety for those you care about. Building trust takes time for you, but results in deep bonds.",
      career: "Your ability to anticipate problems and attention to detail are valuable assets. You excel in roles requiring troubleshooting and careful planning.",
      health: "Anxiety may manifest physically for you. Practices that build security and reduce worry are particularly beneficial for your wellbeing."
    },
    explorer: {
      relationships: "You bring fun and spontaneity to relationships but may avoid difficult emotions. Developing comfort with all emotional states will deepen your connections.",
      career: "Your creativity and enthusiasm make you excellent at generating ideas and starting projects. Working with detail-oriented colleagues can help with follow-through.",
      health: "You're drawn to variety in health approaches but may struggle with consistency. Building enjoyable routines that don't feel restrictive is key."
    },
    protector: {
      relationships: "You offer strength and protection in relationships but may struggle with vulnerability. Opening up gradually to trusted others enhances your connections.",
      career: "Your decisive nature and willingness to take charge make you natural at leadership. Be mindful of including others' perspectives in decision-making.",
      health: "You may push through physical limitations out of determination. Learning to respect your body's signals rather than overriding them improves long-term health."
    },
    harmonizer: {
      relationships: "You create peaceful, harmonious environments and see multiple perspectives. Practicing healthy assertion ensures your own needs are met in relationships.",
      career: "Your mediation skills and ability to work with diverse teams are valuable assets. Setting clear priorities helps combat potential indecision or procrastination.",
      health: "You may neglect health needs to avoid inconveniencing others. Prioritizing your wellbeing is not selfish—it's necessary for sustainable support of others."
    }
  };
  
  // Get domain analysis for primary persona
  const domains = domainPatterns[primaryPersona] || {
    relationships: "No specific pattern identified.",
    career: "No specific pattern identified.",
    health: "No specific pattern identified."
  };
  
  return domains;
}

// Create Express router and expose endpoint
const router = express.Router();

// POST /api/analyze-assessment
router.post('/analyze-assessment', analyzeAssessment);

module.exports = router;