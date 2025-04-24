// Utility functions to detect and apply text direction for mixed content

// Regex covering common RTL ranges (Hebrew, Arabic, etc.)
const rtlCharRegex = /[\u0591-\u07FF\uFB1D-\uFDFD\uFE70-\uFEFC]/;

/**
 * Detect direction of a given string.
 * @param {string} text
 * @returns {'rtl' | 'ltr'}
 */
export function getDirection(text = '') {
  return rtlCharRegex.test(text) ? 'rtl' : 'ltr';
}

/**
 * Apply direction to an element based on text.
 * Adds `dir` attribute, useful for dynamic content blocks.
 * @param {HTMLElement} el
 * @param {string} text
 */
export function applyTextDirection(el, text) {
  if (!el) return;
  const dir = getDirection(text);
  el.setAttribute('dir', dir);
} 