# HCPulse AI CRM

AI-first CRM module for life science field representatives, focused on the **HCP Log Interaction Screen**.

The app supports two interaction capture modes:
- **Structured Form UI** for manual, deterministic logging
- **Conversational Chat UI** powered by a LangGraph agent and sales-focused tools

## What This Project Includes

- Full-stack implementation (`frontend` + `backend`)
- Interaction create/list/update APIs
- LangGraph AI copilot for logging, editing, and follow-up support
- SQLAlchemy ORM models and SQL schema

## Tech Stack

- **Frontend:** React, Redux Toolkit, Vite
- **Backend:** FastAPI, SQLAlchemy
- **AI Agent Framework:** LangGraph
- **LLM Provider:** Groq (`llama-3.3-70b-versatile`)
- **Database:** PostgreSQL (or SQLite for local fallback)

## Repository Structure

```text
.
|-- backend
|   |-- app
|   |   |-- main.py
|   |   |-- config.py
|   |   |-- database.py
|   |   |-- models.py
|   |   |-- schemas.py
|   |   |-- crud.py
|   |   |-- llm.py
|   |   |-- langgraph_agent.py
|   |   `-- routers
|   |       |-- interactions.py
|   |       `-- agent.py
|   |-- requirements.txt
|   |-- .env.example
|   `-- sql
|       `-- schema.sql
|-- frontend
|   |-- src
|   |   |-- components
|   |   |   |-- LogInteractionForm.jsx
|   |   |   |-- ChatInterface.jsx
|   |   |   `-- InteractionList.jsx
|   |   |-- store
|   |   |   |-- index.js
|   |   |   |-- interactionsSlice.js
|   |   |   `-- chatSlice.js
|   |   |-- api
|   |   |   `-- client.js
|   |   |-- App.jsx
|   |   |-- main.jsx
|   |   `-- styles.css
|   |-- package.json
|   `-- .env.example
`-- README.md
```

## Quick Start

### 1) Backend

```bash
cd backend
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
# source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env
```

Update `backend/.env`:
- `GROQ_API_KEY=<your_new_key>`
- `GROQ_MODEL=llama-3.3-70b-versatile`
- `DATABASE_URL=<your_db_url>`

Run backend:

```bash
uvicorn app.main:app --reload --port 8000
```

### 2) Database

Default expectation is PostgreSQL database `hcpulse_crm`.

Optional schema bootstrap:

```bash
psql -U postgres -d hcpulse_crm -f backend/sql/schema.sql
```

Note: ORM tables are also created on FastAPI startup.

### 3) Frontend

```bash
cd frontend
npm install
copy .env.example .env
npm run dev
```

Frontend URL: `http://localhost:5173`  
Backend URL: `http://localhost:8000`

## API Endpoints

- `GET /health`
- `GET /api/interactions`
- `POST /api/interactions`
- `PUT /api/interactions/{interaction_id}`
- `POST /api/agent/chat`

## LangGraph Agent Responsibilities

The agent acts as an AI CRM copilot to:
- parse free-text field input
- decide when to call tools
- summarize and extract key entities
- recommend next-best actions
- draft follow-up content
- support interaction edits and compliance checks

### Implemented Tools

1. `log_interaction`
2. `edit_interaction`
3. `fetch_hcp_timeline`
4. `suggest_next_best_action`
5. `draft_follow_up_message`
6. `run_compliance_guard`

## Typical Usage

1. Open the app.
2. Use **Structured Form** for direct logging/editing.
3. Use **Conversational Chat** for AI-assisted operations.

Example prompts:
- "Log an in-person visit with Dr. Shah. Notes: ..."
- "Edit interaction 4 and change follow-up date to 2026-05-10."
- "Suggest next best action for Dr. Shah to improve formulary adoption."

## Notes

- This implementation follows the written assignment requirements.
- LangGraph and Groq integration are implemented in backend modules:
  - `backend/app/langgraph_agent.py`
  - `backend/app/llm.py`
