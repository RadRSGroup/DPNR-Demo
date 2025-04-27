import { languageConfig, hebrewTranslations, hebrewPersonaDescriptions } from './language-config';
import { personas } from './personas.js';

export class LanguageHandler {
    constructor() {
        this.currentLanguage = 'en';
        this.supportedLanguages = Object.keys(languageConfig);
        this.translations = {
            en: {
                'ui.next': 'Next',
                'ui.back': 'Back',
                'ui.error': 'Error',
                'ui.validation.required': 'Please answer all questions before proceeding.',
                'ui.results.primaryPersona': 'Primary Persona',
                'ui.results.secondaryPersonas': 'Secondary Personas',
                'ui.results.coreValues': 'Core Values',
                'ui.results.innerWorld': 'Inner World',
                'ui.results.fear': 'Fear',
                'ui.results.desire': 'Desire',
                'ui.results.limitingBelief': 'Limiting Belief',
                'ui.results.emotionalNeeds': 'Emotional Needs',
                'ui.results.blindSpots': 'Blind Spots',
                'ui.results.aspirations': 'Aspirations',
                'ui.results.lifeDomainImpact': 'Life Domain Impact',
                'ui.results.potential': 'Potential',
                'ui.results.capabilities': 'Capabilities',
                'ui.results.lifeChanges': 'Life Changes',
                'ui.results.keyTraits': 'Key Traits'
            },
            he: {
                'ui.next': 'הבא',
                'ui.back': 'חזרה',
                'ui.error': 'שגיאה',
                'ui.validation.required': 'אנא ענה על כל השאלות לפני שתמשיך.',
                'ui.results.primaryPersona': 'דמות ראשית',
                'ui.results.secondaryPersonas': 'דמויות משניות',
                'ui.results.coreValues': 'ערכים מרכזיים',
                'ui.results.innerWorld': 'עולם פנימי',
                'ui.results.fear': 'פחד',
                'ui.results.desire': 'רצון',
                'ui.results.limitingBelief': 'אמונה מגבילה',
                'ui.results.emotionalNeeds': 'צרכים רגשיים',
                'ui.results.blindSpots': 'נקודות עיוורון',
                'ui.results.aspirations': 'שאיפות',
                'ui.results.lifeDomainImpact': 'השפעה על תחומי חיים',
                'ui.results.potential': 'פוטנציאל',
                'ui.results.capabilities': 'יכולות',
                'ui.results.lifeChanges': 'שינויים בחיים',
                'ui.results.keyTraits': 'תכונות מפתח'
            }
        };
        this.personaDescriptions = {
            en: {}, // Will be populated from the main app
            he: hebrewPersonaDescriptions
        };
        this.observers = new Set();
        this.fallbackLanguage = 'en';
    }

    async initializeEnglishPersonas(englishPersonas) {
        this.personaDescriptions.en = englishPersonas;
        this.personas = englishPersonas;
        this.translations.en = {
            ...this.personas
        };
    }

    setLanguage(lang) {
        if (this.supportedLanguages.includes(lang)) {
            const previousLang = this.currentLanguage;
            this.currentLanguage = lang;
            
            // Update document attributes
            document.documentElement.lang = lang;
            document.documentElement.dir = languageConfig[lang].dir;
            
            // Notify observers of language change
            this.notifyObservers({
                type: 'languageChange',
                previousLang,
                newLang: lang
            });

            return true;
        }
        return false;
    }

    getTranslation(key, params = {}) {
        const keys = key.split('.');
        let translation = this.translations[this.currentLanguage];
        
        // Traverse the translation object
        for (const k of keys) {
            if (translation && translation[k]) {
                translation = translation[k];
            } else {
                // Try fallback language
                translation = this.getFallbackTranslation(key);
                break;
            }
        }

        // Replace parameters in translation
        if (typeof translation === 'string') {
            return this.interpolateParams(translation, params);
        }

        return key; // Return key if translation not found
    }

    getPersonaDescription(personaId) {
        const currentLangDescriptions = this.personaDescriptions[this.currentLanguage];
        const fallbackDescriptions = this.personaDescriptions[this.fallbackLanguage];
        
        return currentLangDescriptions[personaId] || fallbackDescriptions[personaId] || this.personas[personaId];
    }

    addObserver(observer) {
        if (typeof observer === 'function') {
            this.observers.add(observer);
            return true;
        }
        return false;
    }

    removeObserver(observer) {
        return this.observers.delete(observer);
    }

    notifyObservers(event) {
        this.observers.forEach(observer => {
            try {
                observer(event);
            } catch (error) {
                console.error('Error in language observer:', error);
            }
        });
    }

    getFallbackTranslation(key) {
        const keys = key.split('.');
        let translation = this.translations[this.fallbackLanguage];
        
        for (const k of keys) {
            if (translation && translation[k]) {
                translation = translation[k];
            } else {
                return key;
            }
        }
        
        return translation;
    }

    interpolateParams(text, params) {
        return text.replace(/\{(\w+)\}/g, (match, key) => {
            return params[key] !== undefined ? params[key] : match;
        });
    }

    getDirection() {
        return languageConfig[this.currentLanguage].dir;
    }

    getLanguageName() {
        return languageConfig[this.currentLanguage].name;
    }

    getDateFormat() {
        return languageConfig[this.currentLanguage].dateFormat;
    }

    isRTL() {
        return this.getDirection() === 'rtl';
    }

    addTranslations(lang, translations) {
        if (!this.translations[lang]) {
            this.translations[lang] = {};
        }
        
        this.translations[lang] = {
            ...this.translations[lang],
            ...translations
        };
        
        // Add to supported languages if not already present
        if (!this.supportedLanguages.includes(lang)) {
            this.supportedLanguages.push(lang);
        }
    }

    addPersonaDescriptions(lang, descriptions) {
        if (!this.personaDescriptions[lang]) {
            this.personaDescriptions[lang] = {};
        }
        
        this.personaDescriptions[lang] = {
            ...this.personaDescriptions[lang],
            ...descriptions
        };
    }

    getSupportedLanguages() {
        return this.supportedLanguages.map(lang => ({
            code: lang,
            name: languageConfig[lang].name,
            dir: languageConfig[lang].dir
        }));
    }

    getCurrentLanguage() {
        return this.currentLanguage;
    }
} 