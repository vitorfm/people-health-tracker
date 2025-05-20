# People Health Tracker

## Overview
People Health Tracker is a modular health monitoring system designed to manage patients, blood tests, exam types, and doctors. The system is built to be extensible, supporting multiple health modules and providing a modern web interface for healthcare professionals.

## Main Features
- Patient management (CRUD)
- Blood test management (CRUD, multiple results per test)
- Exam type management (reference values by gender/age group)
- Doctor management (CRUD)
- Modular and scalable backend (FastAPI + MongoDB)
- Modern frontend (Next.js + React + Tailwind CSS)

## Project Structure
```
people-health-tracker/
├── patient-blood-tracker/
│   ├── backend/
│   │   ├── app/
│   │   │   ├── api/endpoints/   # FastAPI endpoints (patients, blood_tests, exam_types, doctors)
│   │   │   ├── models/          # Pydantic models (Patient, Doctor, ExamType, BloodTest, etc)
│   │   │   ├── services/        # Business logic/services
│   │   │   ├── db/              # Database connection
│   │   │   └── core/            # Config and settings
│   │   ├── tests/               # Backend tests
│   │   └── ...
│   └── frontend/
│       └── src/app/             # Next.js app directory (pages, components)
│           ├── pacientes/       # Patient pages
│           ├── exames/          # Exam pages
│           ├── exam-types/      # Exam type pages
│           ├── doctors/         # Doctor pages
│           └── ...
├── .env.example
├── docker-compose.yml
├── README.md
└── ...
```

## Technologies
- **Backend:** FastAPI, Python, MongoDB, Motor (async MongoDB driver)
- **Frontend:** Next.js (React), TypeScript, Tailwind CSS
- **DevOps:** Docker, Docker Compose

## Current Status
- [x] Modular backend and frontend structure
- [x] Patient CRUD (backend & frontend)
- [x] Blood test CRUD (backend & frontend)
- [x] Exam type CRUD (backend & frontend)
- [x] Doctor CRUD (backend & frontend)
- [x] Multiple results per blood test (ExamResult)
- [x] CORS and API integration
- [x] English UI and codebase
- [x] Links between all main modules
- [ ] Edit/delete for all entities (WIP)
- [ ] Authentication and user roles (planned)
- [ ] Dashboard and statistics (planned)
- [ ] Automated tests (planned)

## How to Run
1. **Start MongoDB** (Docker recommended):
   ```sh
   docker run -d --name mongo -p 27017:27017 mongo
   ```
2. **Backend:**
   ```sh
   cd patient-blood-tracker/backend
   python -m venv venv && source venv/bin/activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```
3. **Frontend:**
   ```sh
   cd patient-blood-tracker/frontend
   npm install
   npm run dev
   ```
4. **Access:**
   - Frontend: http://localhost:3000
   - Backend (Swagger): http://localhost:8000/docs

## Next Steps
- [ ] Implement edit/delete for all entities in the frontend
- [ ] Add authentication (JWT) and user roles
- [ ] Add dashboard and statistics pages
- [ ] Write automated tests (backend and frontend)
- [ ] Improve error handling and user feedback
- [ ] Polish UI/UX and add responsive design

---

For questions or contributions, open an issue or pull request!

