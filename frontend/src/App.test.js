import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import axios from 'axios';
import { render, waitFor } from '@testing-library/react';

jest.mock('axios');

describe('App component', () => {
  it('renders users, food intake and physical activity', async () => {
    axios.get.mockResolvedValueOnce({ data: [] });
    axios.get.mockResolvedValueOnce({ data: [] });
    axios.get.mockResolvedValueOnce({ data: [] });

    const { getByText } = render(<App />);

    await waitFor(() => {
      expect(getByText('Users')).toBeInTheDocument();
      expect(getByText('Food Intake')).toBeInTheDocument();
      expect(getByText('Physical Activity')).toBeInTheDocument();
    });
  });
});
