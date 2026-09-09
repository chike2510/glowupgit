# glowupgit

**Repo → landing page agent.** glowupgit takes a public GitHub repository URL and produces a live product landing page concept plus a rewritten README.

## Functional scope

The MVP intentionally has exactly three capabilities:

1. `fetch_repo(url)` pulls the README, package manifest, and top-level file structure through the GitHub API.
2. `generate_copy()` turns that context into a value proposition, install steps, and why-star-this pitch.
3. `rewrite_readme()` formats the same output as an improved README.

The frontend shows the agent's work as explicit processing steps before displaying the generated landing page and README side by side.

## Local setup

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp ../.env.example .env
uvicorn api.routes:app --reload --port 8000
```

The backend accepts `POST /api/glowup` with `{ "url": "https://github.com/owner/repo" }`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Set `VITE_API_BASE_URL=http://localhost:8000` in `frontend/.env.local` if the backend is not proxied.

## Vercel deploy

The included `frontend/vercel.json` serves the Vite build as a static frontend. For the backend, deploy the `backend` directory as a small Python service (or place it behind the same domain with a reverse proxy) and set `VITE_API_BASE_URL` in Vercel to its public URL.

```bash
cd frontend
npm run build
vercel --prod
```

## Project structure

See [ARCHITECTURE.md](./ARCHITECTURE.md) for the system diagram and module boundaries.
