// RTL/LTR layout utility

/**
 * Apply layout direction to the document.
 * Adds or removes a `rtl` class on <body> for scoped styles and sets dir attr.
 * @param {boolean} rtl - true for RTL, false for LTR
 */
export function applyDirection(rtl) {
  const dirValue = rtl ? 'rtl' : 'ltr';
  document.documentElement.dir = dirValue;

  if (rtl) {
    document.body.classList.add('rtl');
  } else {
    document.body.classList.remove('rtl');
  }
} 