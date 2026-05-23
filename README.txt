# Taskora 🚀
A Modern Task Marketplace Desktop Application built with Python, CustomTkinter, and PostgreSQL

===========================================================
📌 OVERVIEW
===========================================================

Taskora is a desktop-based task marketplace application where users can:

- Create tasks
- Browse available tasks
- Apply for tasks
- Approve or reject applicants
- Complete tasks
- Earn points and ranks
- Manage profiles and applications

The system supports two user roles:

1. Worker
   - Browse tasks
   - Apply for tasks
   - Track applications
   - Complete assigned tasks
   - Earn points and rank upgrades

2. Creator
   - Post tasks
   - View posted tasks
   - Manage applicants
   - Approve/reject workers
   - Mark tasks as completed

===========================================================
🛠 TECHNOLOGIES USED
===========================================================

- Python
- CustomTkinter
- PostgreSQL
- psycopg2
- SQL
- Object-Oriented Programming (OOP)

===========================================================
📁 PROJECT STRUCTURE
===========================================================

TaskoraApp/
│
├── app.py
├── database.py
├── theme.py
├── setup.sql
├── requirements.txt
├── README.txt
│
├── screens/
│   ├── splash.py
│   ├── login.py
│   ├── register.py
│   ├── dashboard.py
│   ├── create_task.py
│   ├── browse_tasks.py
│   ├── task_details.py
│   ├── my_applications.py
│   ├── my_posted_task.py
│   ├── manage_applicants.py
│   └── profile.py
│
└── assets/

===========================================================
📂 IMPORTANT FILES
===========================================================

1. app.py
   - Main entry point of the application
   - Starts the app
   - Controls navigation between screens
   - Stores current logged-in user

2. database.py
   - Handles all PostgreSQL database operations
   - Contains SQL queries
   - Manages users, tasks, applications, rewards, and statistics

3. theme.py
   - Stores color constants and UI styling

4. setup.sql
   - Creates all database tables

===========================================================
🧠 OOP CONCEPTS USED
===========================================================

The project uses Object-Oriented Programming.

Example:
class DashboardScreen(ctk.CTkFrame)

This means:
- DashboardScreen is a class
- It inherits from CTkFrame
- Each screen behaves like an object

===========================================================
🖥 MAIN FEATURES
===========================================================

✅ Authentication System
- User registration
- User login
- Role-based access

✅ Task Management
Creators can:
- Create tasks
- View posted tasks
- Assign workers

Workers can:
- Browse tasks
- Apply for tasks

✅ Application System
- Workers apply for tasks
- Creators approve/reject applications
- Only one worker can be assigned per task

✅ Reward & Ranking System

Ranks:
- Bronze
- Silver
- Gold
- Platinum

Workers earn points after completing tasks.

✅ Profile Statistics
Displays:
- Completed tasks
- Posted tasks
- Pending applications
- User rank
- User points

===========================================================
🗄 DATABASE TABLES
===========================================================

1. users
   - id
   - name
   - phone
   - password
   - role
   - rank
   - points

2. tasks
   - id
   - title
   - description
   - location
   - reward
   - status
   - creator_phone
   - assigned_worker

3. applications
   - id
   - task_id
   - worker_phone
   - status

===========================================================
⚙️ INSTALLATION GUIDE
===========================================================

1. Install Python
   Download from:
   https://www.python.org/downloads/

2. Install PostgreSQL
   Download from:
   https://www.postgresql.org/download/

3. During PostgreSQL setup:
   Username: postgres
   Password: 1234

4. Create the database

   Open pgAdmin or psql and run:

   CREATE DATABASE taskora_db;

5. Run setup.sql

   Execute the SQL file to create all tables.

6. Install required packages

   Open terminal inside the project folder:

   pip install -r requirements.txt

7. Run the application

   python app.py

===========================================================
🔐 SECURITY NOTE
===========================================================

Passwords are currently stored as plain text.

For real-world production systems, passwords should be hashed using:
- bcrypt
- argon2

This project was built for educational purposes.

===========================================================
🎨 USER INTERFACE
===========================================================

Taskora uses a futuristic neon-themed dark UI.

Main colors:
- Neon Cyan
- Neon Purple
- Neon Pink
- Dark Background

CustomTkinter was used to create:
- Modern buttons
- Frames
- Textboxes
- Responsive layouts

===========================================================
🔄 APPLICATION FLOW
===========================================================

Splash Screen
      ↓
Login/Register
      ↓
Dashboard
      ↓
Browse/Create Tasks
      ↓
Applications
      ↓
Task Completion
      ↓
Rewards & Rank Updates

===========================================================
📚 CONCEPTS DEMONSTRATED
===========================================================

This project demonstrates:
- Python Programming
- GUI Development
- PostgreSQL Integration
- CRUD Operations
- SQL Queries
- OOP
- User Authentication
- Event Handling
- Screen Navigation
- Database Relationships

===========================================================
🚀 FUTURE IMPROVEMENTS
===========================================================

Possible future upgrades:
- Password hashing
- Email verification
- Notifications
- Search & filtering
- Real-time updates
- Admin panel
- Cloud database hosting
- Executable (.exe) deployment

===========================================================
📌 NOTES FOR LECTURER / EXAMINER
===========================================================

Before running the project:

1. Install PostgreSQL
2. Create database:
   taskora_db
3. Run setup.sql
4. Ensure PostgreSQL password is:
   1234
5. Install dependencies:
   pip install -r requirements.txt
6. Run:
   python app.py

===========================================================
✅ PROJECT STATUS
===========================================================

✔ Completed
✔ Functional
✔ Database Connected
✔ OOP Implemented
✔ GitHub Ready