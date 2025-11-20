import os
import json
from google import genai
from schemas import RankingResponse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Gemini Client
# Ensure GEMINI_API_KEY is set in your .env file
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("WARNING: GEMINI_API_KEY not found in environment variables.")

client = genai.Client(api_key=api_key) if api_key else None

def get_ai_rankings(shift_details: dict, candidates: list[dict]) -> RankingResponse:
    """
    Calls Gemini 2.5 Flash to rank candidates for a shift swap.
    """
    if not client:
        print("AI Service unavailable: No API Key.")
        return RankingResponse(ranked_colleagues=[])

    # 1. Context Construction
    # We convert the list of dicts to a string for the prompt
    candidates_str = json.dumps(candidates, indent=2)
    
    prompt = f"""
    You are the ShiftSwap AI Assist. Your goal is to optimize schedule stability and fairness.
    
    TASK: Rank the eligible candidates for a shift swap.
    
    SHIFT TO BE COVERED:
    Role: {shift_details['role']}
    Time: {shift_details['start']} to {shift_details['end']}
    
    ELIGIBLE CANDIDATES:
    {candidates_str}
    
    RANKING RULES:
    1. FATIGUE CHECK: Prioritize candidates with FEWER hours worked in the last 7 days.
    2. AVAILABILITY: If 'hours' are 0, they are likely very fresh.
    3. REASONING: Provide a short, punchy reason for the top choice (e.g., "Freshest employee, low weekly hours").
    
    OUTPUT:
    Return ONLY the JSON object matching the schema.
    """

    try:
        # 2. Call Gemini with Structured Output
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": RankingResponse,
            },
        )
        
        # 3. Return parsed Pydantic object
        # The SDK automatically validates the JSON against our schema
        return response.parsed

    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        # Return empty list on failure so the app doesn't crash
        return RankingResponse(ranked_colleagues=[])
