CRM Demo — Deploy to Render (Docker)

This README explains how to build the `backend` FastAPI app into Docker and deploy it on Render (recommended for a stable public demo URL).

Prerequisites
- Docker installed (for local build/test)
- Git and a GitHub account
- A Render account (https://render.com)

Quick local checks
1. From repo root, build and run Docker image to verify the app:

```bash
# Build using backend directory as context
docker build -t crm-demo:local backend
# Run container and map port 8000
docker run --rm -p 8000:8000 crm-demo:local
```

Open http://localhost:8000 to verify the app serves the front-end and APIs.

Note: If you use SQLite locally, it will run inside the container. For production / stable demo use PostgreSQL.

Push to GitHub

1. Create a new GitHub repository and push the project:

```bash
git init
git add .
git commit -m "Add CRM demo"
git branch -M main
git remote add origin https://github.com/<your-user>/<your-repo>.git
git push -u origin main
```

Deploy on Render (Docker)

1. Log in to https://render.com and click "New" → "Web Service".
2. Connect your GitHub account and select the repository you pushed.
3. For Service type choose "Web Service".
4. Under "Environment" choose "Docker". Set the Dockerfile path to `backend/Dockerfile` (or leave default if `Dockerfile` is in repo root).
5. Set the port to `8000` (Render will detect or allow you to set this).
6. Add environment variables (in Render dashboard → Environment):
   - `DATABASE_URL` — e.g. `postgres://user:pass@host:port/dbname` (see below how to create a managed Postgres on Render)
   - Any other secret keys your app depends on (JWT secrets, OpenAI key etc.)
7. Click "Create Web Service". Render will build the Docker image and produce a public HTTPS URL once finished.

Persistent database recommendation
- For a durable demo you should create a managed PostgreSQL instance on Render and set `DATABASE_URL` accordingly.
- In Render UI: New → Databases → PostgreSQL → Create. Then copy the `DATABASE_URL` from the database instance and paste into the Web Service env var.

Seeding demo data
- If you have a seed script (e.g. `backend/seed_demo_data.py`) you can run it with the deployed database connection:

Option A — Run locally against the managed Postgres
```bash
# set DATABASE_URL in your shell (use the value from Render DB)
export DATABASE_URL="postgres://user:pass@host:port/dbname"
# install dependencies locally in a venv and run the seed
pip install -r backend/requirements.txt
python backend/seed_demo_data.py
```

Option B — Run inside the Render instance (less common)
- You can run a one-off job or connect via psql to the managed DB and run SQL scripts. Render docs show how to connect to the Postgres instance.

Important notes
- Do NOT use SQLite on Render for production/demo where you expect persistence: container filesystems are ephemeral and will be discarded on redeploy.
- Remove or anonymize any sensitive credentials or production data from the repository before pushing.
- If your app uses external services (OpenAI, Redis), set those credentials as environment variables in Render.

Optional next steps I can do for you
- Create a `render.yaml` (IaC) to configure the Web Service + Postgres as code. (I can add this file and explain usage.)
- Add a small GitHub Actions workflow to run tests and push (optionally trigger Render deploy).
- Automate running the seed script after the DB is provisioned (e.g. Render "cron job" or a one-off deploy hook).

If you want, I can now:
- Create `render.yaml` for infra-as-code (recommended), or
- Create a minimal GitHub Actions workflow to auto-deploy on push, or
- Walk you through pushing the repo and creating the Render Web Service step-by-step.

Which should I do next?