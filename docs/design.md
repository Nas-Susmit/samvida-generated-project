# Design Document for MyProject

## Architecture Overview
{'description': 'A modular fullstack system designed for scalability, maintainability, and security, leveraging a RESTful API backend and a responsive Single Page Application (SPA) frontend. Role-Based Access Control (RBAC) is implemented throughout.', 'components': [{'name': 'Frontend (Client-Side)', 'technology': 'React.js / Vue.js / Angular (SPA Framework)', 'purpose': 'Provides a rich, interactive user interface. Communicates with the Backend API via AJAX/Fetch requests. Handles UI rendering, user input, and client-side routing.', 'deployment': 'Static asset hosting (e.g., AWS S3 + CloudFront, Netlify, Vercel)'}, {'name': 'Backend API (Server-Side)', 'technology': 'Node.js (Express/NestJS) / Python (Django/Flask) / Go (Gin) / Java (Spring Boot)', 'purpose': 'A RESTful API that acts as the central point of communication. Handles business logic, authentication, authorization, data persistence, and integration with external services. Structured into logical modules (User, CRM, Social Media, Finance, Admin).', 'deployment': 'Containerized (Docker) and Orchestrated (Kubernetes) on Cloud VMs (AWS EC2, GCP Compute Engine, Azure VMs), behind a Load Balancer/API Gateway.', 'modules': ['Authentication & User Management', 'CRM (Client Management)', 'Social Media (Content & Metrics)', 'Finance (Invoicing & Payments)', 'Admin & Monitoring']}, {'name': 'Database', 'technology': 'PostgreSQL (Relational Database)', 'purpose': 'Stores all structured application data including users, profiles, clients, invoices, social media accounts, posts, and engagement metrics. Chosen for its reliability, ACID compliance, and robust support for complex queries and relationships.', 'deployment': 'Managed Database Service (e.g., AWS RDS PostgreSQL, GCP Cloud SQL for PostgreSQL, Azure Database for PostgreSQL)'}, {'name': 'Cache', 'technology': 'Redis', 'purpose': 'Used for session management, frequently accessed data (e.g., user profiles), rate limiting, and improving API response times.', 'deployment': 'Managed Cache Service (e.g., AWS ElastiCache for Redis, GCP Memorystore for Redis, Azure Cache for Redis)'}, {'name': 'Object Storage', 'technology': 'AWS S3 / Google Cloud Storage / Azure Blob Storage', 'purpose': 'Stores static and dynamic media files, such as user avatars, social media post images/videos, and invoice attachments. Provides high availability and scalability.', 'deployment': 'Cloud Object Storage Service'}, {'name': 'Message Queue / Background Jobs', 'technology': 'RabbitMQ / Apache Kafka / AWS SQS / Celery (Python)', 'purpose': 'Handles asynchronous tasks such as scheduling social media posts, processing payment notifications, sending emails, and collecting engagement metrics from external APIs. Decouples long-running processes from API requests.', 'deployment': 'Managed Queue Service (e.g., AWS SQS, Azure Service Bus) or self-hosted message broker'}, {'name': 'Monitoring & Logging', 'technology': 'Prometheus & Grafana / ELK Stack (Elasticsearch, Logstash, Kibana) / CloudWatch / Stackdriver', 'purpose': 'Collects system metrics, application logs, and traces to ensure system health, performance, and aid in debugging and security auditing.', 'deployment': 'Integrated cloud services or dedicated monitoring platform'}]}

## Database Schema
{'type': 'Relational Database (PostgreSQL)', 'schema_overview': [{'table_name': 'users', 'description': 'Stores user authentication details and role.', 'fields': [{'name': 'id', 'type': 'UUID (PK)', 'description': 'Unique user identifier.'}, {'name': 'email', 'type': 'VARCHAR(255) (UNIQUE)', 'description': "User's email, used for login."}, {'name': 'password_hash', 'type': 'VARCHAR(255)', 'description': 'Hashed password.'}, {'name': 'role', 'type': "ENUM ('admin', 'freelancer', 'social_media_creator', 'user')", 'description': "User's role for RBAC."}, {'name': 'is_active', 'type': 'BOOLEAN', 'description': 'Account active status.'}, {'name': 'created_at', 'type': 'TIMESTAMP'}, {'name': 'updated_at', 'type': 'TIMESTAMP'}]}, {'table_name': 'profiles', 'description': 'Stores detailed public and private profile information for each user.', 'fields': [{'name': 'id', 'type': 'UUID (PK)', 'description': 'Unique profile identifier.'}, {'name': 'user_id', 'type': 'UUID (FK to users.id, UNIQUE)', 'description': 'Links to the associated user.'}, {'name': 'first_name', 'type': 'VARCHAR(100)'}, {'name': 'last_name', 'type': 'VARCHAR(100)'}, {'name': 'display_name', 'type': 'VARCHAR(200)', 'description': 'Publicly visible name.'}, {'name': 'bio', 'type': 'TEXT', 'description': 'Short biography.'}, {'name': 'avatar_url', 'type': 'VARCHAR(500)', 'description': "URL to user's profile picture in object storage."}, {'name': 'contact_info', 'type': 'JSONB', 'description': 'Flexible field for phone, social links, etc.'}, {'name': 'company_name', 'type': 'VARCHAR(255)', 'description': 'Optional, for freelancers.'}, {'name': 'created_at', 'type': 'TIMESTAMP'}, {'name': 'updated_at', 'type': 'TIMESTAMP'}]}, {'table_name': 'clients', 'description': 'Stores client contact information for freelancers.', 'fields': [{'name': 'id', 'type': 'UUID (PK)'}, {'name': 'freelancer_id', 'type': 'UUID (FK to users.id)', 'description': 'Links to the freelancer who owns this client record.'}, {'name': 'name', 'type': 'VARCHAR(255)'}, {'name': 'email', 'type': 'VARCHAR(255)'}, {'name': 'phone', 'type': 'VARCHAR(50)'}, {'name': 'company_name', 'type': 'VARCHAR(255)'}, {'name': 'address', 'type': 'JSONB', 'description': 'Flexible field for address details.'}, {'name': 'notes', 'type': 'TEXT'}, {'name': 'created_at', 'type': 'TIMESTAMP'}, {'name': 'updated_at', 'type': 'TIMESTAMP'}]}, {'table_name': 'invoices', 'description': 'Stores invoice details generated by freelancers.', 'fields': [{'name': 'id', 'type': 'UUID (PK)'}, {'name': 'freelancer_id', 'type': 'UUID (FK to users.id)'}, {'name': 'client_id', 'type': 'UUID (FK to clients.id)'}, {'name': 'invoice_number', 'type': 'VARCHAR(50) (UNIQUE)'}, {'name': 'issue_date', 'type': 'DATE'}, {'name': 'due_date', 'type': 'DATE'}, {'name': 'total_amount', 'type': 'DECIMAL(10,2)'}, {'name': 'currency', 'type': 'VARCHAR(3)'}, {'name': 'status', 'type': "ENUM ('draft', 'sent', 'paid', 'overdue', 'cancelled')"}, {'name': 'payment_details', 'type': 'JSONB', 'description': 'Bank info, payment link etc.'}, {'name': 'notes', 'type': 'TEXT'}, {'name': 'created_at', 'type': 'TIMESTAMP'}, {'name': 'updated_at', 'type': 'TIMESTAMP'}]}, {'table_name': 'social_media_accounts', 'description': 'Stores connected social media accounts for creators.', 'fields': [{'name': 'id', 'type': 'UUID (PK)'}, {'name': 'creator_id', 'type': 'UUID (FK to users.id)', 'description': 'Links to the social media creator.'}, {'name': 'platform', 'type': "ENUM ('facebook', 'instagram', 'twitter', 'linkedin')", 'description': "e.g., 'facebook', 'instagram'."}, {'name': 'account_id_platform', 'type': 'VARCHAR(255)', 'description': 'ID from the social media platform.'}, {'name': 'access_token', 'type': 'TEXT (ENCRYPTED)', 'description': 'OAuth access token.'}, {'name': 'refresh_token', 'type': 'TEXT (ENCRYPTED)', 'description': 'OAuth refresh token (if applicable).'}, {'name': 'expires_at', 'type': 'TIMESTAMP'}, {'name': 'profile_url', 'type': 'VARCHAR(500)'}, {'name': 'account_name', 'type': 'VARCHAR(255)'}, {'name': 'created_at', 'type': 'TIMESTAMP'}, {'name': 'updated_at', 'type': 'TIMESTAMP'}]}, {'table_name': 'posts', 'description': 'Stores scheduled and published social media content.', 'fields': [{'name': 'id', 'type': 'UUID (PK)'}, {'name': 'account_id', 'type': 'UUID (FK to social_media_accounts.id)'}, {'name': 'content_text', 'type': 'TEXT'}, {'name': 'media_urls', 'type': 'TEXT[]', 'description': 'Array of URLs to images/videos in object storage.'}, {'name': 'scheduled_at', 'type': 'TIMESTAMP'}, {'name': 'published_at', 'type': 'TIMESTAMP'}, {'name': 'status', 'type': "ENUM ('draft', 'scheduled', 'publishing', 'published', 'failed')"}, {'name': 'platform_post_id', 'type': 'VARCHAR(255)', 'description': 'ID returned by social platform after publishing.'}, {'name': 'created_at', 'type': 'TIMESTAMP'}, {'name': 'updated_at', 'type': 'TIMESTAMP'}]}, {'table_name': 'engagement_metrics', 'description': 'Stores engagement metrics collected for social media posts.', 'fields': [{'name': 'id', 'type': 'UUID (PK)'}, {'name': 'post_id', 'type': 'UUID (FK to posts.id)'}, {'name': 'metric_type', 'type': "ENUM ('likes', 'comments', 'shares', 'views', 'reach', 'impressions')", 'description': 'Type of metric.'}, {'name': 'value', 'type': 'INTEGER'}, {'name': 'recorded_at', 'type': 'TIMESTAMP', 'description': 'Timestamp when this metric was collected.'}, {'name': 'created_at', 'type': 'TIMESTAMP'}]}]}

## API Endpoints

- **POST **: Register a new user.

- **POST **: Authenticate user and return JWT.

- **POST **: Refresh access token.

- **GET **: Retrieve current user's profile.

- **PUT **: Update current user's profile.

- **GET **: Get all clients for the freelancer.

- **POST **: Create a new client contact.

- **GET **: Get a specific client contact by ID.

- **PUT **: Update an existing client contact.

- **DELETE **: Delete a client contact.

- **GET **: Get all invoices for the freelancer.

- **POST **: Create a new invoice.

- **GET **: Get a specific invoice by ID.

- **PUT **: Update an existing invoice.

- **DELETE **: Delete an invoice.

- **POST **: Mark an invoice as paid.

- **POST **: Send an invoice (e.g., email notification).

- **GET **: Get connected social media accounts for the creator.

- **POST **: Connect a new social media account (initiates OAuth flow).

- **DELETE **: Disconnect a social media account.

- **GET **: Get all posts (scheduled/published) for the creator.

- **POST **: Create a new post draft.

- **GET **: Get a specific post by ID.

- **PUT **: Update an existing post.

- **DELETE **: Delete a post.

- **POST **: Schedule a post for future publication.

- **POST **: Publish a post immediately.

- **GET **: Get engagement metrics for a specific post.

- **GET **: Get aggregated engagement metrics across all accounts.

- **GET **: Get a list of all user accounts.

- **GET **: Get details of any specific user.

- **PUT **: Activate or deactivate a user account.

- **GET **: Get system health and performance indicators.


## UI Components

- global_components

- user_profile_management

- freelancer_dashboard_components

- social_media_creator_dashboard_components

- admin_dashboard_components
