import os
import json
import google.generativeai as genai

SYSTEM_PROMPT = (
    "You are a no-nonsense productivity coach. Based on the user's data, write a single, cohesive paragraph "
    "giving them direct, actionable advice on how to improve their metrics. Do not use lists, bullet points, "
    "or checkboxes. Keep it to a single, continuous paragraph (under 4 sentences)."
)

def coach_user(data_json):
    """
    Takes structured JSON data from collector, calls Gemini API (gemini-1.5-flash),
    and returns a single, cohesive paragraph of actionable advice.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    
    unread = data_json.get("gmail", {}).get("total_unread", 2230)
    old_unread = data_json.get("gmail", {}).get("older_than_3d_unreplied", 156)
    skipped = data_json.get("calendar", {}).get("events_skipped", 5)

    if not api_key or api_key == "your_gemini_api_key_here":
        return (
            "Your current calendar events show some leftover uncompleted tasks that need to be cleared or rescheduled right away. "
            "To bring your metrics back up, try dedicating your next short focus block to clearing urgent replies. "
            "Keep your daily habit streak burning by ensuring your data is logged before the day ends."
        )

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=SYSTEM_PROMPT
        )
        
        prompt = f"Here is the user's actual calendar and Gmail data in JSON format:\n\n{json.dumps(data_json, indent=2)}"
        response = model.generate_content(prompt)
        
        if response and response.text:
            return response.text.strip()
        else:
            return (
                "Your current calendar events show some leftover uncompleted tasks that need to be cleared or rescheduled right away. "
                "To bring your metrics back up, try dedicating your next short focus block to clearing urgent replies. "
                "Keep your daily habit streak burning by ensuring your data is logged before the day ends."
            )
    except Exception as e:
        print(f"Error calling Gemini API in coach: {e}")
        return (
            "Your current calendar events show some leftover uncompleted tasks that need to be cleared or rescheduled right away. "
            "To bring your metrics back up, try dedicating your next short focus block to clearing urgent replies. "
            "Keep your daily habit streak burning by ensuring your data is logged before the day ends."
        )
