class AssessmentManager {
    constructor() {
        this.currentPhase = 'registration';
        this.phases = [
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
        this.answers = {};
        this.isInitialized = false;
    }

    async initialize() {
        if (this.isInitialized) return;

        // Initialize event listeners
        this.initializeEventListeners();
        
        // Load initial phase
        this.showPhase('registration');
        
        this.isInitialized = true;
    }

    initializeEventListeners() {
        // Registration form submit handler
        const registrationForm = document.getElementById('registration-form');
        if (registrationForm) {
            registrationForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.handleRegistrationSubmit();
            });
        }

        // Navigation buttons handler
        document.addEventListener('click', (e) => {
            if (e.target.matches('.next-phase')) {
                this.nextPhase();
            } else if (e.target.matches('.prev-phase')) {
                this.prevPhase();
            }
        });
    }

    async handleRegistrationSubmit() {
        const form = document.getElementById('registration-form');
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        // Validate form data
        if (!this.validateRegistration(data)) {
            return;
        }

        // Save registration data
        this.answers.registration = data;

        // Show loading
        window.showLoading();

        try {
            // Move to next phase
            await this.nextPhase();
        } catch (error) {
            console.error('Error moving to next phase:', error);
        } finally {
            window.hideLoading();
        }
    }

    validateRegistration(data) {
        if (!data.name || !data.email) {
            alert('Please fill in all required fields');
            return false;
        }

        // Basic email validation
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(data.email)) {
            alert('Please enter a valid email address');
            return false;
        }

        return true;
    }

    showPhase(phaseId) {
        // Hide all phases
        document.querySelectorAll('.phase').forEach(phase => {
            phase.classList.remove('active');
        });

        // Show requested phase
        const phaseElement = document.getElementById(`${phaseId}-phase`);
        if (phaseElement) {
            phaseElement.classList.add('active');
            this.currentPhase = phaseId;
            
            // Load questions if this is a question phase
            if (phaseId !== 'registration' && phaseId !== 'results') {
                this.loadQuestions(phaseId);
            }
        }
    }

    async loadQuestions(phaseId) {
        const container = document.getElementById(`${phaseId}-questions`);
        if (!container) return;

        try {
            // Show loading
            window.showLoading();

            // Load questions based on phase
            const questions = await this.getQuestionsForPhase(phaseId);
            
            // Render questions
            container.innerHTML = this.renderQuestions(questions, phaseId);
            
            // Add navigation buttons
            this.addNavigationButtons(phaseId);
        } catch (error) {
            console.error(`Error loading questions for phase ${phaseId}:`, error);
        } finally {
            window.hideLoading();
        }
    }

    async getQuestionsForPhase(phaseId) {
        // This should be implemented based on your question bank structure
        // For now, returning a placeholder
        return [
            {
                id: 'q1',
                text: 'Sample question 1',
                options: ['Option 1', 'Option 2', 'Option 3']
            },
            {
                id: 'q2',
                text: 'Sample question 2',
                options: ['Option 1', 'Option 2', 'Option 3']
            }
        ];
    }

    renderQuestions(questions, phaseId) {
        return `
            <div class="questions-container">
                ${questions.map((q, index) => `
                    <div class="question-card" data-question-id="${q.id}">
                        <h3>Question ${index + 1}</h3>
                        <p>${q.text}</p>
                        <div class="options">
                            ${q.options.map((option, optIndex) => `
                                <div class="option">
                                    <input type="radio" 
                                           name="${q.id}" 
                                           id="${q.id}_${optIndex}" 
                                           value="${option}">
                                    <label for="${q.id}_${optIndex}">${option}</label>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
    }

    addNavigationButtons(phaseId) {
        const container = document.getElementById(`${phaseId}-phase`);
        if (!container) return;

        const navButtons = document.createElement('div');
        navButtons.className = 'navigation-buttons';
        
        // Add previous button if not first phase
        if (this.phases.indexOf(phaseId) > 0) {
            navButtons.innerHTML += `
                <button class="btn btn-secondary prev-phase">Previous</button>
            `;
        }

        // Add next button
        navButtons.innerHTML += `
            <button class="btn btn-primary next-phase">Next</button>
        `;

        container.appendChild(navButtons);
    }

    async nextPhase() {
        const currentIndex = this.phases.indexOf(this.currentPhase);
        if (currentIndex < this.phases.length - 1) {
            const nextPhase = this.phases[currentIndex + 1];
            this.showPhase(nextPhase);
        }
    }

    prevPhase() {
        const currentIndex = this.phases.indexOf(this.currentPhase);
        if (currentIndex > 0) {
            const prevPhase = this.phases[currentIndex - 1];
            this.showPhase(prevPhase);
        }
    }

    saveAnswers(phaseId) {
        const questions = document.querySelectorAll(`#${phaseId}-questions .question-card`);
        this.answers[phaseId] = {};

        questions.forEach(question => {
            const questionId = question.dataset.questionId;
            const selectedOption = question.querySelector('input[type="radio"]:checked');
            
            if (selectedOption) {
                this.answers[phaseId][questionId] = selectedOption.value;
            }
        });
    }
}

// Export the AssessmentManager class
export const assessmentManager = new AssessmentManager(); 