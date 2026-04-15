# Finance Audit Management System

A Flask-based web application for managing finance audit projects, tracking audits, and generating summary reports.

## Features

- User authentication (register, login, logout)
- Role-based access (`admin` and `user`)
- Project management (create, view, edit, delete)
- Audit management with risk and compliance scoring
- Dashboard statistics and report summaries
- Profile management
- JSON stats API endpoint (`/api/stats`)

## Tech Stack

- Python 3
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-WTF
- SQLite (default)

## Project Structure

```text
.
|-- app.py
|-- auth.py
|-- routes.py
|-- models.py
|-- database.py
|-- config.py
|-- templates/
|-- static/
`-- requirements.txt
```

## Getting Started

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd finance-audit
```

### 2. Create and activate a virtual environment

Windows (PowerShell):

```powershell
python -m venv env
.\env\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
SECRET_KEY=replace-with-a-strong-secret
DATABASE_URL=sqlite:///finance_audit.db
```

### 5. Run the app

```bash
python app.py
```

Open: `http://127.0.0.1:5000`

## Default Admin Account

On first run, the app auto-creates an admin account:

- Username: `admin`
- Password: `admin123`

Change this password immediately after login.

## Notes

- Database tables are created automatically on startup.
- Uploaded files are stored in `static/uploads/`.
- Allowed upload extensions are configured in `config.py`.

## Development Tip (Cookies)

`config.py` currently sets:

- `SESSION_COOKIE_SECURE = True`

If you run locally on plain HTTP, authentication cookies may not persist in some setups.
For local development, you can set it to `False` and keep it `True` in production with HTTPS.

## API

### `GET /api/stats`

Returns dashboard statistics in JSON format for the current user scope.

## License

Add your preferred license here (for example, MIT).
