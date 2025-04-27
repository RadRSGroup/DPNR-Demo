import express from 'express';
import cookieParser from 'cookie-parser';
import cors from 'cors';
import path from 'path';
import { fileURLToPath } from 'url';

// Load content modules
import enTranslations from '../frontend/languages/en/translations.js';
import heTranslations from '../frontend/languages/he/translations.js';
import hebrewQuestionBank from '../frontend/languages/he/question-bank.js';
import hebrewPersonas from '../frontend/languages/he/personas.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
app.use(cors());
app.use(express.json());
app.use(cookieParser());

const PORT = process.env.PORT || 3001;

function detectLangFromHeader(req) {
  const header = req.headers['accept-language'] || '';
  const lang = header.split(',')[0].split('-')[0];
  return ['he', 'en'].includes(lang) ? lang : 'en';
}

// GET /api/language/detect
app.get('/api/language/detect', (req, res) => {
  const cookieLang = req.cookies.lang;
  const lang = cookieLang && ['he', 'en'].includes(cookieLang) ? cookieLang : detectLangFromHeader(req);
  res.json({ language: lang });
});

// POST /api/language/switch
app.post('/api/language/switch', (req, res) => {
  const { language } = req.body;
  if (!['he', 'en'].includes(language)) {
    return res.status(400).json({ error: 'Unsupported language' });
  }
  res.cookie('lang', language, { maxAge: 365 * 24 * 60 * 60 * 1000 });
  res.json({ success: true });
});

// GET translations
app.get('/api/translations/:language', (req, res) => {
  const { language } = req.params;
  const data = language === 'he' ? heTranslations : enTranslations;
  res.json(data);
});

// GET questions
app.get('/api/questions/:language', (req, res) => {
  const { language } = req.params;
  if (language === 'he') {
    res.json(hebrewQuestionBank);
  } else {
    res.json({});
  }
});

// GET personas
app.get('/api/personas/:language', (req, res) => {
  const { language } = req.params;
  if (language === 'he') {
    res.json(hebrewPersonas);
  } else {
    res.json({});
  }
});

// Start server only when not running in test mode
if (process.env.NODE_ENV !== 'test') {
  app.listen(PORT, () => console.log(`API server listening on port ${PORT}`));
}

export { app }; 