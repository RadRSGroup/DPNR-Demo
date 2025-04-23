// Get production flag from window
const IS_PRODUCTION = window.location.hostname !== 'localhost';

// Text Analysis Agent Interface
class TextAnalysisAgent {
    constructor() {
        this.initialized = false;
        this.model = null;
        this.version = '1.0.0';
        this.modelVersions = new Map();
        this.cache = new Map();
        this.cacheTimeout = 1000 * 60 * 60; // 1 hour
        this.nlp = window.nlp;
        this.sentences = window.nlpSentences;
    }

    async initialize() {
        try {
            // Initialize NLP tools and models
            if (!this.nlp) {
                throw new Error('NLP library not loaded');
            }
            
            // Load the default model
            this.model = await this.loadModel(this.version);
            this.initialized = true;
            
            if (!IS_PRODUCTION) {
                console.log('Text analysis agent initialized successfully');
            }
        } catch (error) {
            console.error('Failed to initialize text analysis agent:', error);
            throw error;
        }
    }

    async loadModel(version = this.version) {
        if (this.modelVersions.has(version)) {
            return this.modelVersions.get(version);
        }

        // Load and cache model
        const model = {
            config: {
                threshold: 0.7,
                maxTokens: 500,
                version: version
            },
            nlp: this.nlp
        };

        this.modelVersions.set(version, model);
        return model;
    }

    generateCacheKey(text, question) {
        return `${text.substring(0, 50)}_${question.substring(0, 50)}`;
    }

    async analyzeResponse(text, question) {
        if (!this.initialized) {
            throw new Error('Text analysis agent not initialized');
        }

        try {
            const cacheKey = this.generateCacheKey(text, question);
            if (this.cache.has(cacheKey)) {
                return this.cache.get(cacheKey);
            }

            const analysis = await this.processText(text, question);
            const result = {
                personas: analysis.personas,
                confidence: analysis.confidence,
                keywords: analysis.keywords,
                sentiment: analysis.sentiment,
                entities: analysis.entities,
                topics: analysis.topics
            };

            // Cache the result
            this.cache.set(cacheKey, result);
            setTimeout(() => this.cache.delete(cacheKey), this.cacheTimeout);

            return result;
        } catch (error) {
            console.error('Error analyzing text:', error);
            throw error;
        }
    }

    async processText(text, question) {
        const analysis = {
            personas: [],
            keywords: [],
            confidence: 0,
            sentiment: 'neutral',
            entities: [],
            topics: []
        };

        // Enhanced text processing
        const lowercaseText = text.toLowerCase();
        
        // Extract entities using NLP
        const doc = this.nlp(text);
        analysis.entities = doc.people().out('array');
        
        // Enhanced keyword matching with context
        const keywordMap = {
            // Core values and approach to life (Initial Segmentation)
            'excellence': ['upholder'],
            'helping': ['giver'],
            'success': ['driver'],
            'meaning': ['seeker'],
            'knowledge': ['observer'],
            'security': ['guardian'],
            'adventure': ['explorer'],
            'protect': ['protector'],
            'harmony': ['harmonizer'],
            
            // Decision making and adaptability (Detailed Differentiation)
            'analyze': ['observer', 'driver'],
            'feel': ['harmonizer', 'giver'],
            'plan': ['upholder', 'guardian'],
            'explore': ['explorer', 'seeker'],
            'protect': ['protector', 'guardian'],
            
            // Self-expression and social interaction (Type Confirmation)
            'authentic': ['seeker', 'observer'],
            'support': ['giver', 'harmonizer'],
            'achieve': ['driver', 'upholder'],
            'discover': ['explorer', 'seeker'],
            'secure': ['guardian', 'protector']
        };

        // Context-aware keyword matching
        Object.entries(keywordMap).forEach(([keyword, relatedPersonas]) => {
            if (lowercaseText.includes(keyword)) {
                analysis.keywords.push(keyword);
                analysis.personas.push(...relatedPersonas);
            }
        });

        // Enhanced sentiment analysis
        const sentimentAnalysis = this.analyzeSentiment(text);
        analysis.sentiment = sentimentAnalysis.sentiment;
        
        // Calculate confidence using multiple factors
        analysis.confidence = this.calculateConfidence({
            keywordMatches: analysis.keywords.length,
            semanticRelevance: this.scoreSemanticRelevance(text, question),
            answerQuality: this.scoreAnswerQuality(text),
            contextMatch: this.scoreContextMatch(text, question),
            isPersonalQuestion: this.isPersonalQuestion(question),
            requiresDetail: this.requiresDetail(text)
        });

        // Remove duplicate personas
        analysis.personas = [...new Set(analysis.personas)];

        return analysis;
    }

    analyzeSentiment(text) {
        const positiveWords = ['love', 'happy', 'great', 'excellent', 'good', 'positive', 'wonderful'];
        const negativeWords = ['hate', 'bad', 'terrible', 'poor', 'wrong', 'negative', 'awful'];
        const intensifiers = ['very', 'extremely', 'really', 'absolutely'];
        
        let score = 0;
        const words = text.toLowerCase().split(/\s+/);
        
        for (let i = 0; i < words.length; i++) {
            const word = words[i];
            if (positiveWords.includes(word)) {
                score += 1;
                // Check for intensifiers
                if (i > 0 && intensifiers.includes(words[i-1])) {
                    score += 0.5;
                }
            } else if (negativeWords.includes(word)) {
                score -= 1;
                // Check for intensifiers
                if (i > 0 && intensifiers.includes(words[i-1])) {
                    score -= 0.5;
                }
            }
        }
        
        return {
            sentiment: score > 0 ? 'positive' : score < 0 ? 'negative' : 'neutral',
            score: score
        };
    }

    calculateConfidence(factors) {
        // Dynamic weights based on question type and response characteristics
        const baseWeights = {
            keywordMatches: 0.25,
            semanticRelevance: 0.3,
            answerQuality: 0.25,
            contextMatch: 0.2
        };

        // Adjust weights based on answer characteristics
        const weights = { ...baseWeights };
        
        // Boost semantic relevance for emotional/personal questions
        if (factors.isPersonalQuestion) {
            weights.semanticRelevance += 0.1;
            weights.keywordMatches -= 0.05;
        }

        // Boost answer quality for detailed questions
        if (factors.requiresDetail) {
            weights.answerQuality += 0.1;
            weights.contextMatch -= 0.05;
            weights.keywordMatches -= 0.05;
        }

        let totalScore = 0;
        let totalWeight = 0;

        // Calculate weighted score with normalization
        for (const [factor, weight] of Object.entries(weights)) {
            if (factors[factor] !== undefined) {
                // Normalize factor score between 0 and 1
                const normalizedScore = Math.max(0, Math.min(factors[factor], 1));
                totalScore += normalizedScore * weight;
                totalWeight += weight;
            }
        }

        // Apply confidence penalties for edge cases
        let confidence = totalWeight > 0 ? Math.min(totalScore / totalWeight, 1) : 0;
        
        return Math.max(0, Math.min(confidence, 1));  // Ensure final score is between 0 and 1
    }

    scoreSemanticRelevance(text, question) {
        const doc = this.nlp(text);
        const questionDoc = this.nlp(question);
        
        // Get terms from both texts
        const textTerms = doc.terms().out('array');
        const questionTerms = questionDoc.terms().out('array');
        
        // Calculate overlap
        const overlap = questionTerms.filter(term => 
            textTerms.some(t => t.toLowerCase().includes(term.toLowerCase()))
        ).length;
        
        return Math.min(overlap / questionTerms.length, 1);
    }

    scoreAnswerQuality(text) {
        const doc = this.nlp(text);
        const sentences = doc.sentences().out('array');
        const wordCount = text.split(/\s+/).length;
        
        // Score based on length and sentence structure
        let score = 0;
        
        // Length scoring (ideal range: 20-100 words)
        if (wordCount >= 20 && wordCount <= 100) {
            score += 0.5;
        } else if (wordCount > 100) {
            score += 0.3;
        } else {
            score += 0.2 * (wordCount / 20);
        }
        
        // Sentence structure scoring
        score += 0.5 * Math.min(sentences.length / 3, 1);
        
        return score;
    }

    scoreContextMatch(text, question) {
        const doc = this.nlp(text);
        const questionDoc = this.nlp(question);
        
        // Extract key terms from question
        const questionTerms = questionDoc.terms().out('array');
        const textTerms = doc.terms().out('array');
        
        // Calculate overlap
        const overlap = questionTerms.filter(term => 
            textTerms.some(t => t.toLowerCase().includes(term.toLowerCase()))
        ).length;
        
        return Math.min(overlap / questionTerms.length, 1);
    }

    isPersonalQuestion(question) {
        const personalQuestions = ['What brings you joy?', 'What area of your life would you like to change?', 'What are your goals for your life?', 'How do you typically approach life\'s challenges?', 'What values guide your decisions?', 'How do you handle unexpected changes?', 'What do others appreciate most about you?', 'How do you recharge your energy?', 'What aspects of your personality are hardest to accept?'];
        return personalQuestions.includes(question);
    }

    requiresDetail(text) {
        const wordCount = text.split(/\s+/).length;
        return wordCount > 50;
    }
}

// Create and export a singleton instance
export const textAnalysisAgent = new TextAnalysisAgent(); 