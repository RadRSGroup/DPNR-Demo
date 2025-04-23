const hebrewQuestionBank = {
    initialSegmentation: {
        Q101: {
            text: "מה הכי מתאר את הגישה שלך לחיים?",
            options: {
                A101: {
                    text: "אני שואף למצוינות ולעשיית דברים בדרך הנכונה",
                    personas: ["upholder"]
                },
                A102: {
                    text: "אני מתמקד בעזרה והתחברות לאחרים",
                    personas: ["giver"]
                },
                A103: {
                    text: "אני שואף להצלחה והכרה",
                    personas: ["driver"]
                },
                A104: {
                    text: "אני מחפש משמעות עמוקה ואותנטיות",
                    personas: ["seeker"]
                },
                A105: {
                    text: "אני מעריך ידע והבנה",
                    personas: ["observer"]
                },
                A106: {
                    text: "אני מתמקד בביטחון והיערכות",
                    personas: ["guardian"]
                },
                A107: {
                    text: "אני מאמץ הרפתקאות ואפשרויות",
                    personas: ["explorer"]
                },
                A108: {
                    text: "אני לוקח אחריות ומגן על מה שחשוב",
                    personas: ["protector"]
                },
                A109: {
                    text: "אני שומר על הרמוניה ושלום",
                    personas: ["harmonizer"]
                }
            },
            allowTextInput: true,
            textInputPlaceholder: "או תאר את גישתך לחיים במילים שלך...",
            textInputMaxLength: 500
        },
        Q102: {
            text: "תאר מצב אחרון שבו הגישה שלך לחיים באה לידי ביטוי בבירור.",
            type: "textarea",
            placeholder: "שתף דוגמה ספציפית שמראה איך אתה בדרך כלל מתמודד עם מצבי חיים...",
            required: true,
            maxLength: 500,
            confidenceWeight: 1.5
        }
    },
    detailedDifferentiation: {
        Q201: {
            text: "כיצד אתה מגיב בדרך כלל לחוקים וציפיות?",
            options: {
                A201: {
                    text: "אני מקפיד לפעול לפיהם ומצפה מאחרים לעשות כך",
                    personas: ["upholder"]
                },
                A202: {
                    text: "אני שואל שאלות ומציית רק אם זה הגיוני בעיניי",
                    personas: ["observer"]
                },
                A203: {
                    text: "אני מציית כדי לשמור על יחסים ולהימנע מעימותים",
                    personas: ["harmonizer"]
                },
                A204: {
                    text: "אני מתנגד להם בדרך כלל ומעדיף לעשות דברים בדרך שלי",
                    personas: ["explorer"]
                },
                A205: {
                    text: "אני מתאים אותם לצרכים שלי תוך שמירה על הרמוניה",
                    personas: ["harmonizer"]
                }
            },
            allowTextInput: true,
            textInputPlaceholder: "תאר מצב ספציפי שבו נאלצת להתמודד עם חוקים או ציפיות...",
            textInputMaxLength: 500
        },
        Q202: {
            text: "שתף החלטה מאתגרת שקיבלת לאחרונה. איך התמודדת איתה?",
            type: "textarea",
            placeholder: "תאר את המצב, תהליך החשיבה שלך והתוצאה...",
            required: true,
            maxLength: 500,
            confidenceWeight: 1.5
        }
    },
    typeConfirmation: {
        Q301: {
            text: "איך אתה מתמודד עם ביקורת?",
            options: {
                A301: {
                    text: "אני לוקח אותה ברצינות ומשתמש בה לשיפור",
                    personas: ["upholder"]
                },
                A302: {
                    text: "אני מנתח אותה כדי לקבוע אם היא תקפה",
                    personas: ["observer"]
                },
                A303: {
                    text: "אני נפגע אבל מנסה להתחשב בדעות של אחרים",
                    personas: ["giver"]
                },
                A304: {
                    text: "אני בדרך כלל מתעלם ממנה אם היא לא תואמת את הערכים שלי",
                    personas: ["explorer"]
                },
                A305: {
                    text: "אני מנסה להבין את נקודת המבט של האדם האחר",
                    personas: ["harmonizer"]
                }
            },
            allowTextInput: true,
            textInputPlaceholder: "תאר פעם שקיבלת ביקורת ואיך הגבת...",
            textInputMaxLength: 500
        },
        Q302: {
            text: "תאר מצב שבו הרגשת הכי אותנטי לעצמך.",
            type: "textarea",
            placeholder: "מה עשית? איך זה התאים לאישיות הבסיסית שלך?",
            required: true,
            maxLength: 500,
            confidenceWeight: 1.5
        }
    },
    wingType: {
        Q401: {
            text: "איזה מהטיפוסים הסמוכים האלה מהדהד אצלך יותר?",
            options: {
                A401: {
                    text: "טיפוס 1: הרפורמטור - עקרוני, תכליתי, בעל שליטה עצמית",
                    personas: ["upholder"]
                },
                A402: {
                    text: "טיפוס 2: העוזר - נדיב, בולט, מנסה לרצות אנשים",
                    personas: ["giver"]
                },
                A403: {
                    text: "טיפוס 3: המגשים - מסתגל, מצטיין, מונע",
                    personas: ["driver"]
                },
                A404: {
                    text: "טיפוס 4: האינדיבידואליסט - אקספרסיבי, דרמטי, מרוכז בעצמו",
                    personas: ["seeker"]
                },
                A405: {
                    text: "טיפוס 5: החוקר - תפיסתי, חדשני, מבודד",
                    personas: ["observer"]
                },
                A406: {
                    text: "טיפוס 6: הנאמן - מעורב, אחראי, חרד",
                    personas: ["guardian"]
                },
                A407: {
                    text: "טיפוס 7: הנלהב - ספונטני, רב-גוני, מפוזר",
                    personas: ["explorer"]
                },
                A408: {
                    text: "טיפוס 8: המאתגר - בטוח בעצמו, החלטי, מתעמת",
                    personas: ["protector"]
                },
                A409: {
                    text: "טיפוס 9: עושה השלום - קולט, מרגיע, שאנן",
                    personas: ["harmonizer"]
                }
            },
            allowTextInput: true,
            textInputPlaceholder: "הסבר למה הטיפוס הזה מהדהד אצלך וספק דוגמאות מחייך...",
            textInputMaxLength: 500
        },
        Q402: {
            text: "תאר מצבים שבהם אתה מבחין בעצמך מתנהג אחרת מהדפוסים הרגילים שלך.",
            type: "textarea",
            placeholder: "מה מעורר את השינויים האלה? איך אתה מרגיש ברגעים האלה?",
            required: true,
            maxLength: 500,
            confidenceWeight: 1.5
        }
    },
    instinctualVariant: {
        Q501: {
            text: "מהו הדחף האינסטינקטיבי העיקרי שלך?",
            options: {
                A501: {
                    text: "שימור עצמי - אני מתמקד בביטחון, משאבים ורווחה פיזית",
                    personas: ["guardian"]
                },
                A502: {
                    text: "חברתי - אני מתמקד בדינמיקות קבוצתיות וקשרים חברתיים",
                    personas: ["giver"]
                },
                A503: {
                    text: "אחד על אחד - אני מתמקד ביחסים אינטימיים וקשרים אישיים",
                    personas: ["protector"]
                }
            },
            allowTextInput: true,
            textInputPlaceholder: "תאר איך הדחף האינסטינקטיבי שלך בא לידי ביטוי בחיי היומיום שלך...",
            textInputMaxLength: 500
        },
        Q502: {
            text: "אילו פעילויות או מצבים גורמים לך להרגיש הכי חי ואנרגטי?",
            type: "textarea",
            placeholder: "תאר חוויות ספציפיות ומה בהן מהדהד אצלך...",
            required: true,
            maxLength: 500,
            confidenceWeight: 1.5
        }
    },
    personalization: {
        Q601: {
            text: "איך אתה מעדיף לקבל משוב?",
            options: {
                A601: {
                    text: "ישיר ובונה, מתמקד בשיפור",
                    personas: ["upholder", "driver"]
                },
                A602: {
                    text: "מאוזן עם חיזוקים חיוביים",
                    personas: ["giver", "harmonizer"]
                },
                A603: {
                    text: "עדין ותומך",
                    personas: ["seeker", "observer"]
                }
            },
            allowTextInput: true,
            textInputPlaceholder: "או תאר את סגנון המשוב המועדף עליך במילים שלך...",
            textInputMaxLength: 500
        },
        Q602: {
            text: "תאר אתגר אחרון שבדק את הצמיחה האישית שלך.",
            type: "textarea",
            placeholder: "איך התמודדת איתו? מה למדת על עצמך?",
            required: true,
            maxLength: 500,
            confidenceWeight: 1.5
        }
    },
    confirmation: {
        Q701: {
            text: "מה התגובה האופיינית שלך ללחץ?",
            options: {
                A701: {
                    text: "אני מכפיל את המשמעת והמבנה",
                    personas: ["upholder"]
                },
                A702: {
                    text: "אני מחפש מידע נוסף כדי להבין את המצב",
                    personas: ["observer"]
                },
                A703: {
                    text: "אני מחפש תמיכה והדרכה מאחרים",
                    personas: ["giver"]
                },
                A704: {
                    text: "אני משתחרר מהמגבלות ומחפש גישות חדשות",
                    personas: ["explorer"]
                },
                A705: {
                    text: "אני מנסה לשמור על איזון והרמוניה",
                    personas: ["harmonizer"]
                }
            },
            allowTextInput: true,
            textInputPlaceholder: "תאר מצב מלחיץ ספציפי ואיך התמודדת איתו...",
            textInputMaxLength: 500
        },
        Q702: {
            text: "מאילו היבטים באישיות שלך אתה הכי גאה?",
            type: "textarea",
            placeholder: "שתף דוגמאות ספציפיות של מתי התכונות האלה שירתו אותך היטב...",
            required: true,
            maxLength: 500,
            confidenceWeight: 1.5
        }
    }
};

// Hebrew-specific text analysis rules
const hebrewTextAnalysis = {
    sentiment: {
        positive: ['טוב', 'נהדר', 'מצוין', 'נפלא', 'מעולה', 'מדהים', 'מרגש', 'מספק', 'מתגמל', 'מעורר השראה'],
        negative: ['רע', 'גרוע', 'קשה', 'מאכזב', 'מתסכל', 'מעייף', 'מטריד', 'מאתגר', 'מעיק', 'מתסכל'],
        neutral: ['רגיל', 'סביר', 'מקובל', 'ממוצע', 'רגיל', 'שגרתי', 'רגיל', 'מקובל', 'מקובל', 'מקובל']
    },
    intensifiers: ['מאוד', 'ביותר', 'לגמרי', 'בהחלט', 'במיוחד', 'ממש', 'באמת', 'בכלל', 'בכלל לא', 'בכלל לא'],
    diminishers: ['קצת', 'במקצת', 'יחסית', 'במידה מסוימת', 'במידה מועטה', 'במידה מוגבלת', 'במידה מועטה', 'במידה מוגבלת', 'במידה מועטה', 'במידה מוגבלת'],
    negators: ['לא', 'אין', 'בלי', 'אל', 'אינני', 'אינך', 'אינכם', 'אינכן', 'איננו', 'אינן'],
    connectors: ['וגם', 'או', 'אבל', 'לכן', 'לפיכך', 'לכן', 'לפיכך', 'לכן', 'לפיכך', 'לכן'],
    timeMarkers: ['עכשיו', 'לפני', 'אחרי', 'בעתיד', 'בעתיד הקרוב', 'בעתיד הרחוק', 'בעתיד הקרוב', 'בעתיד הרחוק', 'בעתיד הקרוב', 'בעתיד הרחוק'],
    frequencyMarkers: ['תמיד', 'לעיתים קרובות', 'לעיתים רחוקות', 'לעיתים', 'לעיתים רחוקות', 'לעיתים', 'לעיתים רחוקות', 'לעיתים', 'לעיתים רחוקות', 'לעיתים'],
    certaintyMarkers: ['בטוח', 'כנראה', 'אולי', 'ייתכן', 'ייתכן', 'ייתכן', 'ייתכן', 'ייתכן', 'ייתכן', 'ייתכן'],
    emotionalMarkers: ['מרגיש', 'חושב', 'מאמין', 'מקווה', 'מקווה', 'מקווה', 'מקווה', 'מקווה', 'מקווה', 'מקווה'],
    actionMarkers: ['עושה', 'מבצע', 'מתכנן', 'מארגן', 'מארגן', 'מארגן', 'מארגן', 'מארגן', 'מארגן', 'מארגן']
};

export { hebrewQuestionBank, hebrewTextAnalysis }; 