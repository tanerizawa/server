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

### Database setup

Run Alembic migrations and seed the database with sample articles, audio tracks
and quotes:

```bash
alembic upgrade head
python app/db/seed.py
```

Run the development server from within this directory:

```bash
uvicorn app.main:app --reload

# For production
gunicorn --preload -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

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

## Deployment on Render

The `render.yaml` file provisions the services required to run the API on [Render](https://render.com/): a Postgres database, a Redis instance, the FastAPI web service and a Celery worker. Connect your GitHub repository on Render and it will automatically create these resources.

Secrets referenced in `render.yaml` should be stored in the environment group `dear-diary-secrets`. During each deploy Render executes `build.sh` which installs dependencies and applies Alembic migrations.
