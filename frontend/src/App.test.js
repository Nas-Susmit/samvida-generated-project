import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react';
import App from './App';
import { BrowserRouter } from 'react-router-dom';

describe('App', () => {
  it('renders the navbar and routes', () => {
    const { getByText } = render(
      <BrowserRouter>
        <App />
      </BrowserRouter>
    );
    expect(getByText('Users')).toBeInTheDocument();
    expect(getByText('Foods')).toBeInTheDocument();
  });
});
