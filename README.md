# AI Skin Intelligence

An AI-powered skincare platform with skin assessments, personalized skincare routines, ingredient intelligence, product recommendations, progress tracking, and analytics.

## Tech Stack
- Frontend: React and Vite
- Backend: Python and FastAPI
- Database: PostgreSQL
- Deployment: Docker Compose

## Prerequisites
Install Git and Docker Desktop. Start Docker Desktop before running the project.

## Run Locally

1. Clone the repository:

   git clone https://github.com/akshaymantage4-ui/skin-intelligence.git

2. Open the project folder:

   cd skin-intelligence/skin

3. Create local environment files:

   Copy-Item .env.example .env
   Copy-Item backend/.env.example backend/.env

4. Edit both environment files. Set the same password in POSTGRES_PASSWORD and DB_PASSWORD. Set DB_HOST=db, DB_PORT=5432, and replace the example JWT secret.

5. Build and start the application:

   docker compose up --build -d

6. Open:
   - Web application: http://localhost/login
   - API documentation: http://localhost:8000/docs

## Useful Commands

Check containers:
   docker compose ps

View backend logs:
   docker compose logs backend

Stop containers without deleting database data:
   docker compose down

## Security
Never commit real .env files, passwords, or secrets. Use the provided .env.example files as templates.
