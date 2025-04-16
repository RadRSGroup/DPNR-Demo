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
    startTime: null,
    phaseTimes: {},
    interactionCounts: {},
    confidenceScores: {}
};

// Metrics Tracking
const metrics = {
    startTimer: function(phase) {
        state.phaseTimes[phase] = {
            start: Date.now(),
            end: null
        };
    },
    endTimer: function(phase) {
        if (state.phaseTimes[phase]) {
            state.phaseTimes[phase].end = Date.now();
        }
    },
    recordInteraction: function(phase) {
        state.interactionCounts[phase] = (state.interactionCounts[phase] || 0) + 1;
    },
    calculateConfidence: function(phase) {
        // Simple confidence calculation based on answer consistency
        const phaseAnswers = state.answers[phase] || {};
        const totalQuestions = Object.keys(phaseAnswers).length;
        if (totalQuestions === 0) return 0;
        
        let consistentAnswers = 0;
        // Add logic to check answer consistency based on phase
        state.confidenceScores[phase] = Math.round((consistentAnswers / totalQuestions) * 100);
        return state.confidenceScores[phase];
    }
};

// UI Management
const ui = {
    showPhase: function(phase) {
        document.querySelectorAll('.phase').forEach(el => el.classList.remove('active'));
        document.getElementById(`${phase}-phase`).classList.add('active');
        metrics.startTimer(phase);
        
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
                        <h5 class="card-title">${instinctualVariant}</h5>
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
    updateCharts: function() {
        // Time chart
        const timeCtx = document.getElementById('timeChart').getContext('2d');
        new Chart(timeCtx, {
            type: 'bar',
            data: {
                labels: Object.keys(state.phaseTimes),
                datasets: [{
                    label: 'Time per Phase (seconds)',
                    data: Object.values(state.phaseTimes).map(time => 
                        Math.round((time.end - time.start) / 1000)
                    )
                }]
            }
        });
        
        // Completion chart
        const completionCtx = document.getElementById('completionChart').getContext('2d');
        new Chart(completionCtx, {
            type: 'pie',
            data: {
                labels: Object.keys(state.answers),
                datasets: [{
                    data: Object.values(state.answers).map(phase => 
                        Object.keys(phase).length
                    )
                }]
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