# Backend

This directory hosts the FastAPI service for Dear Diary.

## Setup

Create and activate a virtual environment, then install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

> **Note**: Running `pip install -r requirements.txt` is mandatory before
> starting Uvicorn. Omitting it can lead to import errors such as
> `ModuleNotFoundError` if required packages are missing.

Run the development server from within this directory:

```bash
uvicorn app.main:app --reload
```
gunicorn --preload -w 4 -k uvicorn.workers.UvicornWorker app.main:app

## Configuration

Copy `.env.example` to `.env` and edit the values before running the server.
The repository includes `.env.example` with placeholders for all environment
variables (e.g. `DATABASE_URL`, `OPENROUTER_API_KEY`, `SPOTIFY_CLIENT_ID`, and
`SPOTIFY_CLIENT_SECRET`).

## Background tasks

Motivational quotes are generated automatically using Celery. Ensure Redis is running and start the worker and beat processes alongside Uvicorn:

```bash
celery -A app.celery_app.celery_app worker --loglevel=info
celery -A app.celery_app.celery_app beat --loglevel=info
```

The scheduled task `generate_quote_task` runs every 15 minutes and inserts a new quote based on recent journal moods.
