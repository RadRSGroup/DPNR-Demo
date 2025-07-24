// transcription-ui/public/components/assessment/api-service.js
const ApiService = {
    /**
     * Submit questionnaire responses for analysis
     * @param {Object} responses - The user's question responses
     * @returns {Promise<Object>} Assessment results
     */
    submitQuestionnaire: async (responses) => {
      try {
        const response = await fetch('/api/analyze-assessment', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ responses }),
        });
        
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || 'Failed to analyze questionnaire');
        }
        
        return await response.json();
      } catch (error) {
        console.error('Error submitting questionnaire:', error);
        throw error;
      }
    },
    
    /**
     * Submit text for persona analysis
     * @param {string} text - The text to analyze
     * @returns {Promise<Object>} Assessment results
     */
    analyzeText: async (text) => {
      try {
        const response = await fetch('/api/analyze-text', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ 
            text,
            assessmentType: 'persona'
          }),
        });
        
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || 'Failed to analyze text');
        }
        
        return await response.json();
      } catch (error) {
        console.error('Error analyzing text:', error);
        throw error;
      }
    },
    
    /**
     * Get information about all personas
     * @returns {Promise<Object>} Persona definitions
     */
    getPersonas: async () => {
      try {
        const response = await fetch('/api/personas');
        
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || 'Failed to fetch personas');
        }
        
        return await response.json();
      } catch (error) {
        console.error('Error fetching personas:', error);
        throw error;
      }
    }
  };
  
  // If using as a module
  if (typeof module !== 'undefined') {
    module.exports = ApiService;
  }