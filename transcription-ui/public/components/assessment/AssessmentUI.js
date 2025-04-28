// Define the AssessmentUI component to be accessible from the global scope
window.AssessmentUI = function() {
    // Use React hooks for state management
    const [step, setStep] = React.useState(0);
    const [assessmentType, setAssessmentType] = React.useState('questionnaire');
    const [responses, setResponses] = React.useState({});
    const [uploadedText, setUploadedText] = React.useState('');
    const [results, setResults] = React.useState(null);
    const [loading, setLoading] = React.useState(false);
    const [error, setError] = React.useState(null);
  
    // Steps in the assessment process
    const steps = ['Choose Method', 'Complete Assessment', 'View Results'];
  
    // Sample questions for the questionnaire
    const questions = [
      {
        id: 'qQ101',
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
      {
        id: 'qQ102',
        text: 'The thing that bothers me most in life is:',
        options: [
          { id: 'A110', text: 'Being overwhelmed with too many demands or expectations', persona: 'observer' },
          { id: 'A111', text: 'Feeling like my contributions aren not appreciated', persona: 'giver' },
          { id: 'A112', text: 'Not achieving my goals or living up to my potential', persona: 'driver' },
          { id: 'A113', text: 'Feeling misunderstood or having to be inauthentic', persona: 'seeker' },
          { id: 'A114', text: 'Seeing things done incorrectly or without proper standards', persona: 'upholder' },
          { id: 'A115', text: 'Uncertainty or not being prepared for what might happen', persona: 'guardian' },
          { id: 'A116', text: 'Being restricted or missing out on opportunities', persona: 'explorer' },
          { id: 'A117', text: 'Being controlled or having my autonomy threatened', persona: 'protector' },
          { id: 'A118', text: 'Conflict or discord in my relationships', persona: 'harmonizer' }
        ]
      },
      {
        id: 'qQ201',
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
      }
    ];
  
    // Handle selection of assessment method
    const handleMethodSelection = (method) => {
      console.log('Assessment method selected:', method);
      setAssessmentType(method);
    };
  
    // Handle question responses
    const handleResponse = (questionId, optionId) => {
      console.log('Response recorded:', questionId, optionId);
      setResponses({
        ...responses,
        [questionId]: [optionId] // Using array for potential multi-select in future
      });
    };
  
    // Handle text input for analysis
    const handleTextInput = (event) => {
      setUploadedText(event.target.value);
    };
  
    // Submit assessment for analysis
    const submitAssessment = async () => {
      console.log('Submitting assessment for analysis');
      setLoading(true);
      setError(null);
      
      try {
        let response;
        
        // Handle questionnaire submission
        if (assessmentType === 'questionnaire') {
          console.log('Submitting questionnaire responses:', responses);
          response = await fetch('/api/analyze-assessment', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ responses }),
          });
        } 
        // Handle text analysis submission
        else if (assessmentType === 'text-analysis' && uploadedText) {
          console.log('Submitting text for analysis:', uploadedText.substring(0, 100) + '...');
          response = await fetch('/api/analyze-text', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
              text: uploadedText,
              assessmentType: 'persona'
            }),
          });
        } else {
          throw new Error('No data to analyze');
        }
        
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || 'Analysis failed');
        }
        
        const data = await response.json();
        console.log('Analysis results received:', data);
        setResults(data);
        setStep(2); // Move to results step
      } catch (error) {
        console.error('Analysis error:', error);
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };
  
    // Navigation handlers
    const handleNext = () => {
      if (step === 1) {
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
        return true; // Can always proceed from method selection
      }
      
      if (step === 1) {
        if (assessmentType === 'questionnaire') {
          // Check if all questions have responses
          return questions.every(q => responses[q.id]);
        } else {
          // Check if there's text to analyze
          return uploadedText.length > 0;
        }
      }
      
      return true;
    };
  
    // Render functions for each step
    const renderMethodSelection = () => {
      return React.createElement(
        'div', 
        { className: 'assessment-method-selection' },
        [
          React.createElement('h2', { key: 'title' }, 'Choose Your Assessment Method'),
          React.createElement('p', { key: 'desc' }, 'Select how you\'d like to discover your emotional personas:'),
          
          React.createElement(
            'div', 
            { className: 'method-options', key: 'options' },
            [
              React.createElement(
                'div',
                { 
                  key: 'questionnaire',
                  className: `method-option ${assessmentType === 'questionnaire' ? 'selected' : ''}`,
                  onClick: () => handleMethodSelection('questionnaire')
                },
                [
                  React.createElement('h3', { key: 'title' }, 'Guided Questionnaire'),
                  React.createElement('p', { key: 'desc' }, 'Answer a series of questions about your preferences and tendencies.'),
                  React.createElement('p', { key: 'time' }, [
                    React.createElement('strong', { key: 'label' }, 'Time:'),
                    ' 5-10 minutes'
                  ])
                ]
              ),
              
              React.createElement(
                'div',
                { 
                  key: 'text-analysis',
                  className: `method-option ${assessmentType === 'text-analysis' ? 'selected' : ''}`,
                  onClick: () => handleMethodSelection('text-analysis')
                },
                [
                  React.createElement('h3', { key: 'title' }, 'Text Analysis'),
                  React.createElement('p', { key: 'desc' }, 'Share your thoughts in your own words or upload content for analysis.'),
                  React.createElement('p', { key: 'time' }, [
                    React.createElement('strong', { key: 'label' }, 'Time:'),
                    ' Varies based on content'
                  ])
                ]
              )
            ]
          )
        ]
      );
    };
    
    const renderQuestionnaire = () => {
      return React.createElement(
        'div',
        { className: 'assessment-questionnaire' },
        [
          React.createElement('h2', { key: 'title' }, 'Complete the Assessment'),
          React.createElement('p', { key: 'desc' }, 'Select the option that best describes you in each scenario:'),
          
          ...questions.map((question, index) => 
            React.createElement(
              'div',
              { key: question.id, className: 'question-container' },
              [
                React.createElement('h3', { key: 'question' }, `${index + 1}. ${question.text}`),
                React.createElement(
                  'div',
                  { key: 'options', className: 'options-container' },
                  question.options.map(option => 
                    React.createElement(
                      'div',
                      { 
                        key: option.id,
                        className: `option ${responses[question.id]?.includes(option.id) ? 'selected' : ''}`,
                        onClick: () => handleResponse(question.id, option.id)
                      },
                      option.text
                    )
                  )
                )
              ]
            )
          )
        ]
      );
    };
    
    const renderTextAnalysis = () => {
      return React.createElement(
        'div',
        { className: 'assessment-text-analysis' },
        [
          React.createElement('h2', { key: 'title' }, 'Share Your Thoughts'),
          React.createElement('p', { key: 'desc' }, 'Enter or upload text that reflects your thoughts, experiences, or perspectives.'),
          
          React.createElement(
            'div',
            { key: 'text-input', className: 'text-input-container' },
            [
              React.createElement(
                'textarea',
                {
                  key: 'textarea',
                  placeholder: 'Enter your text here... (minimum 100 characters for accurate analysis)',
                  value: uploadedText,
                  onChange: handleTextInput,
                  rows: 10
                }
              ),
              
              React.createElement(
                'p',
                { key: 'count', className: 'text-count' },
                `${uploadedText.length} characters ${uploadedText.length < 100 ? '(min 100 recommended)' : ''}`
              )
            ]
          )
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
          )
        ]
      );
    };
    
    // Render current step content
    const renderStepContent = () => {
      switch (step) {
        case 0:
          return renderMethodSelection();
        case 1:
          return assessmentType === 'questionnaire' 
            ? renderQuestionnaire() 
            : renderTextAnalysis();
        case 2:
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