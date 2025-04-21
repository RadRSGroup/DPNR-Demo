// Add production optimization flags
const IS_PRODUCTION = window.location.hostname !== 'localhost';
const ENABLE_LOGGING = !IS_PRODUCTION;

// Question Bank
const questionBank = {
    initialSegmentation: {
        Q101: {
            text: "What best describes your approach to life?",
            options: {
                A101: {
                    text: "I strive for excellence and doing things the right way",
                    personas: ["upholder"]
                },
                A102: {
                    text: "I focus on helping and connecting with others",
                    personas: ["obliger"]
                },
                A103: {
                    text: "I aim to achieve success and recognition",
                    personas: ["driver"]
                },
                A104: {
                    text: "I seek deep meaning and authenticity",
                    personas: ["seeker"]
                },
                A105: {
                    text: "I value knowledge and understanding",
                    personas: ["observer"]
                },
                A106: {
                    text: "I prioritize security and preparedness",
                    personas: ["guardian"]
                },
                A107: {
                    text: "I embrace adventure and possibilities",
                    personas: ["explorer"]
                },
                A108: {
                    text: "I take charge and protect what matters",
                    personas: ["protector"]
                },
                A109: {
                    text: "I maintain harmony and peace",
                    personas: ["harmonizer"]
                }
            }
        },
        Q102: {
            text: "What is your greatest fear?",
            options: {
                A110: {
                    text: "Being wrong or making mistakes",
                    personas: ["upholder"]
                },
                A111: {
                    text: "Being unloved or unwanted",
                    personas: ["obliger"]
                },
                A112: {
                    text: "Being seen as a failure",
                    personas: ["driver"]
                },
                A113: {
                    text: "Being emotionally abandoned",
                    personas: ["seeker"]
                },
                A114: {
                    text: "Being overwhelmed or depleted",
                    personas: ["observer"]
                },
                A115: {
                    text: "Being unprepared or unsafe",
                    personas: ["guardian"]
                },
                A116: {
                    text: "Being trapped in pain or limitation",
                    personas: ["explorer"]
                },
                A117: {
                    text: "Being controlled or betrayed",
                    personas: ["protector"]
                },
                A118: {
                    text: "Conflict or disconnection",
                    personas: ["harmonizer"]
                }
            }
        }
    },
    detailedDifferentiation: {
        Q201: {
            text: "How do you typically respond to rules and expectations?",
            options: {
                A201: {
                    text: "I follow them strictly and expect others to do the same",
                    personas: ["upholder"]
                },
                A202: {
                    text: "I question them and only follow if they make sense to me",
                    personas: ["questioner"]
                },
                A203: {
                    text: "I follow them to maintain relationships and avoid conflict",
                    personas: ["obliger"]
                },
                A204: {
                    text: "I often resist them and prefer to do things my own way",
                    personas: ["rebel"]
                },
                A205: {
                    text: "I adapt them to fit my needs while maintaining harmony",
                    personas: ["harmonizer"]
                },
                A206: {
                    text: "I analyze them thoroughly before deciding how to proceed",
                    personas: ["observer"]
                },
                A207: {
                    text: "I challenge them if they limit my freedom or growth",
                    personas: ["explorer"]
                },
                A208: {
                    text: "I enforce them when they protect what matters",
                    personas: ["protector"]
                },
                A209: {
                    text: "I use them as guidelines for success and achievement",
                    personas: ["driver"]
                }
            }
        },
        Q202: {
            text: "What is your approach to decision-making?",
            options: {
                A210: {
                    text: "I make decisions based on clear principles and values",
                    personas: ["upholder"]
                },
                A211: {
                    text: "I gather extensive information before making decisions",
                    personas: ["questioner"]
                },
                A212: {
                    text: "I consider how decisions will affect others",
                    personas: ["obliger"]
                },
                A213: {
                    text: "I make decisions based on what feels right in the moment",
                    personas: ["rebel"]
                },
                A214: {
                    text: "I seek consensus and harmony in decision-making",
                    personas: ["harmonizer"]
                },
                A215: {
                    text: "I analyze all possible outcomes before deciding",
                    personas: ["observer"]
                },
                A216: {
                    text: "I make decisions that open up new possibilities",
                    personas: ["explorer"]
                },
                A217: {
                    text: "I make decisive choices that protect what matters",
                    personas: ["protector"]
                },
                A218: {
                    text: "I make decisions that lead to success and achievement",
                    personas: ["driver"]
                }
            }
        }
    },
    typeConfirmation: {
        Q301: {
            text: "How do you handle criticism?",
            options: {
                A301: {
                    text: "I take it seriously and use it to improve",
                    personas: ["upholder"]
                },
                A302: {
                    text: "I analyze it to determine if it's valid",
                    personas: ["questioner"]
                },
                A303: {
                    text: "I feel hurt but try to accommodate others' views",
                    personas: ["obliger"]
                },
                A304: {
                    text: "I often dismiss it if it doesn't align with my values",
                    personas: ["rebel"]
                },
                A305: {
                    text: "I try to understand the other person's perspective",
                    personas: ["harmonizer"]
                },
                A306: {
                    text: "I examine it objectively and learn from it",
                    personas: ["observer"]
                },
                A307: {
                    text: "I use it as motivation to prove myself",
                    personas: ["driver"]
                },
                A308: {
                    text: "I defend my position strongly",
                    personas: ["protector"]
                },
                A309: {
                    text: "I look for the positive aspects in it",
                    personas: ["explorer"]
                }
            }
        }
    },
    wingType: {
        Q401: {
            text: "Which of these adjacent types resonates with you more?",
            options: {
                A401: {
                    text: "Type 1: The Reformer - Principled, purposeful, self-controlled",
                    personas: ["upholder"]
                },
                A402: {
                    text: "Type 2: The Helper - Generous, demonstrative, people-pleasing",
                    personas: ["giver"]
                },
                A403: {
                    text: "Type 3: The Achiever - Adaptable, excelling, driven",
                    personas: ["driver"]
                },
                A404: {
                    text: "Type 4: The Individualist - Expressive, dramatic, self-absorbed",
                    personas: ["seeker"]
                },
                A405: {
                    text: "Type 5: The Investigator - Perceptive, innovative, isolated",
                    personas: ["observer"]
                },
                A406: {
                    text: "Type 6: The Loyalist - Engaging, responsible, anxious",
                    personas: ["guardian"]
                },
                A407: {
                    text: "Type 7: The Enthusiast - Spontaneous, versatile, scattered",
                    personas: ["explorer"]
                },
                A408: {
                    text: "Type 8: The Challenger - Self-confident, decisive, confrontational",
                    personas: ["protector"]
                },
                A409: {
                    text: "Type 9: The Peacemaker - Receptive, reassuring, complacent",
                    personas: ["harmonizer"]
                }
            }
        }
    },
    instinctualVariant: {
        Q501: {
            text: "What is your primary instinctual drive?",
            options: {
                A501: {
                    text: "Self-Preservation - I focus on security, resources, and physical well-being",
                    personas: ["guardian"]
                },
                A502: {
                    text: "Social - I focus on belonging, status, and group dynamics",
                    personas: ["harmonizer"]
                },
                A503: {
                    text: "One-to-One - I focus on intense relationships and personal connections",
                    personas: ["protector"]
                }
            }
        },
        Q502: {
            text: "How do you typically respond to stress?",
            options: {
                A504: {
                    text: "I focus on practical needs and security",
                    personas: ["guardian"]
                },
                A505: {
                    text: "I seek connection and support from others",
                    personas: ["harmonizer"]
                },
                A506: {
                    text: "I become more intense in my relationships",
                    personas: ["protector"]
                }
            }
        }
    },
    personalization: [
        {
            id: "Q601",
            text: "How do you prefer to receive feedback?",
            options: [
                {
                    id: "A601",
                    text: "Direct and constructive, focusing on improvement"
                },
                {
                    id: "A602",
                    text: "Balanced with positive reinforcement"
                },
                {
                    id: "A603",
                    text: "Gentle and supportive"
                }
            ]
        },
        {
            id: "Q602",
            text: "What motivates you most in your work?",
            options: [
                {
                    id: "A604",
                    text: "Achieving excellence and high standards"
                },
                {
                    id: "A605",
                    text: "Making a positive impact on others"
                },
                {
                    id: "A606",
                    text: "Personal growth and development"
                }
            ]
        },
        {
            id: "Q603",
            text: "How do you handle conflict?",
            options: [
                {
                    id: "A607",
                    text: "Address it directly and seek resolution"
                },
                {
                    id: "A608",
                    text: "Look for compromise and harmony"
                },
                {
                    id: "A609",
                    text: "Take time to process before responding"
                }
            ]
        }
    ],
    confirmation: {
        Q401: {
            text: "What is your typical response to stress?",
            options: {
                A401: {
                    text: "I double down on discipline and structure",
                    personas: ["upholder"]
                },
                A402: {
                    text: "I seek more information to understand the situation",
                    personas: ["questioner"]
                },
                A403: {
                    text: "I look to others for support and guidance",
                    personas: ["obliger"]
                },
                A404: {
                    text: "I break free from constraints and seek new approaches",
                    personas: ["rebel"]
                },
                A405: {
                    text: "I try to maintain balance and harmony",
                    personas: ["harmonizer"]
                },
                A406: {
                    text: "I withdraw to analyze and process",
                    personas: ["observer"]
                },
                A407: {
                    text: "I push harder to achieve and succeed",
                    personas: ["driver"]
                },
                A408: {
                    text: "I take control of the situation",
                    personas: ["protector"]
                },
                A409: {
                    text: "I seek new experiences to distract myself",
                    personas: ["explorer"]
                }
            }
        },
        Q402: {
            text: "How do you approach personal growth?",
            options: {
                A410: {
                    text: "I set clear goals and follow structured plans",
                    personas: ["upholder"]
                },
                A411: {
                    text: "I seek to understand the underlying principles",
                    personas: ["questioner"]
                },
                A412: {
                    text: "I grow through relationships and helping others",
                    personas: ["obliger"]
                },
                A413: {
                    text: "I explore new experiences and challenge norms",
                    personas: ["rebel"]
                },
                A414: {
                    text: "I focus on maintaining balance and harmony",
                    personas: ["harmonizer"]
                },
                A415: {
                    text: "I analyze and understand before taking action",
                    personas: ["observer"]
                },
                A416: {
                    text: "I push myself to achieve and succeed",
                    personas: ["driver"]
                },
                A417: {
                    text: "I strengthen my ability to protect and lead",
                    personas: ["protector"]
                },
                A418: {
                    text: "I seek new adventures and possibilities",
                    personas: ["explorer"]
                }
            }
        }
    }
};

// Persona Descriptions
const personas = {
    upholder: {
        name: "The Upholder",
        description: "You strive for excellence and doing things the right way. You value integrity, responsibility, and moral clarity. Your challenge is learning to be proud without guilt and finding balance between high standards and self-compassion.",
        innerWorld: {
            fear: "Being wrong, flawed, or irresponsible",
            desire: "To be good, ethical, and respected",
            limitingBelief: "If I stop being perfect, I'll lose control and disappoint everyone."
        },
        coreValues: ["Integrity", "Responsibility", "Justice", "Self-discipline", "Improvement", "Moral clarity"],
        coreEmotionalNeeds: {
            certainty: "Maintains routines to feel in control",
            significance: "Finds worth through high standards",
            contribution: "Believes her value is tied to improving the world"
        },
        blindSpots: ["Suppressed emotions", "Over-functioning", "Harsh inner critic"],
        aspirations: ["To lead with calm", "Be proud without guilt", "Live with grace"],
        stressVsGrowth: {
            integrity: { stress: "Rigid, moralistic", growth: "Graceful, values-led", outcome: "Tension vs. trust" },
            selfWorth: { stress: "Earned through perfection", growth: "Rooted in presence", outcome: "Shame vs. peace" },
            discipline: { stress: "Used for control", growth: "Creates freedom", outcome: "Burnout vs. balance" }
        },
        boundaries: {
            tendency: "High expectations, but overextends out of guilt",
            growth: "Learns to say no, rest without shame, and accept imperfection"
        },
        lifeDomainImpact: {
            relationships: "Loyal but critical; struggles with emotional softness",
            career: "High performer but risks burnout; over-responsible",
            health: "Somatic tension; difficulty resting",
            lifestyle: "Structured, but lacks play and spontaneity",
            purpose: "Focused on duty; needs space for soul-driven joy"
        },
        potential: {
            capabilities: [
                "Feel proud of your efforts—without the guilt",
                "Set boundaries that allow for rest, not just results",
                "Lead others through example, not pressure",
                "Let go of what's not yours to fix",
                "Feel aligned with your values and your joy"
            ],
            lifeChanges: {
                relationships: "More compassion, less correction. You connect from warmth, not moral high ground",
                career: "You inspire others through calm leadership, not perfectionism",
                health: "You allow space for rest and pleasure—without shame",
                lifestyle: "Your routines become tools for support, not control",
                purpose: "You no longer carry the weight alone—you create peace by embodying it"
            }
        }
    },
    giver: {
        name: "The Giver",
        description: "You focus on helping and connecting with others. You're generous, loyal, and full of heart. Your challenge is learning to receive love without earning it and setting boundaries that deepen intimacy rather than create distance.",
        innerWorld: {
            fear: "Being unloved, unwanted, or forgotten",
            desire: "To feel emotionally close and needed",
            limitingBelief: "If I'm not useful, I won't be loved."
        },
        coreValues: ["Generosity", "Loyalty", "Compassion", "Service", "Belonging", "Emotional intimacy"],
        coreEmotionalNeeds: {
            loveConnection: "Craves emotional closeness",
            significance: "Seeks approval through service",
            contribution: "Feels valued when giving"
        },
        blindSpots: ["Over-gives", "Suppresses own needs"],
        aspirations: ["To be loved without earning it"],
        stressVsGrowth: {
            connection: { stress: "People-pleasing", growth: "Honest closeness", outcome: "Drained vs. deeply nourished" },
            selfWorth: { stress: "Based on being needed", growth: "Rooted in self-acceptance", outcome: "Conditional vs. stable love" },
            service: { stress: "Giving to be liked", growth: "Giving from overflow", outcome: "Resentment vs. joy" }
        },
        boundaries: {
            tendency: "Says yes too often, avoids conflict",
            growth: "Learns to ask for help, speak his needs, and receive"
        },
        lifeDomainImpact: {
            relationships: "Emotionally present but can lose himself in others",
            career: "Excellent in supportive roles; undervalues himself",
            health: "Neglects self-care; burnout risk",
            lifestyle: "Centered on others' needs",
            purpose: "Service-focused, but must learn to serve himself too"
        },
        potential: {
            capabilities: [
                "Say 'no' with love and 'yes' without resentment",
                "Ask for support—and believe you deserve it",
                "Care for others from overflow, not obligation",
                "Set boundaries that deepen intimacy, not create distance",
                "Feel chosen even when you're not 'helping'"
            ],
            lifeChanges: {
                relationships: "Deep, reciprocal connection where you feel emotionally safe",
                career: "You step into your value, knowing your worth goes beyond service",
                health: "You protect your energy and rest—because you matter too",
                lifestyle: "You make room for your needs and dreams, not just others'",
                purpose: "You serve with joy—not to be loved, but because you are love"
            }
        }
    },
    driver: {
        name: "The Driver",
        description: "You aim to achieve success and recognition. You're efficient, ambitious, and goal-oriented. Your challenge is finding worth beyond achievements and building authentic connections without the mask of success.",
        innerWorld: {
            fear: "Being seen as a failure or worthless",
            desire: "To be admired, successful, and valuable",
            limitingBelief: "If I stop achieving, I stop mattering."
        },
        coreValues: ["Excellence", "Achievement", "Efficiency", "Recognition", "Ambition", "Progress"],
        coreEmotionalNeeds: {
            significance: "Defines herself through external success",
            growth: "Obsessed with goals, avoids inner stillness",
            loveConnection: "Struggles with emotional vulnerability"
        },
        blindSpots: ["Identity built on achievement", "Emotional avoidance"],
        aspirations: ["To feel worthy just by being"],
        stressVsGrowth: {
            success: { stress: "External validation", growth: "Purpose-driven success", outcome: "Burnout vs. meaning" },
            image: { stress: "Persona over presence", growth: "Real authenticity", outcome: "Performance vs. connection" },
            motivation: { stress: "Fear of failure", growth: "Joyful drive", outcome: "Overdrive vs. flow" }
        },
        boundaries: {
            tendency: "Overworks, overcommits",
            growth: "Protects her energy, slows down, chooses alignment over approval"
        },
        lifeDomainImpact: {
            relationships: "High-achieving but emotionally distant",
            career: "Ambitious and productive; risks burnout",
            health: "Ignores fatigue and emotional needs",
            lifestyle: "Structured and fast-paced",
            purpose: "Success without soul—until she reconnects inward"
        },
        potential: {
            capabilities: [
                "Succeed on your terms—not someone else's timeline",
                "Feel proud of who you are—not just what you do",
                "Build connection without the mask",
                "Say no to burnout and yes to real fulfillment",
                "Be admired for your authenticity—not just your image"
            ],
            lifeChanges: {
                relationships: "You allow vulnerability—and feel loved for your truth",
                career: "You work with passion, not pressure; purpose replaces performance",
                health: "You notice your limits and rest without guilt",
                lifestyle: "You create space for presence—not just productivity",
                purpose: "You grow from aligned ambition—not the need to prove"
            }
        }
    },
    seeker: {
        name: "The Seeker",
        description: "You seek deep meaning and authenticity. You're creative, sensitive, and emotionally deep. Your challenge is finding stability in your emotional world and expressing yourself without fear of being too much or not enough.",
        innerWorld: {
            fear: "Being emotionally abandoned, unseen, or insignificant",
            desire: "To be deeply known and unique",
            limitingBelief: "If I'm not special, I don't matter."
        },
        coreValues: ["Authenticity", "Depth", "Individuality", "Emotional truth", "Beauty", "Creativity"],
        coreEmotionalNeeds: {
            loveConnection: "Needs emotional resonance, not surface attention",
            significance: "Seeks meaning and depth in everything",
            growth: "Craves personal transformation and emotional truth"
        },
        blindSpots: ["Idealizes pain", "Romanticizes longing", "Withdraws easily"],
        aspirations: ["To feel whole, steady, and seen without performing for it"],
        stressVsGrowth: {
            identity: { stress: "Based on emotional highs/lows", growth: "Based on core essence", outcome: "Disconnection vs. grounded self-expression" },
            connection: { stress: "Seeks intensity, avoids stability", growth: "Builds consistent, mutual intimacy", outcome: "Longing vs. belonging" },
            selfWorth: { stress: "Based on uniqueness", growth: "Rooted in being present and real", outcome: "Comparison vs. inner peace" }
        },
        boundaries: {
            tendency: "Emotionally porous—blends with others or withdraws suddenly",
            strugglesWith: "Oversharing or withholding, protecting their space",
            growth: "Learns to stay present in relationships and protect their energy without isolating"
        },
        lifeDomainImpact: {
            relationships: "Passionate but inconsistent; can feel misunderstood or too intense",
            career: "Needs purpose and beauty in their work; struggles with mundane tasks",
            health: "Mood-driven; may neglect routine or self-care during emotional lows",
            lifestyle: "Craves creative, meaningful spaces but resists too much structure",
            purpose: "Driven to create something authentic that reflects their soul"
        },
        potential: {
            capabilities: [
                "Share your story without needing to dramatize or dim it",
                "Create from wholeness, not just heartbreak",
                "Build deep emotional relationships with safety and consistency",
                "Trust that your presence—not your pain—is what draws people in",
                "Feel steady, seen, and soul-aligned"
            ],
            lifeChanges: {
                relationships: "You experience emotional intimacy without losing yourself",
                career: "You bring creativity into your work—without relying on chaos for inspiration",
                health: "You ride emotional waves without drowning; self-care becomes a priority",
                lifestyle: "You live meaningfully, with just enough structure to support your passion",
                purpose: "You create from authenticity—not intensity. And it's even more powerful."
            }
        }
    },
    observer: {
        name: "The Observer",
        description: "You value knowledge and understanding. You're thoughtful, private, and analytical. Your challenge is engaging with others without emotional exhaustion and sharing your wisdom while maintaining healthy boundaries.",
        innerWorld: {
            fear: "Being depleted, invaded, or emotionally exposed",
            desire: "To be capable, self-sufficient, and in control",
            limitingBelief: "If I let people in, I'll lose myself."
        },
        coreValues: ["Knowledge", "Autonomy", "Competence", "Objectivity", "Privacy", "Clarity"],
        coreEmotionalNeeds: {
            certainty: "Feels safe through information and solitude",
            growth: "Seeks mastery and understanding",
            significance: "Feels worthy through competence and clarity"
        },
        blindSpots: ["Emotionally avoidant", "Over-isolates", "Intellectualizes everything"],
        aspirations: ["To live from wisdom—not just theory—and experience connection without fear"],
        stressVsGrowth: {
            boundaries: { stress: "Becomes emotionally walled off", growth: "Sets thoughtful, clear limits", outcome: "Isolated vs. respected and connected" },
            knowledge: { stress: "Hoards for protection", growth: "Shares for impact", outcome: "Invisible vs. valued expert" },
            emotionalSafety: { stress: "Avoids feelings entirely", growth: "Chooses when and how to open up", outcome: "Frozen vs. free to engage deeply" }
        },
        boundaries: {
            tendency: "Very strong with physical and time boundaries",
            strugglesWith: "Emotional vulnerability, asking for help, being 'seen'",
            growth: "Learns to share gradually, set boundaries that allow connection—not just block intrusion"
        },
        lifeDomainImpact: {
            relationships: "Loyal and insightful but distant; may struggle to express needs",
            career: "Excels in solo work, research, strategy; avoids team conflict",
            health: "Disconnects from body; may neglect nutrition, rest, or emotion",
            lifestyle: "Structured and minimalist; prioritizes control and quiet",
            purpose: "Feels purposeful when knowledge is shared and contributes meaningfully"
        },
        potential: {
            capabilities: [
                "Build trust without giving up your independence",
                "Engage with others without emotional exhaustion",
                "Move from information to transformation",
                "Share your insight—and watch it impact others",
                "Feel emotionally safe and present in the world"
            ],
            lifeChanges: {
                relationships: "Trust-based, spacious relationships where you feel safe and seen",
                career: "Fulfillment by sharing your expertise—not just collecting it",
                health: "Greater mind-body connection, rest, and emotional attunement",
                lifestyle: "A grounded balance of solitude and meaningful interaction",
                purpose: "You stop just preparing—you start participating. And it's powerful."
            }
        }
    },
    guardian: {
        name: "The Guardian",
        description: "You prioritize security and preparedness. You're loyal, vigilant, and deeply committed to those you trust. Your challenge is finding inner stability and acting with confidence without constant second-guessing.",
        innerWorld: {
            fear: "Being unsafe, betrayed, or left unprepared",
            desire: "To feel secure, supported, and grounded",
            limitingBelief: "If I'm not on guard, I'll get blindsided."
        },
        coreValues: ["Loyalty", "Security", "Preparedness", "Support", "Courage", "Honesty"],
        coreEmotionalNeeds: {
            certainty: "Seeks structure and predictability to feel safe",
            loveConnection: "Deeply values dependable, committed relationships",
            contribution: "Protects, supports, and shows up with consistency"
        },
        blindSpots: ["Over-reliance on authority", "Fear-based decisions", "Self-doubt"],
        aspirations: ["To trust her inner compass and act with quiet confidence"],
        stressVsGrowth: {
            safety: { stress: "Constant vigilance", growth: "Inner stability", outcome: "Overwhelm vs. grounded courage" },
            trust: { stress: "Seeks it externally", growth: "Builds it within", outcome: "Doubt vs. discernment" },
            confidence: { stress: "Paralyzed by fear", growth: "Anchored in action", outcome: "Anxiety loops vs. empowered decision-making" }
        },
        boundaries: {
            tendency: "Holds to external rules more than inner needs",
            strugglesWith: "Asserting herself without reassurance, saying no to people she fears losing",
            growth: "Learns to set boundaries that reflect her own values—not just others' expectations"
        },
        lifeDomainImpact: {
            relationships: "Loyal and deeply supportive, but may become dependent or testing of others' loyalty",
            career: "Reliable, detail-oriented, and prepared—but may struggle to lead or take risks",
            health: "Mental tension and anxiety can lead to fatigue or physical stress",
            lifestyle: "Structured and cautious; resists change unless fully 'ready'",
            purpose: "Feels most purposeful when protecting or supporting others—but needs to lead herself too"
        },
        potential: {
            capabilities: [
                "Make confident decisions without overanalyzing",
                "Trust your gut—even without all the data",
                "Set boundaries without fear of disconnection",
                "Create peace without overplanning",
                "Feel secure—because it lives inside you now"
            ],
            lifeChanges: {
                relationships: "Secure, mutual trust replaces testing and fear",
                career: "You take initiative and step into leadership",
                health: "You calm your nervous system and gain emotional resilience",
                lifestyle: "You live with more flexibility and freedom from fear",
                purpose: "You become a calming force—for yourself and others"
            }
        }
    },
    explorer: {
        name: "The Explorer",
        description: "You embrace adventure and possibilities. You're enthusiastic, optimistic, and full of energy. Your challenge is finding joy in presence rather than constant stimulation and facing discomfort without escaping.",
        innerWorld: {
            fear: "Being trapped in emotional pain, boredom, or limitation",
            desire: "To feel free, fulfilled, and alive",
            limitingBelief: "If I slow down, I'll get stuck in something I can't handle."
        },
        coreValues: ["Freedom", "Adventure", "Optimism", "Flexibility", "Enthusiasm", "Possibility"],
        coreEmotionalNeeds: {
            variety: "Thrives on stimulation, novelty, and inspiration",
            growth: "Seeks expansion, but avoids emotional discomfort",
            loveConnection: "Craves joyful experiences with others, but can avoid deeper emotional intimacy"
        },
        blindSpots: ["Escapes discomfort", "Over-commits", "Fears sitting with pain"],
        aspirations: ["To find joy in presence—not just distraction—and let life feel full, even in quiet moments"],
        stressVsGrowth: {
            joy: { stress: "Used to avoid reality", growth: "Anchored in the present", outcome: "Superficial highs vs. lasting fulfillment" },
            freedom: { stress: "Avoids pain and limits", growth: "Embraces choice and presence", outcome: "Scattered vs. grounded and vibrant" },
            connection: { stress: "Seeks excitement", growth: "Builds emotional intimacy", outcome: "Fun but distant vs. safe and open" }
        },
        boundaries: {
            tendency: "Avoids limitations or anything that feels restrictive",
            strugglesWith: "Saying no to pleasure, slowing down, sitting with emotional truth",
            growth: "Learns that boundaries create more freedom—not less—and that stillness can be safe"
        },
        lifeDomainImpact: {
            relationships: "Fun-loving and generous, but can become avoidant or emotionally inconsistent",
            career: "Creative, visionary, and energetic—but risks distraction or unfinished plans",
            health: "May ignore stress signals; avoids downtime or difficult emotions",
            lifestyle: "Fast-paced and exciting, but often lacks rest or rooted structure",
            purpose: "Feels fulfilled when he creates joy and stays present through the full range of life"
        },
        potential: {
            capabilities: [
                "Embrace joy without running from discomfort",
                "Slow down and savor your life—not just escape it",
                "Create meaningful adventure—rather than constant stimulation",
                "Build deep, safe connections without fear of boredom",
                "Feel free not just in motion, but in stillness too"
            ],
            lifeChanges: {
                relationships: "Emotional depth joins excitement—real intimacy forms",
                career: "You finish what you start, build purpose into creativity",
                health: "Energy becomes sustainable; nervous system settles",
                lifestyle: "Life becomes full and focused—not just busy",
                purpose: "You become a bright, grounded force—living the full range of life with courage and joy"
            }
        }
    },
    protector: {
        name: "The Protector",
        description: "You take charge and protect what matters. You're strong, direct, and full of energy. Your challenge is leading with compassion and allowing vulnerability to coexist with your strength.",
        innerWorld: {
            fear: "Being controlled, betrayed, or emotionally weak",
            desire: "To feel strong, independent, and respected",
            limitingBelief: "If I'm not strong, I'll be hurt."
        },
        coreValues: ["Strength", "Justice", "Protection", "Leadership", "Autonomy", "Directness"],
        coreEmotionalNeeds: {
            certainty: "Needs to feel in control to feel safe",
            significance: "Values strength, influence, and honesty",
            loveConnection: "Deeply loyal, but cautious about vulnerability"
        },
        blindSpots: ["Can become controlling", "Intimidating", "Emotionally guarded"],
        aspirations: ["To lead from compassion", "Trust others", "Allow softness to coexist with power"],
        stressVsGrowth: {
            strength: { stress: "Used to dominate", growth: "Used to empower", outcome: "Fear-based control vs. grounded leadership" },
            vulnerability: { stress: "Rejected and feared", growth: "Welcomed with discernment", outcome: "Isolation vs. connection" },
            power: { stress: "Protects by force", growth: "Protects through presence", outcome: "Intimidation vs. inspiration" }
        },
        boundaries: {
            tendency: "Strong external boundaries; few internal or emotional ones",
            strugglesWith: "Letting people in, releasing control, admitting emotional needs",
            growth: "Learns that healthy boundaries include receptivity, softness, and sharing leadership"
        },
        lifeDomainImpact: {
            relationships: "Protective and loyal, but may dominate or withhold vulnerability",
            career: "Takes initiative, excels in leadership, but can bulldoze or micromanage",
            health: "May override physical or emotional signs in pursuit of control",
            lifestyle: "Structured, intense, focused; needs room for relaxation and reflection",
            purpose: "Feels fulfilled when using power to uplift others—not just to defend"
        },
        potential: {
            capabilities: [
                "Trust others without losing control",
                "Let down your guard and feel more free",
                "Use your energy to build—not just protect",
                "Inspire people through truth and vulnerability",
                "Experience love that doesn't require defense"
            ],
            lifeChanges: {
                relationships: "Deep loyalty transforms into emotional intimacy",
                career: "You empower, not overpower—become a respected force for good",
                health: "You slow down, connect to your body, and allow softness",
                lifestyle: "Intensity becomes purposeful—not reactive",
                purpose: "You become a grounded leader who protects through love, not just force"
            }
        }
    },
    harmonizer: {
        name: "The Harmonizer",
        description: "You maintain harmony and peace. You're calm, kind, and easy to be around. Your challenge is speaking up and taking space while maintaining your natural ability to create harmony.",
        innerWorld: {
            fear: "Conflict, disconnection, or being overlooked",
            desire: "To feel at peace, connected, and in harmony",
            limitingBelief: "If I take up space, I'll create conflict or lose connection."
        },
        coreValues: ["Peace", "Harmony", "Acceptance", "Stability", "Empathy", "Unity"],
        coreEmotionalNeeds: {
            certainty: "Seeks routine and comfort to avoid chaos",
            loveConnection: "Craves belonging—but often stays silent to keep it",
            growth: "Desires personal expression but fears disrupting harmony"
        },
        blindSpots: ["Self-forgetting", "Emotional numbness", "Over-accommodating"],
        aspirations: ["To show up with clarity, assertiveness, and presence—and feel fully alive in her own life"],
        stressVsGrowth: {
            peace: { stress: "Avoids conflict, suppresses self", growth: "Brings calm through engagement", outcome: "Passivity vs. powerful presence" },
            identity: { stress: "Blends into others", growth: "Claims her truth", outcome: "Lost in indecision vs. inner alignment" },
            energy: { stress: "Withdraws, procrastinates", growth: "Focuses and commits", outcome: "Numbness vs. energized clarity" }
        },
        boundaries: {
            tendency: "Fears saying no; avoids direct conflict",
            strugglesWith: "Prioritizing her needs, stating opinions, taking up space",
            growth: "Learns that clear boundaries create real peace—and that her needs matter too"
        },
        lifeDomainImpact: {
            relationships: "Warm and dependable, but may become passive or conflict-avoidant",
            career: "Reliable and steady; may go unnoticed or resist leadership roles",
            health: "May ignore signals from her body, zone out or disengage",
            lifestyle: "Routine-based, comfortable, but can lack intention or excitement",
            purpose: "Longs for deeper fulfillment, but needs clarity and direction to claim it"
        },
        potential: {
            capabilities: [
                "Make decisions that reflect your truth",
                "Speak with clarity and confidence",
                "Prioritize your goals without guilt",
                "Build peace through honesty—not avoidance",
                "Feel alive, focused, and connected to your purpose"
            ],
            lifeChanges: {
                relationships: "You become known and respected—not just liked",
                career: "You step forward, lead when needed, and own your impact",
                health: "You listen to your body and reclaim energy and motivation",
                lifestyle: "You move from autopilot to intentional living",
                purpose: "You stop floating—you start shaping your life with direction and presence"
            }
        }
    }
};

// Scoring Logic
// Debug logging utility
function debugScoring(phase, data, level = 'info') {
    if (!ENABLE_LOGGING) return;
    
    const timestamp = new Date().toISOString();
    const prefix = `[${timestamp}] Scoring Debug - ${phase}`;
    
    console.group(prefix);
    if (level === 'error') {
        console.error(JSON.stringify(data, null, 2));
    } else if (level === 'warn') {
        console.warn(JSON.stringify(data, null, 2));
    } else {
        console.log(JSON.stringify(data, null, 2));
    }
    console.groupEnd();
}

// Constants for scoring
const SCORING_WEIGHTS = {
    initialSegmentation: 0.25,  // 25% weight
    detailedDifferentiation: 0.35,  // 35% weight
    typeConfirmation: 0.25,  // 25% weight
    confirmation: 0.15  // 15% weight
};

// Persona weights from rules
const PERSONA_WEIGHTS = {
    upholder: 1.2,
    giver: 1.1,
    driver: 1.2,
    seeker: 1.0,
    observer: 1.1,
    guardian: 1.2,
    explorer: 1.0,
    protector: 1.2,
    harmonizer: 1.1
};

// Custom error types for scoring
class ScoringError extends Error {
    constructor(message, phase, details = {}) {
        super(message);
        this.name = 'ScoringError';
        this.phase = phase;
        this.details = details;
    }
}

class ValidationError extends Error {
    constructor(message, field, value) {
        super(message);
        this.name = 'ValidationError';
        this.field = field;
        this.value = value;
    }
}

// Memory management
const memoryManager = {
    optimize: function(data) {
        // Create a deep copy of the data
        const optimized = JSON.parse(JSON.stringify(data));
        
        // Clean up any circular references
        this.cleanup();
        
        return optimized;
    },
    
    cleanup: function() {
        // Clear any performance marks if available
        if (window.performance && typeof window.performance.clearMarks === 'function') {
            try {
                window.performance.clearMarks();
            } catch (e) {
                console.warn('Could not clear performance marks:', e);
            }
        }
        
        if (window.performance && typeof window.performance.clearMeasures === 'function') {
            try {
                window.performance.clearMeasures();
            } catch (e) {
                console.warn('Could not clear performance measures:', e);
            }
        }
        
        // Suggest garbage collection
        this.suggestGC();
    },
    
    suggestGC: function() {
        if (window.gc) {
            window.gc();
        } else if (window.performance && window.performance.memory) {
            // If we're using a lot of memory, try to trigger GC
            if (window.performance.memory.usedJSHeapSize > 100000000) { // 100MB
                try {
                    // Try to force garbage collection
                    const arr = new Array(1000000);
                    arr = null;
                } catch (e) {
                    console.warn('Could not trigger garbage collection');
                }
            }
        }
    }
};

function calculatePersonaScore(answers) {
    performance.start('calculatePersonaScore');
    try {
        debugScoring('Start', {
            message: 'Starting persona score calculation',
            answersReceived: Object.keys(answers)
        });

        // Clean up any previous performance marks
        memoryManager.cleanup();
        
        // Optimize input data
        const optimizedAnswers = memoryManager.optimize(answers);
        
        debugScoring('Input Validation', {
            message: 'Validating input data',
            optimizedAnswers: optimizedAnswers
        });

        // Initialize scores for all personas
        const rawScores = {
            upholder: 0,
            giver: 0,
            driver: 0,
            seeker: 0,
            observer: 0,
            guardian: 0,
            explorer: 0,
            protector: 0,
            harmonizer: 0,
            questioner: 0,
            obliger: 0,
            rebel: 0
        };

        // Process each phase with appropriate weights
        const phaseWeights = {
            'initial-segmentation': 0.3,
            'detailed-differentiation': 0.25,
            'type-confirmation': 0.2,
            'wing-type': 0.1,
            'instinctual-variant': 0.1,
            'confirmation': 0.05
        };

        // Track total possible points
        let totalPossiblePoints = 0;
        let totalEarnedPoints = 0;

        // Process each phase
        Object.entries(optimizedAnswers).forEach(([phase, phaseAnswers]) => {
            if (!phaseWeights[phase]) return; // Skip phases without weights
            
            const phaseWeight = phaseWeights[phase];
            const questionsInPhase = Object.keys(phaseAnswers).length;
            
            // Calculate points per answer in this phase
            const pointsPerAnswer = (phaseWeight * 100) / questionsInPhase;
            totalPossiblePoints += phaseWeight * 100;

            Object.entries(phaseAnswers).forEach(([questionId, answerIds]) => {
                const answerArray = Array.isArray(answerIds) ? answerIds : [answerIds];
                answerArray.forEach(answerId => {
                    const persona = answerToPersona[answerId];
                    if (persona) {
                        // Add score based on phase weight and points per answer
                        rawScores[persona] += pointsPerAnswer;
                        totalEarnedPoints += pointsPerAnswer;
                    }
                });
            });
        });

        // Calculate final scores with proper normalization
        const finalScores = {};
        let maxScore = 0;

        // First pass: calculate raw percentages and find max score
        Object.entries(rawScores).forEach(([persona, score]) => {
            if (score > 0) {
                const percentage = (score / totalEarnedPoints) * 100;
                finalScores[persona] = percentage;
                maxScore = Math.max(maxScore, percentage);
            }
        });

        // Second pass: normalize scores to prevent 100% results
        Object.keys(finalScores).forEach(persona => {
            // Scale down scores to prevent 100% results
            finalScores[persona] = Math.round((finalScores[persona] / maxScore) * 90);
        });

        debugScoring('Final Scores', {
            message: 'Calculated final scores',
            scores: finalScores,
            totalPossiblePoints,
            totalEarnedPoints
        });

        return finalScores;
    } catch (error) {
        debugScoring('Error', {
            error: error.message,
            stack: error.stack
        }, 'error');
        throw error;
    } finally {
        performance.end('calculatePersonaScore');
    }
}

// Modify state management
const createState = () => ({
    currentPhase: 'registration',
    answers: {},
    startTime: null,
    phaseTimes: {},
    interactionCounts: {},
    confidenceScores: {},
    cleanup: function() {
        this.answers = {};
        this.phaseTimes = {};
        this.interactionCounts = {};
        this.confidenceScores = {};
    }
});

// Create state instance
let state = createState();

// Add state management utilities
const stateManager = {
    saveState: function() {
        try {
            const serializedState = JSON.stringify(state);
            sessionStorage.setItem('personaState', serializedState);
        } catch (error) {
            console.error('Error saving state:', error);
        }
    },
    
    loadState: function() {
        try {
            const savedState = sessionStorage.getItem('personaState');
            if (savedState) {
                const parsedState = JSON.parse(savedState);
                state = { ...createState(), ...parsedState };
            }
        } catch (error) {
            console.error('Error loading state:', error);
            state = createState();
        }
    },
    
    clearState: function() {
        try {
            sessionStorage.removeItem('personaState');
            state = createState();
        } catch (error) {
            console.error('Error clearing state:', error);
        }
    }
};

// Modify metrics tracking to use more efficient data structures
const metrics = {
    startTimer: function(phase) {
        performance.start(`timer_${phase}`);
        state.phaseTimes[phase] = {
            start: Date.now(),
            end: null
        };
    },
    
    endTimer: function(phase) {
        if (state.phaseTimes[phase]) {
            state.phaseTimes[phase].end = Date.now();
            performance.end(`timer_${phase}`);
            // Save state after significant changes
            stateManager.saveState();
        }
    },
    
    recordInteraction: function(phase) {
        state.interactionCounts[phase] = (state.interactionCounts[phase] || 0) + 1;
        // Don't save state on every interaction to improve performance
        if (state.interactionCounts[phase] % 5 === 0) {
            stateManager.saveState();
        }
    },
    
    calculateConfidence: function(phase) {
        performance.start(`confidence_${phase}`);
        try {
            const phaseAnswers = state.answers[phase] || {};
            const totalQuestions = Object.keys(phaseAnswers).length;
            if (totalQuestions === 0) return 0;
            
            // Calculate confidence based on number of answers per question
            let totalAnswers = 0;
            let answeredQuestions = 0;
            
            Object.values(phaseAnswers).forEach(answers => {
                if (answers.length > 0) {
                    answeredQuestions++;
                    totalAnswers += answers.length;
                }
            });
            
            // Confidence is based on:
            // 1. Percentage of questions answered (50% weight)
            // 2. Average number of answers per question (50% weight)
            const answerRate = answeredQuestions / totalQuestions;
            const avgAnswersPerQuestion = totalAnswers / answeredQuestions;
            
            // Normalize avgAnswersPerQuestion to 0-1 range (assuming max 3 answers per question)
            const normalizedAvgAnswers = Math.min(avgAnswersPerQuestion / 3, 1);
            
            // Calculate final confidence score
            const confidenceScore = Math.round((answerRate * 0.5 + normalizedAvgAnswers * 0.5) * 100);
            state.confidenceScores[phase] = confidenceScore;
            
            return confidenceScore;
        } finally {
            performance.end(`confidence_${phase}`);
        }
    }
};

// Modify performance monitoring for production
const performance = {
    marks: {},
    start: function(label) {
        if (ENABLE_LOGGING) {
            this.marks[label] = {
                start: Date.now(),
                memory: window.performance.memory ? {
                    usedJSHeapSize: window.performance.memory.usedJSHeapSize,
                    totalJSHeapSize: window.performance.memory.totalJSHeapSize
                } : null
            };
            console.log(`Starting ${label}`);
        }
    },
    end: function(label) {
        if (ENABLE_LOGGING && this.marks[label]) {
            this.marks[label].end = Date.now();
            const duration = this.marks[label].end - this.marks[label].start;
            console.log(`${label} took ${duration}ms`);
            
            // Log memory usage if available
            if (window.performance.memory && this.marks[label].memory) {
                const memoryDiff = {
                    usedHeap: (window.performance.memory.usedJSHeapSize - this.marks[label].memory.usedJSHeapSize) / 1048576,
                    totalHeap: (window.performance.memory.totalJSHeapSize - this.marks[label].memory.totalJSHeapSize) / 1048576
                };
                console.log(`Memory impact for ${label}: Used: ${memoryDiff.usedHeap.toFixed(2)}MB, Total: ${memoryDiff.totalHeap.toFixed(2)}MB`);
            }
            
            if (duration > 100) {
                console.warn(`Performance warning: ${label} took longer than 100ms`);
            }
            
            // Cleanup mark to prevent memory leaks
            delete this.marks[label];
        }
    }
};

// UI Management
const ui = {
    showPhase: function(phase) {
        performance.start('showPhase');
        console.log('Showing phase:', phase);
        
        try {
            // Cleanup previous phase
            const phases = document.querySelectorAll('.phase');
            phases.forEach(el => {
                if (el.classList.contains('active')) {
                    const prevPhase = el.id.replace('-phase', '');
                    console.log('Cleaning up phase:', prevPhase);
                    cleanup.removeEventListeners(prevPhase);
                }
                el.classList.remove('active');
            });

            // Show new phase
            const phaseElement = document.getElementById(`${phase}-phase`);
            if (!phaseElement) {
                console.error('Phase element not found:', phase);
                return;
            }
            
            phaseElement.classList.add('active');
            metrics.startTimer(phase);
            
            // Use event delegation for question containers
            if (phase !== 'results' && phase !== 'metrics-dashboard') {
                performance.start('setupQuestionContainer');
                const questionContainer = document.getElementById(`${phase}-questions`);
                if (questionContainer) {
                    // Remove existing event listeners
                    const newContainer = questionContainer.cloneNode(true);
                    questionContainer.parentNode.replaceChild(newContainer, questionContainer);
                    
                    newContainer.addEventListener('change', (e) => {
                        if (e.target.matches('input[type="radio"]')) {
                            metrics.recordInteraction(phase);
                        }
                    });
                }
                performance.end('setupQuestionContainer');
            }
            
            // Phase-specific rendering
            console.log('Rendering phase:', phase);
            performance.start('renderPhase');
            
            switch(phase) {
                case 'detailed-differentiation':
                    const initialAnswers = state.answers['initial-segmentation'] || {};
                    let persona = 'upholder';
                    const answerToPersona = {
                        'A101': 'upholder',
                        'A102': 'giver',
                        'A103': 'driver',
                        'A104': 'seeker',
                        'A105': 'observer',
                        'A106': 'guardian',
                        'A107': 'explorer',
                        'A108': 'protector',
                        'A109': 'harmonizer'
                    };
                    if (initialAnswers['qQ101'] && answerToPersona[initialAnswers['qQ101']]) {
                        persona = answerToPersona[initialAnswers['qQ101']];
                    }
                    this.renderDetailedDifferentiation(persona);
                    break;
                case 'initial-segmentation':
                    this.renderQuestions(phase, questionBank.initialSegmentation);
                    break;
                case 'type-confirmation':
                    this.renderQuestions(phase, questionBank.typeConfirmation);
                    break;
                case 'wing-type':
                    if (!questionBank.wingType || !questionBank.wingType.Q401) {
                        console.error('Wing type questions not properly initialized');
                        return;
                    }
                    this.renderWingType();
                    break;
                case 'instinctual-variant':
                    if (!questionBank.instinctualVariant) {
                        console.error('Instinctual variant questions not properly initialized');
                        return;
                    }
                    this.renderQuestions(phase, questionBank.instinctualVariant);
                    break;
                case 'personalization':
                    this.renderPersonalization();
                    break;
                case 'confirmation':
                    this.renderQuestions(phase, questionBank.confirmation);
                    break;
            }
            
            performance.end('renderPhase');
            
        } catch (error) {
            console.error('Error in showPhase:', error);
            // Show error message to user
            const container = document.getElementById(`${phase}-questions`);
            if (container) {
                container.innerHTML = `
                    <div class="alert alert-danger">
                        <h4>Error Loading Questions</h4>
                        <p>There was a problem loading this section. Please try refreshing the page.</p>
                        <button class="btn btn-outline-danger" onclick="location.reload()">Refresh Page</button>
                    </div>
                `;
            }
        }
        
        performance.end('showPhase');
    },
    
    renderDetailedDifferentiation: function(persona) {
        const container = document.getElementById('detailed-differentiation-questions');
        if (!container) {
            console.error('Container not found');
            return;
        }
        container.innerHTML = '';
        
        // Get questions from the new structure
        const questions = questionBank.detailedDifferentiation;
        if (!questions) {
            console.error('No questions found for detailed differentiation');
            return;
        }
        
        // Create document fragment for better performance
        const fragment = document.createDocumentFragment();
        
        // Add questions
        Object.entries(questions).forEach(([questionId, question], index) => {
            const questionEl = document.createElement('div');
            questionEl.className = 'card mb-3';
            
            // Build options HTML string for better performance
            const optionsHtml = Object.entries(question.options).map(([optionId, option]) => `
                <div class="form-check">
                    <input class="form-check-input" type="checkbox" 
                        name="q${questionId}[]" 
                        id="${optionId}" 
                        value="${optionId}">
                    <label class="form-check-label" for="${optionId}">
                        ${option.text}
                    </label>
                </div>
            `).join('');
            
            questionEl.innerHTML = `
                <div class="card-body">
                    <h5 class="card-title">Question ${index + 1}</h5>
                    <p class="card-text">${question.text}</p>
                    <div class="form-group">${optionsHtml}</div>
                </div>
            `;
            fragment.appendChild(questionEl);
        });
        
        // Add next button
        const nextButton = document.createElement('button');
        nextButton.className = 'btn btn-primary mt-3';
        nextButton.textContent = 'Next';
        nextButton.onclick = () => this.validateAndProceed('detailed-differentiation');
        fragment.appendChild(nextButton);
        
        // Add validation alert
        const validationAlert = document.createElement('div');
        validationAlert.id = 'validation-alert-detailed-differentiation';
        validationAlert.className = 'alert alert-danger d-none mt-3';
        validationAlert.textContent = 'Please answer all questions before proceeding.';
        fragment.appendChild(validationAlert);
        
        // Update container
        container.appendChild(fragment);
    },
    
    renderWingType: function() {
        const container = document.getElementById('wing-type-questions');
        if (!container) {
            console.error('Wing type container not found');
            return;
        }
        container.innerHTML = '';
        
        // Determine primary type from previous answers
        const primaryType = this.determinePrimaryType();
        if (!primaryType) {
            console.error('Could not determine primary type');
            return;
        }
        
        // Get adjacent types
        const adjacentTypes = this.getAdjacentTypes(primaryType);
        if (!adjacentTypes || adjacentTypes.length === 0) {
            console.error('Could not determine adjacent types');
            return;
        }
        
        // Create a copy of the wing type question
        const wingTypeQuestion = JSON.parse(JSON.stringify(questionBank.wingType.Q401));
        if (!wingTypeQuestion || !wingTypeQuestion.options) {
            console.error('Invalid wing type question structure');
            return;
        }
        
        // Filter options to only show adjacent types
        const filteredOptions = {};
        Object.entries(wingTypeQuestion.options).forEach(([key, option]) => {
            if (!option || !option.text) {
                console.error('Invalid option structure:', option);
                return;
            }
            const typeNumber = parseInt(key.replace('A40', ''));
            if (adjacentTypes.includes(typeNumber)) {
                filteredOptions[key] = option;
            }
        });
        
        if (Object.keys(filteredOptions).length === 0) {
            console.error('No valid options found for wing type');
            return;
        }
        
        wingTypeQuestion.options = filteredOptions;
        
        // Render the filtered question
        this.renderQuestions('wing-type', { Q401: wingTypeQuestion });
    },
    
    determinePrimaryType: function() {
        // Get answers from initial segmentation and type confirmation phases
        const initialAnswers = state.answers['initial-segmentation'] || {};
        const confirmationAnswers = state.answers['type-confirmation'] || {};
        
        // Map of answer IDs to type numbers
        const answerToType = {
            'A101': 1, 'A110': 1, // Upholder
            'A102': 2, 'A111': 2, // Giver
            'A103': 3, 'A112': 3, // Driver
            'A104': 4, 'A113': 4, // Seeker
            'A105': 5, 'A114': 5, // Observer
            'A106': 6, 'A115': 6, // Guardian
            'A107': 7, 'A116': 7, // Explorer
            'A108': 8, 'A117': 8, // Protector
            'A109': 9, 'A118': 9  // Harmonizer
        };
        
        // Count occurrences of each type
        const typeCounts = {};
        Object.values(initialAnswers).forEach(answer => {
            const type = answerToType[answer];
            if (type) {
                typeCounts[type] = (typeCounts[type] || 0) + 1;
            }
        });
        
        Object.values(confirmationAnswers).forEach(answer => {
            const type = answerToType[answer];
            if (type) {
                typeCounts[type] = (typeCounts[type] || 0) + 1;
            }
        });
        
        // Find the type with the highest count
        let maxCount = 0;
        let primaryType = 1; // Default to type 1 if no clear winner
        Object.entries(typeCounts).forEach(([type, count]) => {
            if (count > maxCount) {
                maxCount = count;
                primaryType = parseInt(type);
            }
        });
        
        return primaryType;
    },
    
    getAdjacentTypes: function(type) {
        // Get adjacent types (e.g., if type is 1, return [9, 2])
        const enneagramTypes = [1, 2, 3, 4, 5, 6, 7, 8, 9];
        const index = enneagramTypes.indexOf(type);
        return [
            enneagramTypes[(index - 1 + 9) % 9],
            enneagramTypes[(index + 1) % 9]
        ];
    },
    
    getTypeDescription: function(type) {
        // Add brief descriptions for each type
        const descriptions = {
            1: 'The Reformer - Principled, purposeful, self-controlled',
            2: 'The Helper - Generous, demonstrative, people-pleasing',
            3: 'The Achiever - Adaptable, excelling, driven',
            4: 'The Individualist - Expressive, dramatic, self-absorbed',
            5: 'The Investigator - Perceptive, innovative, isolated',
            6: 'The Loyalist - Engaging, responsible, anxious',
            7: 'The Enthusiast - Spontaneous, versatile, scattered',
            8: 'The Challenger - Self-confident, decisive, confrontational',
            9: 'The Peacemaker - Receptive, reassuring, complacent'
        };
        return descriptions[type] || 'Description not available';
    },
    
    renderQuestions: function(phase, questions) {
        performance.start('renderQuestions');
        console.log('Rendering questions for phase:', phase);
        
        try {
            const container = document.getElementById(`${phase}-questions`);
            if (!container) {
                console.error('Question container not found for phase:', phase);
                return;
            }
            
            // Validate questions parameter
            if (!questions || typeof questions !== 'object') {
                console.error('Invalid questions parameter:', questions);
                return;
            }
            
            // Create document fragment for better performance
            const fragment = document.createDocumentFragment();
            
            performance.start('buildQuestions');
            
            // Handle object-based questions structure
            const questionEntries = Object.entries(questions);
            if (!questionEntries || questionEntries.length === 0) {
                console.error('No questions found for phase:', phase);
                return;
            }
            
            questionEntries.forEach(([questionId, question], index) => {
                if (!question || !question.options) {
                    console.error('Invalid question structure:', question);
                    return;
                }
                
                const questionEl = document.createElement('div');
                questionEl.className = 'card mb-3';
                
                // Determine if question should be multiple choice
                const isMultipleChoice = phase === 'detailedDifferentiation' || 
                                       phase === 'confirmation';
                
                // Build options HTML string for better performance
                const optionsHtml = Object.entries(question.options).map(([optionId, option]) => {
                    if (!option || !option.text) {
                        console.error('Invalid option structure:', option);
                        return '';
                    }
                    return `
                        <div class="form-check">
                            <input class="form-check-input" type="${isMultipleChoice ? 'checkbox' : 'radio'}" 
                                name="q${questionId}${isMultipleChoice ? '[]' : ''}" 
                                id="${optionId}" 
                                value="${optionId}"
                                ${!isMultipleChoice ? 'required' : ''}>
                            <label class="form-check-label" for="${optionId}">
                                ${option.text}
                            </label>
                        </div>
                    `;
                }).join('');
                
                questionEl.innerHTML = `
                    <div class="card-body">
                        <h5 class="card-title">Question ${index + 1}</h5>
                        <p class="card-text">${question.text}</p>
                        <div class="form-group">${optionsHtml}</div>
                    </div>
                `;
                fragment.appendChild(questionEl);
            });
            
            performance.end('buildQuestions');
            
            // Add next button
            const nextButton = document.createElement('button');
            nextButton.className = 'btn btn-primary mt-3';
            nextButton.textContent = 'Next';
            nextButton.onclick = () => this.validateAndProceed(phase);
            fragment.appendChild(nextButton);
            
            // Add validation alert
            const validationAlert = document.createElement('div');
            validationAlert.id = `validation-alert-${phase}`;
            validationAlert.className = 'alert alert-danger d-none mt-3';
            validationAlert.textContent = 'Please answer all questions before proceeding.';
            fragment.appendChild(validationAlert);
            
            // Clear and update container in one operation
            performance.start('domUpdate');
            container.innerHTML = '';
            container.appendChild(fragment);
            performance.end('domUpdate');
            
        } catch (error) {
            console.error('Error in renderQuestions:', error);
            const container = document.getElementById(`${phase}-questions`);
            if (container) {
                container.innerHTML = `
                    <div class="alert alert-danger">
                        <h4>Error Loading Questions</h4>
                        <p>There was a problem loading the questions. Please try refreshing the page.</p>
                        <button class="btn btn-outline-danger" onclick="location.reload()">Refresh Page</button>
                    </div>
                `;
            }
        } finally {
            performance.end('renderQuestions');
        }
    },
    validateAndProceed: function(phase) {
        const answers = this.collectAnswers(phase);
        if (this.validateAnswers(answers)) {
            state.answers[phase] = answers;
            metrics.endTimer(phase);
            this.proceedToNextPhase(phase);
        } else {
            document.getElementById(`validation-alert-${phase}`).classList.remove('d-none');
        }
    },
    collectAnswers: function(phase) {
        const answers = {};
        const inputs = document.querySelectorAll(`#${phase}-questions input:checked`);
        inputs.forEach(input => {
            const questionId = input.name.replace('[]', '');
            if (!answers[questionId]) {
                answers[questionId] = [];
            }
            answers[questionId].push(input.value);
        });
        return answers;
    },
    validateAnswers: function(answers) {
        return Object.keys(answers).length > 0;
    },
    proceedToNextPhase: async function(currentPhase) {
        const phases = [
            'registration',
            'initial-segmentation',
            'detailed-differentiation',
            'type-confirmation',
            'wing-type',
            'instinctual-variant',
            'personalization',
            'confirmation',
            'results'
        ];
        const currentIndex = phases.indexOf(currentPhase);
        if (currentIndex < phases.length - 1) {
            const nextPhase = phases[currentIndex + 1];
            
            // Special handling for results phase
            if (nextPhase === 'results') {
                window.showLoading();
                try {
                    // Calculate final scores
                    const scores = calculatePersonaScore(state.answers);
                    
                    // Clear the main content area
                    const mainContent = document.getElementById('persona-details');
                    if (mainContent) {
                        mainContent.innerHTML = '';
                        
                        // Create and append the results
                        const resultsContent = await renderPersonaResults(scores);
                        mainContent.appendChild(resultsContent);
                        
                        // Show the results phase
                        this.showPhase('results');
                        
                        // Update charts after a small delay
                        setTimeout(() => this.updateCharts(), 500);
                    } else {
                        console.error('Results container not found');
                    }
                } catch (error) {
                    console.error('Error in results phase:', error);
                    const mainContent = document.getElementById('persona-details');
                    if (mainContent) {
                        mainContent.innerHTML = `
                            <div class="alert alert-danger">
                                <h4>Error Displaying Results</h4>
                                <p>There was a problem displaying your results. Please try refreshing the page.</p>
                                <button class="btn btn-outline-danger" onclick="location.reload()">Refresh Page</button>
                            </div>
                        `;
                    }
                } finally {
                    window.hideLoading();
                }
            } else {
                this.showPhase(nextPhase);
            }
        }
    },
    renderResults: function() {
        try {
            const scores = calculatePersonaScore(state.answers);
            const resultsContainer = renderPersonaResults(scores);
            
            // Get the results container
            const mainContent = document.getElementById('persona-details');
            if (!mainContent) {
                console.error('Results container not found');
                return;
            }
            
            // Clear existing content and append new results
            mainContent.innerHTML = '';
            mainContent.appendChild(resultsContainer);
            
            // Add export and metrics buttons
            const buttonContainer = document.createElement('div');
            buttonContainer.className = 'mt-4 d-flex gap-3';
            
            const exportButton = document.createElement('button');
            exportButton.className = 'btn btn-primary';
            exportButton.textContent = 'Export Results';
            exportButton.onclick = () => this.exportResults();
            
            const metricsButton = document.createElement('button');
            metricsButton.className = 'btn btn-outline-primary';
            metricsButton.textContent = 'View Assessment Metrics';
            metricsButton.onclick = () => this.showMetricsDashboard();
            
            buttonContainer.appendChild(exportButton);
            buttonContainer.appendChild(metricsButton);
            mainContent.appendChild(buttonContainer);
            
            // Add styles if not already present
            if (!document.getElementById('persona-results-styles')) {
                const style = document.createElement('style');
                style.id = 'persona-results-styles';
                style.textContent = `
                    .persona-results {
                        max-width: 800px;
                        margin: 0 auto;
                        padding: 20px;
                    }
                    
                    .primary-persona {
                        background-color: #f8f9fa;
                        padding: 20px;
                        border-radius: 8px;
                        margin-bottom: 30px;
                    }
                    
                    .secondary-personas {
                        display: grid;
                        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                        gap: 20px;
                        margin-bottom: 30px;
                    }
                    
                    .secondary-persona {
                        background-color: #f1f3f5;
                        padding: 15px;
                        border-radius: 8px;
                    }
                    
                    .core-values, .growth-areas, .strengths {
                        margin: 20px 0;
                    }
                    
                    ul {
                        list-style-type: none;
                        padding: 0;
                    }
                    
                    li {
                        margin: 10px 0;
                        padding: 8px;
                        background-color: #fff;
                        border-radius: 4px;
                        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                    }
                    
                    h2, h3, h4 {
                        color: #2c3e50;
                    }
                    
                    .personalization {
                        background-color: #e9ecef;
                        padding: 20px;
                        border-radius: 8px;
                        margin-top: 30px;
                    }
                `;
                document.head.appendChild(style);
            }
        } catch (error) {
            console.error('Error rendering results:', error);
            const mainContent = document.getElementById('persona-details');
            if (mainContent) {
                mainContent.innerHTML = `
                    <div class="alert alert-danger">
                        <h4>Error Displaying Results</h4>
                        <p>There was a problem displaying your results. Please try refreshing the page.</p>
                    </div>
                `;
            }
        }
    },
    calculatePrimaryType: function() {
        const initialAnswers = state.answers['initial-segmentation'] || {};
        const detailedAnswers = state.answers['detailed-differentiation'] || {};
        const confirmationAnswers = state.answers['type-confirmation'] || {};

        // Simple scoring system (you would want a more sophisticated one in production)
        let typeScores = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0};

        // Score based on initial segmentation
        if (initialAnswers['qQ101'] === 'A101') typeScores[1] += 2;
        if (initialAnswers['qQ101'] === 'A102') typeScores[2] += 2;
        if (initialAnswers['qQ101'] === 'A103') typeScores[8] += 2;

        // Add more scoring logic based on other answers...

        // Find the type with highest score
        return parseInt(Object.entries(typeScores).reduce((a, b) => a[1] > b[1] ? a : b)[0]);
    },
    calculateInstinctualVariant: function() {
        const answers = state.answers['instinctual-variant'] || {};
        
        const variants = {
            'self-preservation': 0,
            'social': 0,
            'one-to-one': 0
        };

        if (answers['qQ501'] === 'A501') variants['self-preservation']++;
        if (answers['qQ501'] === 'A502') variants['one-to-one']++;
        if (answers['qQ501'] === 'A503') variants['social']++;

        if (answers['qQ502'] === 'A504') variants['self-preservation']++;
        if (answers['qQ502'] === 'A505') variants['one-to-one']++;
        if (answers['qQ502'] === 'A506') variants['social']++;

        const primary = Object.entries(variants).reduce((a, b) => a[1] > b[1] ? a : b)[0];
        
        const variantNames = {
            'self-preservation': 'Self-Preservation',
            'social': 'Social',
            'one-to-one': 'One-to-One'
        };

        return variantNames[primary];
    },
    calculateOverallConfidence: function() {
        const allScores = Object.values(state.confidenceScores);
        if (allScores.length === 0) return 70; // Default confidence
        return Math.round(allScores.reduce((a, b) => a + b, 0) / allScores.length);
    },
    generateGrowthAreas: function(type) {
        const growthAreas = {
            1: ['Practice flexibility and acceptance', 'Develop patience with imperfection', 'Balance criticism with compassion'],
            2: ['Set healthy boundaries', 'Acknowledge your own needs', 'Express feelings directly'],
            3: ['Value authentic self over image', 'Connect with true feelings', 'Define success personally'],
            4: ['Build emotional balance', 'Maintain perspective in feelings', 'Develop practical skills'],
            5: ['Engage with others more', 'Balance analysis with action', 'Share knowledge and experiences'],
            6: ['Trust inner guidance', 'Face fears directly', 'Develop self-confidence'],
            7: ['Follow through on commitments', 'Stay with difficult emotions', 'Focus on present experience'],
            8: ['Practice gentleness', 'Allow vulnerability', 'Consider others\' perspectives'],
            9: ['Assert personal priorities', 'Engage with conflict', 'Maintain self-awareness']
        };

        return `
            <h5 class="card-title">Recommended Focus Areas</h5>
            <ul class="list-group list-group-flush">
                ${growthAreas[type].map(area => `
                    <li class="list-group-item">${area}</li>
                `).join('')}
            </ul>
        `;
    },
    showMetricsDashboard: function() {
        document.getElementById('metrics-dashboard').classList.add('active');
        this.updateMetricsDashboard();
    },
    exportResults: function() {
        const results = {
            primaryType: this.calculatePrimaryType(),
            wingType: state.answers['wing-type'] ? 
                parseInt(state.answers['wing-type']['qQ401'].replace('A40', '')) : null,
            instinctualVariant: this.calculateInstinctualVariant(),
            confidenceScore: this.calculateOverallConfidence(),
            answers: state.answers,
            metrics: {
                phaseTimes: state.phaseTimes,
                interactionCounts: state.interactionCounts,
                confidenceScores: state.confidenceScores
            }
        };

        const blob = new Blob([JSON.stringify(results, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'core-persona-results.json';
        a.click();
        URL.revokeObjectURL(url);
    },
    updateMetricsDashboard: function() {
        // Update time metrics
        document.getElementById('total-time').textContent = 
            Math.round((Date.now() - state.startTime) / 1000);
        
        // Update completion metrics
        const totalQuestions = Object.values(state.answers).reduce((sum, phase) => 
            sum + Object.keys(phase).length, 0);
        document.getElementById('questions-answered').textContent = totalQuestions;
        
        // Update confidence score
        const avgConfidence = Object.values(state.confidenceScores).reduce((sum, score) => 
            sum + score, 0) / Object.keys(state.confidenceScores).length;
        document.getElementById('confidence-score').textContent = 
            Math.round(avgConfidence || 0);
        
        // Update charts
        this.updateCharts();
    },
    updateCharts: async function() {
        performance.start('updateCharts');
        
        try {
            // Clear existing charts
            if (this.charts) {
                Object.values(this.charts).forEach(chart => {
                    if (chart && typeof chart.destroy === 'function') {
                        chart.destroy();
                    }
                });
            }
            this.charts = {};

            // Helper function to create chart with memory management
            const createChart = async (chartId, ctx, config) => {
                return new Promise((resolve) => {
                    requestAnimationFrame(() => {
                        try {
                            // Use lower resolution for better performance
                            ctx.canvas.style.width = '100%';
                            ctx.canvas.width = ctx.canvas.offsetWidth * (IS_PRODUCTION ? 1 : 2);
                            ctx.canvas.height = ctx.canvas.offsetHeight * (IS_PRODUCTION ? 1 : 2);
                            
                            this.charts[chartId] = new Chart(ctx, {
                                ...config,
                                options: {
                                    ...config.options,
                                    animation: false,
                                    responsive: true,
                                    maintainAspectRatio: false,
                                    plugins: {
                                        legend: {
                                            display: false
                                        }
                                    },
                                    elements: {
                                        point: {
                                            radius: 0 // Disable points for better performance
                                        },
                                        line: {
                                            borderWidth: 1 // Thinner lines for better performance
                                        }
                                    }
                                }
                            });
                            resolve();
                        } catch (error) {
                            console.error('Error creating chart:', chartId, error);
                            resolve();
                        }
                    });
                });
            };

            // Create charts with reduced data points
            const reducedData = {
                timeChart: Object.entries(state.phaseTimes).slice(-5),
                completionChart: Object.entries(state.answers).slice(-5),
                interactionChart: Object.entries(state.interactionCounts).slice(-5)
            };

            const charts = [
                {
                    id: 'timeChart',
                    config: {
                        type: 'bar',
                        data: {
                            labels: reducedData.timeChart.map(([key]) => key),
                            datasets: [{
                                data: reducedData.timeChart.map(([, value]) => 
                                    Math.round((value.end - value.start) / 1000)
                                )
                            }]
                        }
                    }
                },
                {
                    id: 'completionChart',
                    config: {
                        type: 'pie',
                        data: {
                            labels: reducedData.completionChart.map(([key]) => key),
                            datasets: [{
                                data: reducedData.completionChart.map(([, value]) => 
                                    Object.keys(value).length
                                )
                            }]
                        }
                    }
                },
                {
                    id: 'interactionChart',
                    config: {
                        type: 'line',
                        data: {
                            labels: reducedData.interactionChart.map(([key]) => key),
                            datasets: [{
                                data: reducedData.interactionChart.map(([, value]) => value)
                            }]
                        }
                    }
                }
            ];

            // Create charts sequentially with delays
            for (const chart of charts) {
                const ctx = document.getElementById(chart.id)?.getContext('2d');
                if (ctx) {
                    performance.start(chart.id);
                    await createChart(chart.id, ctx, chart.config);
                    performance.end(chart.id);
                    await new Promise(resolve => setTimeout(resolve, IS_PRODUCTION ? 50 : 100));
                }
            }
            
            // Suggest garbage collection after creating all charts
            memoryManager.suggestGC();
            
        } catch (error) {
            console.error('Error in updateCharts:', error);
        } finally {
            performance.end('updateCharts');
        }
    },
    renderPersonalization: function() {
        try {
            const container = document.getElementById('personalization-questions');
            if (!container) {
                throw new Error('Personalization container not found');
            }
            
            // Clear existing content
            container.innerHTML = '';
            
            // Create document fragment for better performance
            const fragment = document.createDocumentFragment();
            
            // Add questions from questionBank
            questionBank.personalization.forEach((question, index) => {
                const questionEl = document.createElement('div');
                questionEl.className = 'card mb-4';
                questionEl.innerHTML = `
                    <div class="card-body">
                        <h5 class="card-title">Question ${index + 1}</h5>
                        <p class="card-text">${question.text}</p>
                        <div class="form-group">
                            ${question.options.map(option => `
                                <div class="form-check">
                                    <input class="form-check-input" type="radio" 
                                        name="q${question.id}" 
                                        id="${option.id}" 
                                        value="${option.id}"
                                        required>
                                    <label class="form-check-label" for="${option.id}">
                                        ${option.text}
                                    </label>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                `;
                fragment.appendChild(questionEl);
            });
            
            // Add next button
            const nextButton = document.createElement('button');
            nextButton.className = 'btn btn-primary mt-3';
            nextButton.textContent = 'Complete Assessment';
            nextButton.onclick = () => this.validateAndProceed('personalization');
            fragment.appendChild(nextButton);
            
            // Add validation message
            const validationAlert = document.createElement('div');
            validationAlert.id = 'validation-alert-personalization';
            validationAlert.className = 'alert alert-danger d-none mt-3';
            validationAlert.textContent = 'Please answer all questions before proceeding.';
            fragment.appendChild(validationAlert);
            
            // Update container
            container.appendChild(fragment);
            
        } catch (error) {
            console.error('Error in renderPersonalization:', error);
            if (container) {
                container.innerHTML = `
                    <div class="alert alert-danger">
                        <h4>Error Loading Personalization</h4>
                        <p>There was a problem loading the personalization questions. Please try refreshing the page.</p>
                        <button class="btn btn-outline-danger" onclick="location.reload()">Refresh Page</button>
                    </div>
                `;
            }
        }
    }
};

// Modify cleanup to be more thorough
const cleanup = {
    clearPhaseData: function(phase) {
        performance.start(`cleanup_${phase}`);
        try {
            if (state.answers[phase]) {
                delete state.answers[phase];
            }
            if (state.phaseTimes[phase]) {
                delete state.phaseTimes[phase];
            }
            if (state.interactionCounts[phase]) {
                delete state.interactionCounts[phase];
            }
            if (state.confidenceScores[phase]) {
                delete state.confidenceScores[phase];
            }
            
            // Clear DOM elements
            const container = document.getElementById(`${phase}-questions`);
            if (container) {
                container.innerHTML = '';
            }
            
            // Clear event listeners
            this.removeEventListeners(phase);
            
            // Save state after cleanup
            stateManager.saveState();
        } finally {
            performance.end(`cleanup_${phase}`);
        }
    },
    
    removeEventListeners: function(phase) {
        performance.start(`removeListeners_${phase}`);
        try {
            const container = document.getElementById(`${phase}-questions`);
            if (container) {
                const oldContainer = container.cloneNode(true);
                container.parentNode.replaceChild(oldContainer, container);
            }
        } finally {
            performance.end(`removeListeners_${phase}`);
        }
    }
};

// Initialize state on page load
document.addEventListener('DOMContentLoaded', function() {
    performance.start('initialization');
    try {
        stateManager.loadState();
        
        const container = document.querySelector('.container');
        if (!container) {
            console.error('Main container not found');
            return;
        }
        
        // Use event delegation for all form submissions
        container.addEventListener('submit', function(e) {
            if (e.target.id === 'registration-form') {
                e.preventDefault();
                performance.start('registration');
                try {
                    const formData = new FormData(e.target);
                    state.answers.registration = Object.fromEntries(formData);
                    state.startTime = Date.now();
                    stateManager.saveState();
                    ui.showPhase('initial-segmentation');
                } finally {
                    performance.end('registration');
                }
            }
        });
        
        // Use event delegation for all clicks
        container.addEventListener('click', function(e) {
            if (e.target.id === 'export-metrics') {
                performance.start('exportMetrics');
                try {
                    const metricsData = {
                        answers: state.answers,
                        phaseTimes: state.phaseTimes,
                        interactionCounts: state.interactionCounts,
                        confidenceScores: state.confidenceScores
                    };
                    const blob = new Blob([JSON.stringify(metricsData, null, 2)], { type: 'application/json' });
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'core-persona-metrics.json';
                    a.click();
                    URL.revokeObjectURL(url);
                } finally {
                    performance.end('exportMetrics');
                }
            }
        });
    } finally {
        performance.end('initialization');
    }
});

// Add window unload handler to clean up resources
window.addEventListener('unload', function() {
    memoryManager.clearMemory();
}); 

function renderPersonaResults(scores) {
    // Sort personas by score in descending order
    const sortedPersonas = Object.entries(scores)
        .sort(([, a], [, b]) => b - a)
        .map(([persona, score]) => ({ persona, score }));

    // Create results container
    const container = document.createElement('div');
    container.className = 'persona-results';

    // Add primary persona section
    const primaryPersona = sortedPersonas[0];
    const primaryPersonaInfo = personas[primaryPersona.persona];
    
    if (!primaryPersonaInfo) {
        console.error(`Primary persona info not found for: ${primaryPersona.persona}`);
        container.innerHTML = '<div class="alert alert-danger">Error: Could not load persona information. Please try again.</div>';
        return container;
    }

    const primarySection = document.createElement('div');
    primarySection.className = 'primary-persona';
    primarySection.innerHTML = `
        <h2>Your Primary Persona: ${primaryPersona.persona.charAt(0).toUpperCase() + primaryPersona.persona.slice(1)}</h2>
        <p>${primaryPersonaInfo.description}</p>
        <div class="score">Score: ${primaryPersona.score}%</div>
        
        <div class="core-values">
            <h3>Core Values</h3>
            <ul>
                ${primaryPersonaInfo.coreValues.map(value => `<li>${value}</li>`).join('')}
            </ul>
        </div>
        
        <div class="inner-world">
            <h3>Inner World</h3>
            <ul>
                <li>Fear: ${primaryPersonaInfo.innerWorld.fear}</li>
                <li>Desire: ${primaryPersonaInfo.innerWorld.desire}</li>
                <li>Limiting Belief: ${primaryPersonaInfo.innerWorld.limitingBelief}</li>
            </ul>
        </div>

        <div class="core-emotional-needs">
            <h3>Core Emotional Needs</h3>
            <ul>
                ${Object.entries(primaryPersonaInfo.coreEmotionalNeeds).map(([need, description]) => 
                    `<li><strong>${need}:</strong> ${description}</li>`
                ).join('')}
            </ul>
        </div>

        <div class="blind-spots">
            <h3>Blind Spots</h3>
            <ul>
                ${primaryPersonaInfo.blindSpots.map(spot => `<li>${spot}</li>`).join('')}
            </ul>
        </div>

        <div class="aspirations">
            <h3>Aspirations</h3>
            <ul>
                ${primaryPersonaInfo.aspirations.map(aspiration => `<li>${aspiration}</li>`).join('')}
            </ul>
        </div>

        <div class="stress-vs-growth">
            <h3>Stress vs Growth Patterns</h3>
            <div class="pattern-grid">
                ${Object.entries(primaryPersonaInfo.stressVsGrowth).map(([area, patterns]) => `
                    <div class="pattern-card">
                        <h4>${area}</h4>
                        <ul>
                            <li><strong>Stress:</strong> ${patterns.stress}</li>
                            <li><strong>Growth:</strong> ${patterns.growth}</li>
                            <li><strong>Outcome:</strong> ${patterns.outcome}</li>
                        </ul>
                    </div>
                `).join('')}
            </div>
        </div>

        <div class="boundaries">
            <h3>Boundaries</h3>
            <ul>
                <li><strong>Tendency:</strong> ${primaryPersonaInfo.boundaries.tendency}</li>
                <li><strong>Growth:</strong> ${primaryPersonaInfo.boundaries.growth}</li>
            </ul>
        </div>

        <div class="life-domain-impact">
            <h3>Life Domain Impact</h3>
            <div class="domain-grid">
                ${Object.entries(primaryPersonaInfo.lifeDomainImpact).map(([domain, impact]) => `
                    <div class="domain-card">
                        <h4>${domain}</h4>
                        <p>${impact}</p>
                    </div>
                `).join('')}
            </div>
        </div>

        <div class="potential">
            <h3>Potential</h3>
            <div class="capabilities">
                <h4>Capabilities</h4>
                <ul>
                    ${primaryPersonaInfo.potential.capabilities.map(capability => `<li>${capability}</li>`).join('')}
                </ul>
            </div>
            <div class="life-changes">
                <h4>Life Changes</h4>
                <div class="changes-grid">
                    ${Object.entries(primaryPersonaInfo.potential.lifeChanges).map(([area, change]) => `
                        <div class="change-card">
                            <h5>${area}</h5>
                            <p>${change}</p>
                        </div>
                    `).join('')}
                </div>
            </div>
        </div>
    `;
    container.appendChild(primarySection);

    // Add secondary personas section
    const secondarySection = document.createElement('div');
    secondarySection.className = 'secondary-personas';
    
    // Filter out personas that don't have corresponding info
    const validSecondaryPersonas = sortedPersonas.slice(1).filter(({ persona }) => personas[persona]);
    
    if (validSecondaryPersonas.length > 0) {
        secondarySection.innerHTML = `
            <h3>Secondary Personas</h3>
            <div class="persona-grid">
                ${validSecondaryPersonas.map(({ persona, score }) => {
                    const personaInfo = personas[persona];
                    return `
                        <div class="secondary-persona">
                            <h4>${persona.charAt(0).toUpperCase() + persona.slice(1)} (${score}%)</h4>
                            <p>${personaInfo.description}</p>
                        </div>
                    `;
                }).join('')}
            </div>
        `;
        container.appendChild(secondarySection);
    }

    return container;
}

// Answer to Persona mapping
const answerToPersona = {
    // Initial Segmentation
    'A101': 'upholder',
    'A102': 'giver',
    'A103': 'driver',
    'A104': 'seeker',
    'A105': 'observer',
    'A106': 'guardian',
    'A107': 'explorer',
    'A108': 'protector',
    'A109': 'harmonizer',
    'A110': 'upholder',
    'A111': 'giver',
    'A112': 'driver',
    'A113': 'seeker',
    'A114': 'observer',
    'A115': 'guardian',
    'A116': 'explorer',
    'A117': 'protector',
    'A118': 'harmonizer',
    
    // Detailed Differentiation
    'A201': 'upholder',
    'A202': 'questioner',
    'A203': 'obliger',
    'A204': 'rebel',
    'A205': 'harmonizer',
    'A206': 'observer',
    'A207': 'explorer',
    'A208': 'protector',
    'A209': 'driver',
    'A210': 'upholder',
    'A211': 'questioner',
    'A212': 'obliger',
    'A213': 'rebel',
    'A214': 'harmonizer',
    'A215': 'observer',
    'A216': 'explorer',
    'A217': 'protector',
    'A218': 'driver',
    
    // Type Confirmation
    'A301': 'upholder',
    'A302': 'questioner',
    'A303': 'obliger',
    'A304': 'rebel',
    'A305': 'harmonizer',
    'A306': 'observer',
    'A307': 'driver',
    'A308': 'protector',
    'A309': 'explorer',
    
    // Wing Type
    'A401': 'upholder',
    'A402': 'giver',
    'A403': 'driver',
    'A404': 'seeker',
    'A405': 'observer',
    'A406': 'guardian',
    'A407': 'explorer',
    'A408': 'protector',
    'A409': 'harmonizer',
    
    // Instinctual Variant
    'A501': 'guardian',
    'A502': 'harmonizer',
    'A503': 'protector',
    'A504': 'guardian',
    'A505': 'harmonizer',
    'A506': 'protector'
};
