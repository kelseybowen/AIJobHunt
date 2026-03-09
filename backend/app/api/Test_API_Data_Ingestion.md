# Test API Data Ingestion

This guide explains how to **run Adzuna data ingestion locally**: taping  the Adzuna API, pull job data, and write results to a **CSV file** on your machine. No backend server or MongoDB is required. The CSV is written in the **same canonical job schema** that would be used when writing to MongoDB (e.g. `external_id`, `title`, `company`, `description`, `location`, `remote_type`, `skills_required`, `posted_date`, `source_url`, `source_platform`, `salary_range`), so you get MongoDB-ready data locally.

Prerequisites

- **Python** 3.9+ and a virtual environment
- **Environment file** `backend/.env` with Adzuna credentials (no MongoDB needed for local CSV runs):


| Variable         | Purpose                     |
| ---------------- | --------------------------- |
| `ADZUNA_APP_ID`  | Adzuna API Application ID.  |
| `ADZUNA_API_KEY` | Adzuna API Application Key. |


### Get Adzuna API credentials (App ID and App Key)

Adzuna uses an **App ID** and **App Key** (not a single token). Get them from Adzuna’s developer site:

1. **Register** at [https://developer.adzuna.com/signup](https://developer.adzuna.com/signup).
2. **Log in** at [https://developer.adzuna.com/login](https://developer.adzuna.com/login).
3. In your developer dashboard, copy your **Application ID** and **Application Key** (sometimes labeled `app_id` and `app_key`).
4. Create or edit `backend/.env` and add:

```
ADZUNA_APP_ID=your_application_id_here
ADZUNA_API_KEY=your_application_key_here
```

Replace the placeholders with the values from the Adzuna dashboard. Overview and docs: [https://developer.adzuna.com/overview](https://developer.adzuna.com/overview).

## Install dependencies

From the project root, activate the backend virtual environment and install dependencies:

```bash
cd backend
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
# source venv/bin/activate
pip install -r requirements.txt
cd ..
```

Or from the project root without activating: `pip install -r backend/requirements.txt`.

## Run the Adzuna top jobs script (API → CSV)

From the **project root** `AIJobHunt/`:

```bash
python -m backend.app.api.adzuna.test_adzuna_api_top_jobs
```

Or from the **backend** directory (with venv activated):

```bash
python app/api/adzuna/test_adzuna_api_top_jobs.py
```

**What the script does:**

- Calls the Adzuna API for each job title in the TOP_JOBS list.
- Pulls job data (no MongoDB involved).
- Writes results to a **CSV file** in `backend/app/api/adzuna/csv/` (e.g. `adzuna_top_jobs_YYYYMMDD_HH_MM_SS.csv`) in the **canonical job schema** (same structure as used when writing to MongoDB—just stored locally).
- Prints progress, statistics by job title, and a sample of the first 3 jobs to the console.

You do **not** need to start the backend server or have MongoDB configured for this local CSV run.

## Troubleshooting

- **"ADZUNA_APP_ID not set" / "ADZUNA_API_KEY not set"**...Ensure `backend/.env` exists and contains both variables (from [developer.adzuna.com](https://developer.adzuna.com)). No quotes around values unless the key contains spaces.
- **Import errors** ...Run from the project root: `python -m backend.app.api.adzuna.test_adzuna_api_top_jobs` so the `backend` package resolves correctly.

