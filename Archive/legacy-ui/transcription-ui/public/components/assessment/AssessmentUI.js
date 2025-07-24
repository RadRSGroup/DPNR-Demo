// Enhanced AssessmentUI component with multiple-choice and text input questions
// This would replace the AssessmentUI.js file in the components/assessment directory

function AssessmentUI() {
    // Use React hooks for state management
    const [step, setStep] = React.useState(0);
    const [responses, setResponses] = React.useState({});
    const [results, setResults] = React.useState(null);
    const [loading, setLoading] = React.useState(false);
    const [error, setError] = React.useState(null);
    
    // Steps in the assessment process
    const steps = ['Complete Assessment', 'View Results'];
    
    // Enhanced questions array with different question types
    const questions = [
      // Single-select question (original type)
      {
        id: 'qQ101',
        type: 'single-select',
        text: 'When faced with a difficult decision, I typically:',
        options: [
          { id: 'A101', text: 'Take time to analyze all possible outcomes before deciding', persona: 'observer' },
          { id: 'A102', text: 'Consider how it will impact others before myself', persona: 'giver' },
          { id: 'A103', text: 'Look for the most efficient and successful solution', persona: 'driver' },
          { id: 'A104', text: 'Trust my gut feeling about what feels most authentic', persona: 'seeker' },
          { id: 'A105', text: 'Make sure I follow the right procedures and standards', persona: 'upholder' },
          { id: 'A106', text: 'Consider all risks and prepare for potential problems', persona: 'guardian' },
          { id: 'A107', text: 'Look for the most exciting and positive option', persona: 'explorer' },
          { id: 'A108', text: 'Assert my position and take control of the situation', persona: 'protector' },
          { id: 'A109', text: 'Find a compromise that keeps everyone happy', persona: 'harmonizer' }
        ]
      },
      // Multi-select question (new type)
      {
        id: 'qQ102',
        type: 'multi-select',
        text: 'Which of the following qualities do you value most in yourself? (Select all that apply)',
        minSelections: 1,
        maxSelections: 3,
        options: [
          { id: 'A110', text: 'Being analytical and thoughtful', persona: 'observer' },
          { id: 'A111', text: 'Being caring and supportive of others', persona: 'giver' },
          { id: 'A112', text: 'Being productive and achieving goals', persona: 'driver' },
          { id: 'A113', text: 'Being authentic and emotionally expressive', persona: 'seeker' },
          { id: 'A114', text: 'Being principled and doing things right', persona: 'upholder' },
          { id: 'A115', text: 'Being prepared for all possibilities', persona: 'guardian' },
          { id: 'A116', text: 'Being optimistic and enthusiastic', persona: 'explorer' },
          { id: 'A117', text: 'Being strong and standing up for others', persona: 'protector' },
          { id: 'A118', text: 'Being peaceful and keeping harmony', persona: 'harmonizer' }
        ]
      },
      // Text input question (new type)
      {
        id: 'qQ103',
        type: 'text-input',
        text: 'Describe a challenging situation you faced recently and how you handled it:',
        placeholder: 'Write at least 100 characters...',
        minLength: 100,
        maxLength: 1000,
        // List of personas for text analysis mapping
        personas: ['observer', 'giver', 'driver', 'seeker', 'upholder', 'guardian', 'explorer', 'protector', 'harmonizer']
      },
      // Single-select question
      {
        id: 'qQ201',
        type: 'single-select',
        text: 'In my relationships, I tend to:',
        options: [
          { id: 'A201', text: 'Need personal space and time to process my thoughts', persona: 'observer' },
          { id: 'A202', text: 'Focus on the needs of others and how I can support them', persona: 'giver' },
          { id: 'A203', text: 'Be goal-oriented and sometimes struggle with vulnerability', persona: 'driver' },
          { id: 'A204', text: 'Seek deep emotional connection and authentic exchange', persona: 'seeker' },
          { id: 'A205', text: 'Have high expectations and notice when things are not right', persona: 'upholder' },
          { id: 'A206', text: 'Be loyal but cautious about trusting too quickly', persona: 'guardian' },
          { id: 'A207', text: 'Bring energy and fun but may avoid serious issues', persona: 'explorer' },
          { id: 'A208', text: 'Be protective and direct, but sometimes intimidating', persona: 'protector' },
          { id: 'A209', text: 'Be accommodating and avoid creating conflict', persona: 'harmonizer' }
        ]
      },
      // Multi-select question
      {
        id: 'qQ202',
        type: 'multi-select',
        text: 'When I feel stressed, I am most likely to: (Select all that apply)',
        minSelections: 1,
        maxSelections: 3,
        options: [
          { id: 'A210', text: 'Withdraw to process information and recharge alone', persona: 'observer' },
          { id: 'A211', text: 'Reach out to others for support or to help them', persona: 'giver' },
          { id: 'A212', text: 'Create a plan of action to solve the problem', persona: 'driver' },
          { id: 'A213', text: 'Express my emotions or channel them into creative outlets', persona: 'seeker' },
          { id: 'A214', text: 'Focus on what I can control and improve', persona: 'upholder' },
          { id: 'A215', text: 'Prepare for the worst while seeking reassurance', persona: 'guardian' },
          { id: 'A216', text: 'Look for distractions or silver linings', persona: 'explorer' },
          { id: 'A217', text: 'Take charge of the situation or confront issues directly', persona: 'protector' },
          { id: 'A218', text: 'Try to maintain calm and avoid conflict', persona: 'harmonizer' }
        ]
      },
      // Text input question
      {
        id: 'qQ106',
        type: 'text-input',
        text: 'What are your most important goals in life right now?',
        placeholder: 'Write at least 50 characters...',
        minLength: 50,
        maxLength: 500,
        personas: ['observer', 'giver', 'driver', 'seeker', 'upholder', 'guardian', 'explorer', 'protector', 'harmonizer']
      }
    ];
    
    // Handle question responses based on question type
    const handleResponse = (question, value) => {
      const questionId = question.id;
      let updatedResponse;
      
      switch(question.type) {
        case 'single-select':
          // For single select, just set the array with one option ID
          updatedResponse = [value];
          break;
          
        case 'multi-select':
          // For multi-select, toggle the presence of the option ID
          const currentSelections = responses[questionId] || [];
          if (currentSelections.includes(value)) {
            // If already selected, remove it
            updatedResponse = currentSelections.filter(id => id !== value);
          } else {
            // If not selected, add it (respecting maxSelections)
            if (currentSelections.length < question.maxSelections) {
              updatedResponse = [...currentSelections, value];
            } else {
              // If max selections reached, replace the first one
              updatedResponse = [...currentSelections.slice(1), value];
            }
          }
          break;
          
        case 'text-input':
          // For text input, store the text directly
          updatedResponse = value;
          break;
          
        default:
          console.error('Unknown question type:', question.type);
          return;
      }
      
      console.log('Response recorded:', questionId, updatedResponse);
      setResponses({
        ...responses,
        [questionId]: updatedResponse
      });
    };
    
    // Submit assessment for analysis
    const submitAssessment = async () => {
      console.log('Submitting assessment for analysis');
      setLoading(true);
      setError(null);
      
      try {
        console.log('Submitting questionnaire responses:', responses);
        const response = await fetch('/api/analyze-assessment', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ responses }),
        });
        
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || 'Analysis failed');
        }
        
        const data = await response.json();
        console.log('Analysis results received:', data);
        setResults(data);
        setStep(1); // Move to results step
      } catch (error) {
        console.error('Analysis error:', error);
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };
    
    // Navigation handlers
    const handleNext = () => {
      if (step === 0) {
        submitAssessment();
      } else {
        setStep(step + 1);
      }
    };
    
    const handleBack = () => {
      setStep(step - 1);
    };
    
    // Check if user can proceed to next step
    const canProceed = () => {
      if (step === 0) {
        // Check that all questions have valid responses
        return questions.every(question => {
          const response = responses[question.id];
          
          // If no response yet
          if (response === undefined) return false;
          
          switch(question.type) {
            case 'single-select':
              return response && response.length === 1;
              
            case 'multi-select':
              return response && 
                response.length >= question.minSelections && 
                response.length <= question.maxSelections;
                
            case 'text-input':
              return typeof response === 'string' && 
                response.length >= question.minLength && 
                response.length <= question.maxLength;
                
            default:
              return false;
          }
        });
      }
      return true;
    };
    
    // Count characters for text inputs
    const getCharCount = (questionId) => {
      const text = responses[questionId] || '';
      return typeof text === 'string' ? text.length : 0;
    };
    
    // Render different question types
    const renderQuestion = (question, index) => {
      const commonHeader = [
        React.createElement('h3', { key: 'question' }, `${index + 1}. ${question.text}`)
      ];
      
      switch(question.type) {
        case 'single-select':
          return React.createElement(
            'div',
            { key: question.id, className: 'question-container single-select' },
            [
              ...commonHeader,
              React.createElement(
                'div',
                { key: 'options', className: 'options-container' },
                question.options.map(option => 
                  React.createElement(
                    'div',
                    { 
                      key: option.id,
                      className: `option ${responses[question.id]?.includes(option.id) ? 'selected' : ''}`,
                      onClick: () => handleResponse(question, option.id)
                    },
                    option.text
                  )
                )
              )
            ]
          );
          
        case 'multi-select':
          return React.createElement(
            'div',
            { key: question.id, className: 'question-container multi-select' },
            [
              ...commonHeader,
              React.createElement(
                'p', 
                { key: 'instruction', className: 'selection-guide' },
                `Select between ${question.minSelections} and ${question.maxSelections} options`
              ),
              React.createElement(
                'div',
                { key: 'selections', className: 'selection-counter' },
                `${(responses[question.id]?.length || 0)} of ${question.maxSelections} selected`
              ),
              React.createElement(
                'div',
                { key: 'options', className: 'options-container' },
                question.options.map(option => 
                  React.createElement(
                    'div',
                    { 
                      key: option.id,
                      className: `option ${responses[question.id]?.includes(option.id) ? 'selected' : ''}`,
                      onClick: () => handleResponse(question, option.id)
                    },
                    option.text
                  )
                )
              )
            ]
          );
          
        case 'text-input':
          const charCount = getCharCount(question.id);
          const isValid = charCount >= question.minLength && charCount <= question.maxLength;
          
          return React.createElement(
            'div',
            { key: question.id, className: 'question-container text-input' },
            [
              ...commonHeader,
              React.createElement(
                'textarea',
                {
                  key: 'textinput',
                  placeholder: question.placeholder,
                  value: responses[question.id] || '',
                  onChange: (e) => handleResponse(question, e.target.value),
                  className: isValid ? 'valid' : (charCount > 0 ? 'invalid' : '')
                }
              ),
              React.createElement(
                'div',
                { 
                  key: 'char-counter',
                  className: `char-counter ${isValid ? 'valid' : (charCount > 0 ? 'invalid' : '')}`
                },
                `${charCount} / ${question.minLength}-${question.maxLength} characters`
              )
            ]
          );
          
        default:
          return React.createElement('div', { key: question.id }, 'Unknown question type');
      }
    };
    
    // Render functions for each step
    const renderQuestionnaire = () => {
      return React.createElement(
        'div',
        { className: 'assessment-questionnaire' },
        [
          React.createElement('h2', { key: 'title' }, 'Complete the Assessment'),
          React.createElement('p', { key: 'desc' }, 'Answer the following questions about yourself:'),
          
          ...questions.map((question, index) => renderQuestion(question, index))
        ]
      );
    };
    
    const renderResults = () => {
      if (loading) {
        return React.createElement(
          'div',
          { className: 'loading' },
          'Analyzing your responses...'
        );
      }
      
      if (error) {
        return React.createElement(
          'div',
          { className: 'error' },
          `Error: ${error}`
        );
      }
      
      if (!results) {
        return React.createElement(
          'div',
          { className: 'no-results' },
          'No results available.'
        );
      }
      
      return React.createElement(
        'div',
        { className: 'assessment-results' },
        [
          React.createElement('h2', { key: 'title' }, 'Your Emotional Persona Assessment Results'),
          
          React.createElement(
            'div',
            { key: 'primary', className: 'primary-persona' },
            [
              React.createElement('h3', { key: 'title' }, `Primary Persona: ${results.primaryPersona.name}`),
              React.createElement('p', { key: 'desc' }, results.primaryPersona.description)
            ]
          ),
          
          results.secondaryPersonas?.length > 0 &&
          React.createElement(
            'div',
            { key: 'secondary', className: 'secondary-personas' },
            [
              React.createElement('h3', { key: 'title' }, 'Secondary Personas'),
              React.createElement(
                'div',
                { key: 'personas', className: 'persona-chips' },
                results.secondaryPersonas.map(persona => 
                  React.createElement(
                    'span',
                    { key: persona.name, className: 'persona-chip' },
                    persona.name
                  )
                )
              )
            ]
          ),
          
          React.createElement(
            'div',
            { key: 'values', className: 'core-values' },
            [
              React.createElement('h3', { key: 'title' }, 'Core Values'),
              React.createElement(
                'div',
                { key: 'chips', className: 'value-chips' },
                results.coreValues?.map(value => 
                  React.createElement(
                    'span',
                    { key: value, className: 'value-chip' },
                    value
                  )
                )
              )
            ]
          ),
          
          React.createElement(
            'div',
            { key: 'domains', className: 'life-domains' },
            [
              React.createElement('h3', { key: 'title' }, 'Life Domain Impact'),
              
              ...Object.entries(results.lifeDomains || {}).map(([domain, impact]) => 
                React.createElement(
                  'div',
                  { key: domain, className: 'domain-impact' },
                  [
                    React.createElement(
                      'h4',
                      { key: 'title' },
                      domain.charAt(0).toUpperCase() + domain.slice(1)
                    ),
                    React.createElement('p', { key: 'impact' }, impact)
                  ]
                )
              )
            ]
          ),
          
          // New section for text analysis insights
          results.textInsights && results.textInsights.length > 0 &&
          React.createElement(
            'div',
            { key: 'textAnalysis', className: 'text-analysis' },
            [
              React.createElement('h3', { key: 'title' }, 'Text Analysis Insights'),
              React.createElement(
                'div',
                { key: 'insights', className: 'text-insights' },
                results.textInsights.map((insight, idx) => 
                  React.createElement('p', { key: `insight-${idx}` }, insight)
                )
              )
            ]
          )
        ]
      );
    };
    
    // Render current step content
    const renderStepContent = () => {
      switch (step) {
        case 0:
          return renderQuestionnaire();
        case 1:
          return renderResults();
        default:
          return React.createElement('div', {}, 'Unknown step');
      }
    };
    
    // Main component render
    return React.createElement(
      'div',
      { className: 'assessment-container' },
      [
        React.createElement(
          'div',
          { key: 'header', className: 'assessment-header' },
          [
            React.createElement('h1', { key: 'title' }, 'Emotional Persona Assessment'),
            React.createElement(
              'p',
              { key: 'desc' },
              'Discover your emotional personas, core values, and how they impact different life domains.'
            )
          ]
        ),
        
        React.createElement(
          'div',
          { key: 'stepper', className: 'assessment-stepper' },
          steps.map((label, index) => 
            React.createElement(
              'div',
              { 
                key: label,
                className: `step ${index === step ? 'active' : ''} ${index < step ? 'completed' : ''}`
              },
              [
                React.createElement('div', { key: 'number', className: 'step-number' }, index + 1),
                React.createElement('div', { key: 'label', className: 'step-label' }, label)
              ]
            )
          )
        ),
        
        React.createElement(
          'div',
          { key: 'content', className: 'assessment-content' },
          renderStepContent()
        ),
        
        React.createElement(
          'div',
          { key: 'actions', className: 'assessment-actions' },
          [
            step > 0 && React.createElement(
              'button',
              { 
                key: 'back',
                className: 'back-button',
                onClick: handleBack,
                disabled: loading
              },
              'Back'
            ),
            
            step < steps.length - 1 && React.createElement(
              'button',
              { 
                key: 'next',
                className: 'next-button',
                onClick: handleNext,
                disabled: !canProceed() || loading
              },
              loading ? 'Loading...' : 'Next'
            ),
            
            step === steps.length - 1 && React.createElement(
              'button',
              { 
                key: 'finish',
                className: 'finish-button',
                onClick: () => window.location.reload()
              },
              'Start New Assessment'
            )
          ]
        )
      ]
    );
  };
  
  // Expose globally (window.AssessmentUI) for scripts that load the component dynamically
  if (typeof window !== 'undefined') {
    window.AssessmentUI = AssessmentUI;
  }