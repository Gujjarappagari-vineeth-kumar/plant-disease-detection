// API base URL is provided via Vite env at build time
const DEFAULT_LOCAL_API = 'http://localhost:8000';

// Get API URL from environment variable or use default
// In production, this should be set via VITE_API_URL environment variable
// Vite only exposes variables prefixed with VITE_ to the client
const API_BASE_URL = import.meta.env.VITE_API_URL || DEFAULT_LOCAL_API;

export const API_ENDPOINTS = {
    PREDICT: `${API_BASE_URL}/predict`,
    HEALTH: `${API_BASE_URL}/health`,
    CLASSES: `${API_BASE_URL}/classes`
};

// Export API_BASE_URL for use in components
export { API_BASE_URL };
