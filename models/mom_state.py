from typing import TypedDict, Optional

class MeetingMinutesState(TypedDict, total=False):
    file_path: str
    transcript: str
    summary: str
    mom: str
    summary_table: str
    speaker_analysis: str
    action_items: str
    human_feedback: str
    review_approved: bool
    model_used: str        # "ollama", "openai", or "groq"
    api_key: Optional[str] # API key if needed for LLM
