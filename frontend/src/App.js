import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BrowserRouter, Route, Routes } from 'react-router-dom';

import Navbar from './components/Navbar';
import Users from './components/Users';
import Foods from './components/Foods';

function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/users" element={<Users />} />
        <Route path="/foods" element={<Foods />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
