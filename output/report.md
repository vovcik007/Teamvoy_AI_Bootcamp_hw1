# Repository Analysis: vovcik007/Teamvoy_AI_Bootcamp_hw1

## Summary
A full-stack Health Tracker web application consisting of a FastAPI backend using SQLite and SQLAlchemy, paired with a React, TypeScript, and Vite frontend. The application allows users to record and review daily wellness metrics such as mood, sleep hours, water intake, and meals.

## Technologies Used
- FastAPI
- SQLite
- SQLAlchemy
- Pydantic
- React
- TypeScript
- Vite
- Axios
- ESLint

## Strengths
- Clean project structure separating frontend and backend logic.
- Strict type-safety on the frontend with TypeScript interfaces matching backend models.
- Efficient database interaction using SQLAlchemy ORM with a simple SQLite configuration.
- Dynamic health stats endpoints analyzing sleep and mood correlations.
- Pagination support is built into the logs endpoint to handle growth.

## Issues & Concerns
- Hardcoded API URLs and CORS origins hinder flexibility and production deployment.
- Lack of automated tests (unit, integration, or E2E) for both frontend and backend.
- Missing database migration system like Alembic to manage database schema updates.
- Error handling on the frontend only logs to the console and does not notify the user.
- Lack of input validation in backend schemas (e.g., negative values are allowed for sleep/water).

## Recommendations
- Externalize configurations (API base URL, database URL, CORS settings) via environment variables.
- Integrate Alembic to support automated and version-controlled database migrations.
- Add unit tests using pytest for the backend and Vitest/React Testing Library for the frontend.
- Implement user-facing error notifications/banners in React when API requests fail.
- Apply Pydantic validators and Field constraints (e.g., min/max boundaries) on request schemas.
