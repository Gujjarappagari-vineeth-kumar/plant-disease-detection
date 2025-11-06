import { useState, useEffect } from 'react';
import { 
  Box, 
  Typography, 
  Paper, 
  Container, 
  CircularProgress,
  Alert,
  Chip
} from '@mui/material';
import axios from 'axios';
import ImageUpload from './components/ImageUpload';
import ResultDisplay from './components/ResultDisplay';
import { PredictionResult } from './types';

// API Configuration
import { API_BASE_URL } from './config';

function App() {
  const [isLoading, setIsLoading] = useState(true);
  const [predictionResult, setPredictionResult] = useState<PredictionResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [trainingStatus, setTrainingStatus] = useState({
    inProgress: false,
    modelTrained: false,
    usingTempModel: false
  });

  // Check model status on component mount
  useEffect(() => {
    console.log("API Base URL:", API_BASE_URL);
    checkModelStatus();
  }, []);

  const checkModelStatus = async () => {
    try {
      setIsLoading(true);
      const response = await axios.get(`${API_BASE_URL}/health`);
      setError(null);
      
      // Update training status
      setTrainingStatus({
        inProgress: response.data.training_in_progress || false,
        modelTrained: response.data.model_trained || false,
        usingTempModel: response.data.using_temp_model || false
      });
    } catch (err) {
      console.error('Error checking model status:', err);
      setError('Unable to connect to the AI model. Please try again later.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleImageUpload = async (file: File) => {
    try {
      setError(null);
      setPredictionResult(null);

      const formData = new FormData();
      formData.append('file', file);

      const response = await axios.post(`${API_BASE_URL}/predict`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: 30000, // 30 second timeout
      });

      setPredictionResult(response.data);
    } catch (err: any) {
      console.error('Error uploading image:', err);
      
      let errorMessage = 'Error processing image';
      if (err.code === 'ECONNABORTED') {
        errorMessage = 'Request timed out. Please try again.';
      } else if (err.response?.data?.detail) {
        errorMessage = err.response.data.detail;
      } else if (err.message) {
        errorMessage = err.message;
      }
      
      setError(errorMessage);
    }
  };

  return (
    <Box className="animated-bg">
      <Container maxWidth="lg" sx={{ py: 4, position: 'relative', zIndex: 1 }}>
        {/* Header */}
        <Box sx={{ textAlign: 'center', mb: 4 }}>
          <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <Typography
              variant="h2"
              component="h1"
              sx={{
                fontWeight: 700,
                color: 'white',
                textShadow: '2px 2px 4px rgba(0,0,0,0.8)',
                mb: 2,
                fontSize: { xs: '2.5rem', md: '3.5rem' }
              }}
            >
              🌱 Plant Disease Detection
            </Typography>
            
            {trainingStatus.inProgress && (
              <Chip 
                label="Model Training in Progress" 
                color="warning" 
                icon={<CircularProgress size={16} color="inherit" />}
                sx={{ mb: 2, fontWeight: 'bold' }} 
              />
            )}
            
            {trainingStatus.usingTempModel && (
              <Chip 
                label="Using Temporary Model" 
                color="info" 
                sx={{ mb: 2, fontWeight: 'bold' }} 
              />
            )}
            
            {!trainingStatus.inProgress && trainingStatus.modelTrained && (
              <Chip 
                label="Using Trained Model" 
                color="success" 
                sx={{ mb: 2, fontWeight: 'bold' }} 
              />
            )}
          </Box>
          <Typography
            variant="h5"
            sx={{
              color: 'rgba(255, 255, 255, 0.9)',
              textShadow: '1px 1px 2px rgba(0,0,0,0.6)',
              fontWeight: 400,
              mb: 1
            }}
          >
            AI-Powered Plant Disease Analysis
          </Typography>
          <Typography
            variant="body1"
            sx={{
              color: 'rgba(255, 255, 255, 0.8)',
              textShadow: '1px 1px 2px rgba(0,0,0,0.6)',
              maxWidth: 600,
              mx: 'auto'
            }}
          >
            Upload a clear image of a plant leaf to detect diseases and get treatment recommendations
          </Typography>
        </Box>

        {/* Loading State */}
        {isLoading && (
          <Box
            sx={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              py: 8,
              background: 'rgba(255, 255, 255, 0.55)',
              backdropFilter: 'blur(10px)',
              borderRadius: '16px',
              border: '1px solid rgba(255, 255, 255, 0.2)',
              boxShadow: '0 8px 32px rgba(0, 0, 0, 0.1)'
            }}
          >
            <CircularProgress size={60} sx={{ color: '#4caf50', mb: 3 }} />
            <Typography variant="h6" color="primary" sx={{ fontWeight: 600 }}>
              Initializing AI Model...
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
              This may take a few moments on first load
            </Typography>
          </Box>
        )}

        {/* Main Content */}
        {!isLoading && (
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
            {/* Error Alert */}
            {error && (
              <Alert 
                severity="error" 
                sx={{ 
                  borderRadius: '12px',
                  background: 'rgba(255, 255, 255, 0.6)',
                  backdropFilter: 'blur(10px)'
                }}
                onClose={() => setError(null)}
              >
                {error}
              </Alert>
            )}

            {/* Upload Section */}
            <Paper
              elevation={3}
              sx={{
                background: 'rgba(255, 255, 255, 0.55)',
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(255, 255, 255, 0.2)',
                borderRadius: '16px',
                p: 4,
                boxShadow: '0 8px 32px rgba(0, 0, 0, 0.1)'
              }}
            >
                      <ImageUpload 
          onImageUpload={handleImageUpload} 
        />
            </Paper>

            {/* Results Section */}
            {predictionResult && (
              <Paper
                elevation={3}
                sx={{
                  background: 'rgba(255, 255, 255, 0.55)',
                  backdropFilter: 'blur(10px)',
                  border: '1px solid rgba(255, 255, 255, 0.2)',
                  borderRadius: '16px',
                  p: 4,
                  boxShadow: '0 8px 32px rgba(0, 0, 0, 0.1)'
                }}
              >
                <ResultDisplay result={predictionResult} usingTempModel={trainingStatus.usingTempModel} />
              </Paper>
            )}
          </Box>
        )}

        {/* Footer */}
        <Box sx={{ textAlign: 'center', mt: 6 }}>
          <Typography
            variant="body2"
            sx={{
              color: 'rgba(255, 255, 255, 0.7)',
              textShadow: '1px 1px 2px rgba(0,0,0,0.6)'
            }}
          >
            Powered by Deep Learning & Computer Vision
          </Typography>
        </Box>
      </Container>
    </Box>
  );
}

export default App;