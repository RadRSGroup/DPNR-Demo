import { languageConfig, getLanguageConfig } from './config.js';
import { loadLanguageResources } from './index.js';
import { setStoredLanguage } from './storage.js';
import { loadFont } from './font-loader.js';
import { applyDirection } from '../rtl.js';

/**
 * Switch application language
 * @param {string} lang - target language key
 * @returns {Promise<void>}
 */
export async function switchLanguage(lang) {
  if (!languageConfig[lang]) {
    console.warn(`Unsupported language: ${lang}`);
    return;
  }

  try {
    // Persist preference
    setStoredLanguage(lang);

    // Load language resources
    const { translations, questions, personas } = await loadLanguageResources(lang);

    // Update global app state (simple event dispatch)
    const eventDetail = { lang, translations, questions, personas };
    window.dispatchEvent(new CustomEvent('languageChange', { detail: eventDetail }));

    // Update document dir and font
    const { rtl, font } = getLanguageConfig(lang);
    await loadFont(font);
    applyDirection(rtl);
    document.documentElement.style.fontFamily = font;
  } catch (error) {
    console.error('Language switch failed', error);
    throw error;
  }
} 