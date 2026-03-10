import axios from 'axios';

// Get API base URL from environment variables, defaulting to localhost:8000
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

// Create an Axios instance with base URL and default headers
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Sends a POST request to the /calculate endpoint.
 * @param {object} data - The calculation data containing expression and unit_mode.
 * @param {string} data.expression - The mathematical expression.
 * @param {string} data.unit_mode - The unit mode ('degrees' or 'radians').
 * @returns {Promise<AxiosResponse>} A promise that resolves to the API response.
 */
export const postCalculation = (data) => api.post('/calculate', data);

/**
 * Sends a GET request to the /history endpoint.
 * @returns {Promise<AxiosResponse>} A promise that resolves to the API response containing calculation history.
 */
export const getHistory = () => api.get('/history');

export default api;
