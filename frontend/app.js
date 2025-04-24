// Add production optimization flags
const IS_PRODUCTION = window.location.hostname !== 'localhost';
const ENABLE_LOGGING = !IS_PRODUCTION;

// Import the text analysis agent
import { textAnalysisAgent } from './text-analysis-agent.js';

// Import Claude agent
import { claudeAgent } from './claude-agent.js';

// Import assessment manager
import { assessmentManager } from './js/core/assessment-manager.js';

// Import language configuration
import { t, setTranslations, refreshI18nTexts } from './i18n.js';
import { switchLanguage, detectLanguage } from './languages/index.js';

// Import personas configuration
import { personas } from './personas.js';

// Import LanguageHandler
import { LanguageHandler } from './language-handler.js';
import { LanguageSelector } from './components/language-selector.js';

// Initialize components after DOM is loaded
document.addEventListener('DOMContentLoaded', async () => {
    try {
        // Initialize the text analysis agent
        await textAnalysisAgent.initialize().catch(error => {
            console.error('Failed to initialize text analysis agent:', error);
        });

        // Initialize Claude agent with API key
        const CLAUDE_API_KEY = process.env.CLAUDE_API_KEY; // Make sure to set this in your environment
        await claudeAgent.initialize(CLAUDE_API_KEY).catch(error => {
            console.error('Failed to initialize Claude agent:', error);
        });

        // Initialize language handler
        const languageHandler = new LanguageHandler();
        await languageHandler.initializeEnglishPersonas(personas);

        // Initialize language selector
        const languageSelector = new LanguageSelector(languageHandler, 'language-selector-container');

        // Initialize assessment manager
        await assessmentManager.initialize().catch(error => {
            console.error('Failed to initialize assessment manager:', error);
        });

        // Add language change observer for UI updates
        languageHandler.addObserver(event => {
            if (event.type === 'languageChange') {
                updateUI();
                languageSelector.updateStyles();
            }
        });

        // Hide loading overlay once everything is initialized
        window.hideLoading();
    } catch (error) {
        console.error('Error during initialization:', error);
        window.hideLoading();
        // Show error message to user
        alert('There was an error initializing the application. Please refresh the page and try again.');
    }
});

// Initialize language based on detection
const initialLang = detectLanguage();
switchLanguage(initialLang);

function updateUI() {
  refreshI18nTexts();
}

// Enhanced analysis function that uses both agents
async function analyzeResponse(text, question) {
    try {
        // Run both analyses in parallel
        const [textAnalysis, claudeAnalysis] = await Promise.all([
            textAnalysisAgent.analyzeResponse(text, question),
            claudeAgent.analyzeResponse(text, question)
        ]);

        // Combine results with weighted confidence
        return {
            personas: [...new Set([...textAnalysis.personas, ...claudeAnalysis.personas])],
            confidence: (textAnalysis.confidence + claudeAnalysis.confidence) / 2,
            keywords: [...new Set([...textAnalysis.keywords, ...claudeAnalysis.topics])],
            sentiment: textAnalysis.confidence > claudeAnalysis.confidence ? 
                textAnalysis.sentiment : claudeAnalysis.sentiment,
            entities: [...new Set([...textAnalysis.entities, ...claudeAnalysis.entities])],
            insights: claudeAnalysis.insights || []
        };
    } catch (error) {
        console.error('Error in combined analysis:', error);
        throw error;
    }
}
