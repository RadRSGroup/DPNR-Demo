/**
 * Emotional Persona Scoring Engine
 * 
 * This module handles the scoring and analysis of assessment data
 * against the 9 Emotional Personas framework.
 */

// Define the 9 emotional personas with their key attributes
const EMOTIONAL_PERSONAS = {
    upholder: {
      name: "The Upholder",
      type: "Type 1",
      keyTraits: ["Integrity", "Responsibility", "Justice", "Self-discipline", "Improvement", "Moral clarity"],
      scoringWeight: 1.2,
      coreValues: ["Integrity", "Responsibility", "Justice", "Improvement", "Moral clarity"],
      coreNeeds: ["Certainty", "Significance", "Contribution"],
      lifeDomains: {
        relationships: "Loyal but critical; struggles with emotional softness",
        career: "High performer but risks burnout; over-responsible",
        health: "Somatic tension; difficulty resting",
        lifestyle: "Structured, but lacks play and spontaneity",
        purpose: "Focused on duty; needs space for soul-driven joy"
      },
      description: "You have a strong sense of responsibility and integrity. You strive to do things the right way and hold yourself to high standards. You're reliable, ethical, and deeply committed to improvement."
    },
    giver: {
      name: "The Giver",
      type: "Type 2",
      keyTraits: ["Generosity", "Loyalty", "Compassion", "Service", "Belonging", "Emotional intimacy"],
      scoringWeight: 1.1,
      coreValues: ["Generosity", "Loyalty", "Compassion", "Service", "Belonging"],
      coreNeeds: ["Love/Connection", "Significance", "Contribution"],
      lifeDomains: {
        relationships: "Emotionally present but can lose himself in others",
        career: "Excellent in supportive roles; undervalues himself",
        health: "Neglects self-care; burnout risk",
        lifestyle: "Centered on others' needs",
        purpose: "Service-focused, but must learn to serve himself too"
      },
      description: "You're thoughtful, generous, and full of heart. You remember details about others and always show up when needed. You value emotional connection and find meaning in helping others."
    },
    driver: {
      name: "The Driver",
      type: "Type 3",
      keyTraits: ["Excellence", "Achievement", "Efficiency", "Recognition", "Ambition", "Progress"],
      scoringWeight: 1.2,
      coreValues: ["Excellence", "Achievement", "Efficiency", "Recognition", "Ambition"],
      coreNeeds: ["Significance", "Growth", "Love/Connection"],
      lifeDomains: {
        relationships: "High-achieving but emotionally distant",
        career: "Ambitious and productive; risks burnout",
        health: "Ignores fatigue and emotional needs",
        lifestyle: "Structured and fast-paced",
        purpose: "Success without soul—until reconnecting inward"
      },
      description: "You're admired, efficient, and always achieving. You know how to succeed and get things done. You're driven by excellence and progress, and you value recognition for your accomplishments."
    },
    seeker: {
      name: "The Seeker",
      type: "Type 4",
      keyTraits: ["Authenticity", "Depth", "Individuality", "Emotional truth", "Beauty", "Creativity"],
      scoringWeight: 1.0,
      coreValues: ["Authenticity", "Depth", "Individuality", "Emotional truth", "Beauty"],
      coreNeeds: ["Love/Connection", "Significance", "Growth"],
      lifeDomains: {
        relationships: "Passionate but inconsistent; can feel misunderstood",
        career: "Needs purpose and beauty in work; struggles with mundane tasks",
        health: "Mood-driven; may neglect routine during emotional lows",
        lifestyle: "Craves meaningful spaces but resists structure",
        purpose: "Driven to create something authentic that reflects soul"
      },
      description: "You're deeply sensitive and intuitively creative. You value authenticity and emotional depth. You seek meaning in life and have a unique perspective that others may not always understand."
    },
    observer: {
      name: "The Observer",
      type: "Type 5",
      keyTraits: ["Knowledge", "Autonomy", "Competence", "Objectivity", "Privacy", "Clarity"],
      scoringWeight: 1.1,
      coreValues: ["Knowledge", "Autonomy", "Competence", "Objectivity", "Privacy"],
      coreNeeds: ["Certainty", "Growth", "Significance"],
      lifeDomains: {
        relationships: "Loyal and insightful but distant; may struggle to express needs",
        career: "Excels in solo work, research, strategy; avoids team conflict",
        health: "Disconnects from body; may neglect nutrition or emotion",
        lifestyle: "Structured and minimalist; prioritizes control and quiet",
        purpose: "Feels purpose when knowledge is shared meaningfully"
      },
      description: "You're sharp, thoughtful, and deeply private. You notice what others miss and process information thoroughly. You value knowledge, autonomy, and competence in your areas of interest."
    },
    guardian: {
      name: "The Guardian",
      type: "Type 6",
      keyTraits: ["Loyalty", "Security", "Preparedness", "Support", "Courage", "Honesty"],
      scoringWeight: 1.2,
      coreValues: ["Loyalty", "Security", "Preparedness", "Support", "Honesty"],
      coreNeeds: ["Certainty", "Love/Connection", "Contribution"],
      lifeDomains: {
        relationships: "Loyal but may test others' loyalty; can become dependent",
        career: "Reliable, detail-oriented; may struggle with risks",
        health: "Mental tension and anxiety can lead to physical stress",
        lifestyle: "Structured and cautious; resists change unless ready",
        purpose: "Feels purposeful when protecting or supporting others"
      },
      description: "You're dependable, detail-oriented, and prepared for what might go wrong. You value security and loyalty in relationships. You're excellent at anticipating problems and finding solutions."
    },
    explorer: {
      name: "The Explorer",
      type: "Type 7",
      keyTraits: ["Freedom", "Adventure", "Optimism", "Flexibility", "Enthusiasm", "Possibility"],
      scoringWeight: 1.0,
      coreValues: ["Freedom", "Adventure", "Optimism", "Flexibility", "Enthusiasm"],
      coreNeeds: ["Variety", "Growth", "Love/Connection"],
      lifeDomains: {
        relationships: "Fun-loving but can become avoidant or inconsistent",
        career: "Creative and energetic—but risks distraction",
        health: "May ignore stress signals; avoids difficult emotions",
        lifestyle: "Fast-paced and exciting, lacks rest or structure",
        purpose: "Fulfilled when creating joy and staying present"
      },
      description: "You bring energy and enthusiasm to every situation. You're optimistic, spontaneous, and always looking for new possibilities. You value freedom and resist anything that feels limiting."
    },
    protector: {
      name: "The Protector",
      type: "Type 8",
      keyTraits: ["Strength", "Justice", "Protection", "Leadership", "Autonomy", "Directness"],
      scoringWeight: 1.2,
      coreValues: ["Strength", "Justice", "Protection", "Leadership", "Autonomy"],
      coreNeeds: ["Certainty", "Significance", "Love/Connection"],
      lifeDomains: {
        relationships: "Protective but may dominate or withhold vulnerability",
        career: "Takes initiative, leads well, but can bulldoze others",
        health: "May override physical signs in pursuit of control",
        lifestyle: "Structured, intense, focused; needs relaxation",
        purpose: "Fulfilled when using power to uplift others"
      },
      description: "You're bold, direct, and full of energy. You move through life with intensity and don't shy away from challenges. You protect others fiercely and value strength and directness."
    },
    harmonizer: {
      name: "The Harmonizer",
      type: "Type 9",
      keyTraits: ["Peace", "Harmony", "Acceptance", "Stability", "Empathy", "Unity"],
      scoringWeight: 1.1,
      coreValues: ["Peace", "Harmony", "Acceptance", "Stability", "Empathy"],
      coreNeeds: ["Certainty", "Love/Connection", "Growth"],
      lifeDomains: {
        relationships: "Warm but may become passive or conflict-avoidant",
        career: "Reliable but may go unnoticed; resists leadership",
        health: "May ignore body signals, zone out or disengage",
        lifestyle: "Comfortable, routine-based, lacks intention",
        purpose: "Longs for fulfillment but needs direction to claim it"
      },
      description: "You're calm, kind, and easy to be around. You avoid drama and keep the peace. You're adaptable and accepting of others, valuing harmony and stability in your environment."
    }
  };
  
  // Scoring weight constants
  const SCORING_WEIGHTS = {
    initialSegmentation: { weight: 0.3, maxScore: 30 },
    detailedDifferentiation: { weight: 0.4, maxScore: 40 },
    typeConfirmation: { weight: 0.3, maxScore: 30 }
  };
  
  /**
   * Debug scoring issues for troubleshooting
   * @param {string} context - The context of the debug message
   * @param {string} message - The debug message
   */
  function debugScoring(context, message) {
    console.log(`[DEBUG SCORING] ${context}: ${message}`);
  }
  
  /**
   * Calculate persona scores based on assessment responses
   * @param {Object} responses - User responses from questionnaire
   * @param {Object} answerToPersonaMapping - Mapping of answers to personas
   * @returns {Object} Scores for each persona
   */
  function calculatePersonaScores(responses, answerToPersonaMapping) {
    try {
      // Initialize scores for each persona
      const scores = {
        upholder: 0,
        giver: 0,
        driver: 0,
        seeker: 0,
        observer: 0,
        guardian: 0,
        explorer: 0,
        protector: 0,
        harmonizer: 0
      };
      
      // Process each response
      Object.entries(responses).forEach(([questionId, answerIds]) => {
        // Find the phase for this question
        let phase;
        if (questionId.startsWith('qQ1')) phase = 'initialSegmentation';
        else if (questionId.startsWith('qQ2')) phase = 'detailedDifferentiation';
        else if (questionId.startsWith('qQ3')) phase = 'typeConfirmation';
        else if (questionId.startsWith('qQ4')) {
          if (questionId === 'qQ401') phase = 'wing-type';
          else phase = 'confirmation';
        }
        else if (questionId.startsWith('qQ5')) phase = 'instinctual-variant';
        else if (questionId.startsWith('qQ6')) phase = 'personalization';
        
        // Apply phase weight to the score
        const phaseWeight = SCORING_WEIGHTS[phase]?.weight || 0.1;
        
        // Process each answer for this question
        answerIds.forEach(answerId => {
          // Get the persona associated with this answer
          const persona = answerToPersonaMapping[phase]?.[answerId];
          if (persona && scores.hasOwnProperty(persona)) {
            // Apply the persona's scoring weight to its score
            const personaWeight = EMOTIONAL_PERSONAS[persona]?.scoringWeight || 1.0;
            scores[persona] += 10 * phaseWeight * personaWeight;
          }
        });
      });
      
      return scores;
    } catch (error) {
      console.error('Error calculating persona scores:', error);
      debugScoring('Calculation error', error.message);
      // Return default scores if error occurs
      return {
        upholder: 0, giver: 0, driver: 0, seeker: 0, observer: 0,
        guardian: 0, explorer: 0, protector: 0, harmonizer: 0
      };
    }
  }
  
  /**
   * Analyze text input to identify persona traits
   * @param {string} text - User's text input
   * @returns {Promise<Object>} Scores for each persona based on text analysis
   */
  async function analyzeTextForPersonas(text) {
    try {
      debugScoring('Text analysis', 'Starting text analysis for personas');
      
      // Generate the analysis prompt
      const prompt = `
      Analyze the following text to identify traits of the 9 Emotional Personas:
  
      1. The Upholder (Type 1): Values integrity, responsibility, justice, self-discipline. Fears being wrong or flawed.
      2. The Giver (Type 2): Values generosity, loyalty, compassion, service. Fears being unloved or unwanted.
      3. The Driver (Type 3): Values excellence, achievement, efficiency, recognition. Fears being seen as a failure.
      4. The Seeker (Type 4): Values authenticity, depth, individuality, emotional truth. Fears being emotionally abandoned.
      5. The Observer (Type 5): Values knowledge, autonomy, competence, privacy. Fears being depleted or invaded.
      6. The Guardian (Type 6): Values loyalty, security, preparedness, support. Fears being unsafe or betrayed.
      7. The Explorer (Type 7): Values freedom, adventure, optimism, flexibility. Fears being trapped in pain.
      8. The Protector (Type 8): Values strength, justice, protection, leadership. Fears being controlled or betrayed.
      9. The Harmonizer (Type 9): Values peace, harmony, acceptance, stability. Fears conflict or disconnection.
  
      For each persona, assign a score from 0-100 based on how strongly the text exhibits traits of that persona.
      
      TEXT TO ANALYZE:
      ${text}
  
      ANALYSIS RESULT:
      `;
      
      // Call the LLM analysis service
      // Note: You'll need to update this to use your existing axios config for Ollama
      const response = await axios.post(process.env.OLLAMA_URL || 'http://host.docker.internal:11434/api/generate', {
        model: 'llama2',
        prompt: prompt,
        stream: false,
        options: {
          temperature: 0.7,
          top_p: 0.9,
          top_k: 40,
          num_predict: 2048
        }
      });
  
      if (!response.data || !response.data.response) {
        throw new Error('Analysis request failed');
      }
  
      // Parse the LLM response to extract scores
      const scores = {
        upholder: 0,
        giver: 0,
        driver: 0,
        seeker: 0,
        observer: 0,
        guardian: 0,
        explorer: 0,
        protector: 0,
        harmonizer: 0
      };
      
      // Extract scores from LLM response using regex
      const scoreRegex = /(\w+).*?(\d+)/g;
      let match;
      const textToAnalyze = response.data.response;
      
      while ((match = scoreRegex.exec(textToAnalyze)) !== null) {
        const personaType = match[1].toLowerCase();
        const score = parseInt(match[2], 10);
        
        // Map the extracted persona to our internal types
        if (personaType.includes('upholder') || personaType.includes('type 1')) {
          scores.upholder = score;
        } else if (personaType.includes('giver') || personaType.includes('type 2')) {
          scores.giver = score;
        } else if (personaType.includes('driver') || personaType.includes('type 3')) {
          scores.driver = score;
        } else if (personaType.includes('seeker') || personaType.includes('type 4')) {
          scores.seeker = score;
        } else if (personaType.includes('observer') || personaType.includes('type 5')) {
          scores.observer = score;
        } else if (personaType.includes('guardian') || personaType.includes('type 6')) {
          scores.guardian = score;
        } else if (personaType.includes('explorer') || personaType.includes('type 7')) {
          scores.explorer = score;
        } else if (personaType.includes('protector') || personaType.includes('type 8')) {
          scores.protector = score;
        } else if (personaType.includes('harmonizer') || personaType.includes('type 9')) {
          scores.harmonizer = score;
        }
      }
      
      debugScoring('Text analysis complete', JSON.stringify(scores));
      return scores;
    } catch (error) {
      console.error('Error analyzing text:', error);
      debugScoring('Text analysis error', error.message);
      // Return default scores
      return {
        upholder: 0, giver: 0, driver: 0, seeker: 0, observer: 0,
        guardian: 0, explorer: 0, protector: 0, harmonizer: 0
      };
    }
  }
  
  /**
   * Generate assessment results based on scores
   * @param {Object} scores - Calculated scores for each persona
   * @returns {Object} Assessment results with personas, values, and life domains
   */
  function generateAssessmentResults(scores) {
    try {
      // Sort personas by score
      const sortedPersonas = Object.entries(scores)
        .map(([persona, score]) => ({ 
          persona, 
          score,
          details: EMOTIONAL_PERSONAS[persona]
        }))
        .sort((a, b) => b.score - a.score);
      
      // Primary persona is the highest scoring
      const primaryPersona = {
        name: sortedPersonas[0].details.name,
        type: sortedPersonas[0].details.type,
        score: sortedPersonas[0].score,
        description: sortedPersonas[0].details.description
      };
      
      // Secondary personas are the next 2 highest scoring (if score > 30)
      const secondaryPersonas = sortedPersonas
        .slice(1, 3)
        .filter(p => p.score > 30)
        .map(p => ({
          name: p.details.name,
          type: p.details.type,
          score: p.score
        }));
      
      // Get core values from primary and secondary personas
      const coreValues = new Set();
      // Add primary persona values
      sortedPersonas[0].details.coreValues.forEach(value => coreValues.add(value));
      // Add some values from secondary personas (top 2-3 values)
      secondaryPersonas.forEach(p => {
        const persona = EMOTIONAL_PERSONAS[sortedPersonas.find(sp => sp.details.name === p.name).persona];
        persona.coreValues.slice(0, 2).forEach(value => coreValues.add(value));
      });
      
      // Generate life domain insights based on primary and secondary personas
      const lifeDomains = {};
      const domains = ["relationships", "career", "health", "lifestyle", "purpose"];
      
      domains.forEach(domain => {
        // Start with primary persona impact
        let domainInsight = sortedPersonas[0].details.lifeDomains[domain];
        
        // Add influences from secondary personas
        if (secondaryPersonas.length > 0) {
          // Get the domain info from the secondary persona
          const secondaryPersona = EMOTIONAL_PERSONAS[
            sortedPersonas.find(sp => sp.details.name === secondaryPersonas[0].name).persona
          ];
          
          // Add a nuanced insight combining primary and secondary
          domainInsight += ` With secondary ${secondaryPersonas[0].name} influence: ${secondaryPersona.lifeDomains[domain].split(';')[0]}`;
        }
        
        lifeDomains[domain] = domainInsight;
      });
      
      // Results object
      return {
        primaryPersona,
        secondaryPersonas,
        coreValues: Array.from(coreValues),
        coreNeeds: sortedPersonas[0].details.coreNeeds,
        lifeDomains,
        allScores: Object.fromEntries(
          sortedPersonas.map(p => [p.persona, Math.round(p.score)])
        )
      };
    } catch (error) {
      console.error('Error generating assessment results:', error);
      debugScoring('Results generation error', error.message);
      return {
        primaryPersona: { name: "Unknown", score: 0 },
        secondaryPersonas: [],
        coreValues: [],
        coreNeeds: [],
        lifeDomains: {},
        allScores: {}
      };
    }
  }
  
  /**
   * Process assessment data and generate results
   * @param {Object} assessmentData - Assessment data (either responses or text)
   * @param {string} assessmentType - Type of assessment ('questionnaire' or 'text-analysis')
   * @returns {Promise<Object>} Assessment results
   */
  async function processAssessment(assessmentData, assessmentType) {
    try {
      debugScoring('Process assessment', `Starting assessment processing for ${assessmentType}`);
      
      let scores;
      if (assessmentType === 'questionnaire') {
        // Get answer to persona mapping
        const answerMapping = {
          initialSegmentation: {
            'A101': 'observer', 'A102': 'giver', 'A103': 'driver',
            'A104': 'seeker', 'A105': 'upholder', 'A106': 'guardian',
            'A107': 'explorer', 'A108': 'protector', 'A109': 'harmonizer',
            'A110': 'observer', 'A111': 'giver', 'A112': 'driver',
            'A113': 'seeker', 'A114': 'upholder', 'A115': 'guardian',
            'A116': 'explorer', 'A117': 'protector', 'A118': 'harmonizer'
          },
          detailedDifferentiation: {
            'A201': 'observer', 'A202': 'giver', 'A203': 'driver',
            'A204': 'seeker', 'A205': 'upholder', 'A206': 'guardian',
            'A207': 'explorer', 'A208': 'protector', 'A209': 'harmonizer'
          },
          typeConfirmation: {
            'A301': 'upholder', 'A302': 'giver', 'A303': 'driver',
            'A304': 'seeker', 'A305': 'observer', 'A306': 'guardian',
            'A307': 'explorer', 'A308': 'protector', 'A309': 'harmonizer'
          }
        };
        
        // Calculate scores based on questionnaire responses
        scores = calculatePersonaScores(assessmentData, answerMapping);
      } else if (assessmentType === 'text-analysis') {
        // Analyze text to calculate scores
        scores = await analyzeTextForPersonas(assessmentData);
      } else {
        throw new Error(`Unknown assessment type: ${assessmentType}`);
      }
      
      // Generate results from scores
      const results = generateAssessmentResults(scores);
      
      debugScoring('Process assessment', 'Assessment processing complete');
      return results;
    } catch (error) {
      console.error('Error processing assessment:', error);
      debugScoring('Process assessment error', error.message);
      throw error;
    }
  }
  
  // Export functions for use in other modules
  module.exports = {
    EMOTIONAL_PERSONAS,
    SCORING_WEIGHTS,
    calculatePersonaScores,
    analyzeTextForPersonas,
    generateAssessmentResults,
    processAssessment,
    debugScoring
  };