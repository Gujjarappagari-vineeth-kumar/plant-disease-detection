export interface PredictionResult {
  disease_name: string;
  confidence: number;
  scientific_name: string;
  symptoms: string;
  treatment: string;
  all_predictions?: Array<{
    disease: string;
    confidence: number;
  }>;
}

export interface ImageUploadProps {
  onUploadStart: () => void;
  onPredictionResult: (result: PredictionResult) => void;
  onError: (error: string) => void;
}

export interface ResultDisplayProps {
  result: PredictionResult;
  usingTempModel?: boolean;
}