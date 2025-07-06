# 📝 Task Management API (FastAPI + SQL Server)

A simple Task Management REST API built using **FastAPI** and **SQL Server**, using **raw SQL queries with pyodbc**, and tested via **Swagger UI**.

---

## 📌 Project Overview

This project implements basic task management functionality with user registration and login. It supports full CRUD operations on tasks, all linked to users.

---

## 🚀 Features

- ✅ Register new users
- ✅ Login with hashed passwords
- ✅ Create tasks assigned to users
- ✅ View all tasks for a user
- ✅ Update tasks (if owned by user)
- ✅ Delete tasks (if owned by user)
- ✅ Tested using Swagger UI
- ✅ Built with raw SQL (no ORM)

---

## 📄 Files Explained

- **`main.py`**  
  Entry point of the FastAPI application.  
  Contains all route definitions: `/register`, `/login`, and CRUD routes for `/tasks/`.

- **`src/util.py`**  
  Utility functions:  
  - `get_db_connection()` for connecting to SQL Server  
  - `hash_password()` for securely hashing user passwords

- **`src/db_create.py`**  
  Creates the necessary tables (`users`, `tasks`) in the SQL Server database at app startup.

- **`src/models.py`**  
  Defines all Pydantic models used for validating request and response data.

- **`config/config.config`**  
  Configuration file for storing SQL Server connection details.  
  *(Credentials are kept private and not included here.)*

---

## ▶️ Running the App

1. Install the required packages:
**pip install fastapi uvicorn pyodbc**

2. Run the API:
**fastapi dev main.py**

3. Visit Swagger UI:
**http://localhost:8000/docs**


---

## 🛡️ Notes

- Passwords are stored in hashed form (SHA256).
- There is no real authentication yet (e.g., JWT). Requests include `user_id` manually.
- This is intended as a learning project focused on clean, beginner-friendly structure.

---

## Built With

- FastAPI
- pyodbc
- SQL Server
- Pydantic

---
