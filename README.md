# 📄 ResumePro — AI-Powered Resume Builder

> A full-stack **Django Resume Builder** that helps users create, manage, preview, customize, and download professional resumes with multiple templates and an integrated **Google Gemini AI Assistant**.

[![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2%2B-092E20?logo=django)](https://www.djangoproject.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?logo=bootstrap)](https://getbootstrap.com/)
[![MySQL](https://img.shields.io/badge/MySQL-Database-4479A1?logo=mysql)](https://www.mysql.com/)
[![Gemini](https://img.shields.io/badge/Google%20Gemini-AI-4285F4?logo=google)](https://ai.google.dev/)
[![WeasyPrint](https://img.shields.io/badge/WeasyPrint-PDF-red)](https://weasyprint.org/)

---

## 🌐 Project

**ResumePro** is designed to make professional resume creation simple and structured.

A user can:

1. Create an account
2. Build one or more resumes
3. Choose from four resume templates
4. Add personal information
5. Add education, experience, projects, skills, certificates, languages, and hobbies
6. Upload and crop a profile/resume photo
7. Use Gemini AI to generate or improve resume content
8. Preview the resume
9. Print the resume directly from the browser
10. Download the same resume as a PDF

The application also includes a **staff-only custom admin dashboard** for monitoring users, resumes, visitors, template usage, and recent activity.

---

## ✨ Main Features

### 👤 User Accounts

- User registration
- Login / logout
- Password change
- User profile
- Profile photo upload
- Photo crop/zoom/move support
- Bio and contact information
- LinkedIn, GitHub, and website links
- User-specific resume access

### 📄 Resume Builder

Each user can create and manage multiple resumes.

Resume information includes:

- Full name
- Profession
- Profile photo
- Email
- Phone number
- Date of birth
- Gender
- Address
- City
- State
- Country
- Postal code
- Professional summary
- LinkedIn
- GitHub
- Portfolio
- Website

### 🎓 Education

Users can add multiple education records:

- Institution
- Degree
- Field of study
- Grade / CGPA / percentage
- Start date
- End date
- Currently studying status
- Description

### 💼 Work Experience

Users can add multiple experience records:

- Company name
- Job title
- Employment type
- Location
- Start date
- End date
- Currently working status
- Job description

### 💻 Projects

Each resume can contain multiple projects:

- Project name
- Technologies used
- Project URL
- GitHub URL
- Start date
- End date
- Project description

### 🛠️ Skills

Skills support four proficiency levels:

- Beginner
- Intermediate
- Advanced
- Expert

The application also converts the selected level into a visual percentage for the resume template.

### 🏆 Certificates

Users can add:

- Certificate name
- Issuing organization
- Issue date
- Credential URL

### 🌐 Languages

For each language, users can specify:

- Reading ability
- Writing ability
- Speaking ability

### 🎯 Hobbies

Users can add multiple hobbies to their resume.

---

# 🎨 Resume Templates

ResumePro currently includes **four resume templates**:

| Template | Description |
|---|---|
| 🟦 Modern | Clean and contemporary resume layout |
| 🟩 Professional | Traditional professional resume style |
| 🟥 Creative | More visually expressive design |
| ⬛ Executive | Minimal and executive-oriented layout |

The selected template can be changed later without rebuilding the resume from scratch.

Template files are located in:

```text
templates/resume/templates/
├── modern.html
├── professional.html
├── creative.html
└── executive.html
```

---

# 🤖 Gemini AI Assistant

ResumePro integrates **Google Gemini 2.5 Flash** to help users write better resume content.

The AI Assistant provides several tools.

### ✍️ Career Summary Generator

Generates a professional career summary based on:

- Profession
- Existing skills
- Experience

The generated text is shown to the user before saving.

### 🛠️ Skill Suggestions

The AI can suggest relevant skills for the user's profession.

The user can review and edit the suggestions before saving them.

### 💼 Job Description Generator

Generates professional work-experience bullet points using:

- Job title
- Company name
- Employment type

### 💻 Project Description Generator

Generates a concise project description using:

- Project name
- Technologies used

### 🚀 Full Resume Content Generator

Can generate:

- Professional summary
- Multiple skill suggestions

The user can edit the generated content before saving it.

### 🔐 Human Review Before Saving

AI-generated content is **not automatically written directly into the resume**.

The workflow is:

```text
User Input
    ↓
Gemini AI
    ↓
Generated Content
    ↓
User Reviews / Edits
    ↓
User Saves
    ↓
Resume Updated
```

This gives the user control over the final resume content.

---

# 📸 Image Handling

The project uses **Pillow** for image processing.

It supports:

- Profile photos
- Resume photos
- Image upload
- Crop
- Zoom
- Move/position adjustment

The front-end crop functionality is implemented through the project's photo-cropper JavaScript functionality.

---

# 📄 Resume Preview & PDF

ResumePro uses **WeasyPrint** to generate PDFs.

An important design choice is that the project uses the same HTML/CSS resume template for the preview and PDF generation.

The workflow is:

```text
Resume Data
     ↓
Selected Template
     ↓
HTML + CSS
     ↓
Browser Preview
     ↓
WeasyPrint
     ↓
PDF Download
```

This helps keep the downloaded PDF visually consistent with the on-screen resume.

The project also provides a browser **Print** workflow directly from the resume preview.

---

# 👨‍💼 Custom Admin Dashboard

In addition to Django's built-in admin system, ResumePro contains a custom staff-only admin dashboard.

The dashboard provides information such as:

- Total users
- Active users
- New users today
- New users in the last 7 days
- New users in the last 30 days
- Total resumes
- Resumes created today
- Visitors today
- Visitors during the last 7 days
- Approximate real-time visitors
- Visitor trends
- User growth
- Template usage
- Recent users
- Recent resumes
- Popular pages

### Custom Admin URL

```text
/myadmin/
```

Only users with staff access can use the custom admin dashboard.

### Django Built-in Admin

The standard Django admin is available separately at:

```text
/django-admin/
```

The `/admin/` route redirects to the custom admin dashboard.

---

# 📊 Visitor Tracking

ResumePro includes a lightweight visitor-tracking middleware.

For normal page requests, it records analytics information such as:

- Visitor IP address
- Requested page
- User
- Session key
- User agent
- Visit timestamp

Static files, media files, Django admin requests, and the real-time polling endpoint are excluded from tracking.

> Visitor tracking is intended for analytics. The recorded IP address should not be treated as a guaranteed security identity, especially behind proxies.

---

# 🏗️ Technology Stack

## Backend

- Python
- Django
- Django ORM
- Django Authentication
- Django Middleware

## Frontend

- HTML5
- CSS3
- JavaScript
- Bootstrap 5.3
- Bootstrap Icons
- Google Fonts

## Database

- MySQL
- SQLite optional for local development/testing

## AI

- Google Gemini API
- Gemini 2.5 Flash

## PDF

- WeasyPrint

## Image Processing

- Pillow
- Client-side photo crop/zoom functionality

## Configuration

- python-dotenv
- Environment variables

## Production Server

- Gunicorn

## Version Control

- Git
- GitHub

---

# 📂 Project Structure

```text
resume_builder/
│
├── manage.py
├── requirements.txt
├── SETUP.txt
├── .gitignore
├── .env                    # Local secrets - DO NOT COMMIT
│
├── accounts/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── migrations/
│
├── resume/
│   ├── admin.py
│   ├── forms.py
│   ├── middleware.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   ├── templatetags/
│   └── migrations/
│
├── resume_builder/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── dashboard.html
│   ├── create_resume.html
│   ├── edit_resume.html
│   ├── resume_detail.html
│   ├── resume_list.html
│   ├── choose_template.html
│   ├── change_template.html
│   │
│   ├── accounts/
│   │   ├── login.html
│   │   ├── signup.html
│   │   ├── profile.html
│   │   ├── edit_profile.html
│   │   └── change_password.html
│   │
│   ├── custom_admin/
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── users.html
│   │   ├── user_detail.html
│   │   └── resumes.html
│   │
│   └── resume/
│       └── templates/
│           ├── modern.html
│           ├── professional.html
│           ├── creative.html
│           ├── executive.html
│           └── _toolbar.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   ├── script.js
│   │   └── photo-cropper.js
│   └── images/
│       ├── favicon.svg
│       └── ResumeProLogo.png
│
└── media/
    ├── profile_photos/
    └── resume_photos/
```

---

# 🗄️ Database Design

The application uses Django models with relationships between users and resume sections.

## Main Models

### UserProfile

Extends Django's built-in `User` with:

- Photo
- Phone
- Bio
- City
- Website
- LinkedIn
- GitHub

Each Django user automatically receives a `UserProfile`.

### Resume

Stores the main resume information and belongs to one user.

```text
User
 └── Resume
      ├── Education
      ├── Experience
      ├── Project
      ├── Skill
      ├── Certificate
      ├── Language
      └── Hobby
```

The child records use foreign keys to the Resume model.

Deleting a resume also removes its related child records through Django's cascade behavior.

### SiteVisitor

Stores website analytics information used by the custom admin dashboard.

---

# 🔐 Security & Environment Variables

Sensitive configuration is loaded from environment variables rather than being hard-coded into the application.

The project uses variables such as:

```text
DJANGO_SECRET_KEY
DJANGO_DEBUG
DJANGO_ALLOWED_HOSTS

DB_NAME
DB_USER
DB_PASSWORD
DB_HOST
DB_PORT

GEMINI_API_KEY
```

For local development, create a `.env` file in the same directory as `manage.py`.

Example:

```env
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=resume_builder_db
DB_USER=your_mysql_user
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306

GEMINI_API_KEY=your_gemini_api_key

USE_SQLITE=False
```

### SQLite Option

If you do not want to configure MySQL for a quick local test, use:

```env
USE_SQLITE=True
```

The project will then use:

```text
db.sqlite3
```

instead of MySQL.

> ⚠️ Never commit your real `.env` file, API keys, database passwords, or Django production secret key to GitHub.

---

# 🛠️ Local Installation

## 1. Clone the Repository

```bash
git clone https://github.com/sandeepbharat211/resume-builder.git
```

Move into the project:

```bash
cd resume-builder
```

If the downloaded repository contains an additional outer folder, enter the folder containing `manage.py`.

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

The main dependencies include:

```text
Django
mysqlclient
Pillow
WeasyPrint
google-generativeai
python-dotenv
```

---

# 🗄️ MySQL Setup

If you are using MySQL, create the database first.

Example:

```sql
CREATE DATABASE resume_builder_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

Then configure the database variables in `.env`.

```env
DB_NAME=resume_builder_db
DB_USER=your_mysql_user
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
```

---

# 🧪 SQLite Quick Setup

For a simple local test without MySQL:

```env
USE_SQLITE=True
```

Then continue with migrations.

This is useful when you want to test the application before configuring a production database.

---

# 🔑 Gemini API Setup

The AI Assistant requires a Google Gemini API key.

Create a key through Google AI Studio:

https://aistudio.google.com/app/apikey

Add it to `.env`:

```env
GEMINI_API_KEY=your_gemini_api_key
```

The application is configured to use:

```text
gemini-2.5-flash
```

---

# 🗃️ Run Migrations

From the folder containing `manage.py`:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

# 👤 Create Admin / Staff User

Create a Django superuser:

```bash
python manage.py createsuperuser
```

Follow the prompts for:

- Username
- Email
- Password

A superuser has staff access and can access the custom admin dashboard.

---

# 📦 Collect Static Files

For production or deployment:

```bash
python manage.py collectstatic
```

This collects project static assets into:

```text
staticfiles/
```

---

# ▶️ Run the Development Server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

# 🔗 Important URLs

| Purpose | URL |
|---|---|
| Home | `/` |
| Dashboard | `/dashboard/` |
| Choose Template | `/choose-template/` |
| Create Resume | `/create/` |
| Resume List | `/list/` |
| Profile | `/accounts/profile/` |
| Login | `/accounts/login/` |
| Signup | `/accounts/signup/` |
| Custom Admin | `/myadmin/` |
| Django Admin | `/django-admin/` |

Resume-specific URLs are generated dynamically using the resume ID.

---

# ☁️ Deployment

The application can be deployed on a platform such as **Render** using Gunicorn.

A production start command is:

```bash
gunicorn resume_builder.wsgi:application
```

## Recommended Production Environment Variables

Configure these in the hosting platform's environment-variable settings:

```text
DJANGO_SECRET_KEY
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=your-domain.com

DB_NAME
DB_USER
DB_PASSWORD
DB_HOST
DB_PORT

GEMINI_API_KEY

USE_SQLITE=False
```

Do not place production secrets directly into source code.

---

# 🚀 Production Checklist

Before deploying:

- [ ] Set a strong `DJANGO_SECRET_KEY`
- [ ] Set `DJANGO_DEBUG=False`
- [ ] Configure `DJANGO_ALLOWED_HOSTS`
- [ ] Configure the production database
- [ ] Add `GEMINI_API_KEY`
- [ ] Run migrations
- [ ] Run `collectstatic`
- [ ] Confirm Gunicorn starts successfully
- [ ] Test login/signup
- [ ] Test resume creation
- [ ] Test all resume templates
- [ ] Test PDF generation
- [ ] Test AI Assistant
- [ ] Confirm media uploads work
- [ ] Confirm admin access

---

# 🧩 WeasyPrint Notes

WeasyPrint is used for PDF generation.

Depending on the operating system, WeasyPrint may require additional system libraries such as:

- Pango
- Cairo
- GDK-PixBuf

If Python installation succeeds but PDF generation fails, follow the official installation instructions:

https://doc.courtbouillon.org/weasyprint/stable/first_steps.html

---

# 🔄 Application Workflow

The complete user workflow is approximately:

```text
                  ┌─────────────────┐
                  │   Register      │
                  └────────┬────────┘
                           ↓
                  ┌─────────────────┐
                  │    Dashboard    │
                  └────────┬────────┘
                           ↓
                  ┌─────────────────┐
                  │ Choose Template │
                  └────────┬────────┘
                           ↓
                  ┌─────────────────┐
                  │ Create Resume   │
                  └────────┬────────┘
                           ↓
        ┌──────────────────┼──────────────────┐
        ↓                  ↓                  ↓
   Personal Info       Education         Experience
        ↓                  ↓                  ↓
     Projects            Skills          Certificates
        ↓                  ↓                  ↓
   Languages            Hobbies          Photo
        └──────────────────┼──────────────────┘
                           ↓
                  ┌─────────────────┐
                  │   AI Assistant  │
                  └────────┬────────┘
                           ↓
                  ┌─────────────────┐
                  │ Review & Edit   │
                  └────────┬────────┘
                           ↓
                  ┌─────────────────┐
                  │ Resume Preview  │
                  └────────┬────────┘
                           ↓
              ┌────────────┴────────────┐
              ↓                         ↓
        Browser Print              PDF Download
```

---

# 🔒 Data Ownership & Access

Resume records are associated with the authenticated user.

The application uses Django's authentication decorators and object-level filtering so normal users work with their own resumes and related records.

For example, resume operations use the logged-in user when retrieving records:

```python
get_object_or_404(Resume, id=id, user=request.user)
```

This prevents a normal user from simply changing a resume ID in the URL to access another user's resume through these views.

---

# 📁 Important Files

| File | Purpose |
|---|---|
| `manage.py` | Django project command-line utility |
| `resume_builder/settings.py` | Project configuration |
| `resume_builder/urls.py` | Main URL configuration |
| `resume_builder/wsgi.py` | WSGI entry point for deployment |
| `accounts/models.py` | User profile model |
| `accounts/forms.py` | Authentication/profile forms |
| `accounts/views.py` | Login, signup, profile logic |
| `resume/models.py` | Resume and section database models |
| `resume/forms.py` | Resume section forms |
| `resume/views.py` | Resume, AI, PDF and admin logic |
| `resume/middleware.py` | Visitor analytics middleware |
| `static/css/style.css` | Main application styling |
| `static/js/script.js` | Front-end functionality |
| `static/js/photo-cropper.js` | Photo crop/zoom functionality |
| `templates/resume/templates/` | Resume designs |
| `requirements.txt` | Python dependencies |
| `.gitignore` | Files excluded from Git |

---

# 🧠 Architecture Overview

ResumePro follows Django's standard application structure:

```text
Browser
   │
   ▼
Django URLs
   │
   ▼
Views
   │
   ├──────────────► Forms
   │
   ├──────────────► Models
   │
   ├──────────────► Gemini API
   │
   └──────────────► HTML Templates
                         │
                         ▼
                    HTML + CSS
                         │
                         ▼
                     WeasyPrint
                         │
                         ▼
                         PDF
```

The project is separated into two primary Django applications:

### `accounts`

Responsible for:

- Registration
- Login
- Logout
- User profile
- Password changes

### `resume`

Responsible for:

- Resume creation
- Resume editing
- Resume sections
- Templates
- Preview
- PDF generation
- Gemini AI Assistant
- Visitor tracking
- Custom admin dashboard

---

# 🧹 Git & Security

The project's `.gitignore` excludes sensitive and generated files such as:

```text
__pycache__/
*.pyc
db.sqlite3
/staticfiles/
/media/
.env
```

This is important because `.env` can contain:

- Django secret key
- Database password
- Gemini API key

If a secret has accidentally been committed to a public Git repository, it should be rotated immediately.

---

# 🐛 Troubleshooting

## CSS or JavaScript Changes Are Not Appearing

Try:

1. Stop the server.
2. Start it again:

```bash
python manage.py runserver
```

3. Hard refresh the browser:

```text
Ctrl + Shift + R
```

4. If necessary, test in an Incognito/Private window.

---

## Database Connection Error

Check:

```text
DB_NAME
DB_USER
DB_PASSWORD
DB_HOST
DB_PORT
```

Also verify that the MySQL server is running.

For a quick local test, you can temporarily use:

```env
USE_SQLITE=True
```

---

## PDF Generation Error

Confirm that:

```bash
pip install weasyprint
```

completed successfully.

If the error mentions missing native libraries, install the required system dependencies for your operating system using the official WeasyPrint documentation.

---

## Gemini AI Error

Check:

```env
GEMINI_API_KEY=your_key
```

Also verify that the API key is valid and that the configured Gemini model is available for your API account.

---

# 🔮 Future Improvements

Possible future enhancements include:

- More professional resume templates
- ATS-focused resume analysis
- Resume scoring
- Job-description-based resume customization
- AI-powered keyword optimization
- More export formats
- Public/shareable resume links
- Resume version history
- Drag-and-drop resume sections
- Email resume sharing
- More advanced analytics
- Cloud media storage
- Improved mobile UI
- Automated deployment pipeline

---

# 🎯 Project Goals

This project demonstrates practical full-stack development skills including:

- Django web development
- Relational database design
- User authentication
- CRUD operations
- File uploads
- Image processing
- Responsive frontend development
- Third-party API integration
- Generative AI integration
- PDF generation
- Middleware development
- Analytics
- Admin dashboard development
- Environment-based configuration
- Git/GitHub workflow
- Production deployment

---

# 👨‍💻 Author

**Sandeep Bharat**

GitHub:

https://github.com/sandeepbharat211

---

# ⭐ Contributing

Contributions and suggestions are welcome.

If you want to improve the project:

```bash
git fork
```

Create a feature branch:

```bash
git checkout -b feature/your-feature
```

Commit your changes:

```bash
git add .
git commit -m "Add your feature"
```

Push the branch:

```bash
git push origin feature/your-feature
```

Then open a Pull Request.

---

# 📜 License

No explicit open-source license file is currently included in the project.

If this repository is intended to be reused or distributed publicly, consider adding an appropriate `LICENSE` file.

---

## ❤️ ResumePro

**Build your resume. Improve your content. Choose your design. Download your professional resume.**

Built with **Python, Django, Bootstrap, MySQL, Gemini AI and WeasyPrint**.
