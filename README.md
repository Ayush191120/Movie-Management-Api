# Movie-Management-Api (FastAPI + Prisma + PostgreSQL)

This project implements a backend **Movie API** using **FastAPI**, **Prisma ORM**, and **PostgreSQL**.  
It provides full **CRUD** functionality (Create, Read, Update, Delete) for movies and includes built-in **Swagger UI** for API documentation.

# Tech Stack
1)FastApi :- Web framework with async support and automatic OpenAPI docs.
2)Prisma ORM :- Type-safe database client for Python.
3)PostgreSQL :- Relational database for persistent storage.
4)Uvicorn :- ASGI server to run FastAPI.
5)Pydantic :- Used internally by Prisma client for validation.

# How to Run the Project
1) Create & activate a virtual environment
2) Install dependencies for Fastapi and database postgresql.
3) Setup PostgreSQL and postgresql installed and running on port 5432.
4) Configure environment and Create a .env file in the root folder.
5) Setup Prisma schema 
6) Run Prisma migration and command is prisma migrate dev --name init
7) Run the FastAPI server command is fastapi dev main.py

# How to run tests
1) Install test dependencies
2) Run all tests
3) Run tests with detailed output
4) Run a single test file
5) Run with live logs

# Link to Swagger documentation
Swagger UI :- [http://127.0.0.1:8000/docs]
