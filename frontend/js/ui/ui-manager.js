// UI manager module
import { createChart } from './chart-manager.js';
import { renderPersonaResults } from './results-manager.js';

export function initializeUI(languageHandler) {
    console.log('UI system initialized');
    setupEventListeners();
    setupAccessibility();
}

function setupEventListeners() {
    // Question navigation
    document.querySelectorAll('.nav-button').forEach(button => {
        button.addEventListener('click', handleNavigation);
    });
    
    // Answer selection
    document.querySelectorAll('.option-container').forEach(container => {
        container.addEventListener('click', handleAnswerSelection);
    });
    
    // Form submission
    const assessmentForm = document.getElementById('assessment-form');
    if (assessmentForm) {
        assessmentForm.addEventListener('submit', handleFormSubmission);
    }
}

function setupAccessibility() {
    // Add ARIA labels
    document.querySelectorAll('.question-container').forEach((container, index) => {
        container.setAttribute('aria-label', `Question ${index + 1}`);
    });
    
    // Ensure keyboard navigation
    document.querySelectorAll('.option-container').forEach(container => {
        container.setAttribute('tabindex', '0');
    });
}

export async function updateQuestionDisplay(question, phase) {
    const container = document.getElementById('question-container');
    if (!container) return;
    
    container.innerHTML = `
        <div class="question-text" data-i18n="${question.id}">
            ${question.text}
        </div>
        <div class="options-container">
            ${question.options.map(option => `
                <div class="option-container" 
                     data-value="${option.value}"
                     data-persona="${option.persona}">
                    ${option.text}
                </div>
            `).join('')}
        </div>
    `;
    
    // Update progress indicator
    updateProgressIndicator(phase);
}

function updateProgressIndicator(phase) {
    const progressBar = document.getElementById('progress-bar');
    if (progressBar) {
        const progress = calculateProgress(phase);
        progressBar.style.width = `${progress}%`;
        progressBar.setAttribute('aria-valuenow', progress);
    }
}

function calculateProgress(phase) {
    const phases = ['initial', 'personalization', 'final'];
    const currentPhaseIndex = phases.indexOf(phase);
    return ((currentPhaseIndex + 1) / phases.length) * 100;
} 