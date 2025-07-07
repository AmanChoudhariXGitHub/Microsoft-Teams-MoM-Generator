from typing import TypedDict

class MeetingMinutesState(TypedDict):
    file_path: str
    transcript: str
    summary: str
    mom: str
    human_feedback: str
    review_approved: bool
