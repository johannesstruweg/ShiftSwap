from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime

# Import local modules
from database import engine, Base, get_db
from models import User, Shift, SwapRequest
from schemas import SwapRequestCreate, SwapRequestResponse
from ai_service import get_ai_rankings

# Create database tables automatically
Base.metadata.create_all(bind=engine)

app = FastAPI(title="ShiftSwap AI Backend")

# --- CORS SETTINGS (NEW) ---
# Allows the frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "online", "service": "ShiftSwap AI API"}

@app.post("/api/v1/swaps/request", response_model=SwapRequestResponse)
def request_swap(request: SwapRequestCreate, db: Session = Depends(get_db)):
    """
    Core logic:
    1. Validate Shift
    2. Filter Eligible Colleagues (Role match, Not self)
    3. Use Gemini AI to Rank them
    4. Create Request & Notify (Simulated)
    """
    
    # 1. Fetch the shift
    shift = db.query(Shift).filter(Shift.id == request.shift_id).first()
    if not shift:
        raise HTTPException(status_code=404, detail="Shift not found")
    
    # 2. Eligibility Engine (Simple: Same Role, not the requestor)
    candidates = db.query(User).filter(
        User.role == shift.role,
        User.id != request.requesting_user_id
    ).all()
    
    if not candidates:
        return SwapRequestResponse(
            message="No eligible colleagues found.",
            status="FAILED"
        )

    # 3. Prepare Data for AI
    shift_data = {
        "role": shift.role,
        "start": str(shift.start_time),
        "end": str(shift.end_time)
    }
    
    candidate_list = [
        {"id": c.id, "name": c.name, "hours_last_7d": c.hours_worked_last_7d}
        for c in candidates
    ]

    print(f"Sending {len(candidate_list)} candidates to Gemini for ranking...")

    # 4. AI Ranking
    ai_result = get_ai_rankings(shift_data, candidate_list)
    
    top_match = None
    ai_reason = "AI Service unavailable"
    
    if ai_result.ranked_colleagues:
        top_match = ai_result.ranked_colleagues[0]
        ai_reason = top_match.reason
        print(f"AI Selected Top Match: {top_match.name} (Score: {top_match.score})")
    
    # 5. Persist Request
    new_request = SwapRequest(
        requesting_user_id=request.requesting_user_id,
        shift_id=request.shift_id,
        status="PENDING",
        ai_ranking_metadata=ai_result.model_dump_json() if ai_result else "{}"
    )
    db.add(new_request)
    db.commit()

    # 6. Response
    return SwapRequestResponse(
        message="Swap requested successfully.",
        status="PENDING",
        top_match_name=top_match.name if top_match else "None",
        ai_reasoning=ai_reason
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
