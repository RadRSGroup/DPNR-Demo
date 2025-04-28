/**
 * Emotional Persona Analysis Service
 * 
 * This module handles the server-side analysis of assessment data,
 * integrating with the scoring engine and existing text analysis services.
 */

const express = require('express');
const router = express.Router();
const { processAssessment, debugScoring } = require('../modules/scoring-engine');
const axios = require('axios');

// Configuration
const ollamaUrl = process.env.OLLAMA_URL || 'http://host.docker.internal:11434';

/**
 * Process assessment responses from the questionnaire
 */
router.post('/analyze-assessment', async (req, res) => {
  try {
    const { responses } = req.body;
    
    if (!responses || Object.keys(responses).length === 0) {
      return res.status(400).json({ error: 'No assessment responses provided' });
    }
    
    // Process the questionnaire responses
    const results = await processAssessment(responses, 'questionnaire');
    
    // Return the results
    res.json(results);
  } catch (error) {
    console.error('Error analyzing assessment:', error);
    res.status(500).json({ error: 'Error processing assessment', details: error.message });
  }
});

/**
 * Analyze text for emotional personas and traits
 */
router.post('/analyze-text', async (req, res) => {
  try {
    const { text, assessmentType, model = 'llama2' } = req.body;
    
    if (!text) {
      return res.status(400).json({ error: 'No text provided for analysis' });
    }
    
    // If this is specifically for persona assessment
    if (assessmentType === 'persona') {
      // Process text for persona analysis
      const results = await processAssessment(text, 'text-analysis');
      return res.json(results);
    }
    
    // Otherwise, perform general text analysis using LLM
    let prompt = text;
    
    // Check if Ollama is available
    try {
      const ollamaResponse = await axios.post(`${ollamaUrl}/api/generate`, {
        model,
        prompt,
        stream: false,
        options: {
          temperature: 0.7,
          top_p: 0.9,
          top_k: 40,
          num_predict: 2048
        }
      }, {
        timeout: 300000 // 5 minute timeout
      });
      
      if (!ollamaResponse.data || !ollamaResponse.data.response) {
        throw new Error('Invalid response from LLM service');
      }
      
      return res.json({
        analysis: ollamaResponse.data.response,
        model
      });
    } catch (error) {
      console.error('LLM analysis error:', {
        message: error.message,
        code: error.code,
        response: error.response?.data
      });
      
      res.status(500).json({ 
        error: 'Analysis failed', 
        details: error.message
      });
    }
  } catch (error) {
    console.error('Error in text analysis:', error);
    res.status(500).json({ 
      error: 'Error analyzing text', 
      details: error.message
    });
  }
});

/**
 * Comprehensive persona analysis from uploaded media
 */
router.post('/analyze-media', async (req, res) => {
  try {
    const { text } = req.body;
    
    if (!text) {
      return res.status(400).json({ error: 'No transcribed text provided' });
    }
    
    // Process the transcribed text for persona analysis
    const results = await processAssessment(text, 'text-analysis');
    
    res.json(results);
  } catch (error) {
    console.error('Error analyzing media:', error);
    res.status(500).json({ 
      error: 'Error analyzing media', 
      details: error.message
    });
  }
});

/**
 * Get persona information and descriptions
 */
router.get('/personas', (req, res) => {
  try {
    const { EMOTIONAL_PERSONAS } = require('../modules/scoring-engine');
    
    // Return the persona definitions
    res.json({
      personas: EMOTIONAL_PERSONAS
    });
  } catch (error) {
    console.error('Error fetching personas:', error);
    res.status(500).json({ 
      error: 'Error fetching persona information', 
      details: error.message
    });
  }
});

module.exports = router;