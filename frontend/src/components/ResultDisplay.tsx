import { Typography, Box, LinearProgress, Divider, List, ListItem, ListItemText } from '@mui/material';
import type { ResultDisplayProps } from '../types';

const ResultDisplay = ({ result }: ResultDisplayProps) => {
  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 70) return 'success';
    if (confidence >= 40) return 'warning';
    return 'error';
  };

  return (
    <Box sx={{ p: 4 }}>
      <Typography 
        variant="h5" 
        gutterBottom 
        sx={{ 
          color: '#1b5e20',
          fontWeight: 600,
          mb: 3,
          display: 'flex',
          alignItems: 'center',
          gap: 1
        }}
      >
        🔍 Detection Results
      </Typography>
      
      <Box sx={{ mb: 3 }}>
        <Typography variant="subtitle1" gutterBottom>
          Primary Detection:
        </Typography>
        <Typography 
          variant="h4" 
          sx={{ 
            fontWeight: 'bold',
            color: result.disease_name === "Unknown" ? '#f57c00' : '#d32f2f',
            textShadow: '1px 1px 2px rgba(0,0,0,0.1)'
          }}
        >
          {result.disease_name === "Unknown" 
            ? "❓ Unknown Disease" 
            : result.disease_name.replace(/_/g, ' ')}
        </Typography>
        {result.disease_name === "Unknown" && (
          <>
            <Typography variant="body2" sx={{ mt: 1, color: '#5d4037', fontWeight: 500 }}>
              The model couldn't confidently identify this plant disease. This could be due to:
            </Typography>
            <Box component="ul" sx={{ mt: 1, pl: 2 }}>
              <Typography component="li" variant="body2" sx={{ color: '#6d4c41', mb: 0.5 }}>
                🌱 Poor image quality or lighting
              </Typography>
              <Typography component="li" variant="body2" sx={{ color: '#6d4c41', mb: 0.5 }}>
                🌿 Plant species not in our training dataset
              </Typography>
              <Typography component="li" variant="body2" sx={{ color: '#6d4c41', mb: 0.5 }}>
                🔍 Disease not clearly visible in the image
              </Typography>
              <Typography component="li" variant="body2" sx={{ color: '#6d4c41', mb: 0.5 }}>
                ✅ Image shows healthy plant (no disease present)
              </Typography>
            </Box>
            <Typography variant="body2" sx={{ mt: 2, color: '#4caf50', fontWeight: 500 }}>
              💡 Try uploading a clearer image of the affected leaf area.
            </Typography>
          </>
        )}
      </Box>

      {result.disease_name !== "Unknown" && (
        <Box sx={{ mb: 3 }}>
          <Typography variant="subtitle1" gutterBottom sx={{ color: '#2e7d32', fontWeight: 600 }}>
            🎯 Confidence Score:
          </Typography>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
            <Box sx={{ width: '100%', mr: 2 }}>
              <LinearProgress
                variant="determinate"
                value={result.confidence}
                color={getConfidenceColor(result.confidence)}
                sx={{ 
                  height: 12, 
                  borderRadius: 6,
                  backgroundColor: 'rgba(76, 175, 80, 0.2)',
                  '& .MuiLinearProgress-bar': {
                    borderRadius: 6,
                    background: `linear-gradient(90deg, ${getConfidenceColor(result.confidence) === 'success' ? '#4caf50' : getConfidenceColor(result.confidence) === 'warning' ? '#ff9800' : '#f44336'}, ${getConfidenceColor(result.confidence) === 'success' ? '#8bc34a' : getConfidenceColor(result.confidence) === 'warning' ? '#ffb74d' : '#ef5350'})`
                  }
                }}
              />
            </Box>
            <Box sx={{ minWidth: 60 }}>
              <Typography variant="h6" sx={{ 
                color: '#1b5e20', 
                fontWeight: 700,
                textAlign: 'center'
              }}>
                {`${Math.round(result.confidence)}%`}
              </Typography>
            </Box>
          </Box>
        </Box>
      )}

      <Divider sx={{ my: 2 }} />

      {result.all_predictions && (
        <Box sx={{ mb: 3 }}>
          <Typography variant="subtitle1" gutterBottom>
            All Detected Diseases:
          </Typography>
          <List>
            {result.all_predictions.map((pred, index) => (
              <ListItem key={index} sx={{ py: 0 }}>
                <ListItemText
                  primary={pred.disease.replace(/_/g, ' ')}
                  secondary={`Confidence: ${pred.confidence}%`}
                />
              </ListItem>
            ))}
          </List>
        </Box>
      )}

      <Divider sx={{ my: 2 }} />

      {result.disease_name !== "Unknown" && (
        <>
          <Box sx={{ mb: 3 }}>
            <Typography variant="subtitle1" gutterBottom sx={{ color: '#2e7d32', fontWeight: 600 }}>
              🔬 Scientific Name:
            </Typography>
            <Typography variant="body1" sx={{ 
              fontStyle: 'italic',
              color: '#5d4037',
              background: 'rgba(76, 175, 80, 0.1)',
              padding: 2,
              borderRadius: 2,
              border: '1px solid rgba(76, 175, 80, 0.2)'
            }}>
              {result.scientific_name}
            </Typography>
          </Box>

          <Box sx={{ mb: 3 }}>
            <Typography variant="subtitle1" gutterBottom sx={{ color: '#2e7d32', fontWeight: 600 }}>
              🚨 Symptoms:
            </Typography>
            <Typography variant="body1" sx={{ 
              color: '#5d4037',
              background: 'rgba(255, 152, 0, 0.1)',
              padding: 2,
              borderRadius: 2,
              border: '1px solid rgba(255, 152, 0, 0.2)'
            }}>
              {result.symptoms}
            </Typography>
          </Box>

          <Box>
            <Typography variant="subtitle1" gutterBottom sx={{ color: '#2e7d32', fontWeight: 600 }}>
              💊 Treatment:
            </Typography>
            <Typography variant="body1" sx={{ 
              color: '#5d4037',
              background: 'rgba(76, 175, 80, 0.1)',
              padding: 2,
              borderRadius: 2,
              border: '1px solid rgba(76, 175, 80, 0.2)'
            }}>
              {result.treatment}
            </Typography>
          </Box>
        </>
      )}
    </Box>
  );
};

export default ResultDisplay; 