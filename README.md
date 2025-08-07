# 🃏 Poker Planner — Sprint Estimation App (Django + React)

**Poker Planner** is a full-stack web application that helps Agile teams plan sprints using the popular "Planning Poker" technique. It allows users to collaboratively estimate tasks, manage sprint boards, and integrate directly with JIRA.

---

## 🚀 Features

### ✅ Core Functionality
- **User Roles**: Manager, Player, Spectator
- **Pokerboard**: Each board is managed by one Manager
- **JIRA Integration**: Import tickets by Sprint, Ticket IDs, or JQL
- **Estimate Options**: Serial, Even, Odd, Fibonacci, or Custom
- **Session Management**: Real-time game using WebSockets
- **User Sign-up & Invite**: Email-based registration and invitations
- **Estimate History**: Graphs and stats per user and board

### 📊 Reporting & Analytics
- View estimate history (filter by date/ticket type)
- Compare user estimates vs actual effort (line chart)
- Track time spent per ticket (avg, min, max)

### 👤 User Profile
- View/edit profile
- View associated groups and boards
- View all estimated tickets

---

## 🧱 Tech Stack

| Layer      | Tech                     |
|------------|--------------------------|
| Frontend   | React + TypeScript + Vite |
| Backend    | Django + Django REST Framework |
| Database   | PostgreSQL               |
| Realtime   | Django Channels + Redis  |
| Auth       | JWT / Token-based Auth   |
| Integration| JIRA API                 |

---

## 📁 Project Structure

```
poker-planner/
├── backend/              # Django project
│   ├── manage.py
│   ├── settings.py
│   └── apps/             # users, boards, tickets, estimates
```

---

## ⚙️ Setup Instructions

### 1. Backend (Django)
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create DB
psql -U postgres
CREATE DATABASE poker_planner;
CREATE USER user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE poker_planner TO user;

# Run migrations
python manage.py migrate
python manage.py runserver
```

### 2. Frontend (React)
```bash
cd frontend
npm install
npm run dev       # For development
npm run build     # For production
```

### 3. WebSocket (Redis)
```bash
sudo service redis-server start
```

---

## 🔄 Workflow

1. Manager creates a board
2. Manager imports tickets from JIRA
3. Users are invited via email
4. Players select estimates (hidden until revealed)
5. Timer ends → estimates are shown
6. Estimates are saved and reports generated

---

## Optional/Nice to Have

- Guest URLs to join boards
- User-configurable credentials for JIRA
- Dark mode + responsive design

---

## To Do

- [x] User authentication
- [x] WebSocket integration
- [x] Ticket importing
- [x] Testing & CI

---

Maintainer: Abhijeet Kumar 
Email: abhijeet.kumar@joshtechnologygroup.com
Project: **Poker Planner**
