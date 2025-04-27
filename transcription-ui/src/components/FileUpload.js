import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import { Box, Button, CircularProgress, Typography, Alert } from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';

const MAX_FILE_SIZE = 100 * 1024 * 1024; // 100MB

const FileUpload = ({ onTranscriptionComplete, onError, prompt, model }) => {
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [error, setError] = useState(null);

  const onDrop = useCallback(async (acceptedFiles) => {
    const file = acceptedFiles[0];
    
    // Validate file size
    if (file.size > MAX_FILE_SIZE) {
      setError(`File size (${(file.size / (1024 * 1024)).toFixed(2)}MB) exceeds the maximum limit of ${MAX_FILE_SIZE / (1024 * 1024)}MB`);
      return;
    }

    setUploading(true);
    setError(null);
    
    const formData = new FormData();
    formData.append('file', file);
    formData.append('prompt', prompt);
    formData.append('model', model);

    try {
      const response = await axios.post('http://localhost:8081/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          setUploadProgress(percentCompleted);
        },
        maxContentLength: Infinity,
        maxBodyLength: Infinity
      });

      if (response.data.error) {
        throw new Error(response.data.error);
      }

      onTranscriptionComplete(response.data);
    } catch (error) {
      console.error('Upload error:', error);
      const errorMessage = error.response?.data?.error || error.message || 'An error occurred during upload';
      setError(errorMessage);
      onError(errorMessage);
    } finally {
      setUploading(false);
      setUploadProgress(0);
    }
  }, [onTranscriptionComplete, onError, prompt, model]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'audio/*': ['.mp3', '.wav'],
      'video/*': ['.mp4', '.mov'],
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'text/plain': ['.txt']
    },
    multiple: false
  });

  return (
    <Box sx={{ width: '100%', textAlign: 'center' }}>
      <Box
        {...getRootProps()}
        sx={{
          border: '2px dashed #ccc',
          borderRadius: 2,
          p: 3,
          mb: 2,
          cursor: 'pointer',
          backgroundColor: isDragActive ? '#f0f0f0' : 'transparent',
          '&:hover': {
            backgroundColor: '#f0f0f0'
          }
        }}
      >
        <input {...getInputProps()} />
        <CloudUploadIcon sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
        <Typography variant="h6" gutterBottom>
          {isDragActive ? 'Drop the file here' : 'Drag & drop a file here, or click to select'}
        </Typography>
        <Typography variant="body2" color="textSecondary">
          Supported formats: MP3, WAV, MP4, MOV, PDF, DOCX, TXT
        </Typography>
        <Typography variant="body2" color="textSecondary">
          Maximum file size: {MAX_FILE_SIZE / (1024 * 1024)}MB
        </Typography>
      </Box>

      {uploading && (
        <Box sx={{ mt: 2, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          <CircularProgress variant="determinate" value={uploadProgress} />
          <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
            {uploadProgress}% uploaded
          </Typography>
        </Box>
      )}

      {error && (
        <Alert severity="error" sx={{ mt: 2 }}>
          {error}
        </Alert>
      )}
    </Box>
  );
};

export default FileUpload; 