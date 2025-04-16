// Question Bank
const questionBank = {
    initialSegmentation: [
        {
            id: 'Q101',
            text: 'What best describes your daily focus?',
            options: [
                { id: 'A101', text: 'Correctness and efficiency (Performance & Competency)' },
                { id: 'A102', text: 'Relationships and connections (Relationship & Connection)' },
                { id: 'A103', text: 'Freedom and independence (Control & Freedom)' }
            ]
        },
        {
            id: 'Q102',
            text: 'What primarily influences your decisions?',
            options: [
                { id: 'A104', text: 'Logic/principles' },
                { id: 'A105', text: 'Feelings/authenticity' },
                { id: 'A106', text: 'Freedom/security' }
            ]
        },
        {
            id: 'Q103',
            text: 'What situation causes you most discomfort?',
            options: [
                { id: 'A107', text: 'Being unprepared' },
                { id: 'A108', text: 'Being disconnected' },
                { id: 'A109', text: 'Losing control' }
            ]
        },
        {
            id: 'Q104',
            text: 'How open are you to change in your daily routine?',
            options: [
                { id: 'A110', text: 'Very open' },
                { id: 'A111', text: 'Somewhat open' },
                { id: 'A112', text: 'Prefer stability' }
            ]
        }
    ],
    detailedDifferentiation: {
        performance: [
            {
                id: 'Q201',
                text: 'What\'s essential to your work approach?',
                options: [
                    { id: 'A201', text: 'Ensuring high standards' },
                    { id: 'A202', text: 'Achieving impressive results' },
                    { id: 'A203', text: 'Understanding deeply first' }
                ]
            },
            {
                id: 'Q202',
                text: 'How do you react to constructive criticism?',
                options: [
                    { id: 'A204', text: 'Check if criticism is correct' },
                    { id: 'A205', text: 'Consider the impact on success' },
                    { id: 'A206', text: 'Seek more information' }
                ]
            }
        ],
        relationship: [
            {
                id: 'Q203',
                text: 'How do you respond to relationship tension?',
                options: [
                    { id: 'A207', text: 'Immediately help or resolve' },
                    { id: 'A208', text: 'Reflect emotionally for understanding' },
                    { id: 'A209', text: 'Quickly restore harmony' }
                ]
            },
            {
                id: 'Q204',
                text: 'What draws your attention in social settings?',
                options: [
                    { id: 'A210', text: 'Connect deeply' },
                    { id: 'A211', text: 'Seek unique meaning' },
                    { id: 'A212', text: 'Create comfort for everyone' }
                ]
            }
        ],
        control: [
            {
                id: 'Q205',
                text: 'What\'s your usual approach to authority figures?',
                options: [
                    { id: 'A213', text: 'Seek security or reassurance' },
                    { id: 'A214', text: 'Explore excitement and possibilities' },
                    { id: 'A215', text: 'Take immediate control' }
                ]
            },
            {
                id: 'Q206',
                text: 'How do you handle risky situations?',
                options: [
                    { id: 'A216', text: 'Feel anxious' },
                    { id: 'A217', text: 'Regain personal freedom' },
                    { id: 'A218', text: 'Assert yourself clearly' }
                ]
            }
        ]
    },
    typeConfirmation: [
        {
            id: 'Q301',
            text: 'How do you typically react under stress vs. at your best?',
            options: [
                { id: 'A301', text: 'Become more critical and demanding' },
                { id: 'A302', text: 'Withdraw and analyze' },
                { id: 'A303', text: 'Seek support and connection' }
            ]
        },
        {
            id: 'Q302',
            text: 'What fundamental drive resonates deeply?',
            options: [
                { id: 'A304', text: 'The need to be right and competent' },
                { id: 'A305', text: 'The need to be unique and authentic' },
                { id: 'A306', text: 'The need to be secure and stable' }
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

// State Management
let state = {
    currentPhase: 'registration',
    answers: {},
    startTime: Date.now(), // Initialize start time immediately
    phaseTimes: {},
    interactionCounts: {},
    confidenceScores: {}
};

// Metrics Tracking
const metrics = {
    startTimer: function(phase) {
        if (!state.phaseTimes[phase]) {
            state.phaseTimes[phase] = {
                start: Date.now(),
                end: null
            };
        }
    },
    endTimer: function(phase) {
        if (state.phaseTimes[phase] && !state.phaseTimes[phase].end) {
            state.phaseTimes[phase].end = Date.now();
        }
    },
    recordInteraction: function(phase) {
        state.interactionCounts[phase] = (state.interactionCounts[phase] || 0) + 1;
    },
    getTotalTime: function() {
        // Calculate total time from all completed phases
        let total = 0;
        Object.values(state.phaseTimes).forEach(time => {
            if (time.start && time.end) {
                total += (time.end - time.start);
            }
        });
        return Math.round(total / 1000); // Convert to seconds
    }
};

// UI Management
const ui = {
    showPhase: function(phase) {
        // End timer for current phase if exists
        if (state.currentPhase) {
            metrics.endTimer(state.currentPhase);
        }
        
        document.querySelectorAll('.phase').forEach(el => el.classList.remove('active'));
        document.getElementById(`${phase}-phase`).classList.add('active');
        
        // Start timer for new phase
        metrics.startTimer(phase);
        state.currentPhase = phase;
        
        // Special handling for detailed differentiation phase
        if (phase === 'detailed-differentiation') {
            // Determine which set of questions to show based on initial segmentation answers
            const initialAnswers = state.answers['initial-segmentation'] || {};
            let category = 'performance'; // Default category
            
            // Logic to determine category based on initial answers
            if (initialAnswers['qQ101'] === 'A102') {
                category = 'relationship';
            } else if (initialAnswers['qQ101'] === 'A103') {
                category = 'control';
            }
            
            this.renderDetailedDifferentiation(category);
        } else if (phase === 'initial-segmentation') {
            this.renderQuestions(phase, questionBank.initialSegmentation);
        } else if (phase === 'type-confirmation') {
            this.renderQuestions(phase, questionBank.typeConfirmation);
        } else if (phase === 'wing-type') {
            this.renderWingType();
        } else if (phase === 'instinctual-variant') {
            this.renderQuestions(phase, questionBank.instinctualVariant);
        } else if (phase === 'personalization') {
            this.renderQuestions(phase, questionBank.personalization);
        }
    },
    
    renderDetailedDifferentiation: function(category) {
        const container = document.getElementById('detailed-differentiation-questions');
        container.innerHTML = '';
        
        const questions = questionBank.detailedDifferentiation[category];
        
        // Add category indicator
        const categoryIndicator = document.createElement('div');
        categoryIndicator.className = 'alert alert-info mb-4';
        categoryIndicator.textContent = `Exploring ${category.charAt(0).toUpperCase() + category.slice(1)} aspects`;
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
        
        const nextButton = document.createElement('button');
        nextButton.className = 'btn btn-primary';
        nextButton.textContent = 'Next';
        nextButton.onclick = () => this.validateAndProceed('detailed-differentiation');
        container.appendChild(nextButton);
    },
    
    renderWingType: function() {
        const container = document.getElementById('wing-type-questions');
        container.innerHTML = '';
        
        // Calculate primary type based on previous answers
        const primaryType = this.calculatePrimaryType();
        console.log('Primary Type:', primaryType);
        
        // Get adjacent types
        const adjacentTypes = this.calculateAdjacentTypes(primaryType);
        console.log('Adjacent Types:', adjacentTypes);

        // Get descriptions for the wing types
        const wingDescriptions = {
            1: "Focused on doing things right, bringing structure and high standards",
            2: "Warm and caring, focused on helping and connecting with others",
            3: "Achievement-oriented, adaptable and image-conscious",
            4: "Emotionally deep, creative and authentic in expression",
            5: "Analytical and knowledgeable, seeking understanding",
            6: "Loyal and committed, focused on security and preparation",
            7: "Enthusiastic and adventurous, bringing positive energy",
            8: "Strong and protective, taking charge naturally",
            9: "Peace-seeking and inclusive, bringing harmony"
        };
        
        // Create the wing type question with warm, descriptive options
        const questionEl = document.createElement('div');
        questionEl.className = 'card mb-3';
        questionEl.innerHTML = `
            <div class="card-body">
                <h5 class="card-title">Wing Type Selection</h5>
                <p class="card-text">Your core type shows strong alignment with Type ${primaryType}. Which of these additional influences resonates more with your personality?</p>
                <div class="form-group">
                    <div class="form-check mb-4">
                        <input class="form-check-input" type="radio" 
                            name="qQ401" 
                            id="A401" 
                            value="A401">
                        <label class="form-check-label" for="A401">
                            <strong>Type ${adjacentTypes.wings[0]} Wing:</strong><br>
                            <p class="text-muted mb-0">${wingDescriptions[adjacentTypes.wings[0]]}</p>
                            <small class="text-muted">This influence adds ${this.getWingInfluence(primaryType, adjacentTypes.wings[0])}</small>
                        </label>
                    </div>
                    <div class="form-check mb-4">
                        <input class="form-check-input" type="radio" 
                            name="qQ401" 
                            id="A402" 
                            value="A402">
                        <label class="form-check-label" for="A402">
                            <strong>Type ${adjacentTypes.wings[1]} Wing:</strong><br>
                            <p class="text-muted mb-0">${wingDescriptions[adjacentTypes.wings[1]]}</p>
                            <small class="text-muted">This influence adds ${this.getWingInfluence(primaryType, adjacentTypes.wings[1])}</small>
                        </label>
                    </div>
                </div>
            </div>
        `;
        container.appendChild(questionEl);

        // Add next button
        const nextButton = document.createElement('button');
        nextButton.className = 'btn btn-primary';
        nextButton.textContent = 'Next';
        nextButton.onclick = () => this.validateAndProceed('wing-type');
        container.appendChild(nextButton);
    },
    
    calculateAdjacentTypes: function(primaryType) {
        // Convert primaryType to number if it's a string
        primaryType = parseInt(primaryType);
        
        // Define the Enneagram connections
        const connections = {
            1: { integration: 7, disintegration: 4, wings: [9, 2] },
            2: { integration: 4, disintegration: 8, wings: [1, 3] },
            3: { integration: 6, disintegration: 9, wings: [2, 4] },
            4: { integration: 1, disintegration: 2, wings: [3, 5] },
            5: { integration: 8, disintegration: 7, wings: [4, 6] },
            6: { integration: 9, disintegration: 3, wings: [5, 7] },
            7: { integration: 5, disintegration: 1, wings: [6, 8] },
            8: { integration: 2, disintegration: 5, wings: [7, 9] },
            9: { integration: 3, disintegration: 6, wings: [8, 1] }
        };

        return connections[primaryType] || { 
            integration: null, 
            disintegration: null, 
            wings: [null, null] 
        };
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
        const container = document.getElementById(`${phase}-questions`);
        container.innerHTML = '';
        
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
        
        const nextButton = document.createElement('button');
        nextButton.className = 'btn btn-primary';
        nextButton.textContent = 'Next';
        nextButton.onclick = () => this.validateAndProceed(phase);
        container.appendChild(nextButton);
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
    proceedToNextPhase: function(currentPhase) {
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
            this.showPhase(nextPhase);
            
            // Special handling for results phase
            if (nextPhase === 'results') {
                this.renderResults();
            }
        }
    },
    renderResults: function() {
        const container = document.getElementById('persona-details');
        if (!container) return;

        // Calculate primary type
        const primaryType = this.calculatePrimaryType();
        const wingType = state.answers['wing-type'] ? 
            this.getTypeDescription(parseInt(state.answers['wing-type']['qQ401'].replace('A40', ''))) :
            'Not determined';
        
        // Calculate instinctual variant
        const instinctualVariant = this.calculateInstinctualVariant();
        
        // Calculate confidence score
        const confidenceScore = this.calculateOverallConfidence();

        // Get detailed persona description
        const personaDescription = this.getPersonaDescription(primaryType);

        // Create the results HTML
        container.innerHTML = `
            <div class="results-section mb-4">
                <h4 class="text-primary mb-3">Core Type</h4>
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">${this.getTypeDescription(primaryType)}</h5>
                        <p class="card-text">Your core type reflects your fundamental motivations and patterns.</p>
                        <div class="progress mb-3">
                            <div class="progress-bar bg-success" role="progressbar" 
                                style="width: ${confidenceScore}%" 
                                aria-valuenow="${confidenceScore}" 
                                aria-valuemin="0" 
                                aria-valuemax="100">
                                ${confidenceScore}% Confidence
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="results-section mb-4">
                <h4 class="text-primary mb-3">Persona Description</h4>
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Your Core Characteristics</h5>
                        <div class="persona-description">
                            ${personaDescription}
                        </div>
                        <div class="confirmation-section mt-4">
                            <p class="text-muted">Does this description resonate with you?</p>
                            <div class="btn-group" role="group">
                                <button type="button" class="btn btn-success" onclick="ui.confirmPersona(true)">
                                    Yes, this describes me well
                                </button>
                                <button type="button" class="btn btn-danger" onclick="ui.confirmPersona(false)">
                                    No, this doesn't feel right
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="results-section mb-4">
                <h4 class="text-primary mb-3">Wing Influence</h4>
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Wing: ${wingType}</h5>
                        <p class="card-text">Your wing adds nuance and depth to your core type.</p>
                    </div>
                </div>
            </div>

            <div class="results-section mb-4">
                <h4 class="text-primary mb-3">Instinctual Variant</h4>
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">${instinctualVariant.variant}</h5>
                        <p class="card-text">This reflects your primary survival strategy and focus of attention.</p>
                    </div>
                </div>
            </div>

            <div class="results-section mb-4">
                <h4 class="text-primary mb-3">Growth Areas</h4>
                <div class="card">
                    <div class="card-body">
                        ${this.generateGrowthAreas(primaryType)}
                    </div>
                </div>
            </div>

            <div class="mt-4">
                <button class="btn btn-primary me-2" onclick="ui.showMetricsDashboard()">View Assessment Metrics</button>
                <button class="btn btn-outline-primary" onclick="ui.exportResults()">Export Results</button>
            </div>
        `;
    },
    calculatePrimaryType: function() {
        const initialAnswers = state.answers['initial-segmentation'] || {};
        const detailedAnswers = state.answers['detailed-differentiation'] || {};
        const confirmationAnswers = state.answers['type-confirmation'] || {};

        // Initialize scores for all types
        let typeScores = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0};

        // Score based on initial segmentation (weight: 3)
        if (initialAnswers['qQ101'] === 'A101') {
            typeScores[1] += 3;
            typeScores[5] += 2;
        }
        if (initialAnswers['qQ101'] === 'A102') {
            typeScores[2] += 3;
            typeScores[4] += 2;
        }
        if (initialAnswers['qQ101'] === 'A103') {
            typeScores[8] += 3;
            typeScores[7] += 2;
        }

        if (initialAnswers['qQ102'] === 'A104') {
            typeScores[1] += 2;
            typeScores[6] += 1;
        }
        if (initialAnswers['qQ102'] === 'A105') {
            typeScores[2] += 2;
            typeScores[9] += 1;
        }
        if (initialAnswers['qQ102'] === 'A106') {
            typeScores[3] += 2;
            typeScores[8] += 1;
        }

        if (initialAnswers['qQ103'] === 'A107') {
            typeScores[5] += 2;
            typeScores[1] += 1;
        }
        if (initialAnswers['qQ103'] === 'A108') {
            typeScores[4] += 2;
            typeScores[2] += 1;
        }
        if (initialAnswers['qQ103'] === 'A109') {
            typeScores[7] += 2;
            typeScores[3] += 1;
        }

        // Score based on detailed differentiation (weight: 4)
        if (detailedAnswers['qQ201'] === 'A201') typeScores[1] += 4;
        if (detailedAnswers['qQ201'] === 'A202') typeScores[3] += 4;
        if (detailedAnswers['qQ201'] === 'A203') typeScores[5] += 4;

        if (detailedAnswers['qQ202'] === 'A204') typeScores[1] += 4;
        if (detailedAnswers['qQ202'] === 'A205') typeScores[3] += 4;
        if (detailedAnswers['qQ202'] === 'A206') typeScores[5] += 4;

        // Score based on type confirmation (weight: 5)
        if (confirmationAnswers['qQ301'] === 'A301') typeScores[1] += 5;
        if (confirmationAnswers['qQ301'] === 'A302') typeScores[5] += 5;
        if (confirmationAnswers['qQ301'] === 'A303') typeScores[2] += 5;

        if (confirmationAnswers['qQ302'] === 'A304') typeScores[1] += 5;
        if (confirmationAnswers['qQ302'] === 'A305') typeScores[4] += 5;
        if (confirmationAnswers['qQ302'] === 'A306') typeScores[6] += 5;

        // Find the type with highest score
        const maxType = Object.entries(typeScores).reduce((a, b) => a[1] > b[1] ? a : b);
        
        // Calculate confidence based on score difference
        const sortedScores = Object.values(typeScores).sort((a, b) => b - a);
        const scoreDifference = sortedScores[0] - sortedScores[1];
        const maxPossibleScore = 30; // Sum of all weights
        const confidence = Math.min(100, Math.round((scoreDifference / maxPossibleScore) * 100));
        
        state.confidenceScores['primary-type'] = confidence;
        
        return parseInt(maxType[0]);
    },
    calculateInstinctualVariant: function() {
        const answers = state.answers['instinctual-variant'] || {};
        
        const variants = {
            'self-preservation': 0,
            'social': 0,
            'one-to-one': 0
        };

        // First question (weight: 3)
        if (answers['qQ501'] === 'A501') variants['self-preservation'] += 3;
        if (answers['qQ501'] === 'A502') variants['one-to-one'] += 3;
        if (answers['qQ501'] === 'A503') variants['social'] += 3;

        // Second question (weight: 2)
        if (answers['qQ502'] === 'A504') variants['self-preservation'] += 2;
        if (answers['qQ502'] === 'A505') variants['one-to-one'] += 2;
        if (answers['qQ502'] === 'A506') variants['social'] += 2;

        // Find the primary variant
        const maxVariant = Object.entries(variants).reduce((a, b) => a[1] > b[1] ? a : b);
        
        // Calculate confidence
        const sortedScores = Object.values(variants).sort((a, b) => b - a);
        const scoreDifference = sortedScores[0] - sortedScores[1];
        const maxPossibleScore = 5; // Sum of weights
        const confidence = Math.min(100, Math.round((scoreDifference / maxPossibleScore) * 100));
        
        state.confidenceScores['instinctual-variant'] = confidence;
        
        const variantNames = {
            'self-preservation': 'Self-Preservation',
            'social': 'Social',
            'one-to-one': 'One-to-One'
        };

        return {
            variant: variantNames[maxVariant[0]],
            confidence: confidence
        };
    },
    calculateOverallConfidence: function() {
        const weights = {
            'primary-type': 0.5,      // Primary type is most important
            'wing-type': 0.2,         // Wing type is secondary
            'instinctual-variant': 0.3 // Instinctual variant is also important
        };

        let totalWeight = 0;
        let weightedSum = 0;

        // Calculate weighted average of all confidence scores
        for (const [component, weight] of Object.entries(weights)) {
            if (state.confidenceScores[component] !== undefined) {
                weightedSum += state.confidenceScores[component] * weight;
                totalWeight += weight;
            }
        }

        // If no scores are available, return minimum confidence
        if (totalWeight === 0) return 50;

        // Calculate final confidence score and ensure it's between 50-100
        const overallConfidence = Math.round(weightedSum / totalWeight);
        return Math.max(50, Math.min(100, overallConfidence));
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
        // Calculate total time from all phases
        const totalSeconds = metrics.getTotalTime();
        
        // Format total time display
        const totalTimeText = totalSeconds < 60 
            ? `${totalSeconds} seconds` 
            : `${Math.floor(totalSeconds / 60)} minutes ${totalSeconds % 60} seconds`;
        document.getElementById('total-time').textContent = totalTimeText;
        
        // Calculate questions answered
        const totalQuestions = Object.values(state.answers).reduce((sum, phase) => 
            sum + Object.keys(phase).length, 0);
        
        // Calculate and format average time
        const avgSeconds = totalQuestions > 0 ? Math.round(totalSeconds / totalQuestions) : 0;
        const avgTimeText = `${avgSeconds} seconds`;
        document.getElementById('avg-time-per-question').textContent = avgTimeText;
        
        // Update other metrics
        document.getElementById('questions-answered').textContent = totalQuestions;
        document.getElementById('confidence-score').textContent = this.calculateOverallConfidence();
        
        // Update charts
        this.updateCharts();
    },
    updateCharts: function() {
        const timeCtx = document.getElementById('timeChart').getContext('2d');
        
        // Calculate phase durations
        const timeData = Object.entries(state.phaseTimes).map(([phase, time]) => ({
            phase: phase,
            duration: time.end ? Math.max(0, Math.round((time.end - time.start) / 1000)) : 
                (time.start ? Math.max(0, Math.round((Date.now() - time.start) / 1000)) : 0)
        }));

        new Chart(timeCtx, {
            type: 'bar',
            data: {
                labels: timeData.map(d => this.formatPhaseLabel(d.phase)),
                datasets: [{
                    label: 'Time per Phase (seconds)',
                    data: timeData.map(d => d.duration),
                    backgroundColor: 'rgba(54, 162, 235, 0.5)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Seconds'
                        }
                    }
                },
                plugins: {
                    title: {
                        display: true,
                        text: 'Time Spent per Assessment Phase'
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const seconds = context.raw;
                                if (seconds < 60) {
                                    return `${seconds} seconds`;
                                }
                                const minutes = Math.floor(seconds / 60);
                                const remainingSeconds = seconds % 60;
                                return `${minutes}m ${remainingSeconds}s`;
                            }
                        }
                    }
                }
            }
        });
        
        // Completion chart - now showing answer distribution by type
        const completionCtx = document.getElementById('completionChart').getContext('2d');
        
        // Calculate answer distribution by type
        const typeDistribution = this.calculateTypeDistribution();
        
        new Chart(completionCtx, {
            type: 'pie',
            data: {
                labels: Object.keys(typeDistribution).map(type => `Type ${type}`),
                datasets: [{
                    data: Object.values(typeDistribution),
                    backgroundColor: [
                        '#FF6384',
                        '#36A2EB',
                        '#FFCE56',
                        '#4BC0C0',
                        '#9966FF',
                        '#FF9F40',
                        '#8AC24A',
                        '#FF6B6B',
                        '#47B8E0'
                    ]
                }]
            },
            options: {
                plugins: {
                    title: {
                        display: true,
                        text: 'Answer Distribution by Type'
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const type = context.label;
                                const value = context.raw;
                                return `${type}: ${value} answers`;
                            }
                        }
                    }
                }
            }
        });
        
        // Interaction chart
        const interactionCtx = document.getElementById('interactionChart').getContext('2d');
        new Chart(interactionCtx, {
            type: 'line',
            data: {
                labels: Object.keys(state.interactionCounts),
                datasets: [{
                    label: 'Interactions per Phase',
                    data: Object.values(state.interactionCounts)
                }]
            }
        });
    },
    calculateTypeDistribution: function() {
        const distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0};
        
        // Map of answer IDs to their corresponding types
        const answerTypeMap = {
            // Initial Segmentation (Q101-Q104)
            'A101': [1, 5], // Both Type 1 and 5 tendencies
            'A102': [2, 4], // Both Type 2 and 4 tendencies
            'A103': [8, 7], // Both Type 8 and 7 tendencies
            'A104': [1, 6], // Logic/principles
            'A105': [4, 2], // Feelings/authenticity
            'A106': [8, 3], // Freedom/security
            'A107': [1, 5], // Being unprepared
            'A108': [2, 4], // Being disconnected
            'A109': [8, 7], // Losing control
            'A110': [7, 3], // Very open to change
            'A111': [9, 6], // Somewhat open
            'A112': [1, 6], // Prefer stability
            
            // Detailed Differentiation - Performance (Q201-Q202)
            'A201': [1, 3], // High standards
            'A202': [3, 8], // Impressive results
            'A203': [5, 4], // Understanding deeply
            'A204': [1, 5], // Check criticism
            'A205': [3, 7], // Impact on success
            'A206': [5, 6], // Seek information
            
            // Detailed Differentiation - Relationship (Q203-Q204)
            'A207': [2, 9], // Help or resolve
            'A208': [4, 2], // Emotional reflection
            'A209': [9, 7], // Restore harmony
            'A210': [2, 6], // Connect deeply
            'A211': [4, 5], // Unique meaning
            'A212': [9, 2], // Create comfort
            
            // Detailed Differentiation - Control (Q205-Q206)
            'A213': [6, 9], // Security/reassurance
            'A214': [7, 3], // Excitement/possibilities
            'A215': [8, 1], // Take control
            'A216': [6, 5], // Feel anxious
            'A217': [7, 4], // Regain freedom
            'A218': [8, 3], // Assert yourself
            
            // Type Confirmation (Q301-Q302)
            'A301': [1, 3], // Critical under stress
            'A302': [5, 4], // Withdraw and analyze
            'A303': [2, 6], // Seek support
            'A304': [1, 5], // Need to be right
            'A305': [4, 7], // Need to be unique
            'A306': [6, 9]  // Need to be secure
        };

        // Count answers for each type, including secondary influences
        Object.values(state.answers).forEach(phaseAnswers => {
            Object.values(phaseAnswers).forEach(answerId => {
                const types = answerTypeMap[answerId];
                if (types) {
                    // Primary type gets 1 point, secondary type gets 0.5 points
                    distribution[types[0]] += 1;
                    if (types[1]) {
                        distribution[types[1]] += 0.5;
                    }
                }
            });
        });

        // Round the numbers to 1 decimal place
        Object.keys(distribution).forEach(type => {
            distribution[type] = Math.round(distribution[type] * 10) / 10;
        });

        return distribution;
    },
    getPersonaDescription: function(type) {
        const descriptions = {
            1: `
                <p>You're someone who values doing things the right way. You have a strong inner compass that guides you toward excellence and integrity in everything you do. While others might cut corners, you take pride in maintaining high standards and paying attention to the details that matter.</p>
                <p>What drives you is a deep desire to make things better - whether it's improving a process, fixing an error, or upholding important principles. You're naturally responsible and reliable, often taking on the role of ensuring things are done properly.</p>
                <p>Your attention to detail and commitment to quality make you someone others can depend on. You bring structure and order to chaotic situations, and your dedication to doing things right often inspires those around you to raise their own standards.</p>
                <p><strong>Challenges & Pain Points:</strong></p>
                <ul>
                    <li>You might struggle with perfectionism, sometimes spending too much time on details</li>
                    <li>It can be hard to delegate when you believe you can do something better</li>
                    <li>You may feel frustrated when others don't share your high standards</li>
                    <li>Balancing your need for order with flexibility can be challenging</li>
                </ul>
                <p><strong>Core Needs & Their Impact:</strong></p>
                <ul>
                    <li><strong>Certainty:</strong> Your need for clear standards and predictable outcomes drives your attention to detail, but can also lead to perfectionism when things don't meet your expectations.</li>
                    <li><strong>Significance:</strong> You want to be recognized for your competence and integrity, which motivates your high standards, but can make criticism particularly difficult to handle.</li>
                    <li><strong>Growth:</strong> Your drive to improve yourself and your environment fuels your dedication to excellence, but can make it hard to accept things as "good enough."</li>
                    <li><strong>Connection:</strong> You value relationships built on mutual respect and shared values, which can make it challenging when others don't share your standards.</li>
                    <li><strong>Contribution:</strong> Your desire to make a positive impact through your work drives your reliability, but can lead to taking on too much responsibility.</li>
                    <li><strong>Variety:</strong> You seek new challenges that allow you to demonstrate excellence, but may struggle when these challenges require flexibility or compromise.</li>
                </ul>
            `,
            2: `
                <p>You're someone who naturally puts others first. You have an intuitive understanding of what people need, often before they realize it themselves. Your warmth and generosity create strong connections with those around you.</p>
                <p>What drives you is the joy of helping others and creating meaningful relationships. You thrive when you can make a positive difference in someone's life, whether through practical support, emotional understanding, or simply being there when needed.</p>
                <p>Your ability to connect with others and your generous spirit make you a natural caregiver and friend. People often turn to you for support because they know you'll listen with empathy and offer help without judgment.</p>
                <p><strong>Challenges & Pain Points:</strong></p>
                <ul>
                    <li>You might neglect your own needs while focusing on others</li>
                    <li>It can be hard to say no when others need help</li>
                    <li>You may feel unappreciated when your efforts aren't recognized</li>
                    <li>Setting boundaries in relationships can be difficult</li>
                </ul>
                <p><strong>Core Needs & Their Impact:</strong></p>
                <ul>
                    <li><strong>Connection:</strong> Your need for deep, meaningful relationships drives your generosity, but can make it hard to set boundaries when others need help.</li>
                    <li><strong>Significance:</strong> You want to feel valued and appreciated for your help, which motivates your caring nature, but can lead to feeling unappreciated when efforts go unnoticed.</li>
                    <li><strong>Growth:</strong> Your drive to develop deeper emotional connections fuels your empathy, but can make it challenging to maintain your own emotional boundaries.</li>
                    <li><strong>Certainty:</strong> Your need to feel secure in your relationships drives your helpfulness, but can make you anxious when relationships feel uncertain.</li>
                    <li><strong>Contribution:</strong> Your desire to make a difference in others' lives motivates your support, but can lead to neglecting your own needs.</li>
                    <li><strong>Variety:</strong> You enjoy new ways to help and connect with people, but may struggle when these new ways require setting limits.</li>
                </ul>
            `,
            3: `
                <p>You're someone who's driven to succeed and make an impact. You have a natural ability to adapt to different situations and present your best self. Your energy and focus help you achieve your goals efficiently.</p>
                <p>What drives you is the desire to excel and be recognized for your accomplishments. You're motivated by challenges and opportunities to prove your capabilities. You have a knack for identifying what needs to be done and doing it well.</p>
                <p>Your ability to get things done and your natural charisma make you an effective leader and team player. You inspire others with your work ethic and your ability to turn goals into reality.</p>
                <p><strong>Challenges & Pain Points:</strong></p>
                <ul>
                    <li>You might struggle with work-life balance</li>
                    <li>It can be hard to slow down and be present in the moment</li>
                    <li>You may feel pressure to maintain a perfect image</li>
                    <li>Failure or criticism can be particularly difficult to handle</li>
                </ul>
                <p><strong>Core Needs & Their Impact:</strong></p>
                <ul>
                    <li><strong>Significance:</strong> Your need to be recognized for your achievements drives your success, but can make failure or criticism particularly painful.</li>
                    <li><strong>Growth:</strong> Your drive to constantly improve and succeed fuels your ambition, but can make it hard to slow down and be present.</li>
                    <li><strong>Variety:</strong> You thrive on new challenges and opportunities, which keeps you motivated, but can lead to difficulty maintaining focus on long-term projects.</li>
                    <li><strong>Certainty:</strong> Your need to feel in control of your success drives your planning, but can make unexpected setbacks difficult to handle.</li>
                    <li><strong>Connection:</strong> You value relationships that support your goals, which helps your success, but can make it hard to develop deeper emotional connections.</li>
                    <li><strong>Contribution:</strong> Your desire to make an impact through your success motivates your achievements, but can lead to work-life imbalance.</li>
                </ul>
            `,
            4: `
                <p>You're someone who experiences emotions deeply and values authenticity above all else. You have a rich inner world and a unique perspective that sets you apart. Your sensitivity to beauty and meaning in the world around you is a gift.</p>
                <p>What drives you is the need to express your true self and create something meaningful. You're drawn to depth and authenticity in all aspects of life, whether in relationships, art, or personal expression.</p>
                <p>Your emotional depth and creative spirit allow you to see beauty and meaning where others might not. You bring a unique perspective to situations and help others connect with their own authentic selves.</p>
                <p><strong>Challenges & Pain Points:</strong></p>
                <ul>
                    <li>You might struggle with intense emotional highs and lows</li>
                    <li>It can be hard to feel understood by others</li>
                    <li>You may feel different or isolated from those around you</li>
                    <li>Balancing idealism with reality can be challenging</li>
                </ul>
                <p><strong>Core Needs & Their Impact:</strong></p>
                <ul>
                    <li><strong>Connection:</strong> Your need for deep, authentic relationships drives your emotional expression, but can make you feel isolated when others don't understand your depth.</li>
                    <li><strong>Significance:</strong> You want to be valued for your unique perspective, which motivates your authenticity, but can make you feel different from others.</li>
                    <li><strong>Growth:</strong> Your drive to understand yourself deeply fuels your introspection, but can lead to intense emotional highs and lows.</li>
                    <li><strong>Variety:</strong> You seek new emotional and creative experiences, which enriches your life, but can make it hard to find stability.</li>
                    <li><strong>Contribution:</strong> Your desire to share your unique gifts with the world motivates your creativity, but can make you vulnerable to criticism.</li>
                    <li><strong>Certainty:</strong> Your need to feel secure in your identity drives your self-expression, but can make it challenging when your identity feels uncertain.</li>
                </ul>
            `,
            5: `
                <p>You're someone who values knowledge and understanding. You have a natural curiosity about how things work and enjoy diving deep into subjects that interest you. Your ability to analyze and think independently is a strength.</p>
                <p>What drives you is the desire to understand the world around you. You're motivated by the pursuit of knowledge and the satisfaction of solving complex problems. You value your independence and the space to think deeply.</p>
                <p>Your analytical mind and thirst for knowledge make you an excellent problem-solver and researcher. You bring clarity and insight to complex situations, helping others see patterns and connections they might have missed.</p>
                <p><strong>Challenges & Pain Points:</strong></p>
                <ul>
                    <li>You might struggle with emotional expression</li>
                    <li>It can be hard to engage in small talk or social situations</li>
                    <li>You may feel overwhelmed by too much social interaction</li>
                    <li>Balancing intellectual pursuits with practical needs can be challenging</li>
                </ul>
                <p><strong>Core Needs & Their Impact:</strong></p>
                <ul>
                    <li><strong>Growth:</strong> Your need to constantly expand your knowledge drives your curiosity, but can make it hard to focus on practical matters.</li>
                    <li><strong>Certainty:</strong> Your desire to understand how things work fuels your analysis, but can lead to overthinking in social situations.</li>
                    <li><strong>Connection:</strong> You value intellectual connections with others, which helps your understanding, but can make emotional connections challenging.</li>
                    <li><strong>Significance:</strong> You want to be recognized for your expertise, which motivates your learning, but can make you reluctant to share incomplete knowledge.</li>
                    <li><strong>Variety:</strong> You enjoy exploring new ideas and concepts, which stimulates your mind, but can make it hard to stay focused on one topic.</li>
                    <li><strong>Contribution:</strong> Your desire to share your knowledge with others drives your teaching, but can make you feel drained by too much social interaction.</li>
                </ul>
            `,
            6: `
                <p>You're someone who's both loyal and cautious. You have a strong sense of responsibility and a keen eye for potential problems. Your ability to anticipate challenges and prepare for them is valuable.</p>
                <p>What drives you is the need for security and reliable guidance. You're motivated by creating stable, trustworthy relationships and environments. You value loyalty and commitment, both giving and receiving it.</p>
                <p>Your careful approach and commitment to others make you a reliable team member and friend. You help create stability and security in your relationships and environments, often being the one who thinks through potential challenges.</p>
                <p><strong>Challenges & Pain Points:</strong></p>
                <ul>
                    <li>You might struggle with anxiety and overthinking</li>
                    <li>It can be hard to trust your own judgment</li>
                    <li>You may feel overwhelmed by uncertainty</li>
                    <li>Balancing caution with action can be challenging</li>
                </ul>
                <p><strong>Core Needs & Their Impact:</strong></p>
                <ul>
                    <li><strong>Certainty:</strong> Your need for security and predictability drives your planning, but can lead to anxiety when things feel uncertain.</li>
                    <li><strong>Connection:</strong> You value trustworthy relationships, which helps you feel secure, but can make it hard to trust your own judgment.</li>
                    <li><strong>Growth:</strong> Your desire to develop confidence in your decisions motivates your preparation, but can lead to overthinking.</li>
                    <li><strong>Significance:</strong> You need to feel valued for your reliability, which drives your commitment, but can make you doubt your worth when things go wrong.</li>
                    <li><strong>Contribution:</strong> Your desire to help create stability for others motivates your support, but can make you feel responsible for things beyond your control.</li>
                    <li><strong>Variety:</strong> You enjoy new challenges within safe boundaries, which helps you grow, but can make you anxious when boundaries feel unclear.</li>
                </ul>
            `,
            7: `
                <p>You're someone who embraces life with enthusiasm and curiosity. You have a natural ability to see possibilities and opportunities everywhere. Your energy and optimism are infectious.</p>
                <p>What drives you is the desire for new experiences and the freedom to explore them. You're motivated by variety, excitement, and the joy of discovery. You have a talent for finding the positive in any situation.</p>
                <p>Your enthusiasm and creativity make you a natural problem-solver and idea generator. You help others see opportunities and possibilities, bringing energy and optimism to challenging situations.</p>
                <p><strong>Challenges & Pain Points:</strong></p>
                <ul>
                    <li>You might struggle with commitment to long-term projects</li>
                    <li>It can be hard to stay focused on one thing</li>
                    <li>You may avoid dealing with difficult emotions</li>
                    <li>Balancing freedom with responsibility can be challenging</li>
                </ul>
                <p><strong>Core Needs & Their Impact:</strong></p>
                <ul>
                    <li><strong>Variety:</strong> Your need for new experiences drives your enthusiasm, but can make it hard to commit to long-term projects.</li>
                    <li><strong>Growth:</strong> Your drive to explore and learn new things fuels your curiosity, but can lead to scattered focus.</li>
                    <li><strong>Connection:</strong> You value fun and stimulating relationships, which energizes you, but can make deep emotional connections challenging.</li>
                    <li><strong>Significance:</strong> You want to be recognized for your creativity, which motivates your ideas, but can make you avoid difficult situations.</li>
                    <li><strong>Contribution:</strong> Your desire to bring joy to others drives your optimism, but can make it hard to deal with negative emotions.</li>
                    <li><strong>Certainty:</strong> Your need for freedom to explore fuels your spontaneity, but can make responsibility feel restrictive.</li>
                </ul>
            `,
            8: `
                <p>You're someone who's direct, decisive, and protective. You have a natural confidence and strength that others often rely on. Your ability to take charge and make tough decisions is valuable.</p>
                <p>What drives you is the need to be strong and in control of your environment. You're motivated by protecting what matters to you and standing up for what's right. You value honesty and directness in all your interactions.</p>
                <p>Your strength and decisiveness make you a natural leader and protector. You help create security and stability for those around you, often being the one who takes charge in difficult situations.</p>
                <p><strong>Challenges & Pain Points:</strong></p>
                <ul>
                    <li>You might struggle with vulnerability</li>
                    <li>It can be hard to trust others</li>
                    <li>You may come across as too intense or controlling</li>
                    <li>Balancing strength with sensitivity can be challenging</li>
                </ul>
                <p><strong>Core Needs & Their Impact:</strong></p>
                <ul>
                    <li><strong>Significance:</strong> Your need to feel strong and in control drives your leadership, but can make vulnerability feel like weakness.</li>
                    <li><strong>Connection:</strong> You value loyalty and trust in relationships, which helps you protect others, but can make it hard to trust new people.</li>
                    <li><strong>Growth:</strong> Your desire to develop emotional intelligence motivates your self-awareness, but can make sensitivity feel challenging.</li>
                    <li><strong>Certainty:</strong> Your need to feel secure in your environment drives your control, but can make you come across as too intense.</li>
                    <li><strong>Contribution:</strong> Your desire to protect and empower others motivates your strength, but can make it hard to let others take charge.</li>
                    <li><strong>Variety:</strong> You enjoy challenges that test your strength, which keeps you engaged, but can make routine situations feel boring.</li>
                </ul>
            `,
            9: `
                <p>You're someone who values peace and harmony. You have a natural ability to see different perspectives and find common ground. Your calm presence and acceptance of others create a welcoming environment.</p>
                <p>What drives you is the desire to maintain balance and avoid conflict. You're motivated by creating harmony in your relationships and environments. You value stability and the comfort of familiar routines.</p>
                <p>Your ability to mediate and create harmony makes you a valuable team member and friend. You help others find common ground and maintain peaceful relationships, often being the one who smooths over tensions and keeps things running smoothly.</p>
                <p><strong>Challenges & Pain Points:</strong></p>
                <ul>
                    <li>You might struggle with asserting your needs</li>
                    <li>It can be hard to deal with conflict</li>
                    <li>You may avoid making difficult decisions</li>
                    <li>Balancing others' needs with your own can be challenging</li>
                </ul>
                <p><strong>Core Needs & Their Impact:</strong></p>
                <ul>
                    <li><strong>Connection:</strong> Your need for harmonious relationships drives your peacemaking, but can make it hard to assert your own needs.</li>
                    <li><strong>Certainty:</strong> Your desire for stability and peace fuels your mediation, but can make conflict feel threatening.</li>
                    <li><strong>Growth:</strong> Your drive to develop assertiveness motivates your self-awareness, but can make difficult decisions feel overwhelming.</li>
                    <li><strong>Significance:</strong> You want to be valued for your peacemaking, which helps create harmony, but can make you avoid standing out.</li>
                    <li><strong>Contribution:</strong> Your desire to create harmony for others drives your support, but can lead to neglecting your own needs.</li>
                    <li><strong>Variety:</strong> You enjoy gentle changes within familiar patterns, which helps you adapt, but can make major changes feel disruptive.</li>
                </ul>
            `
        };

        return descriptions[type] || '<p>Description not available for this type.</p>';
    },
    confirmPersona: function(confirmed) {
        const confirmationSection = document.querySelector('.confirmation-section');
        if (confirmed) {
            confirmationSection.innerHTML = `
                <div class="alert alert-success">
                    <h5>Thank you for confirming!</h5>
                    <p>Your feedback helps us improve the assessment accuracy.</p>
                </div>
            `;
        } else {
            confirmationSection.innerHTML = `
                <div class="alert alert-warning">
                    <h5>We appreciate your feedback</h5>
                    <p>Would you like to:</p>
                    <div class="btn-group" role="group">
                        <button type="button" class="btn btn-outline-primary" onclick="ui.showPhase('initial-segmentation')">
                            Retake the assessment
                        </button>
                        <button type="button" class="btn btn-outline-secondary" onclick="ui.showFeedbackForm()">
                            Provide detailed feedback
                        </button>
                    </div>
                </div>
            `;
        }
    },
    showFeedbackForm: function() {
        const confirmationSection = document.querySelector('.confirmation-section');
        confirmationSection.innerHTML = `
            <div class="alert alert-info">
                <h5>Help us improve</h5>
                <form id="feedback-form">
                    <div class="mb-3">
                        <label for="feedback" class="form-label">What aspects of the description don't match your experience?</label>
                        <textarea class="form-control" id="feedback" rows="3"></textarea>
                    </div>
                    <div class="mb-3">
                        <label for="suggested-type" class="form-label">Which type do you think better describes you?</label>
                        <select class="form-select" id="suggested-type">
                            <option value="">Select a type</option>
                            ${Object.entries(this.getTypeDescription).map(([type, desc]) => 
                                `<option value="${type}">Type ${type}: ${desc.split(' - ')[0]}</option>`
                            ).join('')}
                        </select>
                    </div>
                    <button type="submit" class="btn btn-primary">Submit Feedback</button>
                </form>
            </div>
        `;

        document.getElementById('feedback-form').addEventListener('submit', function(e) {
            e.preventDefault();
            const feedback = {
                text: document.getElementById('feedback').value,
                suggestedType: document.getElementById('suggested-type').value
            };
            // Here you would typically send this feedback to your backend
            confirmationSection.innerHTML = `
                <div class="alert alert-success">
                    <h5>Thank you for your feedback!</h5>
                    <p>We'll use this information to improve our assessment.</p>
                </div>
            `;
        });
    },
    renderWelcome: function() {
        const container = document.getElementById('welcome-phase');
        container.innerHTML = `
            <div class="welcome-container">
                <h1 class="text-center mb-4">Onboard Demo</h1>
                <div class="card">
                    <div class="card-body">
                        <div class="text-center mt-4">
                            <button class="btn btn-primary" onclick="ui.showPhase('initial-segmentation')">Begin Assessment</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
    },
    getWingInfluence: function(primaryType, wingType) {
        const influences = {
            '1-9': "more adaptability and ability to go with the flow",
            '1-2': "more warmth and consideration for others' feelings",
            '2-1': "more structure and principle-based decision making",
            '2-3': "more focus on personal achievement and presentation",
            '3-2': "more emotional awareness and helping tendencies",
            '3-4': "more creativity and emotional depth",
            '4-3': "more drive for achievement and social awareness",
            '4-5': "more analytical thinking and objectivity",
            '5-4': "more emotional awareness and creative expression",
            '5-6': "more awareness of security and loyalty",
            '6-5': "more intellectual curiosity and independence",
            '6-7': "more optimism and adventurousness",
            '7-6': "more awareness of risks and commitment",
            '7-8': "more assertiveness and protective instincts",
            '8-7': "more playfulness and openness to experiences",
            '8-9': "more patience and diplomatic abilities",
            '9-8': "more self-assertion and leadership qualities",
            '9-1': "more focus on improvement and standards"
        };
        
        return influences[`${primaryType}-${wingType}`] || "complementary qualities to your core type";
    },
    formatPhaseLabel: function(phase) {
        // Convert phase names to more readable format
        return phase
            .split('-')
            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
            .join(' ');
    }
};

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    // Initialize registration form
    document.getElementById('registration-form').addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        state.answers.registration = Object.fromEntries(formData);
        state.startTime = Date.now();
        ui.showPhase('initial-segmentation');
        ui.renderQuestions('initial-segmentation', questionBank.initialSegmentation);
    });
    
    // Initialize metrics export
    document.getElementById('export-metrics').addEventListener('click', function() {
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
    });
}); 