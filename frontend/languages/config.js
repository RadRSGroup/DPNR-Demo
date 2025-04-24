// Core language configuration for supported languages
// This structure can be expanded as new languages are added

export const languageConfig = {
  en: {
    locale: 'en',
    rtl: false,
    font: 'Roboto',
  },
  he: {
    locale: 'he',
    rtl: true,
    font: 'Assistant',
  },
};

// Helper to retrieve config for current language
export const getLanguageConfig = (lang) => languageConfig[lang] || languageConfig.en; 