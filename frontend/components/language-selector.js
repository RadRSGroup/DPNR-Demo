// language-selector.js
export class LanguageSelector {
    constructor(languageHandler, containerId) {
        this.languageHandler = languageHandler;
        this.container = document.getElementById(containerId);
        this.initialize();
    }

    initialize() {
        if (!this.container) return;

        // Create language select element
        const select = document.getElementById('languageSelect');
        if (!select) return;

        // Add event listener
        select.addEventListener('change', (e) => {
            const selectedLang = e.target.value;
            this.languageHandler.setLanguage(selectedLang);
            this.updateStyles();
        });
    }

    updateStyles() {
        document.documentElement.setAttribute('dir', 
            this.languageHandler.isRTL() ? 'rtl' : 'ltr'
        );
        document.body.classList.toggle('rtl', this.languageHandler.isRTL());
    }
} 