// Entry point for language support system

export { languageConfig, getLanguageConfig } from './config.js';
export { detectLanguage } from './detect.js';
export { switchLanguage } from './switch.js';
export { getDirection, applyTextDirection } from './text-direction.js';

// Dynamically import translations/question banks/personas based on language
export async function loadLanguageResources(lang = 'en') {
  switch (lang) {
    case 'he':
      return Promise.all([
        import('./he/translations.js'),
        import('./he/question-bank.js'),
        import('./he/personas.js'),
      ]).then(([translations, questions, personas]) => ({
        translations: translations.default || translations,
        questions: questions.default || questions,
        personas: personas.default || personas,
      }));

    case 'en':
      return Promise.all([
        import('./en/translations.js'),
      ]).then(([translations]) => ({
        translations: translations.default || translations,
        questions: [],
        personas: {},
      }));

    default:
      return { translations: {}, questions: [], personas: {} };
  }
} 