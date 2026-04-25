from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.langgraph_agent import HCPInteractionAgent
from app.schemas import AgentChatRequest, AgentChatResponse

router = APIRouter(prefix="/api/agent", tags=["agent"])


@router.post("/chat", response_model=AgentChatResponse)
def chat_with_agent(payload: AgentChatRequest, db: Session = Depends(get_db)):
    context = []
    if payload.representative_name:
        context.append(f"Representative: {payload.representative_name}")
    if payload.hcp_name:
        context.append(f"HCP: {payload.hcp_name}")

    final_message = payload.message
    if context:
        final_message = f"{' | '.join(context)}\nUser request: {payload.message}"

    agent = HCPInteractionAgent(db)
    result = agent.chat(final_message)
    return AgentChatResponse(response=result["response"], trace=result["trace"])

