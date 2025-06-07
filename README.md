# 📊 Stakeholder Communication & Log Dashboard

A full-stack web-based platform to manage stakeholder interactions, log communications, and monitor project touchpoints efficiently — designed for Project Managers and teams.

---

## Overview

This project was built as part of my learning journey during **Course 3: Project Planning: Putting It All Together** in the **Google Project Management Certificate**. It aims to help project teams:

- Log stakeholder details
- Record communication history
- Monitor follow-up actions
- View centralized dashboard insights
- Authenticate users securely with JWT

---

## Key Features

- **JWT Authentication** — Secure login & protected dashboard access  
- **Stakeholder Management** — Add, view, and manage stakeholder data  
- **Communication Log** — Record key updates and meeting outcomes  
- **Follow-up Tracker** — Never miss an upcoming task or reminder  
- **Dashboard Analytics** — Real-time stats for quick visibility  
- **Frontend UI** — Clean, responsive HTML/CSS/JS design  
- **Backend API** — Built in Python Flask, connected with MySQL

---

## Tech Stack

| Layer         | Tools/Frameworks                   |
|---------------|------------------------------------|
| **Frontend**  | HTML, CSS, JavaScript              |
| **Backend**   | Python Flask                       |
| **Database**  | MySQL                              |
| **Authentication** | JWT (JSON Web Tokens)         |
| **Testing**   | Postman                            |

---

## Folder Structure

├── backend/
│ ├── app.py
│ ├── routes/
│ ├── models/
│ ├── utils/
│ └── database_config.py
├── frontend/
│ ├── Login.html
│ ├── Signup.html
│ ├── Dashboard.html
│ ├── Add_Stake.html
│ ├── Communication.html
│ ├── assets/
│ └── images/
├── README.md
└── requirements.txt


---

## Setup Instructions

### Prerequisites

- Python 3.x  
- MySQL installed & configured  
- Basic understanding of Flask & HTML

### Clone the Repository

```bash
git clone https://github.com/omvashishtha039/stakeholder-log-dashboard.git
cd stakeholder-log-dashboard
