import React, { useState, useEffect, useCallback } from 'react';
import * as math from 'mathjs';
import { getHistory, postCalculation } from './services/api';

const Calculator = () => {
  const [expression, setExpression] = useState('');
  const [result, setResult] = useState('0');
  const [unitMode, setUnitMode] = useState('degrees'); // 'degrees' or 'radians'
  const [history, setHistory] = useState([]);
  const [error, setError] = useState('');

  // Create a math.js instance that can be reconfigured based on unitMode
  const [mathInstance, setMathInstance] = useState(() => math.create(math.all, { unit: 'degrees' }));

  // Effect to reconfigure math.js instance when unitMode changes
  useEffect(() => {
    // math.js expects 'deg' or 'rad' for the unit property
    const newUnitConfig = unitMode === 'degrees' ? 'deg' : 'rad';
    setMathInstance(prev => { 
      prev.config({ unit: newUnitConfig });
      return prev; 
    });
  }, [unitMode]);

  const fetchHistory = useCallback(async () => {
    try {
      const response = await getHistory();
      setHistory(response.data);
    } catch (err) {
      console.error('Failed to fetch history:', err);
      setError('Failed to load history.');
    }
  }, []);

  useEffect(() => {
    fetchHistory();
  }, [fetchHistory]);

  const handleButtonClick = (value) => {
    setError('');

    // If a number is entered after a result (and no operator), start a new calculation
    if (result !== '0' && expression === '' && !isNaN(parseFloat(value)) && isFinite(value)) {
      setExpression(value);
      setResult('0'); // Reset result when starting new expression
      return;
    }

    // Handle operators after a previous result
    if (['+', '-', '*', '/'].includes(value) && !expression && result !== '0') {
      setExpression(result + value);
      setResult('0'); // Clear result for new operation
    } else if (value === '=' && expression === '' && result !== '0') {
      // If '=' is pressed with a result but no new expression, do nothing or re-evaluate result
      return; 
    } else if (value === 'AC') {
      handleClear();
    } else if (value === 'CE') {
      handleClearEntry();
    } else if (value === '=') {
      handleEquals();
    } else if (value === 'toggleUnit') {
      handleUnitToggle();
    } else {
      setExpression((prev) => prev + value);
    }
  };

  const handleClear = () => {
    setExpression('');
    setResult('0');
    setError('');
  };

  const handleClearEntry = () => {
    setError('');
    setExpression((prev) => prev.slice(0, -1));
    if (expression.length === 1) {
      setResult('0');
    }
  };

  const handleEquals = async () => {
    setError('');
    if (!expression) {
      if (result !== '0' && result !== 'Error') { // If there's a previous result but no new expression, effectively do nothing
          return;
      }
      setResult('0'); // Reset if expression is empty and result is 0 or Error
      return;
    }

    let calculatedResult = '';
    try {
      // Client-side calculation for immediate feedback and error handling
      calculatedResult = mathInstance.evaluate(expression);
      
      // Format result: convert to integer if it's a whole number
      let formattedResult = String(calculatedResult);
      if (typeof calculatedResult === 'number' && calculatedResult % 1 === 0) {
        formattedResult = String(parseInt(calculatedResult));
      }
      setResult(formattedResult);

      // Post to backend for logging and persistence
      const response = await postCalculation({
        expression: expression,
        unit_mode: unitMode,
      });
      // Add new calculation to history, keeping it limited (e.g., 100 items)
      setHistory((prev) => [response.data, ...prev].slice(0, 100)); 

    } catch (e) {
      console.error('Calculation error:', e);
      setResult('Error');
      setError('Invalid expression');
    }
    setExpression(''); // Clear expression after evaluation
  };

  const handleUnitToggle = () => {
    setUnitMode((prev) => (prev === 'degrees' ? 'radians' : 'degrees'));
    setError('');
  };

  // Define calculator buttons and their properties
  const buttons = [
    { value: 'AC', className: 'clear', handler: () => handleButtonClick('AC') },
    { value: 'CE', className: 'ce', handler: () => handleButtonClick('CE') },
    { value: '(', className: 'function' },
    { value: ')', className: 'function' },

    { value: 'sin', className: 'function', handler: () => handleButtonClick('sin(') },
    { value: 'cos', className: 'function', handler: () => handleButtonClick('cos(') },
    { value: 'tan', className: 'function', handler: () => handleButtonClick('tan(') },
    { value: '/', className: 'operator' },

    { value: '7' },
    { value: '8' },
    { value: '9' },
    { value: '*', className: 'operator' },

    { value: '4' },
    { value: '5' },
    { value: '6' },
    { value: '-', className: 'operator' },

    { value: '1' },
    { value: '2' },
    { value: '3' },
    { value: '+', className: 'operator' },

    { value: 'e', className: 'function', handler: () => handleButtonClick('e') },
    { value: '0' },
    { value: '.', className: 'function' },
    { value: '=', className: 'equals', handler: () => handleButtonClick('=') },

    { value: 'pi', className: 'function', handler: () => handleButtonClick('pi') },
    { value: 'sqrt', className: 'function', handler: () => handleButtonClick('sqrt(') },
    { value: '^', className: 'function' },
    { value: 'log', className: 'function', handler: () => handleButtonClick('log(') },
  ];

  return (
    <>
      <div className="calculator-container">
        <div className="display">
          <div className="expression-display">{expression || '0'}</div>
          <div className="result-display" style={{ color: error ? 'red' : 'white' }}>{error || result}</div>
        </div>
        <div className="unit-toggle-container">
          <button onClick={handleUnitToggle} className="unit-toggle-button" aria-label="Toggle unit mode">
            Unit: {unitMode === 'degrees' ? 'Degrees' : 'Radians'}
          </button>
        </div>
        <div className="buttons-grid">
          {buttons.map((btn) => (
            <button
              key={btn.value}
              className={`button ${btn.className || ''}`}
              onClick={btn.handler || (() => handleButtonClick(btn.value))}
              aria-label={btn.value === '=' ? 'Equals' : btn.value}
            >
              {btn.value === 'pi' ? '\u03c0' : btn.value === 'sqrt' ? '\u221a' : btn.value}
            </button>
          ))}
        </div>
      </div>
      <div className="history-panel">
        <h2>Calculation History</h2>
        <ul className="history-list">
          {history.length > 0 ? (
            history.map((item) => (
              <li key={item.id} className="history-item">
                <span className="history-item-expression">{item.expression}</span>
                <span className="history-item-result">= {item.result}</span>
              </li>
            ))
          ) : (
            <li className="no-history">No history yet.</li>
          )}
        </ul>
      </div>
    </>
  );
};

export default Calculator;
