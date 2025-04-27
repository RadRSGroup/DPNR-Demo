// Add production optimization flags
const IS_PRODUCTION = window.location.hostname !== 'localhost';
const ENABLE_LOGGING = !IS_PRODUCTION;

// Import dependencies
import { textAnalysisAgent } from '/text-analysis-agent.js';
import { claudeAgent } from '/claude-agent.js';
import { assessmentManager } from '/js/core/assessment-manager.js';
import { t, setTranslations, refreshI18nTexts } from '/i18n.js';
import { switchLanguage, detectLanguage } from '/languages/index.js';
import { recordMetric } from '/monitoring/performance-monitor.js';
import { logUserMetrics } from '/monitoring/user-metrics.js';
import { personas } from '/personas.js';
import { LanguageHandler } from '/language-handler.js';
import { LanguageSelector } from '/components/language-selector.js';
import { LanguageTest } from '/components/LanguageTest.js';

// Initialize components after DOM is loaded
document.addEventListener('DOMContentLoaded', async () => {
    try {
        // Initialize the text analysis agent
        await textAnalysisAgent.initialize().catch(error => {
            console.error('Failed to initialize text analysis agent:', error);
        });

        // Initialize Claude agent
        // Note: API key should be provided by the backend
        await claudeAgent.initialize().catch(error => {
            console.error('Failed to initialize Claude agent:', error);
        });

        // Initialize language handler
        const languageHandler = new LanguageHandler();
        await languageHandler.initializeEnglishPersonas(personas);

        // Initialize language selector
        const languageSelector = new LanguageSelector(languageHandler, 'language-selector-container');
        
        // Initialize language test component
        const languageTest = new LanguageTest();
        languageTest.render('language-test-container');

        // Initialize assessment manager
        await assessmentManager.initialize().catch(error => {
            console.error('Failed to initialize assessment manager:', error);
        });

        // Add language change observer for UI updates
        languageHandler.addObserver(event => {
            if (event.type === 'languageChange') {
                updateUI();
                languageSelector.updateStyles();
                // Update language test when language changes
                languageTest.currentLanguage = event.language;
                languageTest.render('language-test-container');
                // Update document direction and language
                document.documentElement.dir = event.language === 'he' ? 'rtl' : 'ltr';
                document.documentElement.lang = event.language;
                // Record language switch time
                const switchDuration = performance.now() - window.lastSwitchStart;
                recordMetric('languageSwitchTime', switchDuration.toFixed(0));
            }
        });

        // Add click handler for language selector
        const languageSelect = document.getElementById('languageSelect');
        if (languageSelect) {
            languageSelect.addEventListener('change', async (event) => {
                window.lastSwitchStart = performance.now();
                await switchLanguage(event.target.value);
            });
        }

        // Hide loading overlay once everything is initialized
        window.hideLoading();
    } catch (error) {
        console.error('Error during initialization:', error);
        window.hideLoading();
        // Show error message in current language
        const errorMessage = {
            en: 'There was an error initializing the application. Please refresh the page and try again.',
            he: 'אירעה שגיאה באתחול האפליקציה. אנא רענן את הדף ונסה שוב.'
        };
        alert(errorMessage[document.documentElement.lang] || errorMessage.en);
    }
});

// Initialize language based on detection or saved preference
const initialLang = localStorage.getItem('preferredLanguage') || detectLanguage();
window.lastSwitchStart = performance.now();
switchLanguage(initialLang).finally(() => {
    const duration = performance.now() - window.lastSwitchStart;
    recordMetric('languageSwitchTime', duration.toFixed(0));
    // Save language preference
    localStorage.setItem('preferredLanguage', initialLang);
});

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

window.addEventListener('beforeunload', () => {
    // For demo, log metrics to console
    logMetrics();
    logUserMetrics();
}); 