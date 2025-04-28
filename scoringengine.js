/**
 * Emotional Personas Data Module
 *
 * Exports the EMOTIONAL_PERSONAS constant for use across the codebase.
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

module.exports = { EMOTIONAL_PERSONAS }; 