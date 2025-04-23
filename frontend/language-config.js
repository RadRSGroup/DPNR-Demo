// language-config.js
const languageConfig = {
  he: {
    dir: 'rtl',
    name: 'עברית',
    dateFormat: 'DD/MM/YYYY',
    numeralSystem: 'latn', // Using Latin numerals
    code: 'he'
  },
  en: {
    dir: 'ltr',
    name: 'English',
    dateFormat: 'MM/DD/YYYY',
    numeralSystem: 'latn',
    code: 'en'
  }
};

// Hebrew translations for UI elements
const hebrewTranslations = {
  ui: {
    welcome: 'ברוכים הבאים ל-Core Persona',
    begin: 'התחל הערכה',
    next: 'הבא',
    previous: 'הקודם',
    submit: 'שלח',
    loading: 'טוען...',
    error: 'שגיאה',
    requiredField: 'שדה חובה',
    validation: {
      required: 'אנא ענה על כל השאלות לפני שתמשיך',
      invalidInput: 'קלט לא חוקי',
    },
    phases: {
      registration: 'הרשמה',
      initialSegmentation: 'היכרות ראשונית',
      detailedDifferentiation: 'מה הופך אותך לייחודי?',
      typeConfirmation: 'אישור סוג',
      wingType: 'סוג כנף',
      instinctualVariant: 'וריאנט אינסטינקטיבי',
      personalization: 'התאמה אישית',
      textInput: 'במילים שלי',
      results: 'תוצאות',
    },
    progress: {
      step: 'שלב',
      of: 'מתוך',
    }
  },
  // General
  'general.loading': 'טוען...',
  'general.error': 'שגיאה',
  'general.success': 'הצלחה',
  'general.submit': 'שלח',
  'general.cancel': 'ביטול',
  
  // Persona selection
  'persona.select': 'בחר אישיות',
  'persona.analytical': 'אנליטי',
  'persona.emotional': 'רגשי',
  'persona.creative': 'יצירתי',
  'persona.practical': 'מעשי',
  
  // Questions
  'questions.title': 'שאלות',
  'questions.add': 'הוסף שאלה',
  'questions.remove': 'הסר שאלה',
  'questions.placeholder': 'הקלד את השאלה שלך כאן...',
  
  // Analysis
  'analysis.title': 'ניתוח',
  'analysis.start': 'התחל ניתוח',
  'analysis.stop': 'עצור ניתוח',
  'analysis.results': 'תוצאות ניתוח',
  
  // Results
  'results.title': 'תוצאות',
  'results.download': 'הורד תוצאות',
  'results.clear': 'נקה תוצאות',
  'results.noData': 'אין נתונים להצגה'
};

// Hebrew translations for persona descriptions
const hebrewPersonaDescriptions = {
  upholder: {
    name: "השומר",
    description: "אתה שואף למצוינות ולעשיית דברים בדרך הנכונה. אתה מעריך יושרה, אחריות ובהירות מוסרית.",
    // Add all other persona fields translated to Hebrew...
  },
  // Add translations for all other personas...
  analytical: {
    name: 'אנליטי',
    description: 'מתמקד בעובדות, נתונים, והגיון. מחפש הסברים רציונליים ופתרונות מעשיים.',
    traits: ['לוגי', 'מעשי', 'מפורט', 'אובייקטיבי']
  },
  emotional: {
    name: 'רגשי',
    description: 'מתמקד ברגשות, ערכים, וקשרים אנושיים. מחפש הבנה אמפתית ופתרונות הרמוניים.',
    traits: ['אמפתי', 'אינטואיטיבי', 'חברתי', 'סובייקטיבי']
  },
  creative: {
    name: 'יצירתי',
    description: 'מתמקד בחשיבה מחוץ לקופסה, רעיונות חדשים, ופתרונות מקוריים.',
    traits: ['יצירתי', 'חדשני', 'גמיש', 'מקורי']
  },
  practical: {
    name: 'מעשי',
    description: 'מתמקד בפתרונות מעשיים, יעילות, ותוצאות מיידיות.',
    traits: ['יעיל', 'מעשי', 'תכליתי', 'ממוקד']
  }
};

export { languageConfig, hebrewTranslations, hebrewPersonaDescriptions }; 