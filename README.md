# NYC Taxi Data Pipeline (Still in development)

A small PostgreSQL loading pipeline for NYC taxi trip parquet files, with a local Airflow environment.
Airflow is still in development...
## Prerequisites

- Python 3.10+
- Docker Desktop

## Set up PostgreSQL in Docker Desktop

If you do not already have a PostgreSQL container, run this command in PowerShell or the Docker Desktop terminal:

```powershell
docker run --name nyc-taxi-postgres `
	-e POSTGRES_USER=postgres `
	-e POSTGRES_PASSWORD=change-me `
	-e POSTGRES_DB=nyc_taxi `
	-p 5431:5432 `
	-d postgres:16
```

This creates a PostgreSQL container with the database and port expected by this project. In Docker Desktop, the container should appear as `nyc-taxi-postgres`. If it already exists but is stopped, start it with:

```powershell
docker start nyc-taxi-postgres
```

Verify that it is running:

```powershell
docker ps
```

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` with the PostgreSQL connection values. The Docker command above matches the values in `.env.example`. Put input parquet files in `data/`; they are intentionally ignored by Git because they can be large.

## Create the schema

```powershell
python db_connection.py
```

## Load a parquet batch

The loader asks for the parquet filename without the `.parquet` extension:

```powershell
python extract_and_load.py
```

For example, enter `yellow_tripdata_2026-01` when `data/yellow_tripdata_2026-01.parquet` exists.

## Airflow

The Compose file is the standard local Airflow development setup. From the `airflow` directory:

```powershell
docker compose up airflow-init
docker compose up -d
```

Open `http://localhost:8080` and sign in with the default local credentials `airflow` / `airflow` unless you override them in the Airflow environment.

## Repository policy

Secrets, virtual environments, Airflow logs, generated scheduler state, and parquet datasets are excluded from version control. Use `.env.example` as the shareable configuration template.
