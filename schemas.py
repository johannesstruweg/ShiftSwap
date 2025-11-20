from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# --- API Input Models (Frontend -> Backend) ---

class SwapRequestCreate(BaseModel):
    requesting_user_id: int
    shift_id: int
    optional_message: Optional[str] = None

class SwapRequestResponse(BaseModel):
    message: str
    status: str
    top_match_name: Optional[str] = None
    ai_reasoning: Optional[str] = None

# --- AI Structured Output Models (Gemini -> Backend) ---
# We define exactly what we want Gemini to give us.

class RankedColleague(BaseModel):
    user_id: int = Field(..., description="The database ID of the colleague")
    name: str = Field(..., description="Name of the colleague")
    score: float = Field(..., description="A score between 0.0 and 1.0 indicating match quality")
    reason: str = Field(..., description="A brief, professional reason for this ranking based on fairness and fatigue.")

class RankingResponse(BaseModel):
    ranked_colleagues: List[RankedColleague]
