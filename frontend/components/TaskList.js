import React from 'react';

const TaskList = ({ tasks }) => {
  return (
    <div>
      {tasks.map(task => (
        <div key={task.id}>{task.title}</div>
      ))}
    </div>
  );
};

export default TaskList;