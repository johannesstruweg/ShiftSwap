# ShiftSwap (AI Assist Backend)

This is the MVP Backend for ShiftSwap. It uses FastAPI, SQLite, and Google Gemini 2.5 Flash to rank shift swap candidates.

## Setup

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Environment Variables:**
    Create a `.env` file in this folder and add your API key:
    ```env
    GEMINI_API_KEY=your_actual_api_key_here
    ```

3.  **Seed the Database:**
    Run this script to create dummy users and a shift to swap.
    ```bash
    python seed.py
    ```

4.  **Run the Server:**
    ```bash
    python main.py
    ```

## Testing the AI

Once the server is running (http://localhost:8000), you can test the `request_swap` endpoint.

**Use Curl:**
```bash
curl -X POST http://localhost:8000/api/v1/swaps/request -H "Content-Type: application/json" -d '{
    "requesting_user_id": 1,
    "shift_id": 1,
    "optional_message": "I have a dentist appointment."
}'
```
