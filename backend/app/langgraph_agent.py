import json
from datetime import date
from typing import Any

from langchain_core.tools import StructuredTool
from langgraph.prebuilt import create_react_agent
from sqlalchemy.orm import Session

from app import models
from app.llm import MockLLM, get_llm


SYSTEM_PROMPT = """
You are an AI-first CRM copilot for life science field representatives.
Primary goals:
1) Capture HCP interactions with high-quality summaries.
2) Keep records compliant and editable.
3) Recommend next best sales actions grounded in interaction history.
Always prefer using tools when the user asks to log, edit, review, or follow up on interactions.
""".strip()


def _safe_json_loads(payload: str) -> dict[str, Any]:
    try:
        return json.loads(payload)
    except Exception:
        return {}


def build_sales_tools(db: Session, llm) -> list[StructuredTool]:
    def log_interaction(
        representative_name: str,
        hcp_name: str,
        specialty: str,
        interaction_type: str,
        channel: str,
        interaction_date: str,
        notes_raw: str,
        products_discussed: str = "",
        follow_up_action: str = "",
        follow_up_date: str = "",
    ) -> str:
        """
        Log Interaction tool:
        Creates a CRM interaction record by summarizing notes and extracting entities.
        """
        summary_prompt = (
            "Summarize this field interaction in 4 bullet points with outcomes and objections:\n"
            f"{notes_raw}"
        )
        summary = llm.invoke(summary_prompt).content

        extraction_prompt = (
            "Extract JSON with keys: sentiment, objections, competitor_mentions, products, next_steps.\n"
            f"Notes: {notes_raw}\n"
            "Return JSON only."
        )
        entity_raw = llm.invoke(extraction_prompt).content
        key_entities = _safe_json_loads(entity_raw if isinstance(entity_raw, str) else "{}")

        model = models.Interaction(
            representative_name=representative_name,
            hcp_name=hcp_name,
            specialty=specialty,
            interaction_type=interaction_type,
            channel=channel,
            interaction_date=date.fromisoformat(interaction_date),
            notes_raw=notes_raw,
            notes_summary=summary if isinstance(summary, str) else str(summary),
            key_entities=json.dumps(key_entities),
            products_discussed=products_discussed,
            follow_up_action=follow_up_action,
            follow_up_date=date.fromisoformat(follow_up_date) if follow_up_date else None,
        )
        db.add(model)
        db.commit()
        db.refresh(model)
        return f"Interaction logged successfully with id={model.id} for HCP {hcp_name}."

    def edit_interaction(interaction_id: int, updates_json: str) -> str:
        """
        Edit Interaction tool:
        Modifies an existing interaction using a JSON patch-style payload.
        Example updates_json: {"notes_raw":"...", "follow_up_action":"...", "channel":"Virtual"}
        """
        item = db.query(models.Interaction).filter(models.Interaction.id == interaction_id).first()
        if not item:
            return f"Interaction {interaction_id} not found."

        updates = _safe_json_loads(updates_json)
        if not updates:
            return "No valid updates were provided."

        for key, value in updates.items():
            if key == "key_entities" and isinstance(value, dict):
                value = json.dumps(value)
            if hasattr(item, key):
                setattr(item, key, value)

        db.commit()
        db.refresh(item)
        return f"Interaction {interaction_id} updated successfully."

    def fetch_hcp_timeline(hcp_name: str, limit: int = 5) -> str:
        """Fetch recent interactions for an HCP to support call planning."""
        rows = (
            db.query(models.Interaction)
            .filter(models.Interaction.hcp_name.ilike(hcp_name))
            .order_by(models.Interaction.interaction_date.desc())
            .limit(limit)
            .all()
        )
        if not rows:
            return f"No interactions found for {hcp_name}."

        timeline = []
        for row in rows:
            timeline.append(
                f"{row.interaction_date} | {row.channel} | {row.interaction_type} | {row.notes_summary[:180]}"
            )
        return "\n".join(timeline)

    def suggest_next_best_action(hcp_name: str, business_goal: str) -> str:
        """Generate a next-best-action recommendation using recent HCP history."""
        rows = (
            db.query(models.Interaction)
            .filter(models.Interaction.hcp_name.ilike(hcp_name))
            .order_by(models.Interaction.interaction_date.desc())
            .limit(6)
            .all()
        )
        context = "\n".join([f"- {r.notes_summary}" for r in rows]) or "No historical context."
        prompt = (
            "You are a life science sales strategist.\n"
            f"HCP: {hcp_name}\nGoal: {business_goal}\n"
            f"History:\n{context}\n"
            "Return:\n1) next action\n2) rationale\n3) risk to monitor\n4) measurable outcome."
        )
        return str(llm.invoke(prompt).content)

    def draft_follow_up_message(hcp_name: str, objective: str, tone: str = "professional") -> str:
        """Draft a compliant post-visit follow-up message for the representative."""
        prompt = (
            "Draft a concise follow-up email to an HCP.\n"
            f"HCP: {hcp_name}\nObjective: {objective}\nTone: {tone}\n"
            "Include: appreciation, medical value point, and clear next step."
        )
        return str(llm.invoke(prompt).content)

    def run_compliance_guard(notes_text: str) -> str:
        """Scan notes for potential compliance risks (off-label or unsupported claims)."""
        prompt = (
            "Classify compliance risk in this interaction note.\n"
            "Return JSON keys: risk_level, risk_flags, remediation.\n"
            f"Notes:\n{notes_text}"
        )
        result = llm.invoke(prompt).content
        return str(result)

    return [
        StructuredTool.from_function(log_interaction),
        StructuredTool.from_function(edit_interaction),
        StructuredTool.from_function(fetch_hcp_timeline),
        StructuredTool.from_function(suggest_next_best_action),
        StructuredTool.from_function(draft_follow_up_message),
        StructuredTool.from_function(run_compliance_guard),
    ]


class HCPInteractionAgent:
    def __init__(self, db: Session):
        llm = get_llm()
        if isinstance(llm, MockLLM):
            self.graph = None
            self.mock_response = (
                "Mock mode is active because GROQ_API_KEY is missing or invalid. "
                "Set a valid key in backend/.env to enable full tool-calling chat."
            )
            return

        tools = build_sales_tools(db, llm)
        self.graph = create_react_agent(llm, tools, prompt=SYSTEM_PROMPT)

    def chat(self, message: str) -> dict[str, Any]:
        if self.graph is None:
            return {"response": self.mock_response, "trace": [f"user: {message[:120]}", "assistant: mock response"]}

        try:
            result = self.graph.invoke({"messages": [("user", message)]})
            messages = result.get("messages", [])
            trace = [f"{m.type}: {str(m.content)[:120]}" for m in messages]
            response = str(messages[-1].content) if messages else "No response generated."
            return {"response": response, "trace": trace}
        except Exception as exc:
            fallback = (
                "Copilot could not reach the LLM provider. "
                "Check GROQ_API_KEY, model availability, and outbound network access, then restart backend."
            )
            return {
                "response": fallback,
                "trace": [f"user: {message[:120]}", f"error: {type(exc).__name__}"],
            }
