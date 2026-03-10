# Design Document for MyProject

## Architecture Overview
A typical three-tier web application architecture. A frontend client built with a modern JavaScript framework (e.g., React) interacts with a backend API (e.g., FastAPI) which in turn communicates with a relational database (e.g., PostgreSQL) for data persistence.

## Database Schema
{'tables': [{'name': 'tasks', 'columns': [{'name': 'id', 'type': 'UUID', 'constraints': ['PRIMARY KEY', 'NOT NULL', 'DEFAULT gen_random_uuid()']}, {'name': 'description', 'type': 'TEXT', 'constraints': ['NOT NULL']}, {'name': 'due_date', 'type': 'TIMESTAMP WITH TIME ZONE', 'constraints': ['NULLABLE']}, {'name': 'status', 'type': 'VARCHAR(20)', 'constraints': ['NOT NULL', "DEFAULT 'pending'", "CHECK (status IN ('pending', 'completed'))"]}, {'name': 'created_at', 'type': 'TIMESTAMP WITH TIME ZONE', 'constraints': ['NOT NULL', 'DEFAULT CURRENT_TIMESTAMP']}, {'name': 'updated_at', 'type': 'TIMESTAMP WITH TIME ZONE', 'constraints': ['NOT NULL', 'DEFAULT CURRENT_TIMESTAMP']}]}]}

## API Endpoints

- **POST /api/tasks**: Create a new task. (US1)

- **GET /api/tasks**: Retrieve all tasks. Supports filtering by status. (US4)

- **GET /api/tasks/{task_id}**: Retrieve a specific task by ID. (Supporting US4)

- **PATCH /api/tasks/{task_id}**: Update an existing task. Can update description, due_date, or status. (US2, US3)

- **DELETE /api/tasks/{task_id}**: Delete a task by ID.


## UI Components

- Task Input Form (for description and due date)

- Due Date Picker

- Task List (displays pending and completed tasks)

- Task Item Card/Row (for individual task display, including description, due date, status)

- Complete Task Toggle/Checkbox

- Edit Task Button

- Delete Task Button

- Task Filter/Sort Options (e.g., 'All', 'Pending', 'Completed')

- Notifications/Toasts (for success/error messages)
