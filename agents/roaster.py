import os
import json
from groq import Groq

def get_system_prompt(intensity='medium'):
    if intensity == 'gentle':
        tone = (
            "You are a caring friend giving someone a gentle reality check. "
            "Be soft, warm, and encouraging. Point out issues with kindness and light humor. "
            "End on a positive note like you believe in them."
        )
    elif intensity == 'savage':
        tone = (
            "You are absolutely ruthless with zero mercy. "
            "Destroy them using their own data as weapons. "
            "Use Gen Z language — bro, ngl, lowkey, actually, bffr. "
            "Every single line is a punchline. "
            "Last line is the most brutal thing you've ever said."
        )
    else:
        tone = (
            "You are a funny friend calling someone out. "
            "Witty, direct, casual. Make them laugh but feel called out. "
            "Use natural language like you're texting them."
        )

    return (
        f"{tone}\n\n"
        "Roast rules:\n"
        "- If lazy events outnumber productive events: roast their calendar hard. "
        "Mention specific lazy event names and times naturally. "
        "If something happened after 10pm call it out. If after 12am destroy them for it.\n"
        "- If productive events are equal or more: do NOT roast calendar. "
        "Say something like 'calendar looks solid this week' and move on.\n"
        "- Always roast emails if unread count is high.\n"
        "- Use exact event names from the data. Never say 'entertainment' or 'activities'.\n"
        "- Sound like a real person, not a corporate report.\n"
        "- No fixed format. No templates. React naturally to what you see.\n"
        "- 4-6 lines total. Last line hits hardest."
    )

def roast_user(data_json, intensity='medium', focus_metric=None):
    api_key = os.environ.get("GROQ_API_KEY")

    cal_data = data_json.get("calendar", {})
    lazy_events = cal_data.get("lazy_events", [])
    productive_events = cal_data.get("productive_events", [])
    lazy_count = cal_data.get("lazy_count", 0)
    productive_count = cal_data.get("productive_count", 0)
    unread = data_json.get("gmail", {}).get("total_unread", 0)
    old_unread = data_json.get("gmail", {}).get("older_than_3d_unreplied", 0)

    def get_fallback_roast():
        lazy_sample = lazy_events[0] if lazy_events else "your calendar"
        return (
            f"bro I just checked your week and {lazy_sample} was literally on your schedule.\n"
            f"meanwhile {unread} unread emails are just sitting there aging like fine wine.\n"
            f"ngl your whole week looks like an elaborate plan to avoid doing anything real."
        )

    if not api_key:
        return get_fallback_roast()

    try:
        client = Groq(api_key=api_key)
        prompt = (
            f"Here is the user's real data:\n\n"
            f"Lazy events this week: {lazy_events}\n"
            f"Productive events this week: {productive_events}\n"
            f"Lazy count: {lazy_count}, Productive count: {productive_count}\n"
            f"Unread emails: {unread}\n"
            f"Emails older than 3 days unreplied: {old_unread}\n\n"
            f"Intensity level: {intensity}\n\n"
            f"Now roast them."
        )
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": get_system_prompt(intensity)},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"Roaster error: {e}")
        return get_fallback_roast()