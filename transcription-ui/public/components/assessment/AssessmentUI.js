// transcription-ui/public/components/assessment/AssessmentUI.js
import React, { useState, useEffect } from 'react';
import FileUpload from '../../../src/components/FileUpload';

// Primary component that manages the assessment flow
function AssessmentUI() {
  const [step, setStep] = useState(0);
  const [assessmentType, setAssessmentType] = useState('questionnaire');
  const [responses, setResponses] = useState({});
  const [uploadedText, setUploadedText] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

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
    setAssessmentType(method);
  };

  // Handle question responses
  const handleResponse = (questionId, optionId) => {
    setResponses({
      ...responses,
      [questionId]: [optionId] // Using array for potential multi-select in future
    });
  };

  // Handle text input for analysis
  const handleTextInput = (event) => {
    setUploadedText(event.target.value);
  };

  // Handle file upload result
  const handleFileUploadComplete = (result) => {
    if (result && result.text) {
      setUploadedText(result.text);
    }
  };

  // Submit assessment for analysis
  const submitAssessment = async () => {
    setLoading(true);
    setError(null);
    
    try {
      let response;
      
      // Handle questionnaire submission
      if (assessmentType === 'questionnaire') {
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
      setResults(data);
      setStep(2); // Move to results step
    } catch (error) {
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

  // Render method selection step
  const renderMethodSelection = () => {
    return (
      <div className="assessment-method-selection">
        <h2>Choose Your Assessment Method</h2>
        <p>Select how you'd like to discover your emotional personas:</p>
        
        <div className="method-options">
          <div 
            className={`method-option ${assessmentType === 'questionnaire' ? 'selected' : ''}`}
            onClick={() => handleMethodSelection('questionnaire')}
          >
            <h3>Guided Questionnaire</h3>
            <p>Answer a series of questions about your preferences and tendencies.</p>
            <p><strong>Time:</strong> 5-10 minutes</p>
          </div>
          
          <div 
            className={`method-option ${assessmentType === 'text-analysis' ? 'selected' : ''}`}
            onClick={() => handleMethodSelection('text-analysis')}
          >
            <h3>Text Analysis</h3>
            <p>Share your thoughts in your own words or upload content for analysis.</p>
            <p><strong>Time:</strong> Varies based on content</p>
          </div>
        </div>
      </div>
    );
  };

  // Render questionnaire step
  const renderQuestionnaire = () => {
    return (
      <div className="assessment-questionnaire">
        <h2>Complete the Assessment</h2>
        <p>Select the option that best describes you in each scenario:</p>
        
        {questions.map((question, index) => (
          <div key={question.id} className="question-container">
            <h3>{index + 1}. {question.text}</h3>
            <div className="options-container">
              {question.options.map(option => (
                <div 
                  key={option.id} 
                  className={`option ${responses[question.id]?.includes(option.id) ? 'selected' : ''}`}
                  onClick={() => handleResponse(question.id, option.id)}
                >
                  {option.text}
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    );
  };

  // Render text analysis step
  const renderTextAnalysis = () => {
    return (
      <div className="assessment-text-analysis">
        <h2>Share Your Thoughts</h2>
        <p>Enter or upload text that reflects your thoughts, experiences, or perspectives.</p>
        
        <div className="text-input-container">
          <textarea
            placeholder="Enter your text here... (minimum 100 characters for accurate analysis)"
            value={uploadedText}
            onChange={handleTextInput}
            rows={10}
          ></textarea>
          
          <p className="text-count">
            {uploadedText.length} characters {uploadedText.length < 100 ? '(min 100 recommended)' : ''}
          </p>
        </div>
        
        <div className="or-separator">
          <span>OR</span>
        </div>
        
        <div className="file-upload-container">
          <p>Upload an audio, video, or text file for analysis:</p>
          <FileUpload 
            assessmentMode={true}
            onAssessmentTextReady={text => setUploadedText(text)}
            onError={error => setError(error.message)}
          />
        </div>
      </div>
    );
  };

  // Render results step
  const renderResults = () => {
    if (loading) {
      return <div className="loading">Analyzing your responses...</div>;
    }
    
    if (error) {
      return <div className="error">Error: {error}</div>;
    }
    
    if (!results) {
      return <div className="no-results">No results available.</div>;
    }
    
    return (
      <div className="assessment-results">
        <h2>Your Emotional Persona Assessment Results</h2>
        
        <div className="primary-persona">
          <h3>Primary Persona: {results.primaryPersona.name}</h3>
          <p>{results.primaryPersona.description}</p>
        </div>
        
        {results.secondaryPersonas?.length > 0 && (
          <div className="secondary-personas">
            <h3>Secondary Personas</h3>
            <div className="persona-chips">
              {results.secondaryPersonas.map(persona => (
                <span key={persona.name} className="persona-chip">{persona.name}</span>
              ))}
            </div>
          </div>
        )}
        
        <div className="core-values">
          <h3>Core Values</h3>
          <div className="value-chips">
            {results.coreValues?.map(value => (
              <span key={value} className="value-chip">{value}</span>
            ))}
          </div>
        </div>
        
        <div className="life-domains">
          <h3>Life Domain Impact</h3>
          
          {Object.entries(results.lifeDomains || {}).map(([domain, impact]) => (
            <div key={domain} className="domain-impact">
              <h4>{domain.charAt(0).toUpperCase() + domain.slice(1)}</h4>
              <p>{impact}</p>
            </div>
          ))}
        </div>
        
        <div className="persona-chart">
          <h3>Persona Distribution</h3>
          <div className="chart-placeholder">
            {/* This is where you'd add a visualization of the scores */}
            <p>Chart visualization would appear here</p>
          </div>
        </div>
      </div>
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
        return <div>Unknown step</div>;
    }
  };

  return (
    <div className="assessment-container">
      <div className="assessment-header">
        <h1>Emotional Persona Assessment</h1>
        <p>Discover your emotional personas, core values, and how they impact different life domains.</p>
      </div>
      
      <div className="assessment-stepper">
        {steps.map((label, index) => (
          <div 
            key={label}
            className={`step ${index === step ? 'active' : ''} ${index < step ? 'completed' : ''}`}
          >
            <div className="step-number">{index + 1}</div>
            <div className="step-label">{label}</div>
          </div>
        ))}
      </div>
      
      <div className="assessment-content">
        {renderStepContent()}
      </div>
      
      <div className="assessment-actions">
        {step > 0 && (
          <button 
            className="back-button"
            onClick={handleBack}
            disabled={loading}
          >
            Back
          </button>
        )}
        
        {step < steps.length - 1 && (
          <button 
            className="next-button"
            onClick={handleNext}
            disabled={!canProceed() || loading}
          >
            {loading ? 'Loading...' : 'Next'}
          </button>
        )}
        
        {step === steps.length - 1 && (
          <button 
            className="finish-button"
            onClick={() => window.location.reload()}
          >
            Start New Assessment
          </button>
        )}
      </div>
    </div>
  );
}

export default AssessmentUI;