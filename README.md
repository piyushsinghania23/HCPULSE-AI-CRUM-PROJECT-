# HCPulse AI CRM - Task 1 (AI-First HCP Log Interaction Screen)

This repository contains a full-stack implementation of an **AI-first CRM HCP module** focused on the **Log Interaction Screen**, built for life science field representatives.

It supports two ways to capture HCP interactions:
- **Structured Form UI** (manual entry)
- **Conversational Chat UI** (LangGraph AI agent + tools)

## Tech Stack

- **Frontend:** React + Redux Toolkit + Vite
- **Backend:** Python + FastAPI
- **AI Agent Framework:** LangGraph
- **LLM:** Groq `llama-3.3-70b-versatile` (configurable via env)
- **Database:** PostgreSQL (SQLAlchemy ORM, with SQL schema included)
- **Font:** Google Inter (`@fontsource/inter`)

## Repository Structure

```text
.
â”œâ”€â”€ backend
â”‚   â”œâ”€â”€ app
â”‚   â”‚   â”œâ”€â”€ main.py
â”‚   â”‚   â”œâ”€â”€ config.py
â”‚   â”‚   â”œâ”€â”€ database.py
â”‚   â”‚   â”œâ”€â”€ models.py
â”‚   â”‚   â”œâ”€â”€ schemas.py
â”‚   â”‚   â”œâ”€â”€ crud.py
â”‚   â”‚   â”œâ”€â”€ llm.py
â”‚   â”‚   â”œâ”€â”€ langgraph_agent.py
â”‚   â”‚   â””â”€â”€ routers
â”‚   â”‚       â”œâ”€â”€ interactions.py
â”‚   â”‚       â””â”€â”€ agent.py
â”‚   â”œâ”€â”€ requirements.txt
â”‚   â”œâ”€â”€ .env.example
â”‚   â””â”€â”€ sql
â”‚       â””â”€â”€ schema.sql
â”œâ”€â”€ frontend
â”‚   â”œâ”€â”€ src
â”‚   â”‚   â”œâ”€â”€ components
â”‚   â”‚   â”‚   â”œâ”€â”€ LogInteractionForm.jsx
â”‚   â”‚   â”‚   â”œâ”€â”€ ChatInterface.jsx
â”‚   â”‚   â”‚   â””â”€â”€ InteractionList.jsx
â”‚   â”‚   â”œâ”€â”€ store
â”‚   â”‚   â”‚   â”œâ”€â”€ index.js
â”‚   â”‚   â”‚   â”œâ”€â”€ interactionsSlice.js
â”‚   â”‚   â”‚   â””â”€â”€ chatSlice.js
â”‚   â”‚   â”œâ”€â”€ api
â”‚   â”‚   â”‚   â””â”€â”€ client.js
â”‚   â”‚   â”œâ”€â”€ App.jsx
â”‚   â”‚   â”œâ”€â”€ main.jsx
â”‚   â”‚   â””â”€â”€ styles.css
â”‚   â”œâ”€â”€ package.json
â”‚   â””â”€â”€ .env.example
â””â”€â”€ README.md
```

## Task 1 Coverage

### 1. Log Interaction Screen

The UI provides:
- **Structured mode** for deterministic logging
- **Conversational mode** for AI-assisted logging and follow-up planning

In structured mode, users can create and edit interactions with fields such as:
- representative name
- HCP name and specialty
- interaction type and channel
- raw notes
- products discussed
- follow-up action/date

### 2. LangGraph Agent Role in HCP Interaction Management

The LangGraph agent acts as an **AI CRM copilot** that:
- understands free-text representative instructions
- decides when to call CRM tools
- uses LLM reasoning for summary, extraction, strategy, and drafting
- writes results back to the CRM interaction store
- supports record correction through edit tools

### 3. LangGraph Tools (Sales-Focused)

The agent includes at least five tools:

1. **Log Interaction** (`log_interaction`)
- Captures interaction data from conversational input.
- Uses LLM to generate:
  - concise summary
  - key entities (sentiment, objections, competitor mentions, product mentions, next steps)
- Persists output to SQL as a new interaction record.

2. **Edit Interaction** (`edit_interaction`)
- Updates an existing interaction by ID using a JSON patch payload.
- Supports updates to notes, follow-up fields, channel/type, and extracted entity metadata.

3. **Fetch HCP Timeline** (`fetch_hcp_timeline`)
- Retrieves recent interactions for an HCP.
- Helps representatives prep for next calls with historical context.

4. **Suggest Next Best Action** (`suggest_next_best_action`)
- Uses recent interaction summaries + current goal.
- Returns recommended action, rationale, risk, and measurable outcome.

5. **Draft Follow-up Message** (`draft_follow_up_message`)
- Produces a concise HCP follow-up email/message with objective and tone controls.

6. **Compliance Guard** (`run_compliance_guard`)
- Flags potential risk signals (e.g., unsupported claims/off-label tone).
- Returns risk level and remediation guidance.

## API Endpoints

### Health
- `GET /health`

### Structured Interaction APIs
- `GET /api/interactions` - list logged interactions
- `POST /api/interactions` - create interaction from structured form
- `PUT /api/interactions/{interaction_id}` - edit interaction

### Conversational Agent API
- `POST /api/agent/chat`
  - Sends user message + optional rep/HCP context
  - Returns AI response and lightweight execution trace

## Setup Instructions

## 1) Backend

```bash
cd backend
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env
```

Edit `backend/.env`:
- set `GROQ_API_KEY` with a new token
- keep `GROQ_MODEL=llama-3.3-70b-versatile`
- verify `DATABASE_URL`

Run API:

```bash
uvicorn app.main:app --reload --port 8000
```

## 2) Database

Use PostgreSQL and create database `hcpulse_crm`.

Optional manual schema:

```bash
psql -U postgres -d hcpulse_crm -f backend/sql/schema.sql
```

Note: FastAPI startup also auto-creates ORM tables.

## 3) Frontend

```bash
cd frontend
npm install
copy .env.example .env
npm run dev
```

Frontend runs at `http://localhost:5173` and calls backend at `http://localhost:8000`.

## How to Use

1. Open the app.
2. Use **Structured Form** tab to log/edit directly.
3. Use **Conversational Chat** tab to ask AI actions like:
   - "Log an in-person visit with Dr. Shah today. Notes: ..."
   - "Edit interaction 4 and update follow-up date to 2026-05-10."
   - "Suggest next best action for Dr. Shah to increase formulary adoption."

## Notes and Assumptions

- The provided assignment video URL requires Google Drive access permissions; implementation here follows the written requirements exactly.
- LangGraph and Groq model integration are implemented in backend code (`langgraph_agent.py`, `llm.py`).
- Repository is intentionally organized so frontend and backend are in one submission repo, per requirement.


