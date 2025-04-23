// Add production optimization flags
const IS_PRODUCTION = window.location.hostname !== 'localhost';
const ENABLE_LOGGING = !IS_PRODUCTION;

// Import the text analysis agent
import { textAnalysisAgent } from './text-analysis-agent.js';

// Import language configuration
import { languageConfig, hebrewTranslations, hebrewPersonaDescriptions } from './language-config.js';

// Import personas configuration
import { personas } from './personas.js';

// Import LanguageHandler
import LanguageHandler from './language-handler.js';
import LanguageSelector from './components/language-selector.js';

// Initialize the text analysis agent
textAnalysisAgent.initialize().catch(error => {
    console.error('Failed to initialize text analysis agent:', error);
});

// Initialize language handler
const languageHandler = new LanguageHandler();
languageHandler.initializeEnglishPersonas(personas);

// Initialize language selector
const languageSelector = new LanguageSelector(languageHandler, 'language-selector-container');

// Add language change observer for UI updates
languageHandler.addObserver(event => {
    if (event.type === 'languageChange') {
        updateUI();
        languageSelector.updateStyles();
    }
});

// Update UI elements with translations
function updateUI() {
    // Update all UI elements with translations
    const elements = document.querySelectorAll('[data-i18n]');
    elements.forEach(el => {
        const key = el.getAttribute('data-i18n');
        el.textContent = languageHandler.getTranslation(key);
    });
    
    // Update RTL/LTR specific styles
    const rtlStyles = document.getElementById('rtl-styles');
    if (languageHandler.isRTL()) {
        if (!rtlStyles) {
            const style = document.createElement('style');
            style.id = 'rtl-styles';
            style.textContent = `
                body { direction: rtl; }
                .question-container { text-align: right; }
                .option-container { text-align: right; }
            `;
            document.head.appendChild(style);
        }
    } else if (rtlStyles) {
        rtlStyles.remove();
    }
}
