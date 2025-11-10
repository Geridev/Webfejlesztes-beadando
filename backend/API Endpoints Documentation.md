## 🐍 API Endpoints Documentation

This document outlines all available endpoints for the service booking backend.

---

### 🔑 Authentication Endpoints (`/auth`)

These routes handle user registration, login, and token revocation (logout).

| Method | Endpoint | Description | Authentication | Expected Payload (JSON) |
| :--- | :--- | :--- | :--- | :--- |
| **POST** | `/auth/register` | Creates a new **User** account. | None | `{"username": "...", "email": "...", "password": "..."}` |
| **POST** | `/auth/login` | Authenticates a user and issues a **JWT access token**. | None | `{"username": "...", "password": "..."}` |
| **POST** | `/auth/logout` | Revokes the current JWT (by adding its JTI to the `RevokedToken` model). | JWT Required | None |

---

### 👤 User Endpoints (`/users`)

These routes manage user information, visible to the user themselves or an Administrator.

| Method | Endpoint | Description | Authentication | Expected Payload (JSON) |
| :--- | :--- | :--- | :--- | :--- |
| **GET** | `/users/` | Retrieves a list of **all users**. | JWT Required (**Admin Only**) | None |
| **GET** | `/users/<int:id>` | Retrieves details for a specific user. | JWT Required (**Admin or Self**) | None |
| **PUT** | `/users/<int:id>` | Updates a user's details (username, email, password, or role). | JWT Required (**Admin or Self**) | `{"username": "...", "email": "...", "password": "...", "role": "..."}` *(Fields are optional)* |
| **DELETE** | `/users/<int:id>` | **Deletes** a specific user account. | JWT Required (**Admin Only**) | None |

---

### 📅 Appointment Endpoints (`/appointments`)

These routes handle the scheduling and management of appointments.

| Method | Endpoint | Description | Authentication | Expected Payload (JSON) |
| :--- | :--- | :--- | :--- | :--- |
| **GET** | `/appointments/` | Retrieves all appointments (Admin) or only the **current user's** appointments. | JWT Required | None |
| **POST** | `/appointments/` | Creates a new appointment for the authenticated user. | JWT Required | `{"service_id": 1, "datetime": "YYYY-MM-DD HH:MM"}` |
| **PUT** | `/appointments/<int:id>` | Updates the datetime or status of an appointment. | JWT Required (**Admin or Owner**) | `{"datetime": "...", "status": "..."}` *(Fields are optional)* |
| **DELETE** | `/appointments/<int:id>` | Deletes a specific appointment. | JWT Required (**Admin or Owner**) | None |

---

### 🛠️ Service Endpoints (`/services`)

These routes manage the available services. All users can view services, but only Admins can manage them.

| Method | Endpoint | Description | Authentication | Expected Payload (JSON) |
| :--- | :--- | :--- | :--- | :--- |
| **GET** | `/services/` | Retrieves a list of **all available services**. | None | None |
| **POST** | `/services/` | Adds a new service to the system. | JWT Required (**Admin Only**) | `{"name": "...", "description": "...", "duration": 60, "price": 50.00}` |
| **PUT** | `/services/<int:id>` | Updates an existing service's details. | JWT Required (**Admin Only**) | `{"name": "...", "description": "...", "duration": 60, "price": 50.00}` *(Fields are optional)* |
| **DELETE** | `/services/<int:id>` | Deletes a specific service. | JWT Required (**Admin Only**) | None |
