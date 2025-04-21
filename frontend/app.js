// Add production optimization flags
const IS_PRODUCTION = window.location.hostname !== 'localhost';
const ENABLE_LOGGING = !IS_PRODUCTION;

// Question Bank
const questionBank = {
    initialSegmentation: [
        {
            id: 'Q101',
            text: 'What best describes your approach to life?',
            options: [
                { id: 'A101', text: 'I strive for excellence and doing things the right way' },
                { id: 'A102', text: 'I focus on helping and connecting with others' },
                { id: 'A103', text: 'I aim to achieve success and recognition' },
                { id: 'A104', text: 'I seek deep meaning and authenticity' },
                { id: 'A105', text: 'I value knowledge and understanding' },
                { id: 'A106', text: 'I prioritize security and preparedness' },
                { id: 'A107', text: 'I embrace adventure and possibilities' },
                { id: 'A108', text: 'I take charge and protect what matters' },
                { id: 'A109', text: 'I maintain harmony and peace' }
            ]
        },
        {
            id: 'Q102',
            text: 'What is your greatest fear?',
            options: [
                { id: 'A110', text: 'Being wrong or making mistakes' },
                { id: 'A111', text: 'Being unloved or unwanted' },
                { id: 'A112', text: 'Being seen as a failure' },
                { id: 'A113', text: 'Being emotionally abandoned' },
                { id: 'A114', text: 'Being overwhelmed or depleted' },
                { id: 'A115', text: 'Being unprepared or unsafe' },
                { id: 'A116', text: 'Being trapped in pain or limitation' },
                { id: 'A117', text: 'Being controlled or betrayed' },
                { id: 'A118', text: 'Conflict or disconnection' }
            ]
        },
        {
            id: 'Q103',
            text: 'How do you typically handle stress?',
            options: [
                { id: 'A119', text: 'I become more critical and demanding' },
                { id: 'A120', text: 'I give more to others' },
                { id: 'A121', text: 'I work harder to prove myself' },
                { id: 'A122', text: 'I withdraw into my emotions' },
                { id: 'A123', text: 'I retreat into analysis' },
                { id: 'A124', text: 'I become more anxious and vigilant' },
                { id: 'A125', text: 'I seek new distractions' },
                { id: 'A126', text: 'I become more controlling' },
                { id: 'A127', text: 'I avoid conflict and adapt' }
            ]
        },
        {
            id: 'Q104',
            text: 'What do you value most in relationships?',
            options: [
                { id: 'A128', text: 'Integrity and moral clarity' },
                { id: 'A129', text: 'Emotional closeness and being needed' },
                { id: 'A130', text: 'Admiration and success' },
                { id: 'A131', text: 'Deep understanding and authenticity' },
                { id: 'A132', text: 'Privacy and independence' },
                { id: 'A133', text: 'Loyalty and security' },
                { id: 'A134', text: 'Excitement and freedom' },
                { id: 'A135', text: 'Honesty and directness' },
                { id: 'A136', text: 'Harmony and acceptance' }
            ]
        }
    ],
    detailedDifferentiation: {
        upholder: [
            {
                id: 'Q201',
                text: 'How do you feel about rules and standards?',
                options: [
                    { id: 'A201', text: 'They provide necessary structure' },
                    { id: 'A202', text: 'They should be followed with integrity' },
                    { id: 'A203', text: 'They help maintain order and improvement' }
                ]
            }
        ],
        giver: [
            {
                id: 'Q202',
                text: 'How do you feel about helping others?',
                options: [
                    { id: 'A204', text: 'It\'s natural and fulfilling' },
                    { id: 'A205', text: 'It makes me feel valued' },
                    { id: 'A206', text: 'I sometimes give too much' }
                ]
            }
        ],
        driver: [
            {
                id: 'Q203',
                text: 'How do you view success?',
                options: [
                    { id: 'A207', text: 'It\'s essential to my identity' },
                    { id: 'A208', text: 'It proves my worth' },
                    { id: 'A209', text: 'I need to keep achieving' }
                ]
            }
        ],
        seeker: [
            {
                id: 'Q204',
                text: 'How do you experience emotions?',
                options: [
                    { id: 'A210', text: 'Deeply and intensely' },
                    { id: 'A211', text: 'I need to express them authentically' },
                    { id: 'A212', text: 'I often feel misunderstood' }
                ]
            }
        ],
        observer: [
            {
                id: 'Q205',
                text: 'How do you handle social situations?',
                options: [
                    { id: 'A213', text: 'I prefer to observe and analyze' },
                    { id: 'A214', text: 'I need time to process' },
                    { id: 'A215', text: 'I value my privacy' }
                ]
            }
        ],
        guardian: [
            {
                id: 'Q206',
                text: 'How do you approach security?',
                options: [
                    { id: 'A216', text: 'I\'m always prepared' },
                    { id: 'A217', text: 'I need to feel safe' },
                    { id: 'A218', text: 'I\'m loyal to those I trust' }
                ]
            }
        ],
        explorer: [
            {
                id: 'Q207',
                text: 'How do you handle limitations?',
                options: [
                    { id: 'A219', text: 'I seek ways around them' },
                    { id: 'A220', text: 'I need freedom to explore' },
                    { id: 'A221', text: 'I avoid feeling trapped' }
                ]
            }
        ],
        protector: [
            {
                id: 'Q208',
                text: 'How do you handle power?',
                options: [
                    { id: 'A222', text: 'I take charge when needed' },
                    { id: 'A223', text: 'I protect what matters' },
                    { id: 'A224', text: 'I value strength and control' }
                ]
            }
        ],
        harmonizer: [
            {
                id: 'Q209',
                text: 'How do you handle conflict?',
                options: [
                    { id: 'A225', text: 'I avoid it when possible' },
                    { id: 'A226', text: 'I seek harmony' },
                    { id: 'A227', text: 'I adapt to maintain peace' }
                ]
            }
        ]
    },
    typeConfirmation: [
        {
            id: 'Q301',
            text: 'Which of these statements resonates most with you?',
            options: [
                { id: 'A301', text: 'I need to do things the right way' },
                { id: 'A302', text: 'I need to be loved and needed' },
                { id: 'A303', text: 'I need to be successful and admired' },
                { id: 'A304', text: 'I need to be authentic and understood' },
                { id: 'A305', text: 'I need to understand and be competent' },
                { id: 'A306', text: 'I need to be secure and prepared' },
                { id: 'A307', text: 'I need to be free and excited' },
                { id: 'A308', text: 'I need to be strong and in control' },
                { id: 'A309', text: 'I need to be at peace and connected' }
            ]
        }
    ],
    wingType: [
        {
            id: 'Q401',
            text: 'Which closely related type feels more like you?',
            options: [] // Will be populated based on primary type
        }
    ],
    instinctualVariant: [
        {
            id: 'Q501',
            text: 'What is your top daily life priority?',
            options: [
                { id: 'A501', text: 'Physical comfort (Self-Preservation)' },
                { id: 'A502', text: 'Personal connections (One-to-One)' },
                { id: 'A503', text: 'Social role (Social)' }
            ]
        },
        {
            id: 'Q502',
            text: 'Which fear or insecurity resonates most?',
            options: [
                { id: 'A504', text: 'Practical security (Self-Preservation)' },
                { id: 'A505', text: 'Depth of connections (One-to-One)' },
                { id: 'A506', text: 'Social acceptance (Social)' }
            ]
        }
    ],
    personalization: [
        {
            id: 'Q601',
            text: 'Which areas would you like to explore further?',
            options: [
                { id: 'A601', text: 'Personal Growth' },
                { id: 'A602', text: 'Relationships' },
                { id: 'A603', text: 'Career' },
                { id: 'A604', text: 'Stress Management' }
            ]
        },
        {
            id: 'Q602',
            text: 'How frequently do you want new insights?',
            options: [
                { id: 'A605', text: 'Daily' },
                { id: 'A606', text: 'Weekly' },
                { id: 'A607', text: 'Bi-Weekly' },
                { id: 'A608', text: 'Monthly' }
            ]
        }
    ]
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
function calculatePersonaScore(answers) {
    const scores = {
        upholder: 0,
        giver: 0,
        driver: 0,
        seeker: 0,
        observer: 0,
        guardian: 0,
        explorer: 0,
        protector: 0,
        harmonizer: 0
    };

    // Initial segmentation scoring
    const initialAnswers = answers.initialSegmentation || {};
    Object.entries(initialAnswers).forEach(([questionId, answerId]) => {
        const question = questionBank.initialSegmentation.find(q => q.id === questionId);
        const answer = question.options.find(a => a.id === answerId);
        
        // Map answers to personas
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

        if (answerToPersona[answerId]) {
            scores[answerToPersona[answerId]] += 2;
        }
    });

    // Detailed differentiation scoring
    const detailedAnswers = answers.detailedDifferentiation || {};
    Object.entries(detailedAnswers).forEach(([persona, answer]) => {
        if (scores[persona] !== undefined) {
            scores[persona] += 3;
        }
    });

    // Type confirmation scoring
    const confirmationAnswers = answers.typeConfirmation || {};
    Object.entries(confirmationAnswers).forEach(([questionId, answerId]) => {
        const question = questionBank.typeConfirmation.find(q => q.id === questionId);
        const answer = question.options.find(a => a.id === answerId);
        
        const answerToPersona = {
            'A301': 'upholder',
            'A302': 'giver',
            'A303': 'driver',
            'A304': 'seeker',
            'A305': 'observer',
            'A306': 'guardian',
            'A307': 'explorer',
            'A308': 'protector',
            'A309': 'harmonizer'
        };

        if (answerToPersona[answerId]) {
            scores[answerToPersona[answerId]] += 4;
        }
    });

    return scores;
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
            
            let consistentAnswers = 0;
            // Add logic to check answer consistency based on phase
            state.confidenceScores[phase] = Math.round((consistentAnswers / totalQuestions) * 100);
            return state.confidenceScores[phase];
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
                    this.renderWingType();
                    break;
                case 'instinctual-variant':
                    this.renderQuestions(phase, questionBank.instinctualVariant);
                    break;
                case 'personalization':
                    this.renderPersonalization();
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
        
        const questions = questionBank.detailedDifferentiation[persona];
        if (!questions) {
            console.error('No questions found for persona:', persona);
            return;
        }
        
        // Add persona indicator
        const personaInfo = personas[persona];
        const categoryIndicator = document.createElement('div');
        categoryIndicator.className = 'alert alert-info mb-4';
        categoryIndicator.innerHTML = `
            <h4>Exploring ${personaInfo.name}</h4>
            <p>${personaInfo.description}</p>
        `;
        container.appendChild(categoryIndicator);
        
        questions.forEach((question, index) => {
            const questionEl = document.createElement('div');
            questionEl.className = 'card mb-3';
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
                                    value="${option.id}">
                                <label class="form-check-label" for="${option.id}">
                                    ${option.text}
                                </label>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
            container.appendChild(questionEl);
        });
        
        // Add validation alert
        const validationAlert = document.createElement('div');
        validationAlert.id = 'validation-alert-detailed-differentiation';
        validationAlert.className = 'alert alert-danger d-none';
        validationAlert.textContent = 'Please answer all questions before proceeding.';
        container.appendChild(validationAlert);
        
        const nextButton = document.createElement('button');
        nextButton.className = 'btn btn-primary mt-3';
        nextButton.textContent = 'Next';
        nextButton.onclick = () => this.validateAndProceed('detailed-differentiation');
        container.appendChild(nextButton);
    },
    
    renderWingType: function() {
        const container = document.getElementById('wing-type-questions');
        container.innerHTML = '';
        
        // Determine primary type from previous answers
        const primaryType = this.determinePrimaryType();
        
        // Get adjacent types
        const adjacentTypes = this.getAdjacentTypes(primaryType);
        
        // Update wing type question options
        questionBank.wingType[0].options = adjacentTypes.map((type, index) => ({
            id: `A40${index + 1}`,
            text: `Type ${type}: ${this.getTypeDescription(type)}`
        }));
        
        this.renderQuestions('wing-type', questionBank.wingType);
    },
    
    determinePrimaryType: function() {
        // Logic to determine primary type based on previous answers
        // This is a simplified version - you would need to implement the actual logic
        return 1; // Default to type 1 for demo
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
            
            // Create document fragment for better performance
            const fragment = document.createDocumentFragment();
            
            performance.start('buildQuestions');
            questions.forEach((question, index) => {
                const questionEl = document.createElement('div');
                questionEl.className = 'card mb-3';
                
                // Build options HTML string for better performance
                const optionsHtml = question.options.map(option => `
                    <div class="form-check">
                        <input class="form-check-input" type="radio" 
                            name="q${question.id}" 
                            id="${option.id}" 
                            value="${option.id}">
                        <label class="form-check-label" for="${option.id}">
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
            performance.end('buildQuestions');
            
            const nextButton = document.createElement('button');
            nextButton.className = 'btn btn-primary';
            nextButton.textContent = 'Next';
            nextButton.onclick = () => this.validateAndProceed(phase);
            fragment.appendChild(nextButton);
            
            // Clear and update container in one operation
            performance.start('domUpdate');
            container.innerHTML = '';
            container.appendChild(fragment);
            performance.end('domUpdate');
            
        } catch (error) {
            console.error('Error in renderQuestions:', error);
        }
        
        performance.end('renderQuestions');
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
            answers[input.name] = input.value;
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

// Add memory management
const memoryManager = {
    gcThreshold: 50, // Number of operations before suggesting garbage collection
    operationCount: 0,
    
    incrementOperations: function() {
        this.operationCount++;
        if (this.operationCount >= this.gcThreshold) {
            this.suggestGC();
        }
    },
    
    suggestGC: function() {
        if (window.gc) {
            try {
                window.gc();
            } catch (e) {
                console.warn('Manual GC not available');
            }
        }
        this.operationCount = 0;
    },
    
    clearMemory: function() {
        // Clear large objects
        if (ui.charts) {
            Object.values(ui.charts).forEach(chart => {
                if (chart && typeof chart.destroy === 'function') {
                    chart.destroy();
                }
            });
            ui.charts = null;
        }
        
        // Clear cached data
        if (window.questionBank) {
            window.questionBank = null;
        }
        
        this.suggestGC();
    }
};

// Modify chunked rendering to be more memory efficient
const chunkRenderer = {
    timeout: null,
    queue: [],
    chunkSize: 5, // Number of operations per chunk
    
    add: function(task) {
        this.queue.push(task);
        if (!this.timeout) {
            this.processNext();
        }
    },
    
    processNext: function() {
        if (this.queue.length === 0) {
            this.timeout = null;
            memoryManager.suggestGC();
            return;
        }
        
        let processedInChunk = 0;
        while (processedInChunk < this.chunkSize && this.queue.length > 0) {
            const task = this.queue.shift();
            this.timeout = requestAnimationFrame(() => {
                try {
                    task();
                    memoryManager.incrementOperations();
                } catch (error) {
                    console.error('Error in chunked render task:', error);
                }
            });
            processedInChunk++;
        }
        
        if (this.queue.length > 0) {
            setTimeout(() => this.processNext(), 16); // Approximately 1 frame at 60fps
        } else {
            memoryManager.suggestGC();
        }
    }
};

// Modify results rendering to be more memory efficient
function renderPersonaResults(scores) {
    // Sort personas by score
    const sortedPersonas = Object.entries(scores)
        .sort(([, a], [, b]) => b - a)
        .map(([type, score]) => ({ type, score }));

    // Calculate total score for percentage
    const totalScore = sortedPersonas.reduce((sum, { score }) => sum + score, 0);

    // Create results container
    const resultsContainer = document.createElement('div');
    resultsContainer.className = 'results-container';
    resultsContainer.innerHTML = `
        <h2>Your Emotional Persona Assessment Results</h2>
        <div class="results-summary">
            <p>Based on your responses, here's how you align with each emotional persona type:</p>
        </div>
    `;

    // Add primary persona section
    const primaryPersona = sortedPersonas[0];
    const primaryPersonaData = personas[primaryPersona.type];
    const primaryPercentage = Math.round((primaryPersona.score / totalScore) * 100);

    const primarySection = document.createElement('div');
    primarySection.className = 'primary-persona';
    primarySection.innerHTML = `
        <h3>Your Primary Persona: ${primaryPersonaData.name}</h3>
        <div class="confidence-rating">
            <div class="confidence-bar" style="width: ${primaryPercentage}%"></div>
            <span class="confidence-text">${primaryPercentage}% Confidence Rating</span>
        </div>
        <p class="persona-description">${primaryPersonaData.description}</p>
        
        <div class="persona-details">
            <div class="detail-section">
                <h4>Inner World</h4>
                <ul>
                    <li><strong>Core Fear:</strong> ${primaryPersonaData.innerWorld.fear}</li>
                    <li><strong>Core Desire:</strong> ${primaryPersonaData.innerWorld.desire}</li>
                    <li><strong>Limiting Belief:</strong> ${primaryPersonaData.innerWorld.limitingBelief}</li>
                </ul>
            </div>
            
            <div class="detail-section">
                <h4>Core Values</h4>
                <ul>
                    ${primaryPersonaData.coreValues.map(value => `<li>${value}</li>`).join('')}
                </ul>
            </div>
            
            <div class="detail-section">
                <h4>Core Emotional Needs</h4>
                <ul>
                    ${Object.entries(primaryPersonaData.coreEmotionalNeeds)
                        .map(([key, value]) => `<li><strong>${key}:</strong> ${value}</li>`)
                        .join('')}
                </ul>
            </div>
            
            <div class="detail-section">
                <h4>Blind Spots</h4>
                <ul>
                    ${primaryPersonaData.blindSpots.map(spot => `<li>${spot}</li>`).join('')}
                </ul>
            </div>
            
            <div class="detail-section">
                <h4>Aspirations</h4>
                <ul>
                    ${primaryPersonaData.aspirations.map(aspiration => `<li>${aspiration}</li>`).join('')}
                </ul>
            </div>
            
            <div class="detail-section">
                <h4>Stress vs Growth</h4>
                <ul>
                    ${Object.entries(primaryPersonaData.stressVsGrowth)
                        .map(([key, value]) => `
                            <li>
                                <strong>${key}:</strong>
                                <ul>
                                    <li>Stress: ${value.stress}</li>
                                    <li>Growth: ${value.growth}</li>
                                    <li>Outcome: ${value.outcome}</li>
                                </ul>
                            </li>
                        `).join('')}
                </ul>
            </div>
            
            <div class="detail-section">
                <h4>Boundaries</h4>
                <ul>
                    <li><strong>Tendency:</strong> ${primaryPersonaData.boundaries.tendency}</li>
                    ${primaryPersonaData.boundaries.strugglesWith ? 
                        `<li><strong>Struggles With:</strong> ${primaryPersonaData.boundaries.strugglesWith}</li>` : ''}
                    <li><strong>Growth:</strong> ${primaryPersonaData.boundaries.growth}</li>
                </ul>
            </div>
            
            <div class="detail-section">
                <h4>Life Domain Impact</h4>
                <ul>
                    ${Object.entries(primaryPersonaData.lifeDomainImpact)
                        .map(([domain, impact]) => `<li><strong>${domain}:</strong> ${impact}</li>`)
                        .join('')}
                </ul>
            </div>
            
            <div class="detail-section">
                <h4>Potential</h4>
                <div class="potential-section">
                    <h5>Capabilities</h5>
                    <ul>
                        ${primaryPersonaData.potential.capabilities.map(capability => `<li>${capability}</li>`).join('')}
                    </ul>
                    
                    <h5>Life Changes</h5>
                    <ul>
                        ${Object.entries(primaryPersonaData.potential.lifeChanges)
                            .map(([domain, change]) => `<li><strong>${domain}:</strong> ${change}</li>`)
                            .join('')}
                    </ul>
                </div>
            </div>
        </div>
    `;
    resultsContainer.appendChild(primarySection);

    // Add secondary personas section
    const secondarySection = document.createElement('div');
    secondarySection.className = 'secondary-personas';
    secondarySection.innerHTML = '<h3>Your Secondary Persona Types</h3>';
    
    const secondaryList = document.createElement('ul');
    secondaryList.className = 'secondary-list';
    
    sortedPersonas.slice(1).forEach(({ type, score }) => {
        const personaData = personas[type];
        const percentage = Math.round((score / totalScore) * 100);
        
        const listItem = document.createElement('li');
        listItem.innerHTML = `
            <div class="secondary-persona">
                <h4>${personaData.name} (${percentage}%)</h4>
                <p>${personaData.description}</p>
            </div>
        `;
        secondaryList.appendChild(listItem);
    });
    
    secondarySection.appendChild(secondaryList);
    resultsContainer.appendChild(secondarySection);

    // Add styles
    const style = document.createElement('style');
    style.textContent = `
        .results-container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            font-family: Arial, sans-serif;
        }
        
        .results-container h2 {
            color: #333;
            text-align: center;
            margin-bottom: 20px;
        }
        
        .results-summary {
            margin-bottom: 30px;
            text-align: center;
        }
        
        .primary-persona {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
        }
        
        .primary-persona h3 {
            color: #2c3e50;
            margin-bottom: 15px;
        }
        
        .confidence-rating {
            margin: 15px 0;
            background: #e9ecef;
            height: 20px;
            border-radius: 10px;
            position: relative;
        }
        
        .confidence-bar {
            background: #4CAF50;
            height: 100%;
            border-radius: 10px;
            transition: width 1s ease-in-out;
        }
        
        .confidence-text {
            position: absolute;
            right: 10px;
            top: 50%;
            transform: translateY(-50%);
            color: #fff;
            font-weight: bold;
        }
        
        .persona-description {
            font-style: italic;
            margin-bottom: 20px;
        }
        
        .persona-details {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }
        
        .detail-section {
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .detail-section h4 {
            color: #2c3e50;
            margin-bottom: 10px;
            border-bottom: 2px solid #e9ecef;
            padding-bottom: 5px;
        }
        
        .detail-section ul {
            list-style-type: none;
            padding-left: 0;
        }
        
        .detail-section li {
            margin-bottom: 8px;
            line-height: 1.4;
        }
        
        .secondary-personas {
            margin-top: 30px;
        }
        
        .secondary-personas h3 {
            color: #2c3e50;
            margin-bottom: 15px;
        }
        
        .secondary-list {
            list-style-type: none;
            padding-left: 0;
        }
        
        .secondary-persona {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 15px;
        }
        
        .secondary-persona h4 {
            color: #2c3e50;
            margin-bottom: 10px;
        }
        
        .potential-section {
            margin-top: 15px;
        }
        
        .potential-section h5 {
            color: #2c3e50;
            margin: 10px 0;
        }
    `;
    document.head.appendChild(style);

    return resultsContainer;
}

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