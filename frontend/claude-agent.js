import { IS_PRODUCTION } from './config.js';

// Claude Agent Interface
class ClaudeAgent {
    constructor() {
        this.initialized = false;
        this.apiKey = null;
        this.model = 'claude-3-opus-20240229'; // Default model
        this.cache = new Map();
        this.cacheTimeout = 1000 * 60 * 60; // 1 hour
    }

    async initialize(apiKey) {
        try {
            if (!apiKey) {
                throw new Error('Claude API key is required');
            }
            
            this.apiKey = apiKey;
            this.initialized = true;
            
            if (!IS_PRODUCTION) {
                console.log('Claude agent initialized successfully');
            }
        } catch (error) {
            console.error('Failed to initialize Claude agent:', error);
            throw error;
        }
    }

    generateCacheKey(text, question) {
        return `${text.substring(0, 50)}_${question.substring(0, 50)}`;
    }

    async analyzeResponse(text, question) {
        if (!this.initialized) {
            throw new Error('Claude agent not initialized');
        }

        try {
            const cacheKey = this.generateCacheKey(text, question);
            if (this.cache.has(cacheKey)) {
                return this.cache.get(cacheKey);
            }

            const analysis = await this.processWithClaude(text, question);
            
            // Cache the result
            this.cache.set(cacheKey, analysis);
            setTimeout(() => this.cache.delete(cacheKey), this.cacheTimeout);

            return analysis;
        } catch (error) {
            console.error('Error analyzing text with Claude:', error);
            throw error;
        }
    }

    async processWithClaude(text, question) {
        const prompt = `Analyze the following response to the question "${question}":
        
        Response: ${text}
        
        Please provide:
        1. Key personas identified
        2. Confidence score (0-1)
        3. Key themes and topics
        4. Sentiment analysis
        5. Notable entities mentioned
        6. Any other relevant insights`;

        try {
            const response = await fetch('https://api.anthropic.com/v1/messages', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'x-api-key': this.apiKey,
                    'anthropic-version': '2023-06-01'
                },
                body: JSON.stringify({
                    model: this.model,
                    max_tokens: 1000,
                    messages: [{
                        role: 'user',
                        content: prompt
                    }]
                })
            });

            if (!response.ok) {
                throw new Error(`Claude API error: ${response.statusText}`);
            }

            const data = await response.json();
            return this.parseClaudeResponse(data.content[0].text);
        } catch (error) {
            console.error('Error processing with Claude:', error);
            throw error;
        }
    }

    parseClaudeResponse(responseText) {
        // Parse the structured response from Claude
        // This is a simplified version - you may want to enhance this based on your needs
        const analysis = {
            personas: [],
            confidence: 0,
            topics: [],
            sentiment: 'neutral',
            entities: [],
            insights: []
        };

        // Basic parsing logic - you may want to enhance this
        const lines = responseText.split('\n');
        for (const line of lines) {
            if (line.toLowerCase().includes('personas')) {
                analysis.personas = line.split(':')[1].split(',').map(p => p.trim());
            } else if (line.toLowerCase().includes('confidence')) {
                analysis.confidence = parseFloat(line.split(':')[1].trim());
            } else if (line.toLowerCase().includes('themes') || line.toLowerCase().includes('topics')) {
                analysis.topics = line.split(':')[1].split(',').map(t => t.trim());
            } else if (line.toLowerCase().includes('sentiment')) {
                analysis.sentiment = line.split(':')[1].trim().toLowerCase();
            } else if (line.toLowerCase().includes('entities')) {
                analysis.entities = line.split(':')[1].split(',').map(e => e.trim());
            }
        }

        return analysis;
    }
}

// Export the ClaudeAgent class
export const claudeAgent = new ClaudeAgent(); 