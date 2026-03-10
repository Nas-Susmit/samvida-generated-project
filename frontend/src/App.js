import React, { useState, useEffect } from 'react';
import api from './services/api';

function App() {
  const [items, setItems] = useState([]);
  const [newItemName, setNewItemName] = useState('');
  const [newItemDescription, setNewItemDescription] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchItems();
  }, []);

  const fetchItems = async () => {
    try {
      setLoading(true);
      const response = await api.get('/items/');
      setItems(response.data);
      setError(null);
    } catch (err) {
      console.error('Error fetching items:', err);
      setError('Failed to fetch items. Please ensure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const addItem = async (e) => {
    e.preventDefault();
    if (!newItemName.trim()) {
      alert('Item name cannot be empty.');
      return;
    }
    try {
      const response = await api.post('/items/', {
        name: newItemName,
        description: newItemDescription
      });
      setItems([...items, response.data]);
      setNewItemName('');
      setNewItemDescription('');
      setError(null);
    } catch (err) {
      console.error('Error adding item:', err);
      setError('Failed to add item. Please try again.');
    }
  };

  const updateItemStatus = async (item) => {
    try {
      const updatedItem = { ...item, is_completed: !item.is_completed };
      const response = await api.put(`/items/${item.id}`, updatedItem);
      setItems(items.map((i) => (i.id === item.id ? response.data : i)));
      setError(null);
    } catch (err) {
      console.error('Error updating item:', err);
      setError('Failed to update item. Please try again.');
    }
  };

  const deleteItem = async (itemId) => {
    if (!window.confirm('Are you sure you want to delete this item?')) {
      return;
    }
    try {
      await api.delete(`/items/${itemId}`);
      setItems(items.filter((item) => item.id !== itemId));
      setError(null);
    } catch (err) {
      console.error('Error deleting item:', err);
      setError('Failed to delete item. Please try again.');
    }
  };

  if (loading) return <div className="loading-message">Loading items...</div>;
  if (error) return <div className="error-message">Error: {error}</div>;

  return (
    <div className="App">
      <h1>Item Manager</h1>

      <form onSubmit={addItem}>
        <h2>Add New Item</h2>
        <div>
          <label htmlFor="itemName">Item Name:</label>
          <input
            id="itemName"
            type="text"
            value={newItemName}
            onChange={(e) => setNewItemName(e.target.value)}
            placeholder="e.g., Buy groceries"
            required
          />
        </div>
        <div>
          <label htmlFor="itemDescription">Description (Optional):</label>
          <textarea
            id="itemDescription"
            value={newItemDescription}
            onChange={(e) => setNewItemDescription(e.target.value)}
            placeholder="e.g., Milk, eggs, bread for the week."
            rows="3"
          />
        </div>
        <button type="submit">Add Item</button>
      </form>

      <h2>Current Items</h2>
      {items.length === 0 ? (
        <p className="empty-message">No items found. Add one above!</p>
      ) : (
        <ul>
          {items.map((item) => (
            <li key={item.id}>
              <h3>{item.name}</h3>
              {item.description && <p>{item.description}</p>}
              <div className="item-actions">
                <label>
                  <input
                    type="checkbox"
                    checked={item.is_completed}
                    onChange={() => updateItemStatus(item)}
                  />
                  {item.is_completed ? 'Completed' : 'Mark as Complete'}
                </label>
                <button onClick={() => deleteItem(item.id)}>Delete</button>
              </div>
            </li>
          ))
          }
        </ul>
      )}
    </div>
  );
}

export default App;
