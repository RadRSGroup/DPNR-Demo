// Simple font loader using the FontFace API

const loadedFonts = new Set();

// Map of font names to URLs (WOFF2 for modern browsers)
const fontSources = {
  Assistant: 'https://fonts.gstatic.com/s/assistant/v16/2sDfZG1Wl4LcnbuKgE0mAxGA.woff2', // Google Fonts
};

/**
 * Load a web font if not already loaded.
 * @param {string} fontName
 * @returns {Promise<void>}
 */
export async function loadFont(fontName) {
  if (!fontName || loadedFonts.has(fontName)) return;

  const src = fontSources[fontName];
  if (!src) {
    // No external source – assume font is already available (system or CSS import)
    loadedFonts.add(fontName);
    return;
  }

  try {
    const fontFace = new FontFace(fontName, `url(${src}) format('woff2')`);
    await fontFace.load();
    document.fonts.add(fontFace);
    loadedFonts.add(fontName);
  } catch (err) {
    console.error(`Failed to load font "${fontName}":`, err);
  }
} 