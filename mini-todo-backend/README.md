# Todo Backend (Flask + SQLite)

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
# open http://127.0.0.1:5000/health
```
The server listens on `PORT` env var when provided (required by Render/Railway).

## Deploy
- Use `gunicorn app:app` as the start command (Procfile included).
- SQLite is stored in `database.db`. On free hosts, the file can be ephemeral; this is fine for demo.
