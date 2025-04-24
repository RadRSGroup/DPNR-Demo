// Utility to detect the user's preferred language
// Checks URL parameter (?lang=), session/local storage, and browser settings
// Falls back to 'en' if no supported language is found

import { languageConfig } from './config.js';
import { getStoredLanguage } from './storage.js';

/**
 * Detect the most suitable language for the user.
 * Order of precedence:
 * 1. URL query parameter `?lang=`
 * 2. Session / local storage preference
 * 3. Browser navigator language
 * 4. Default 'en'
 *
 * @returns {string} A language key present in languageConfig
 */
export const detectLanguage = () => {
  // 1. URL param (?lang=he)
  const urlLang = new URLSearchParams(window.location.search).get('lang');
  if (urlLang && languageConfig[urlLang]) {
    return urlLang;
  }

  // 2. Stored preference (sessionStorage, then localStorage)
  const storedLang = getStoredLanguage();
  if (storedLang && languageConfig[storedLang]) {
    return storedLang;
  }

  // 3. Browser language (navigator.language -> 'en-US' -> 'en')
  const browserLang = navigator.language?.split('-')[0];
  if (browserLang && languageConfig[browserLang]) {
    return browserLang;
  }

  // 4. Fallback
  return 'en';
}; 