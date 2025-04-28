const express = require('express');
const cors = require('cors');
const multer = require('multer');
const path = require('path');
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');
const { PDFDocument } = require('pdf-lib');
const mammoth = require('mammoth');
const pdfParse = require('pdf-parse');
const analysisService = require('./server/routes/analysis-service');
const { EMOTIONAL_PERSONAS } = require('../scoringengine');

const app = express();
const port = process.env.PORT || 3003;
const whisperUrl = process.env.WHISPER_URL || 'http://whisper:9000';
const ollamaUrl = process.env.OLLAMA_URL || 'http://host.docker.internal:11434';

// Configure CORS
app.use(cors({
  origin: ['http://localhost:8081', 'http://localhost:3003'],
  methods: ['GET', 'POST'],
  allowedHeaders: ['Content-Type']
}));
app.use('/api', analysisService);

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

// Configure axios with increased limits
const axiosInstance = axios.create({
  maxBodyLength: Infinity,
  maxContentLength: Infinity,
  timeout: 300000 // 5 minute timeout
});

// Middleware
app.use(express.static('public'));
app.use(express.json());

// Helper function to check if Ollama is available
async function checkOllamaConnection() {
  try {
    console.log('Checking Ollama connection...');
    const response = await axios.get(`${ollamaUrl}/api/tags`);
    console.log('Ollama connection successful:', response.data);
    return true;
  } catch (error) {
    console.error('Ollama connection error:', {
      message: error.message,
      code: error.code,
      response: error.response?.data
    });
    return false;
  }
}

// Helper function to extract text from PDF
async function extractTextFromPDF(filePath) {
  try {
    console.log('Extracting text from PDF:', filePath);
    // Switch to pdf-parse for reliable text extraction
    const dataBuffer = fs.readFileSync(filePath);
    const data = await pdfParse(dataBuffer);
    console.log('PDF text extraction successful, length:', data.text.length);
    return data.text;
  } catch (error) {
    console.error('PDF extraction error:', {
      message: error.message,
      stack: error.stack
    });
    throw new Error(`Failed to extract text from PDF: ${error.message}`);
  }
}

// Helper function to extract text from DOCX
async function extractTextFromDOCX(filePath) {
  try {
    console.log('Extracting text from DOCX:', filePath);
    const result = await mammoth.extractRawText({ path: filePath });
    console.log('DOCX text extraction successful, length:', result.value.length);
    return result.value;
  } catch (error) {
    console.error('DOCX extraction error:', {
      message: error.message,
      stack: error.stack
    });
    throw new Error(`Failed to extract text from DOCX: ${error.message}`);
  }
}

// Helper function to read text from TXT
async function readTextFromTXT(filePath) {
  try {
    console.log('Reading text file:', filePath);
    const text = fs.readFileSync(filePath, 'utf8');
    console.log('Text file read successful, length:', text.length);
    return text;
  } catch (error) {
    console.error('Text file read error:', {
      message: error.message,
      stack: error.stack
    });
    throw new Error(`Failed to read text file: ${error.message}`);
  }
}

// Transcribe audio/video using Whisper
async function transcribeMedia(filePath) {
  console.log('Starting transcription...');
  const formData = new FormData();
  
  try {
    // Get file stats
    const stats = fs.statSync(filePath);
    console.log(`File size: ${(stats.size / (1024 * 1024)).toFixed(2)} MB`);
    
    // Stream the file instead of loading it all at once
    formData.append('audio_file', fs.createReadStream(filePath));
    formData.append('task', 'transcribe');
    formData.append('language', 'en');

    console.log(`Sending request to ${whisperUrl}/asr`);
    const response = await axiosInstance.post(`${whisperUrl}/asr`, formData, {
      headers: {
        ...formData.getHeaders(),
        'Accept': 'application/json'
      },
      maxContentLength: Infinity,
      maxBodyLength: Infinity,
      timeout: 300000 // 5 minute timeout
    });

    console.log('Transcription completed successfully:', response.data);
    return response.data;
  } catch (error) {
    console.error('Transcription error:', {
      message: error.message,
      code: error.code,
      response: error.response?.data,
      stack: error.stack
    });
    
    // Provide more specific error messages
    if (error.code === 'ECONNREFUSED') {
      throw new Error('Could not connect to transcription service. Please ensure the service is running.');
    }
    if (error.code === 'ETIMEDOUT') {
      throw new Error('Transcription request timed out. The file might be too large or the service is busy.');
    }
    if (error.response?.status === 413) {
      throw new Error('File is too large for the transcription service to process.');
    }
    
    throw new Error(`Transcription failed: ${error.message}`);
  }
}

// Analyze text using Ollama
async function analyzeText(text, prompt, model) {
  try {
    // Check Ollama connection first
    const isOllamaAvailable = await checkOllamaConnection();
    if (!isOllamaAvailable) {
      throw new Error('Cannot connect to Ollama service. Please ensure Ollama is running and accessible.');
    }

    console.log('Sending analysis request to Ollama:', {
      model,
      promptLength: prompt.length,
      textLength: text.length
    });

    // Format the prompt to be more explicit
    const formattedPrompt = `You are a text analysis assistant. Your task is to ${prompt}\n\nHere is the text to analyze:\n\n"${text}"\n\nPlease provide your analysis:`;

    const response = await axios.post(`${ollamaUrl}/api/generate`, {
      model: model,
      prompt: formattedPrompt,
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

    if (!response.data || !response.data.response) {
      console.error('Invalid Ollama response:', response.data);
      throw new Error('Invalid response from Ollama service');
    }

    console.log('Analysis completed successfully, response length:', response.data.response.length);
    return response.data.response;
  } catch (error) {
    console.error('Analysis error:', {
      message: error.message,
      code: error.code,
      response: error.response?.data,
      stack: error.stack
    });
    
    if (error.code === 'ECONNREFUSED') {
      throw new Error('Cannot connect to Ollama service. Please ensure Ollama is running and accessible.');
    }
    if (error.response?.status === 404) {
      throw new Error(`Model '${model}' not found. Please ensure the model is installed in Ollama.`);
    }
    throw new Error('Analysis failed: ' + error.message);
  }
}

app.post('/upload', upload.single('file'), async (req, res) => {
  let textContent = null;
  let analysisResult = null;

  try {
    console.log('Upload request received');
    
    if (!req.file) {
      console.error('No file uploaded');
      return res.status(400).json({ error: 'No file uploaded' });
    }

    console.log('File received:', {
      filename: req.file.originalname,
      mimetype: req.file.mimetype,
      size: req.file.size,
      path: req.file.path
    });

    // Extract text based on file type
    try {
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
    } catch (error) {
      console.error('Text extraction error:', {
        message: error.message,
        stack: error.stack
      });
      throw new Error(`Failed to extract text: ${error.message}`);
    }

    if (!textContent || textContent.trim().length === 0) {
      console.error('No text content extracted');
      throw new Error('No text content could be extracted from the file');
    }

    console.log('Text extraction successful, length:', textContent.length);

    // Analyze the text
    try {
      const analysisPrompt = req.body.prompt || 'Analyze the following text and provide insights about its content, sentiment, and key points:';
      const model = req.body.model || 'llama2';
      
      console.log('Starting analysis with:', {
        model,
        promptLength: analysisPrompt.length
      });

      analysisResult = await analyzeText(textContent, analysisPrompt, model);
      console.log('Analysis successful, length:', analysisResult.length);
    } catch (error) {
      console.error('Analysis error:', {
        message: error.message,
        stack: error.stack
      });
      // If analysis fails but we have text, return the text with a warning
      return res.json({
        text: textContent,
        analysis: null,
        warning: `Analysis failed: ${error.message}`
      });
    }

    // Return both results
    console.log('Sending successful response');
    res.json({
      text: textContent,
      analysis: analysisResult
    });

  } catch (error) {
    console.error('Error processing file:', {
      message: error.message,
      stack: error.stack,
      textContent: !!textContent,
      analysisResult: !!analysisResult
    });
    res.status(500).json({ 
      error: 'Error processing file',
      details: error.message
    });
  } finally {
    // Clean up uploaded file
    if (req.file && fs.existsSync(req.file.path)) {
      try {
        fs.unlinkSync(req.file.path);
        console.log('Cleaned up uploaded file:', req.file.path);
      } catch (error) {
        console.error('Error cleaning up file:', {
          path: req.file.path,
          message: error.message
        });
      }
    }
  }
});

app.get('/api/personas', (req, res) => {
  res.json(EMOTIONAL_PERSONAS);
});

// Start server
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
  console.log(`Whisper URL: ${whisperUrl}`);
  console.log(`Ollama URL: ${ollamaUrl}`);
}); 