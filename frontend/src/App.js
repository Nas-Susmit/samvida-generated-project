import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [dailyCalorieGoals, setDailyCalorieGoals] = useState('');

  const [foodName, setFoodName] = useState('');
  const [calories, setCalories] = useState('');
  const [date, setDate] = useState('');

  const [user, setUser] = useState({});
  const [foodIntake, setFoodIntake] = useState([]);
  const [foodDatabase, setFoodDatabase] = useState([]);

  const createUser = async () => {
    try {
      const response = await axios.post('http://localhost:8000/users', {
        username,
        password,
        dailyCalorieGoals
      });
      console.log(response);
    } catch (error) {
      console.error(error);
    }
  };

  const getUserDetails = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/users/1`);
      setUser(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  const logFoodIntake = async () => {
    try {
      const response = await axios.post('http://localhost:8000/food-intake', {
        user_id: 1,
        food_name: foodName,
        calories,
        date
      });
      console.log(response);
    } catch (error) {
      console.error(error);
    }
  };

  const getFoodIntakeHistory = async () => {
    try {
      const response = await axios.get('http://localhost:8000/food-intake/1');
      setFoodIntake(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    getUserDetails();
    getFoodIntakeHistory();
  }, []);

  return (
    <div>
      <h1>Frontend</h1>
      <form>
        <label>Username:</label>
        <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} />
        <br />
        <label>Password:</label>
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        <br />
        <label>Daily Calorie Goals:</label>
        <input type="number" value={dailyCalorieGoals} onChange={(e) => setDailyCalorieGoals(e.target.value)} />
        <br />
        <button type="button" onClick={createUser}>Create User</button>
      </form>
      <br />
      <h2>Food Intake</h2>
      <form>
        <label>Food Name:</label>
        <input type="text" value={foodName} onChange={(e) => setFoodName(e.target.value)} />
        <br />
        <label>Calories:</label>
        <input type="number" value={calories} onChange={(e) => setCalories(e.target.value)} />
        <br />
        <label>Date:</label>
        <input type="date" value={date} onChange={(e) => setDate(e.target.value)} />
        <br />
        <button type="button" onClick={logFoodIntake}>Log Food Intake</button>
      </form>
      <br />
      <h2>Food Intake History</h2>
      <ul>
        {foodIntake.map((food) => (
          <li key={food.id}>{food.food_name} - {food.calories} calories - {food.date}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
