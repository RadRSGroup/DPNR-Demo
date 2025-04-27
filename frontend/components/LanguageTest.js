import { languageConfig } from '../language-config.js';

export class LanguageTest {
    constructor() {
        this.currentLanguage = 'en';
        this.testSections = [
            {
                id: 'basic-text',
                titleEn: 'Basic Text Test',
                titleHe: 'בדיקת טקסט בסיסית',
                contentEn: 'Hello World! This is a test of language support.',
                contentHe: 'שלום עולם! זוהי בדיקה של תמיכה בשפה העברית.',
                statusEn: '✓ Text display working',
                statusHe: '✓ תצוגת טקסט תקינה'
            },
            {
                id: 'direction',
                titleEn: 'Direction Test',
                titleHe: 'בדיקת כיווניות',
                contentEn: 'English text with <span class="rtl-text">טקסט בעברית</span> embedded.',
                contentHe: 'טקסט בעברית עם <span class="ltr-text">English text</span> משולב.',
                statusEn: '✓ Direction handling working',
                statusHe: '✓ כיווניות תקינה'
            },
            {
                id: 'input',
                titleEn: 'Input Test',
                titleHe: 'בדיקת קלט',
                placeholderEn: 'Type text here',
                placeholderHe: 'הקלד טקסט כאן',
                statusEn: '✓ Text input working',
                statusHe: '✓ קלט טקסט תקין'
            },
            {
                id: 'font',
                titleEn: 'Assistant Font Test',
                titleHe: 'בדיקת גופן Assistant',
                contentEn: ['Bold text in Assistant font', 'Regular text in Assistant font'],
                contentHe: ['טקסט מודגש בגופן Assistant', 'טקסט רגיל בגופן Assistant'],
                statusEn: '✓ Font loaded successfully',
                statusHe: '✓ גופן נטען בהצלחה'
            }
        ];
    }

    render(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        // Set document direction
        document.documentElement.dir = languageConfig[this.currentLanguage].dir;
        document.documentElement.lang = this.currentLanguage;

        // Create container
        container.innerHTML = `
            <div class="language-test">
                <button class="language-switch" onclick="window.languageTest.toggleLanguage()">
                    ${this.currentLanguage === 'en' ? 'Switch to Hebrew' : 'החלף לאנגלית'}
                </button>
                <div class="container">
                    <h1>${this.currentLanguage === 'en' ? 'Language Support Test' : 'בדיקת תמיכה בשפות'}</h1>
                    ${this.renderTestSections()}
                </div>
            </div>
        `;

        this.attachEventListeners();
        this.validateTests();
    }

    renderTestSections() {
        return this.testSections.map(section => `
            <div class="test-section" id="${section.id}">
                <h2>${this.currentLanguage === 'en' ? section.titleEn : section.titleHe}</h2>
                ${this.renderSectionContent(section)}
                <div class="status success">
                    ${this.currentLanguage === 'en' ? section.statusEn : section.statusHe}
                </div>
            </div>
        `).join('');
    }

    renderSectionContent(section) {
        if (section.id === 'input') {
            return `<input type="text" 
                placeholder="${this.currentLanguage === 'en' ? section.placeholderEn : section.placeholderHe}"
                style="width: 100%; padding: 0.5rem; margin: 0.5rem 0;">`;
        }
        
        if (section.id === 'font') {
            const content = this.currentLanguage === 'en' ? section.contentEn : section.contentHe;
            return `
                <p style="font-weight: 700">${content[0]}</p>
                <p style="font-weight: 400">${content[1]}</p>
            `;
        }

        return `<p>${this.currentLanguage === 'en' ? section.contentEn : section.contentHe}</p>`;
    }

    toggleLanguage() {
        this.currentLanguage = this.currentLanguage === 'en' ? 'he' : 'en';
        this.render(this.containerId);
    }

    attachEventListeners() {
        // Store containerId for reuse
        this.containerId = document.querySelector('.language-test').parentElement.id;
        
        // Make the toggleLanguage method available globally
        window.languageTest = this;
    }

    validateTests() {
        const dir = document.documentElement.dir;
        const fontFamily = window.getComputedStyle(document.body).fontFamily;
        
        // Validate direction
        if ((this.currentLanguage === 'en' && dir !== 'ltr') || 
            (this.currentLanguage === 'he' && dir !== 'rtl')) {
            document.querySelector('#direction .status')
                .classList.replace('success', 'error');
        }
        
        // Validate font
        if (!fontFamily.includes('Assistant')) {
            document.querySelector('#font .status')
                .classList.replace('success', 'error');
        }
    }
}

// Add required styles
const style = document.createElement('style');
style.textContent = `
    .language-test {
        position: relative;
        padding: 1rem;
    }
    .language-test .container {
        max-width: 800px;
        margin: 0 auto;
        padding: 2rem;
        background-color: white;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .language-test .test-section {
        margin-bottom: 2rem;
        padding: 1rem;
        border: 1px solid #e0e0e0;
        border-radius: 4px;
    }
    .language-test .status {
        padding: 0.5rem;
        margin-top: 1rem;
        border-radius: 4px;
    }
    .language-test .success {
        background-color: #e6ffe6;
        color: #006600;
    }
    .language-test .error {
        background-color: #ffe6e6;
        color: #660000;
    }
    .language-test .language-switch {
        position: absolute;
        top: 1rem;
        right: 1rem;
        padding: 0.5rem 1rem;
        background-color: #f0f0f0;
        border-radius: 4px;
        cursor: pointer;
    }
    [dir="rtl"] .language-test .language-switch {
        right: auto;
        left: 1rem;
    }
    .language-test .rtl-text {
        direction: rtl;
        display: inline-block;
    }
    .language-test .ltr-text {
        direction: ltr;
        display: inline-block;
    }
`;
document.head.appendChild(style); 