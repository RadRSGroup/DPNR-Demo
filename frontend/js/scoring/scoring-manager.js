// Scoring manager module
import { debugScoring } from '../utils/logger.js';
import { ScoringError } from '../utils/errors.js';

export function initializeScoring() {
    console.log('Scoring system initialized');
}

export function calculatePersonaScore(answers, currentPhase) {
    try {
        debugScoring('calculatePersonaScore', { answers, currentPhase });
        
        // Validate inputs
        if (!answers || !Array.isArray(answers)) {
            throw new ScoringError('Invalid answers format', 'scoring', { answers });
        }
        
        // Calculate scores based on phase
        const scores = {};
        const weights = getPhaseWeights(currentPhase);
        
        answers.forEach(answer => {
            if (!scores[answer.persona]) {
                scores[answer.persona] = 0;
            }
            scores[answer.persona] += answer.value * weights[answer.persona];
        });
        
        // Normalize scores
        const maxScore = Math.max(...Object.values(scores));
        if (maxScore > 0) {
            Object.keys(scores).forEach(persona => {
                scores[persona] = (scores[persona] / maxScore) * 100;
            });
        }
        
        return scores;
    } catch (error) {
        console.error('Error calculating persona scores:', error);
        throw error;
    }
}

function getPhaseWeights(phase) {
    const weights = {
        'initial': { 'type1': 1, 'type2': 1, 'type3': 1 },
        'personalization': { 'type1': 1.5, 'type2': 1.5, 'type3': 1.5 },
        'final': { 'type1': 2, 'type2': 2, 'type3': 2 }
    };
    
    return weights[phase] || weights.initial;
} 