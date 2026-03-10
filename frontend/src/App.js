import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [users, setUsers] = useState([]);
  const [foodIntake, setFoodIntake] = useState([]);
  const [physicalActivity, setPhysicalActivity] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:8000/api/users')
      .then(response => {
        setUsers(response.data);
      });

    axios.get('http://localhost:8000/api/food_intake')
      .then(response => {
        setFoodIntake(response.data);
      });

    axios.get('http://localhost:8000/api/physical_activity')
      .then(response => {
        setPhysicalActivity(response.data);
      });
  }, []);

  return (
    <div>
      <h1>Users</h1>
      <ul>
        {users.map(user => (
          <li key={user.id}>{user.email}</li>
        ))}
      </ul>

      <h1>Food Intake</h1>
      <ul>
        {foodIntake.map(intake => (
          <li key={intake.id}>{intake.food_name} - {intake.calories} calories</li>
        ))}
      </ul>

      <h1>Physical Activity</h1>
      <ul>
        {physicalActivity.map(activity => (
          <li key={activity.id}>{activity.activity_name} - {activity.calories_burned} calories</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
