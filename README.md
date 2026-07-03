# -ai-solutions-website
AI-Solutions official website


# AI-Solutions Website

AI-Solutions official website — a responsive web platform with AI chatbot, contact form, and secure admin dashboard with Two-Factor Authentication.



## Project Overview

AI-Solutions is a Sunderland-based startup that makes AI accessible to businesses of all sizes. This website serves as their digital identity, showcasing their expertise in intelligent virtual assistants and rapid prototyping tools.



## Key Features

- 8 Public Pages: Home, Solutions, Past Work, Feedback, Articles, Gallery, Events, Contact
- Contact Us Form: 7 fields with 10-digit phone validation
- Admin Dashboard: Secure login with password protection
- Two-Factor Authentication: Google Authenticator integration
- AI Chatbot: Rule-based virtual assistant for customer queries
- 5-Star Feedback System: Rate and review services
- Responsive Design: Works on all devices (Chrome and Firefox)



## Technologies Used

| Category | Technology | Purpose |
|----------|------------|---------|
| Frontend | HTML5, CSS3 | Structure and styling for 8 pages |
| Backend | Python Flask | Routing, form handling, session management |
| Database | SQLite 3 | Store customer inquiries and feedback |
| Security | pyotp, qrcode | Google Authenticator 2FA |
| Development | VS Code, XAMPP | Code editor and local server |
| Testing | Chrome, Firefox | Cross-browser compatibility |


## Project Structure

ai-solutions-website/
│
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── database.db                     # SQLite database
├── README.md                       # Project documentation
│
├── templates/                      # All HTML templates
│   ├── admin_2fa.html              # 2FA verification page
│   ├── admin_dashboard.html        # Admin dashboard
│   ├── admin_login.html            # Admin login page
│   ├── articles.html               # Articles/Blog page
│   ├── base.html                   # Base template (navbar + footer)
│   ├── chatbot.html                # AI Chatbot page
│   ├── contact.html                # Contact Us form (7 fields)
│   ├── events.html                 # Events page
│   ├── feedback.html
# Feedback page (5-star ratings)
│   ├── gallery.html                # Gallery page
│   ├── index.html                  # Home page
│   ├── past_work.html              # Past Work page
│   └── solutions.html              # Solutions page
│
└── static/                         # Static assets
    ├── script.js                   # JavaScript (chatbot + validation)
    └── style.css                   # Main CSS file


    
---

## Installation and Setup

### Prerequisites

- Python 3.10 or higher
- Google Authenticator app (for 2FA)
- XAMPP (optional, for local server)

### Step 1: Clone the Repository

```bash
git clone https://gith
ub.com/kit23dpuj-coder/-ai-solutions-website.git
cd ai-solutions-website


Step 2: Install Dependencies
pip install flask flask-mail pyotp qrcode


Run the Application
python app.py

Access the Website
Open your browser and go to: http://127.0.0.1:5000

Admin Credentials
Username	Password
admin	Admin@2026


2FA Setup
Log in with admin credentials
Scan the QR code with Google Authenticator
Enter the 6-digit code
Access the dashboard


Database Schema (SQLite)
inquiries Table
Field	Type	Description
id (PK)	INTEGER	Unique identifier
name	TEXT	Customer's full name
email	TEXT	Customer's email
phone	TEXT	Phone number (10 digits)
company	TEXT	Company name
country	TEXT	Country
job_title	TEXT	Job title
job_details	TEXT	Requirements
status	TEXT	pending / replied
reply	TEXT	Admin's reply
submitted_at	TIMESTAMP	Submission date
feedback Table
Field	Type	Description
id (PK)	INTEGER	Unique identifier
name	TEXT	Customer's name
email	TEXT	Customer's email
rating	INTEGER	1-5 stars
comment	TEXT	Review text
admin Table
Field	Type	Description
id (PK)	INTEGER	Unique identifier
username	TEXT	Admin username
password_hash	TEXT	SHA-256 hashed password
twofa_secret	TEXT	Google Authenticator secret key



SQL Schema
sql
CREATE TABLE IF NOT EXISTS inquiries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    company TEXT,
    country TEXT,
    job_title TEXT,
    job_details TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    reply TEXT,
    replied_at TIMESTAMP,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    rating INTEGER NOT NULL,
    comment TEXT,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    twofa_secret TEXT
);



Security Features
In line with the SSDLC methodology, the following security measures are implemented:
Admin Authentication: Password-protected with session management
Two-Factor Authentication: Google Authenticator (pyotp + qrcode)
Access Control: Unauthenticated users redirected to login
SQL Injection Prevention: Parameterized queries
Phone Validation: Regex for exactly 10 digits
Secure Session Management: Flask sessions with secret key
No Customer Login: Reduced attack surface




Testing Results
Test Category	Total Tests	Pass	Fail
Functional Tests	12	12	0
Non-Functional Tests	6	6	0
Client Acceptance	7	7	0
TOTAL	25	25	0
Pass Rate: 100%

Deployment
Local Deployment (XAMPP)
Install XAMPP (v8.2 or higher)
Place project in htdocs folder
Run Flask app: python app.py
Access: http://127.0.0.1:5000



Production Considerations
Use Gunicorn/uWSGI for production WSGI server
Enable HTTPS with SSL/TLS certificate
Use PostgreSQL/MySQL for production database
Store credentials in environment variables



Future Improvements
HTTPS/SSL encryption for secure data transmission
Multi-admin accounts with role-based access control
Automated testing with pytest
Dynamic image upload for gallery
Email notifications for customers
Analytics dashboard with charts
Mobile app for AI chatbot
Cloud deployment (AWS/Azure)


License
This project is licensed under the MIT License.

Author
Kit23dpuj-coder — GitHub: https://github.com/kit23dpuj-coder 

Acknowledgments
AI-Solutions: Client and project owner
ISMT College: Academic guidance
Flask Documentation: Framework reference
SQLite Documentation: Database reference
Google Authenticator: 2FA integration


Contact
For any inquiries, please visit the Contact Us page on the website.

If you found this project helpful, please star it on GitHub.
