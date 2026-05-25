# AlbumCloud — Photo Album Management System

A **production-ready** Photo Album Management application built with Django, Cloudinary, and PostgreSQL. Deployed on Render.

## 🚀 Live Application

**Live URL:** [[https://my-application-demo.onrender.com](https://cloud-render-gep1.onrender.com))

## 📸 Features

- **Album Management** — Create, edit, and delete photo albums with cover images
- **Photo Uploads** — Upload photos to albums with titles and descriptions, stored on Cloudinary
- **Cloud Storage** — All media is managed via Cloudinary API (no local storage in production)
- **Role-Based Access Control (RBAC)** — Three-tier permission system:
  - **Anonymous Users** — Browse and view albums/photos
  - **Authenticated Users** — Create albums, upload photos, edit/delete their own content
  - **Admins (staff/superuser)** — Full access to edit/delete any content + Django Admin panel
- **Search** — Filter albums and photos by title/description
- **Pagination** — Efficient browsing with paginated results
- **Class-Based Views** — All CRUD operations use Django's CBVs (`ListView`, `CreateView`, `UpdateView`, `DeleteView`)
- **Responsive Design** — Premium dark glassmorphism UI that works on all devices

## 🛠 Tech Stack

| Component | Technology |
|-----------|-----------|
| **Framework** | Django 6.0 (Python) |
| **Database** | PostgreSQL (via Render) |
| **Media Storage** | Cloudinary API |
| **Static Files** | WhiteNoise |
| **Deployment** | Render |
| **Auth** | Django's built-in authentication system |

## 📂 Project Structure

```
cloud-render/
├── recipe_project/          # Django project settings
│   ├── settings.py          # Configuration (env vars, Cloudinary, DB)
│   ├── urls.py              # Root URL config
│   └── wsgi.py              # WSGI entry point
├── gallery/                 # Main application
│   ├── models.py            # Album & Photo models
│   ├── views.py             # Class-Based Views for all CRUD
│   ├── forms.py             # AlbumForm, PhotoForm, CustomUserCreationForm
│   ├── mixins.py            # OwnerOrAdminMixin (RBAC)
│   ├── urls.py              # App URL patterns
│   ├── admin.py             # Admin site configuration
│   └── templates/           # HTML templates
│       ├── gallery/         # Album & photo templates
│       └── registration/    # Login & register templates
├── manage.py
├── requirements.txt
├── build.sh                 # Render build script
├── .env                     # Environment variables (not in repo)
├── .gitignore
└── README.md
```

## 🔧 Local Development Setup

### Prerequisites
- Python 3.10+
- PostgreSQL (or use SQLite locally)
- A Cloudinary account

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/cloud-render.git
   cd cloud-render
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate    # Linux/Mac
   .venv\Scripts\activate       # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   CLOUDINARY_CLOUD_NAME=your_cloud_name
   CLOUDINARY_API_KEY=your_api_key
   CLOUDINARY_API_SECRET=your_api_secret
   DATABASE_URL=postgresql://user:pass@host/dbname  # optional, falls back to SQLite
   ALLOWED_HOSTS=localhost,127.0.0.1
   CSRF_TRUSTED_ORIGINS=http://localhost:8000
   ```

5. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser (admin):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

8. **Visit** `http://localhost:8000`

## 🌐 Environment Variables Reference

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | Django secret key | Yes |
| `DEBUG` | Debug mode (`True`/`False`) | Yes |
| `DATABASE_URL` | PostgreSQL connection string | Production |
| `CLOUDINARY_CLOUD_NAME` | Cloudinary cloud name | Yes |
| `CLOUDINARY_API_KEY` | Cloudinary API key | Yes |
| `CLOUDINARY_API_SECRET` | Cloudinary API secret | Yes |
| `ALLOWED_HOSTS` | Comma-separated hostnames | Yes |
| `RENDER_EXTERNAL_HOSTNAME` | Render hostname (auto-set) | Production |
| `CSRF_TRUSTED_ORIGINS` | Trusted origins for CSRF | Production |

## 🚀 Deployment to Render

1. Push code to GitHub
2. Create a **New Web Service** on [Render](https://render.com)
3. Connect your GitHub repository
4. Configure:
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn recipe_project.wsgi:application`
5. Add all environment variables in Render's dashboard
6. Provision a **PostgreSQL** database on Render and link the `DATABASE_URL`

## 🔐 Role-Based Access Control

| Role | View | Create | Edit Own | Edit Any | Delete Own | Delete Any | Admin Panel |
|------|------|--------|----------|----------|------------|------------|-------------|
| Anonymous | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| User | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ |
| Admin | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

## 📄 License

This project is for educational purposes.
