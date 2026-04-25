from langchain_groq import ChatGroq
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.outputs import ChatGeneration, ChatResult

from app.config import settings


class MockLLM(BaseChatModel):
    """Mock LLM for development when Groq API is not available."""
    
    @property
    def _llm_type(self) -> str:
        return "mock"
    
    def _generate(self, messages: list[BaseMessage], **kwargs) -> ChatResult:
        """Generate mock response."""
        mock_response = "This is a mock response from development mode. Please add a valid GROQ_API_KEY to .env to enable real AI responses."
        message = AIMessage(content=mock_response)
        generation = ChatGeneration(message=message)
        return ChatResult(generations=[generation])


def get_llm():
    api_key = settings.groq_api_key
    
    # Use mock LLM if key is missing or placeholder
    if not api_key or api_key.startswith("gsk_test") or api_key == "gsk_test_placeholder":
        print("Using Mock LLM - no valid Groq API key found")
        return MockLLM()
    
    # Use real Groq LLM with valid key
    return ChatGroq(
        api_key=api_key,
        model=settings.groq_model,
        temperature=0.2,
    )

