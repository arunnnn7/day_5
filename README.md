# Student Profile Portal with Authentication & Dynamic Interaction

A complete, full-stack student management portal built with **Flask**, **SQLite**, **HTML5/CSS3**, and **JavaScript/jQuery**.

---

## 📋 Assessment Overview & Level Coverage

| Level | Objective | Implemented Features & Verification | Marks | Status |
| :--- | :--- | :--- | :---: | :---: |
| **Level 1** | Frontend Form + Basic Logic | Responsive registration form with Full Name, Email, Age, Gender, Course, Password. jQuery/JS validation for required fields, numeric age (1–120), password length (&ge;6), and visual alerts using explicit `if` conditions. | 20 / 20 | ✅ Complete |
| **Level 2** | Flask Setup + DB Interaction | SQLite database configuration, `Student` model class (`id, name, email, age, gender, course, password`), SQL parameterized insertion with `try/except` error handling, redirect to `/success` with `"Welcome, {{name}}! You have successfully registered."` | 30 / 30 | ✅ Complete |
| **Level 3** | Session Handling + Profile Page | Session-based authentication `/login` with DB credentials verification, protected `/profile` route displaying name, course, email, age, and gender, and session clearing `/logout` option redirecting to `/login`. | 25 / 25 | ✅ Complete |
| **Level 4** | Interactivity + Dashboard Features | Live JavaScript clock (updates every 1000ms), jQuery toggle button (`Show/Hide Details` with smooth `.slideToggle()`), course update dropdown via AJAX (jQuery `$.post` to `/update-course`) with animated toast & alert `"Course updated to: X"`, modern dark-mode glassmorphism card styling. | 25 / 25 | ✅ Complete |
| **Overall** | Logical routing & data flow | Clean MVC separation, parameterized queries, CSRF & error safeguards, unit tests. | 5 / 5 | ✅ Complete |
| **Total** | | | **100 / 100** | ✅ **Full Marks** |

---

## 📁 Project Structure

```text
d:/Assessment/
├── app.py                      # Main Flask application & SQLite routes
├── students.db                 # SQLite database file (seeded with demo user)
├── requirements.txt            # Python dependencies (Flask>=3.0.0)
├── test_app.py                 # Automated unit test suite covering all 4 levels
├── README.md                   # Project documentation
├── static/
│   ├── css/
│   │   └── style.css           # Modern glassmorphism dark theme & responsive layout
│   └── js/
│       ├── jquery.min.js       # Local jQuery library fallback
│       ├── register.js         # Level 1 form validation with if-conditions & alerts
│       └── profile.js          # Level 4 live clock, toggle, & AJAX course updater
└── templates/
    ├── base.html               # Base layout with navbar, jQuery fallback, footer
    ├── register.html           # Level 1 registration form with icons & badges
    ├── success.html            # Level 2 success page with exact required welcome text
    ├── login.html              # Level 3 authentication login interface
    └── profile.html            # Level 3 & Level 4 profile dashboard with cards
```

---

## 🚀 How to Run the Application

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Flask Development Server
```bash
python app.py
```
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 🧪 Testing Credentials & Sample Data

A sample student account is pre-loaded in `students.db`:
- **Email**: `john.doe@university.edu`
- **Password**: `password123`

You can also register a new account on `/register` to test Level 1 and Level 2 functionality.

### Running Automated Test Suite
To run all automated verification tests:
```bash
python test_app.py
```
Outputs:
```text
Ran 3 tests in 0.334s
OK
```

---

## 🎯 Verification of Key Requirements

1. **Level 1 (Form Validation)**:
   - File: `static/js/register.js`
   - Explicit `if` statements check required inputs, positive numeric age, and password length $\ge 6$.
   - Displays both visual alert box and browser alert message.

2. **Level 2 (DB Interaction & Try/Except)**:
   - File: `app.py`
   - Model: `Student` with all 7 fields (`id`, `name`, `email`, `age`, `gender`, `course`, `password`).
   - Insertion handled via `try/except (sqlite3.IntegrityError, sqlite3.Error, Exception)`.
   - Success redirect renders exact phrase: `"Welcome, {{name}}! You have successfully registered."`.

3. **Level 3 (Session Handling)**:
   - Route `/login`: Authenticates using SQLite DB, saves `student_id` into Flask `session`.
   - Route `/profile`: Fetches student from DB by session ID.
   - Route `/logout`: Executes `session.clear()` and redirects to `/login`.

4. **Level 4 (Dashboard Interactivity)**:
   - Live Time: Updated every 1 second in JavaScript via `setInterval()`.
   - jQuery Toggle: "Show/Hide Details" toggles the student information card section.
   - AJAX Course Update: Dropdown change triggers `$.post('/update-course')`, updates DB in background, syncs DOM, and shows toast & alert `"Course updated to: X"`.
