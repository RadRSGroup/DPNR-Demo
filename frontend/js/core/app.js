// Core application module
import { textAnalysisAgent } from '../../text-analysis-agent.js';
import { languageConfig } from '../../language-config.js';
import LanguageHandler from '../../language-handler.js';
import LanguageSelector from '../components/language-selector.js';
import { initializeState } from '../state/state-manager.js';
import { initializeUI } from '../ui/ui-manager.js';
import { initializeScoring } from '../scoring/scoring-manager.js';

// Production optimization flags
const IS_PRODUCTION = window.location.hostname !== 'localhost';
const ENABLE_LOGGING = !IS_PRODUCTION;

export class Application {
    constructor() {
        this.languageHandler = new LanguageHandler();
        this.languageSelector = new LanguageSelector(this.languageHandler, 'language-selector-container');
        this.state = null;
    }

    async initialize() {
        try {
            // Initialize text analysis agent
            await textAnalysisAgent.initialize();
            
            // Initialize language handler
            this.languageHandler.initializeEnglishPersonas(personas);
            
            // Initialize state
            this.state = initializeState();
            
            // Initialize UI
            initializeUI(this.languageHandler);
            
            // Initialize scoring system
            initializeScoring();
            
            // Set up language change observer
            this.setupLanguageObserver();
            
            console.log('Application initialized successfully');
        } catch (error) {
            console.error('Failed to initialize application:', error);
            throw error;
        }
    }

    setupLanguageObserver() {
        this.languageHandler.addObserver(event => {
            if (event.type === 'languageChange') {
                this.updateUI();
                this.languageSelector.updateStyles();
            }
        });
    }

    updateUI() {
        const elements = document.querySelectorAll('[data-i18n]');
        elements.forEach(el => {
            const key = el.getAttribute('data-i18n');
            el.textContent = this.languageHandler.getTranslation(key);
        });
        
        // Update RTL/LTR specific styles
        const rtlStyles = document.getElementById('rtl-styles');
        if (this.languageHandler.isRTL()) {
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
}

// Export singleton instance
export const app = new Application(); 