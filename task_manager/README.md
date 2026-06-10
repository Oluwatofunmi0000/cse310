# Task Manager (Web App)

Simple Flask-based task manager with create/read/update/delete features, search, and filtering.

Setup:

1. Create and activate a virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # macOS / Linux
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app

```bash
python app.py
```

Open http://127.0.0.1:5000 in your browser.

Files:

- `app.py` — main Flask application
- `templates/` — HTML templates
- `static/css/styles.css` — styles
- `task_manager.db` — SQLite database (created on first run)
