// Simple i18n translator
let translations = {};

export function setTranslations(obj = {}) {
  translations = obj;
  refreshI18nTexts();
}

export function t(key) {
  return translations[key] || key;
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