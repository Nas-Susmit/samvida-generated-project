import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000'
});

export const getUsers = async () => {
  const response = await api.get('/users');
  return response.data;
};

export const getFoods = async () => {
  const response = await api.get('/foods');
  return response.data;
};
