# 🎓 LearnLoop – Quiz Platform (Browser App)

---

LearnLoop is a browser-based quiz platform that allows teachers to create and manage quizzes, while students can solve them and track their progress.

It aims to:

- Cover the full process from requirements analysis to implementation
- Apply advanced Python concepts in a web-based application
- Demonstrate data validation, layered architecture, and ORM usage
- Produce clean, maintainable, and well-tested code
- Support teamwork and professional documentation

---

## 📑 Table of Contents

- [Application Requirements](#application-requirements)
- [User Stories](#user-stories)
- [Use Cases](#use-cases)
- [App Screenshots](#app-screenshots)
- [Architecture](#architecture)
- [Database and ORM](#database-and-orm)
- [Project Requirements](#project-requirements)
- [Implementation](#implementation)
- [Repository Structure](#repository-structure)
- [How to Run](#how-to-run)
- [Testing](#testing)
- [Team & Contributions](#team-contributions)
- [License](#license)


---

<a id="application-requirements"></a>
## 📝 Application Requirements

### Problem

In educational settings, creating and distributing quizzes is often time-consuming and results are hard to track. Teachers need a simple tool to create quizzes with different question types, and students need a clean interface to solve them and see their results.

### Scenario

The application allows users to:

- Register and log in as either a teacher or a student
- Teachers can create, edit, publish, unpublish, and delete quizzes
- Teachers can view detailed results for each student per question
- Students can browse available quizzes and attempt them
- Students can review their results with a detailed per-question breakdown
- Students can track their overall statistics and history

---

<a id="user-stories"></a>
## 📖 User Stories

### 1. Register and Login

As a user, I want to register with a username, email, password, and role (teacher or student) so I can access the platform.

- Inputs: username, email, password, role
- Outputs: new user account, redirect to dashboard

---

### 2. Create a Quiz (Teacher)

As a teacher, I want to create a quiz with a title, description, and questions so my students can attempt it.

- Inputs: title (str), description (str), questions with type and answer options
- Outputs: saved quiz (draft), visible in dashboard

---

### 3. Publish / Unpublish a Quiz (Teacher)

As a teacher, I want to publish a quiz so students can see it, or set it back to draft if needed.

- Inputs: quiz ID (int), action (publish | unpublish)
- Outputs: updated quiz status

---

### 4. View Student Results (Teacher)

As a teacher, I want to see detailed results per student, including which questions were answered correctly or incorrectly.

- Inputs: quiz ID (int)
- Outputs: list of attempts with per-question breakdown

---

### 5. Solve a Quiz (Student)

As a student, I want to answer all questions in a quiz and submit my answers to get a score.

- Inputs: selected answer options per question
- Outputs: score, percentage, correct/wrong count

---

### 6. View My Statistics (Student)

As a student, I want to see all my past quiz attempts with scores and percentages so I can track my progress.

- Inputs: none
- Outputs: list of attempts (list[QuizAttempt]), average, best result

---

<a id="use-cases"></a>
## 🧩 Use Cases

### Main Use Cases

- Register / Login (Teacher & Student)
- Create Quiz (Teacher)
- Edit / Delete Quiz (Teacher)
- Publish / Unpublish Quiz (Teacher)
- View Student Results (Teacher)
- Browse Available Quizzes (Student)
- Solve Quiz (Student)
- View Results & Statistics (Student)

### Actors

- Teacher
- Student

### Use Case Diagram

The following Use Case Diagram shows the main actors and their primary interactions with the system.

```mermaid
flowchart TD
    T[Teacher]
    S[Student]

    T --> CreateQuiz[Create Quiz]
    T --> EditQuiz[Edit Quiz]
    T --> PublishQuiz[Publish and Unpublish Quiz]
    T --> ViewResults[View Student Results]
    T --> Register[Register and Login]

    S --> Register[Register and Login]
    S --> Browse[Browse Quizzes]
    S --> Attempt[Attempt Quiz]
    S --> ViewStats[View Results and Statistics]
```

---

<a id="app-screenshots"></a>
## 🧱 App Screenshots

The UI of LearnLoop focuses on a clean, browser-friendly learning flow and the main pages used by teachers and students.

### Login / Registration Page

The screenshot below represents the login / registration page and introduces the application entry flow.

<img width="2988" height="1740" alt="image" src="https://github.com/user-attachments/assets/c04d5338-f335-4238-8ef3-483227a75108" />

### Teacher Dashboard

This page shows quiz management actions, published and draft quizzes, and the main controls teachers need at a glance.

<img width="2984" height="1742" alt="image" src="https://github.com/user-attachments/assets/76b8e11e-2439-419a-9086-61309e18dcb0" />

### Quiz Creation and Editing

These forms allow teachers to build new quizzes or update existing ones with questions, answer options, and status changes.

<img width="2958" height="1742" alt="image" src="https://github.com/user-attachments/assets/6b8a2f31-287e-43dc-ba5f-c39816d7503e" />

### Student Dashboard

This page presents available quizzes for students and gives them a simple starting point for browsing and attempting quizzes.

<img width="2986" height="1744" alt="image" src="https://github.com/user-attachments/assets/6cb03996-5f1e-469b-a815-093f2e6f1868" />

### Quiz Solving View

This screen guides students through one question at a time so the answering flow stays clear and focused.

<img width="2992" height="1746" alt="image" src="https://github.com/user-attachments/assets/ec6359ee-8dfd-454a-98e6-3e466caec366" />

### Results and Statistics

These pages summarize quiz attempts, scores, and progress so students can review their performance after submitting a quiz.

<img width="2990" height="1706" alt="image" src="https://github.com/user-attachments/assets/c6358191-46a7-4e70-819a-eef35c76b857" />

### Profile Page

This page allows users to change their password.

<img width="2992" height="1748" alt="image" src="https://github.com/user-attachments/assets/b25bb7f3-d405-4fd5-a1ef-396c0d413e4c" />

### Main Screens

- Login / Registration page
- Teacher dashboard with quiz management actions
- Quiz creation and editing forms
- Student dashboard with available quizzes
- Quiz solving view with one question per step
- Results and statistics pages
- Profile page for password changes

### Design Goal

The design emphasizes simple navigation, clear status information, and a colorful layout that works well in a browser-based classroom setting.

---

<a id="architecture"></a>
## 🏛️ Architecture

### Layers

- UI: NiceGUI browser-based interface
- Application logic: Services and page controllers
- Persistence: SQLite + SQLModel ORM + Data Access Layer / DAO

### Design Decisions

- Layered MVC structure
- Clear separation of concerns between UI, services, and data access
- Business logic such as authentication, scoring, quiz management and statistics is handled in services
- UI pages mainly handle input, navigation and display
- All scores are stored as whole integers — no partial credit

### Design Patterns Used

- Layered Architecture / MVC: The application separates UI pages, service classes, and database models into distinct layers. This makes the codebase easier to understand, test, and extend.
- Facade Pattern: The Database class encapsulates engine creation, schema initialisation, and seeding. The rest of the application only calls db.get_session().
- Service Layer: AuthService, QuizService, and AttemptService encapsulate business logic. Pages call services rather than implementing business rules directly in the UI.

### Architecture Diagram

The following diagram shows the main components and their relationships: browser, NiceGUI server, UI pages, service layer, data access layer, and database.

```mermaid
flowchart TD
    Browser[Browser / Thin Client] --> UI[NiceGUI UI Pages]
    UI --> Service[Service Layer]
    Service --> DAO[Data Access Layer / DAO]
    DAO --> DB[(SQLite Database)]

    Service --> AuthService[AuthService]
    Service --> QuizService[QuizService]
    Service --> AttemptService[AttemptService]
```

The UI does not access the database directly. The flow is UI → Service → DAO → SQLite.

---

<a id="database-and-orm"></a>
## 🗄️ Database and ORM

The application uses SQLModel to map domain objects to a SQLite database.

### Entities

- User — teachers and students
- Quiz — quizzes created by teachers
- Question — questions belonging to a quiz
- AnswerOption — answer choices for each question
- QuizAttempt — one attempt by a student on a quiz
- StudentAnswer — the answer a student gave for one question
- StudentAnswerSelection — links a StudentAnswer to one or more AnswerOption rows, used for multiple-choice answers

### Relationships

- One User (teacher) → many Quiz
- One Quiz → many Question
- One Question → many AnswerOption
- One User (student) → many QuizAttempt
- One QuizAttempt → many StudentAnswer
- One StudentAnswer → many StudentAnswerSelection
- One AnswerOption → many StudentAnswerSelection

### Question Types

| Type | Key | Description |
|------|-----|-------------|
| Single Choice | single | One correct answer from 4 options |
| Multiple Choice | multiple | Multiple correct answers — all correct answers must be selected to get the full point |
| True / False | truefalse | True or False — one correct answer from 2 options |

### ER Diagram

<img width="1998" height="1552" alt="image" src="https://github.com/user-attachments/assets/93bad87c-5333-4e4f-b61b-e9eb10bb7e18" />

### Class Diagram

<img width="720" height="1018" alt="image" src="https://github.com/user-attachments/assets/99169c6e-0b70-499d-970a-03742e9e709e" />

---

<a id="project-requirements"></a>
## ✅ Project Requirements

### 1. Browser-based App with NiceGUI

The application runs in the browser. All UI components (ui.button, ui.input, ui.card, etc.) are created server-side via NiceGUI. The browser acts as a thin client and does not contain persistent application state or business logic.

Key pages:

- Login & Registration
- Teacher Dashboard with quiz management, search, publish and delete actions
- Quiz Creator and Editor
- Student Dashboard with available quizzes and search
- Quiz View with question-by-question flow
- Results Page with per-question breakdown
- Statistics Page
- Profile Page for password changes

### 2. Data Validation and Security

The application validates user input and protects passwords:

- Empty title or missing questions → quiz cannot be saved
- Password must be at least 6 characters on registration
- All questions must be answered before quiz submission
- Multiple Choice requires at least one correct answer
- Passwords are hashed with bcrypt and are never stored in plain text
- Old password is verified before allowing a password change

### 3. Database Management

All data is managed via SQLModel, an ORM built on SQLAlchemy. No raw SQL is written in the application. The Database class initialises the schema and seeds demo data on first run.

---

<a id="implementation"></a>
## ⚙️ Implementation

### Technology

- Python 3.x
- NiceGUI
- SQLModel / SQLAlchemy
- SQLite
- pytest
- bcrypt

### 📚 Libraries Used

| Library | Purpose |
|---------|---------|
| nicegui | Browser-based UI framework |
| sqlmodel | ORM — maps Python classes to SQLite tables, built on SQLAlchemy |
| sqlalchemy | Database toolkit used internally by SQLModel |
| pytest | Testing framework |
| bcrypt | Secure password hashing with salt |

### Password Security

Passwords are not stored in plain text. LearnLoop uses bcrypt to hash passwords before storing them in the database. During login, the entered password is verified against the stored bcrypt hash.

### Service Layer Responsibilities

The main business logic is organized in service classes:

- AuthService: registration, login, password hashing and password changes
- QuizService: quiz creation, editing, publishing, unpublishing and deletion
- AttemptService: quiz attempts, scoring, results and statistics

---

<a id="repository-structure"></a>
## 📂 Repository Structure

```text
quiz-app/
├── __init__.py
├── __main__.py
├── application.py          ← App entry point (QuizApplication class)
├── requirements.txt
├── data_access/
│   ├── __init__.py
│   ├── dao.py              ← Data Access Objects (UserDAO, QuizDAO)
│   ├── db.py               ← Database class (Facade)
│   └── seed.py             ← Demo data seeder
├── domain/
│   ├── __init__.py
│   └── models.py           ← SQLModel table definitions
├── pages/
│   ├── __init__.py
│   ├── login.py
│   ├── profile.py
│   ├── register.py
│   ├── student/
│   │   ├── __init__.py
│   │   ├── dashboard.py
│   │   ├── quiz_view.py
│   │   ├── results.py
│   │   └── statistics.py
│   └── teacher/
│       ├── __init__.py
│       ├── dashboard.py
│       ├── quiz_create.py
│       ├── quiz_edit.py
│       └── quiz_results.py
├── services/
│   ├── __init__.py
│   ├── auth_service.py     ← Login, register, password change
│   ├── attempt_service.py  ← Score calculation and statistics
│   └── quiz_service.py     ← Quiz creation and management
├── tests/
│   ├── __init__.py
│   ├── test_db.py          ← TC_007–TC_009
│   ├── test_integration.py ← TC_010–TC_012
│   ├── test_services.py    ← TC_013–TC_018
│   └── test_unit.py        ← TC_001–TC_006, TC_019–TC_023
└── ui/
    ├── __init__.py
    ├── controllers.py
    └── pages.py            ← URL routing
```

---

<a id="how-to-run"></a>
## 🚀 How to Run

### 1. Project Setup

Python 3.10 or higher is required.

Create and activate a virtual environment:

macOS/Linux:

bash python3 -m venv .venv source .venv/bin/activate 

Windows PowerShell:

powershell python -m venv .venv .\.venv\Scripts\Activate.ps1 

If python is not found on Windows, use py instead:

powershell py -3 -m venv .venv .\.venv\Scripts\Activate.ps1 

Install dependencies:

bash python -m pip install -r requirements.txt 

### 2. Launch

bash python application.py 

Open the URL printed in the console, for example:

text http://localhost:8080 

### 3. Demo Accounts

| Role | Username | Password |
|------|----------|----------|
| Teacher 1 | lehrer | lehrer123 |
| Teacher 2 | frau_huber | huber123 |
| Student 1 | schueler | schueler123 |
| Student 2 | max | max123 |
| Student 3 | lena | lena123 |

Note: On the login screen under Demo-Zugänge, you can click on the teacher demo account or on the student demo account. After that click, the username and password are filled in automatically.

### 4. Usage

As a Teacher:

1. Log in with a teacher account
2. Create a new quiz with the + Neues Quiz button
3. Add questions: Single Choice, Multiple Choice, or True/False
4. Save and publish the quiz so students can see it
5. View detailed student results via Auswertungen

As a Student:

1. Log in with a student account
2. Browse available quizzes and click Quiz starten
3. Answer all questions and submit
4. Review your results per question
5. Check your overall statistics via Statistik

### Troubleshooting

- Port already in use: Ensure no other server is running on port 8080, or change the port in the start configuration.
- Virtual environment not activated: Make sure to activate .venv before installing dependencies or starting the app.
- Missing dependencies / ImportError: Run python -m pip install -r requirements.txt again.
- Database issues after model changes: Delete the local quiz.db file and restart the app so the demo database can be recreated.
- NiceGUI version issues: requirements.txt contains the tested version. Check compatibility before upgrading to a newer major version.

---

<a id="testing"></a>
## 🧪 Testing

Tests are organised into four files. Run all tests with:

bash python -m pytest tests/ 

| File | Test IDs | Description |
|------|----------|-------------|
| test_unit.py | TC_001–TC_006, TC_019–TC_023 | Score calculation, validation, password hashing, AttemptService |
| test_db.py | TC_007–TC_009 | User, Quiz, and AnswerOption persistence in SQLite |
| test_integration.py | TC_010–TC_012 | Quiz publish, student attempt, quiz with questions |
| test_services.py | TC_013–TC_018 | AuthService and QuizService business logic |

Total: 24 test cases

Note: All tests use an in-memory SQLite database (sqlite:///:memory:). They run independently from quiz.db, so no existing data is affected when running the test suite.

### Template used for writing test cases

1. Test case ID — unique identifier, for example TC_001
2. Title / description — what is being tested
3. Preconditions — what must be set up first
4. Test steps — actions performed
5. Test data / input
6. Expected result
7. Actual result
8. Status — pass or fail
9. Comments

---

<a id="team-contributions"></a>
## 👥 Team & Contributions

| Name | Branch | Contribution |
|------|--------|--------------|
| Dario | feature/database | Domain models, database connection, seed data, services (AuthService, QuizService, AttemptService), service tests (TC_013–TC_018) |
| Arthur | feature/teacher | Teacher dashboard with search, publish, unpublish and delete actions; quiz creator for Single Choice, Multiple Choice and True/False; detailed quiz results per student; quiz edit page; README |
| Sharun | feature/student | Login with clickable demo cards, register with role selection, profile, student dashboard with search, quiz view for Single Choice, Multiple Choice and True/False, results, statistics, routing (ui/pages.py), unit tests (TC_001–TC_006, TC_019–TC_023), final integration |

---

## Refactoring Update: Security and Service Layer

- Passwords are hashed with bcrypt instead of SHA256/hashlib. bcrypt uses salts and is more suitable for password storage.
- UI pages mainly handle input, navigation and display.
- Business logic is centralized in AuthService, QuizService and AttemptService.
- Teacher actions such as publish, unpublish, delete and result loading use service methods.
- Student quiz submission, results and statistics use AttemptService.

---

<a id="license"></a>
## 📝 License

This project is provided for educational use only as part of the module «Objektorientierte Programmierung
