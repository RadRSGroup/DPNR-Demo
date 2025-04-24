import enTranslations from './languages/en/translations.js';

let translations = {};
const fallbackTranslations = enTranslations;

const missingKeys = new Set();

export function setTranslations(obj = {}) {
  translations = obj;
  refreshI18nTexts();
}

export function t(key) {
  if (key in translations) return translations[key];

  // Fallback to English if available
  if (key in fallbackTranslations) {
    if (!missingKeys.has(key)) {
      console.warn(`[i18n] Missing translation for key "${key}" in current language. Using fallback.`);
      missingKeys.add(key);
    }
    return fallbackTranslations[key];
  }

  // Return key itself if missing in fallback as well
  if (!missingKeys.has(key)) {
    console.warn(`[i18n] Missing translation key "${key}" in all languages.`);
    missingKeys.add(key);
  }
  return key;
}

export function refreshI18nTexts() {
  document.querySelectorAll('[data-i18n]').forEach((el) => {
    const key = el.getAttribute('data-i18n');
    if (key) el.textContent = t(key);
  });
}

// Listen for languageChange events from switchLanguage
window.addEventListener('languageChange', (e) => {
  if (e.detail?.translations) {
    setTranslations(e.detail.translations);
  }
}); 