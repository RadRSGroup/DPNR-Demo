// Language manager module
export const languageConfig = {
    he: {
        dir: 'rtl',
        name: 'עברית',
        dateFormat: 'DD/MM/YYYY',
        numeralSystem: 'latn',
        code: 'he'
    },
    en: {
        dir: 'ltr',
        name: 'English',
        dateFormat: 'MM/DD/YYYY',
        numeralSystem: 'latn',
        code: 'en'
    }
};

export const translations = {
    he: {
        ui: {
            welcome: 'ברוכים הבאים ל-Core Persona',
            begin: 'התחל הערכה',
            next: 'הבא',
            previous: 'הקודם',
            submit: 'שלח',
            loading: 'טוען...',
            error: 'שגיאה',
            requiredField: 'שדה חובה',
            validation: {
                required: 'אנא ענה על כל השאלות לפני שתמשיך',
                invalidInput: 'קלט לא חוקי',
            },
            phases: {
                registration: 'הרשמה',
                initialSegmentation: 'היכרות ראשונית',
                detailedDifferentiation: 'מה הופך אותך לייחודי?',
                typeConfirmation: 'אישור סוג',
                wingType: 'סוג כנף',
                instinctualVariant: 'וריאנט אינסטינקטיבי',
                personalization: 'התאמה אישית',
                textInput: 'במילים שלי',
                results: 'תוצאות',
            },
            progress: {
                step: 'שלב',
                of: 'מתוך',
            }
        }
    },
    en: {
        ui: {
            welcome: 'Welcome to Core Persona',
            begin: 'Begin Assessment',
            next: 'Next',
            previous: 'Previous',
            submit: 'Submit',
            loading: 'Loading...',
            error: 'Error',
            requiredField: 'Required field',
            validation: {
                required: 'Please answer all questions before continuing',
                invalidInput: 'Invalid input',
            },
            phases: {
                registration: 'Registration',
                initialSegmentation: 'Initial Segmentation',
                detailedDifferentiation: 'Detailed Differentiation',
                typeConfirmation: 'Type Confirmation',
                wingType: 'Wing Type',
                instinctualVariant: 'Instinctual Variant',
                personalization: 'Personalization',
                textInput: 'Text Input',
                results: 'Results',
            },
            progress: {
                step: 'Step',
                of: 'of',
            }
        }
    }
};

export class LanguageManager {
    constructor() {
        this.currentLanguage = 'en';
        this.observers = new Set();
    }

    initialize() {
        // Set initial language based on browser or user preference
        const browserLang = navigator.language.split('-')[0];
        this.setLanguage(browserLang in languageConfig ? browserLang : 'en');
    }

    setLanguage(lang) {
        if (lang in languageConfig) {
            this.currentLanguage = lang;
            this.notifyObservers({ type: 'languageChange', language: lang });
            return true;
        }
        return false;
    }

    getTranslation(key) {
        const keys = key.split('.');
        let translation = translations[this.currentLanguage];
        
        for (const k of keys) {
            if (!translation || !(k in translation)) {
                return key; // Return the key if translation not found
            }
            translation = translation[k];
        }
        
        return translation;
    }

    isRTL() {
        return languageConfig[this.currentLanguage].dir === 'rtl';
    }

    addObserver(observer) {
        this.observers.add(observer);
    }

    removeObserver(observer) {
        this.observers.delete(observer);
    }

    notifyObservers(event) {
        this.observers.forEach(observer => observer(event));
    }
}

// Export singleton instance
export const languageManager = new LanguageManager(); 