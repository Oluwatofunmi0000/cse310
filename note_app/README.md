# Note App

A simple Flask note-taking application with search, tags, and CRUD operations.

## Setup

```powershell
cd "C:\Users\HP15\Desktop\hello world\note_app"
python -m venv venv
.\venv\Scripts\Activate
python -m pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000 in your browser.

## Features

- Create, edit, view, and delete notes
- Search by title, body, and tags
- Tags are stored as comma-separated text
- Uses SQLite database `notes.db`
