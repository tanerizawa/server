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

## Configuration

Copy `.env.example` to `.env` and edit the values before running the server.
The file lists all environment variables used by `app/core/config.py`.
