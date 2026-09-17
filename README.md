# AMAN ENTERPRISE — Crane & Heavy Machinery Website

A complete, production-style business website with a dynamic **Flask + MySQL** backend
and a fully functional **Admin Panel**.

## Features

- Modern, responsive, industrial-themed public website (Home, About, Services, Equipment,
  Projects, Contact) fully driven by MySQL content
- Secure admin panel with hashed passwords and session-based authentication
- Full CRUD for Services, Equipment, Projects, Testimonials, Enquiries, Admin Users
- Website Settings panel (company info, socials, hero content, stats) editable live
- Image upload system with file-type validation and safe filenames
- Enquiry form with server-side validation, stored in MySQL
- Floating WhatsApp + Call buttons
- Custom 404 / 403 / 500 error pages
- SEO basics: titles, meta descriptions, Open Graph tags, robots.txt

## Tech Stack

- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5, Font Awesome
- **Backend:** Python, Flask (blueprints)
- **Database:** MySQL (via PyMySQL)
- **Auth:** Werkzeug password hashing + Flask sessions

## Project Structure

```
aman_enterprise/
├── app.py                 # App factory / entry point
├── config.py               # Configuration (reads .env)
├── db.py                    # MySQL connection helpers
├── utils.py                 # Auth decorators, upload/validation helpers
├── routes_public.py         # Public website routes
├── routes_admin.py          # Admin panel routes
├── requirements.txt
├── schema.sql                # Full DB schema + sample data
├── .env.example
├── templates/
│   ├── base.html, index.html, about.html, services.html,
│   │   equipment.html, projects.html, contact.html, login.html
│   ├── errors/ (404, 403, 500)
│   └── admin/ (base, dashboard, services, equipment, projects,
│                 testimonials, enquiries, enquiry_detail, admins, settings)
└── static/
    ├── css/style.css
    ├── js/script.js
    ├── robots.txt
    └── uploads/           # Uploaded images land here
```

## Installation

### Step 1 — Install Python
Make sure Python 3.10+ is installed: `python3 --version`

### Step 2 — Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Create the MySQL database
```bash
mysql -u root -p
CREATE DATABASE aman_enterprise;
exit;
```

### Step 5 — Import the schema
```bash
mysql -u root -p aman_enterprise < schema.sql
```
This creates all tables and inserts sample services, equipment, projects,
testimonials, settings, and one sample admin account.

### Step 6 — Configure environment variables
```bash
cp .env.example .env
```
Edit `.env` and set `SECRET_KEY`, `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`, `DB_PORT`.

### Step 7 — Run the app
```bash
python app.py
```

### Step 8 — Open the website
Visit **http://localhost:5000** in your browser.

## Admin Access

- URL: **http://localhost:5000/admin/login**
- Sample credentials (from `schema.sql`):
  - Email: `admin@amanenterprise.in`
  - Password: `Admin@123`

  **⚠️ Change this password immediately after first login** via
  Website Settings → Change My Password, or through the Admin Users page.

## Security Notes

- Passwords are hashed with Werkzeug's `generate_password_hash` (scrypt) — never stored
  in plain text.
- All SQL queries use parameterized statements (`%s` placeholders) to prevent SQL injection.
- Admin routes are protected by `login_required` / `super_admin_required` decorators.
- File uploads are restricted to `jpg`, `jpeg`, `png`, `webp`, renamed with UUIDs, and
  size-capped at 5MB.
- Database credentials and the secret key live in `.env` (never committed, see
  `.env.example`) — not hardcoded in source.

## Troubleshooting

| Problem | Fix |
|---|---|
| `Can't connect to MySQL server` | Check `DB_HOST`/`DB_PORT` in `.env` and that MySQL is running |
| `Access denied for user` | Verify `DB_USER` / `DB_PASSWORD` in `.env` |
| Images not showing after upload | Ensure `static/uploads/` is writable by the app |
| Admin login fails with correct password | Re-import `schema.sql` — the sample hash must match `Admin@123`, or create a new admin manually with a Python shell:<br>`from werkzeug.security import generate_password_hash; print(generate_password_hash("yourpassword"))` and insert it into the `admins` table |
| 500 error page shown for everything | Set `debug=True` temporarily in `app.py` to see the traceback in your terminal (never enable debug mode in production) |

## Notes

- The public website only ever shows records with `status = 'Active'` — deactivating an
  item from the admin panel hides it publicly without deleting it from the database.
- All content (services, equipment, projects, testimonials, site settings) is loaded
  live from MySQL on every page request — this is a dynamic site, not static HTML.
