# Import required libraries
import axios from 'axios';

# Define the API service
const api = axios.create({
    baseURL: 'http://localhost:8000/api/v1'
});

# Export the API service
export default api;
