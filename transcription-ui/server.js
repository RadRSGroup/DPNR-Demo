const express = require('express');
const cors = require('cors');
const multer = require('multer');
const path = require('path');
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');
const { PDFDocument } = require('pdf-lib');
const mammoth = require('mammoth');

const app = express();
const port = process.env.PORT || 3003;
const whisperUrl = process.env.WHISPER_URL || 'http://whisper:9000';
const ollamaUrl = process.env.OLLAMA_URL || 'http://host.docker.internal:11434';

// Configure multer for file uploads
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    const uploadDir = path.join(__dirname, 'uploads');
    if (!fs.existsSync(uploadDir)) {
      fs.mkdirSync(uploadDir, { recursive: true });
    }
    cb(null, uploadDir);
  },
  filename: (req, file, cb) => {
    cb(null, Date.now() + path.extname(file.originalname));
  }
});

const upload = multer({ 
  storage,
  fileFilter: (req, file, cb) => {
    // Check file type
    const allowedTypes = [
      'audio/wav', 
      'audio/mp3', 
      'audio/mpeg', 
      'video/mp4',
      'video/quicktime',
      'video/x-quicktime',
      'text/plain',
      'application/pdf',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    ];
    console.log('Uploaded file type:', file.mimetype);
    if (allowedTypes.includes(file.mimetype)) {
      cb(null, true);
    } else {
      console.log('File type not allowed:', file.mimetype);
      cb(new Error(`Invalid file type. Allowed types: ${allowedTypes.join(', ')}`));
    }
  },
  limits: {
    fileSize: 100 * 1024 * 1024 // 100MB limit
  }
});

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// Get available Ollama models
async function getModels() {
  try {
    console.log('Fetching models from Ollama...');
    const response = await axios.get(`${ollamaUrl}/api/tags`, {
      timeout: 5000 // 5 second timeout
    });
    
    // Validate response structure
    if (!response.data) {
      console.error('Empty response from Ollama');
      throw new Error('Invalid response: Empty response from Ollama service');
    }

    // Handle the case where models is not an array
    if (!Array.isArray(response.data.models)) {
      console.error('Invalid models format:', response.data);
      throw new Error('Invalid response: Expected models to be an array');
    }
    
    // Validate each model object has required properties
    const validModels = response.data.models.filter(model => {
      return model && typeof model === 'object' && typeof model.name === 'string';
    });

    if (validModels.length === 0) {
      throw new Error('No valid models found in Ollama response');
    }
    
    console.log('Available models:', validModels);
    return validModels;
  } catch (error) {
    console.error('Error fetching models:', {
      message: error.message,
      code: error.code,
      response: error.response?.data
    });
    
    if (error.code === 'ECONNREFUSED' || error.code === 'ETIMEDOUT') {
      throw new Error('Cannot connect to Ollama service. Please ensure Ollama is running.');
    }

    // Handle specific error cases
    if (error.response?.status === 404) {
      throw new Error('Ollama API endpoint not found. Please check your Ollama installation.');
    }
    
    if (error.message.includes('Invalid response')) {
      throw new Error(`Ollama returned an invalid response: ${error.message}`);
    }
    
    throw new Error(`Failed to fetch models: ${error.message}`);
  }
}

// Helper function to extract text from PDF
async function extractTextFromPDF(filePath) {
  try {
    const pdfBytes = fs.readFileSync(filePath);
    const pdfDoc = await PDFDocument.load(pdfBytes);
    const pages = pdfDoc.getPages();
    let text = '';
    
    for (let i = 0; i < pages.length; i++) {
      const page = pages[i];
      text += await page.getText() + '\n';
    }
    
    return text;
  } catch (error) {
    throw new Error(`Failed to extract text from PDF: ${error.message}`);
  }
}

// Helper function to extract text from DOCX
async function extractTextFromDOCX(filePath) {
  try {
    const result = await mammoth.extractRawText({ path: filePath });
    return result.value;
  } catch (error) {
    throw new Error(`Failed to extract text from DOCX: ${error.message}`);
  }
}

// Helper function to read text from TXT
async function readTextFromTXT(filePath) {
  try {
    return fs.readFileSync(filePath, 'utf8');
  } catch (error) {
    throw new Error(`Failed to read text file: ${error.message}`);
  }
}

// Transcribe audio/video using Whisper
async function transcribeMedia(filePath) {
  console.log('Starting transcription...');
  const formData = new FormData();
  formData.append('audio_file', fs.createReadStream(filePath));

  try {
    console.log(`Sending request to ${whisperUrl}/asr`);
    const response = await axios.post(`${whisperUrl}/asr`, formData, {
      headers: {
        ...formData.getHeaders(),
        'Accept': 'application/json'
      },
      timeout: 300000 // 5 minute timeout
    });

    console.log('Transcription completed successfully');
    return response.data;
  } catch (error) {
    console.error('Transcription error:', error.message);
    if (error.response) {
      console.error('Whisper response:', error.response.data);
    }
    throw new Error('Transcription failed: ' + error.message);
  }
}

// Analyze text using Ollama
async function analyzeText(text, prompt, model) {
  try {
    const response = await axios.post(`${ollamaUrl}/api/generate`, {
      model: model,
      prompt: `${prompt}\n\n${text}`,
      stream: false
    });

    return response.data.response;
  } catch (error) {
    console.error('Analysis error:', error.message);
    throw new Error('Analysis failed: ' + error.message);
  }
}

// Routes
app.get('/models', async (req, res) => {
  try {
    // Test Ollama connection first
    try {
      await axios.get(`${ollamaUrl}/api/version`, { timeout: 2000 });
    } catch (error) {
      console.error('Ollama service check failed:', error.message);
      return res.status(503).json({
        error: 'Ollama service unavailable',
        details: 'Cannot connect to Ollama. Please ensure the service is running.',
        code: error.code
      });
    }

    const models = await getModels();
    res.json({ models });
  } catch (error) {
    console.error('Error in /models endpoint:', error);
    res.status(500).json({ 
      error: 'Error fetching models',
      details: error.message,
      code: error.code
    });
  }
});

app.post('/upload', upload.single('file'), async (req, res) => {
  let textContent = null;
  let analysisResult = null;

  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No file uploaded' });
    }

    console.log('File received:', {
      filename: req.file.originalname,
      mimetype: req.file.mimetype,
      size: req.file.size
    });

    // Extract text based on file type
    switch (req.file.mimetype) {
      case 'application/pdf':
        textContent = await extractTextFromPDF(req.file.path);
        break;
      case 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        textContent = await extractTextFromDOCX(req.file.path);
        break;
      case 'text/plain':
        textContent = await readTextFromTXT(req.file.path);
        break;
      default:
        // For audio/video files, use transcription
        const transcriptionResult = await transcribeMedia(req.file.path);
        textContent = transcriptionResult.text;
    }

    // Analyze the text
    try {
      const analysisPrompt = req.body.prompt || 'Analyze the following text and provide insights about its content, sentiment, and key points:';
      const model = req.body.model || 'llama2';
      
      analysisResult = await analyzeText(textContent, analysisPrompt, model);
      console.log('Analysis successful, length:', analysisResult.length);
    } catch (error) {
      return res.json({
        text: textContent,
        analysis: null,
        warning: `Analysis failed: ${error.message}`
      });
    }

    // Return both results
    res.json({
      text: textContent,
      analysis: analysisResult
    });

  } catch (error) {
    console.error('Error processing file:', error);
    console.error('Error details:', {
      message: error.message,
      textSuccess: !!textContent,
      analysisSuccess: !!analysisResult
    });

    res.status(500).json({ 
      error: 'Error processing file',
      details: error.message,
      text: textContent, // Include text if we have it
      analysis: null
    });

  } finally {
    // Clean up uploaded file
    if (req.file && fs.existsSync(req.file.path)) {
      fs.unlinkSync(req.file.path);
    }
  }
});

// Generate endpoint for direct text generation
app.post('/generate', async (req, res) => {
  try {
    const { model, prompt, stream = false } = req.body;

    // Validate required fields
    if (!model) {
      return res.status(400).json({
        error: 'Missing required field',
        details: 'Model name is required'
      });
    }

    if (!prompt || prompt.trim().length === 0) {
      return res.status(400).json({
        error: 'Missing required field',
        details: 'Prompt cannot be empty'
      });
    }

    // Check if model exists
    try {
      const models = await getModels();
      if (!models.some(m => m.name === model)) {
        return res.status(400).json({
          error: 'Invalid model',
          details: `Model '${model}' is not available. Please choose from: ${models.map(m => m.name).join(', ')}`
        });
      }
    } catch (error) {
      console.error('Error checking model availability:', error);
      return res.status(503).json({
        error: 'Service unavailable',
        details: 'Could not verify model availability. Please ensure Ollama is running.'
      });
    }

    // Make request to Ollama
    try {
      console.log('Starting generation with:', {
        model,
        promptLength: prompt.length,
        stream
      });

      if (stream) {
        // Set headers for SSE
        res.setHeader('Content-Type', 'text/event-stream');
        res.setHeader('Cache-Control', 'no-cache');
        res.setHeader('Connection', 'keep-alive');

        // Create axios request with responseType: 'stream'
        const response = await axios.post(`${ollamaUrl}/api/generate`, {
          model,
          prompt,
          stream: true
        }, {
          responseType: 'stream',
          timeout: 300000 // 5 minute timeout for streaming
        });

        // Handle streaming response
        response.data.on('data', chunk => {
          try {
            const lines = chunk.toString().split('\n').filter(line => line.trim());
            lines.forEach(line => {
              try {
                const data = JSON.parse(line);
                // Send each chunk as an SSE event
                res.write(`data: ${JSON.stringify({
                  response: data.response,
                  done: data.done
                })}\n\n`);

                // If this is the final message, end the stream
                if (data.done) {
                  res.end();
                }
              } catch (e) {
                console.error('Error parsing streaming response:', e);
              }
            });
          } catch (e) {
            console.error('Error processing stream chunk:', e);
          }
        });

        // Handle stream errors
        response.data.on('error', error => {
          console.error('Stream error:', error);
          res.write(`data: ${JSON.stringify({
            error: 'Stream error',
            details: error.message,
            done: true
          })}\n\n`);
          res.end();
        });

        // Clean up on client disconnect
        req.on('close', () => {
          response.data.destroy();
        });
      } else {
        // Non-streaming response (existing code)
        const response = await axios.post(`${ollamaUrl}/api/generate`, {
          model,
          prompt,
          stream: false
        }, {
          timeout: 60000 // 1 minute timeout for non-streaming
        });

        if (!response.data || !response.data.response) {
          throw new Error('Invalid response from Ollama');
        }

        res.json({
          response: response.data.response,
          model,
          prompt_length: prompt.length
        });
      }
    } catch (error) {
      console.error('Generation error:', error);
      
      if (error.code === 'ECONNREFUSED' || error.code === 'ETIMEDOUT') {
        return res.status(503).json({
          error: 'Service unavailable',
          details: 'Cannot connect to Ollama service. Please ensure it is running.'
        });
      }

      if (error.response?.status === 404) {
        return res.status(404).json({
          error: 'Model not found',
          details: `Model '${model}' was not found in Ollama`
        });
      }

      if (error.response?.status === 400) {
        return res.status(400).json({
          error: 'Bad request',
          details: error.response.data.error || 'Invalid request to Ollama service'
        });
      }

      res.status(500).json({
        error: 'Generation failed',
        details: error.message
      });
    }
  } catch (error) {
    console.error('Unexpected error in /generate:', error);
    res.status(500).json({
      error: 'Internal server error',
      details: 'An unexpected error occurred'
    });
  }
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'healthy' });
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
  console.log(`Whisper service URL: ${whisperUrl}`);
  console.log(`Ollama service URL: ${ollamaUrl}`);
}); 