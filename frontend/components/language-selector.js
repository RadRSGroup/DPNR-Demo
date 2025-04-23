// language-selector.js
class LanguageSelector {
    constructor(languageHandler, containerId) {
        this.languageHandler = languageHandler;
        this.container = document.getElementById(containerId);
        this.render();
        this.attachEventListeners();
    }

    render() {
        const languages = this.languageHandler.getSupportedLanguages();
        const currentLanguage = this.languageHandler.currentLanguage;

        const selectHtml = `
            <div class="language-selector">
                <select class="form-select" id="language-select" aria-label="Select language">
                    ${languages.map(lang => `
                        <option value="${lang.code}" ${lang.code === currentLanguage ? 'selected' : ''}>
                            ${lang.name}
                        </option>
                    `).join('')}
                </select>
            </div>
        `;

        if (this.container) {
            this.container.innerHTML = selectHtml;
        }
    }

    attachEventListeners() {
        const select = document.getElementById('language-select');
        if (select) {
            select.addEventListener('change', (e) => {
                this.languageHandler.setLanguage(e.target.value);
            });

            // Update selector when language changes
            this.languageHandler.addObserver(event => {
                if (event.type === 'languageChange') {
                    select.value = event.newLang;
                }
            });
        }
    }

    // Add custom styling for RTL languages
    updateStyles() {
        const select = document.getElementById('language-select');
        if (select) {
            select.style.direction = this.languageHandler.getDirection();
            select.style.textAlign = this.languageHandler.isRTL() ? 'right' : 'left';
        }
    }
}

export default LanguageSelector; 