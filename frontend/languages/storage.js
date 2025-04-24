// Utilities to persist/retrieve language preference

const STORAGE_KEY = 'lang';

export const getStoredLanguage = () =>
  window.sessionStorage.getItem(STORAGE_KEY) || window.localStorage.getItem(STORAGE_KEY);

export const setStoredLanguage = (lang) => {
  window.sessionStorage.setItem(STORAGE_KEY, lang);
  window.localStorage.setItem(STORAGE_KEY, lang);
};

export const clearStoredLanguage = () => {
  window.sessionStorage.removeItem(STORAGE_KEY);
  window.localStorage.removeItem(STORAGE_KEY);
}; 