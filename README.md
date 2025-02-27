# Referral System API

## Overview

This project is a backend for a platform similar to Linktree or Bento.me, built using Flask. It includes user registration, authentication, a referral system, and other essential functionalities. Users can register, log in, refer others, and earn rewards. The API also features a test suite to verify its functionality.

## Features

- **User Registration & Authentication** (JWT-based authentication)
- **Referral System** (Users can refer others and earn rewards)
- **Email-based Password Reset** (Using a local SMTP server)
- **Test Cases** (Using pytest)

## Technologies Used

- **Flask** (Backend framework)
- **Flask-JWT-Extended** (Authentication & token management)
- **SQLAlchemy** (Database ORM)
- **Pytest** (Testing framework)
- **Local SMTP Server** (For email services)

---

## Setup Instructions

### **1. Clone the Repository**

```sh
$ git clone <repository-url>
$ cd <project-directory>
```

### **2. Create and Activate a Virtual Environment**

```sh
$ python -m venv env
$ source env/bin/activate   # On Mac/Linux
$ env\Scripts\activate     # On Windows
```

### **3. Install Dependencies**

```sh
$ pip install -r requirements.txt
```

### **4. Set Up Environment Variables**

Create a `.env` file and add the following:

```env
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///database.db
MAIL_SERVER=localhost
MAIL_PORT=1025
MAIL_USE_TLS=False
MAIL_USE_SSL=False
MAIL_USERNAME=None
MAIL_PASSWORD=None
```

### **5. Run Database Migrations**

```sh
$ flask db init
$ flask db migrate -m "Initial migration"
$ flask db upgrade
```

### **6. Start the Local SMTP Server** (For email functionality)

```sh
$ python -m aiosmtpd -n -c aiosmtpd.handlers.Debugging stdout --listen localhost:1025
```

### **7. Run the Application**

```sh
$ flask run
```

The API should now be running at `http://127.0.0.1:5000/`.

---

## API Endpoints

### **User Authentication**

- **Register**: `POST /api/register`
- **Login**: `POST /api/login`
- **Reset Password (Request)**: `POST /api/reset-password`


### **Referral System**

- **Refer a User**: Handled during registration
- **View User Referrals**: `GET /api/referrals`
- **Get Referral Statistics**: `GET /api/referral-stats`

---

## Running Tests

To run all test cases, execute:

```sh
$ pytest
```

If you want to see detailed test output, run:

```sh
$ pytest -v
```

---

## Issues & Debugging

- If you encounter an `Email is already registered` error, ensure that you are using a unique email for each registration.
- Use the `print(response.get_json())` statement in test cases to debug unexpected failures.
- Ensure the local SMTP server is running before testing password reset functionality.

---

## Future Improvements

- Implement a production-ready email service (e.g., SendGrid, Mailgun)
- Add front-end UI for managing referrals and rewards
- Introduce caching for improved API performance
- Implement user roles and permissions for more complex access control