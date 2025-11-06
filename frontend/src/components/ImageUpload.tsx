import { useCallback, useState, useEffect } from 'react';
import { useDropzone } from 'react-dropzone';
import { 
  Box, 
  Typography, 
  Paper, 
  Alert, 
  CircularProgress,
  Button
} from '@mui/material';
import { CloudUpload, Image } from '@mui/icons-material';

interface ImageUploadProps {
  onImageUpload: (file: File) => void;
}

const ImageUpload: React.FC<ImageUploadProps> = ({ onImageUpload }) => {
  const [isProcessing, setIsProcessing] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<'idle' | 'success' | 'error'>('idle');
  const [errorMessage, setErrorMessage] = useState('');
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  // Revoke previous object URL when it changes or component unmounts
  useEffect(() => {
    return () => {
      if (previewUrl) {
        URL.revokeObjectURL(previewUrl);
      }
    };
  }, [previewUrl]);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return;

    const file = acceptedFiles[0];
    
    // Validate file type
    if (!file.type.startsWith('image/')) {
      setErrorMessage('Please upload an image file (JPEG, PNG, etc.)');
      setUploadStatus('error');
      return;
    }

    // Validate file size (10MB limit)
    if (file.size > 10 * 1024 * 1024) {
      setErrorMessage('File size must be less than 10MB');
      setUploadStatus('error');
      return;
    }

    setIsProcessing(true);
    setUploadStatus('idle');
    setErrorMessage('');

    // Create local preview URL
    const nextUrl = URL.createObjectURL(file);
    setPreviewUrl((oldUrl) => {
      if (oldUrl) URL.revokeObjectURL(oldUrl);
      return nextUrl;
    });

    // Simulate processing delay for better UX
    setTimeout(() => {
      onImageUpload(file);
      setIsProcessing(false);
      setUploadStatus('success');
    }, 1000);
  }, [onImageUpload]);

  const { getRootProps, getInputProps, isDragActive, isDragReject, open } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.gif', '.bmp', '.webp']
    },
    maxFiles: 1,
    disabled: isProcessing
  });

  const getDropzoneStyle = () => ({
    border: previewUrl ? 'none' : '2px dashed',
    borderColor: previewUrl
      ? 'transparent'
      : isDragActive 
        ? '#4caf50' 
        : isDragReject 
          ? '#f44336' 
          : '#2196f3',
    borderRadius: '12px',
    padding: previewUrl ? 0 : '40px 20px',
    textAlign: 'center' as const,
    cursor: !isProcessing ? 'pointer' : 'not-allowed',
    opacity: 1,
    background: previewUrl
      ? 'transparent'
      : isDragActive 
        ? 'linear-gradient(135deg, rgba(76, 175, 80, 0.1) 0%, rgba(76, 175, 80, 0.05) 100%)'
        : isDragReject
          ? 'linear-gradient(135deg, rgba(244, 67, 54, 0.1) 0%, rgba(244, 67, 54, 0.05) 100%)'
          : 'linear-gradient(135deg, rgba(34, 139, 34, 0.1) 0%, rgba(144, 238, 144, 0.05) 100%)',
    transition: 'all 0.3s ease',
    position: 'relative' as const,
    overflow: 'hidden'
  });

  return (
    <Box sx={{ width: '100%', maxWidth: 600, mx: 'auto' }}>


      {/* Upload Area */}
      <Paper
        elevation={3}
        sx={{
          background: 'rgba(255, 255, 255, 0.95)',
          backdropFilter: 'blur(10px)',
          border: '1px solid rgba(255, 255, 255, 0.2)',
          borderRadius: '16px',
          overflow: 'hidden'
        }}
      >
        <Box
          {...getRootProps()}
          sx={getDropzoneStyle()}
        >
          <input {...getInputProps()} />
          
          {/* Processing Overlay */}
          {isProcessing && (
            <Box
              sx={{
                position: 'absolute',
                top: 0,
                left: 0,
                right: 0,
                bottom: 0,
                background: 'rgba(255, 255, 255, 0.9)',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                zIndex: 10
              }}
            >
              <CircularProgress size={40} sx={{ color: '#2e7d32', mb: 2 }} />
              <Typography variant="h6" sx={{ color: '#2e7d32', fontWeight: 600 }}>
                🌿 Analyzing Plant Health...
              </Typography>
            </Box>
          )}

          {previewUrl ? (
            <Box sx={{ width: '100%', height: 400, overflow: 'hidden' }}>
              <img
                src={previewUrl}
                alt="Uploaded preview"
                style={{ width: '100%', height: '100%', objectFit: 'contain', display: 'block' }}
              />
            </Box>
          ) : (
            <>
              {/* Upload Icon */}
              <CloudUpload 
                sx={{ 
                  fontSize: 64, 
                  color: '#4caf50',
                  mb: 2,
                  transition: 'all 0.3s ease'
                }} 
              />

              {/* Upload Text */}
              <Typography variant="h5" gutterBottom sx={{ fontWeight: 600 }}>
                {isDragActive 
                  ? 'Drop the image here' 
                  : isProcessing 
                    ? 'Processing...' 
                    : 'Upload Plant Image'}
              </Typography>

              <Typography variant="body1" color="text.secondary" sx={{ mb: 2 }}>
                {isDragActive 
                  ? 'Release to upload' 
                  : 'Drag & drop an image here, or click to select'}
              </Typography>
            </>
          )}

          {/* File Requirements (hidden when an image is selected) */}
          {!previewUrl && (
            <Box sx={{ mt: 2 }}>
              <Typography variant="caption" color="text.secondary" display="block">
                📸 Supported formats: JPEG, PNG, GIF, BMP, WebP
              </Typography>
              <Typography variant="caption" color="text.secondary" display="block">
                📏 Maximum size: 10MB
              </Typography>
              <Typography variant="caption" color="text.secondary" display="block">
                🌱 Best results with clear, well-lit leaf images
              </Typography>
            </Box>
          )}

          {/* Manual Upload Button */}
          {!previewUrl && (
            <Button
              variant="contained"
              startIcon={<Image />}
              disabled={isProcessing}
              onClick={(e) => { e.preventDefault(); open(); }}
              sx={{
                mt: 3,
                background: 'linear-gradient(45deg, #2e7d32 30%, #4caf50 90%)',
                color: 'white',
                borderRadius: '25px',
                padding: '12px 24px',
                fontSize: '1rem',
                fontWeight: 600,
                boxShadow: '0 3px 15px rgba(46, 125, 50, 0.4)',
                '&:hover': {
                  background: 'linear-gradient(45deg, #1b5e20 30%, #2e7d32 90%)',
                  boxShadow: '0 5px 20px rgba(46, 125, 50, 0.5)'
                },
                '&:disabled': {
                  background: '#ccc',
                  boxShadow: 'none'
                }
              }}
            >
              Choose Image
            </Button>
          )}
        </Box>
      </Paper>

      {/* Status Messages */}
      {uploadStatus === 'success' && (
        <Alert 
          severity="success" 
          sx={{ mt: 2, borderRadius: '12px' }}
          onClose={() => setUploadStatus('idle')}
        >
          Image uploaded successfully! Analyzing for plant diseases...
        </Alert>
      )}

      {uploadStatus === 'error' && (
        <Alert 
          severity="error" 
          sx={{ mt: 2, borderRadius: '12px' }}
          onClose={() => setUploadStatus('idle')}
        >
          {errorMessage}
        </Alert>
      )}


    </Box>
  );
};

export default ImageUpload; 