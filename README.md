# 🗓️ Appointment Booking System — Backend

This project is a **Flask-based RESTful API** for an Appointment Booking System.  
It allows users to **register**, **log in**, and **book, update, or cancel appointments** for various services.  
The backend includes secure **JWT authentication with token blacklisting**, **role-based access control**,  
and prevents **double-booking** of the same service and time slot.  
It uses **SQLite** as the database and is designed to integrate seamlessly with a React frontend.

---

## 🚀 Features

- 🔒 User registration and login with hashed passwords (`Flask-Bcrypt`)
- 🪪 JWT authentication and logout with token blacklisting (`Flask-JWT-Extended`)
- 👤 Role-based access control (admin / user)
- 🧾 CRUD endpoints for users, services, and appointments
- ⚠️ Prevents double-booking for the same service and datetime
- 🗄️ SQLite database for simplicity and portability

---

## How to Start the Backend

Follow these steps to set up and run the backend locally:

### Clone the repository
```bash
git clone https://github.com/your-username/appointment-booking-system.git
cd appointment-booking-system/backend
```

### Create and activate a virtual environment
```bash
python -m venv venv
# Activate it:
source venv/bin/activate      # on macOS/Linux
venv\Scripts\activate         # on Windows
```

### Install dependencies
Make sure you have Flask and required packages installed:
```bash
pip install -r requirements.txt
```
### Run the Flask backend
```bash
python app.py
```
You should see output similar to:
 * Running on http://127.0.0.1:5000



# Frontend

## 1. Prerequisites

Before starting, ensure you have [Node.js](https://nodejs.org/) installed on your system. This includes **npm** (Node Package Manager).

## 2. Install Dependencies

You must install all necessary packages defined in `package.json` into the `node_modules` folder.

1.  **Open your terminal** and navigate to the root directory of the project (where `package.json` is located).
    ```bash
    cd path/to/your/project
    ```
2.  **Run the install command** using your preferred package manager:

| Package Manager | Command | Notes |
| :--- | :--- | :--- |
| **npm** (Recommended) | `npm install` | Most common and reliable. |


## 3. Start the Development Server

Once dependencies are installed, you can start the local development server.

1.  **Run the development script:**

    ```bash
    npm run dev
    ```

2.  The terminal will output the local address (e.g., `http://localhost:5173/`). **Open this link** in your browser to view the running application.

---
**💡 Tip:** The `dev` script in a Vite project usually uses the `vite` command to hot-reload changes as you code.