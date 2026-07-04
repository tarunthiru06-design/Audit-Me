import os
import json
from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from data_pipeline import fetch_data, get_auth_flow, save_credentials, get_credentials, TOKEN_FILE, fetch_gmail_unread_count_startup, get_last_week_summary, calculate_score, update_productivity_streak
from agents.roaster import roast_user
from agents.coach import coach_user

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "audit_me_super_secret_key_99")

# Allow OAuth over http for local development
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# In-memory session cache for fast re-roasting and deep dives
DATA_CACHE = {}


def identify_worst_metric(data):
    """Identifies the single worst habit metric for targeted deep roasts."""
    unread = data.get("gmail", {}).get("total_unread", 0)
    skipped = data.get("calendar", {}).get("events_skipped", 0)
    old_unread = data.get("gmail", {}).get("older_than_3d_unreplied", 0)
    
    if unread > 500:
        return f"{unread} unread emails clogging your inbox"
    elif skipped >= 3:
        return f"{skipped} calendar events skipped this week"
    elif old_unread > 50:
        return f"{old_unread} emails ghosted for over 3 days"
    else:
        return f"your habit of scheduling meetings and ignoring focus time"

@app.route('/')
def index():
    """Renders the dark themed frontend UI."""
    is_connected = os.path.exists(TOKEN_FILE) or (get_credentials() is not None)
    unread_count = None
    if is_connected:
        try:
            unread_count = fetch_gmail_unread_count_startup()
        except Exception as e:
            print(f"[APP] Error fetching unread count on index load: {e}")
            unread_count = 0
    return render_template('index.html', is_connected=is_connected, unread_count=unread_count)

@app.route('/connect')
def connect():
    """Initiates Google OAuth authentication."""
    try:
        redirect_uri = url_for('connect_callback', _external=True)
        flow = get_auth_flow(redirect_uri=redirect_uri)
        auth_url, state = flow.authorization_url(prompt='consent', access_type='offline', include_granted_scopes='true')
        session['oauth_state'] = state
        if hasattr(flow, 'code_verifier') and flow.code_verifier:
            session['code_verifier'] = flow.code_verifier
        return redirect(auth_url)
    except Exception as e:
        print(f"OAuth initiation error: {e}")
        return redirect(url_for('index', auth_error=str(e)))

@app.route('/connect_callback')
def connect_callback():
    """Handles Google OAuth callback and stores credentials."""
    try:
        state = session.get('oauth_state')
        code_verifier = session.get('code_verifier')
        redirect_uri = url_for('connect_callback', _external=True)
        flow = get_auth_flow(redirect_uri=redirect_uri)
        if code_verifier:
            flow.code_verifier = code_verifier
        
        flow.fetch_token(authorization_response=request.url)
        creds = flow.credentials
        save_credentials(creds)
        print("OAuth flow successful. Credentials saved.")
        return redirect(url_for('index', connected='true'))
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"OAuth callback error: {e}")
        return redirect(url_for('index', auth_error=str(e)))

@app.route('/status')
def status():
    """Returns connection status."""
    connected = os.path.exists(TOKEN_FILE) or (get_credentials() is not None)
    return jsonify({"connected": connected})

@app.route('/audit', methods=['GET', 'POST'])
def audit():
    """Orchestrates the 3 agents and score calculation."""
    try:
        intensity = request.args.get('intensity', request.json.get('intensity', 'medium') if request.is_json else 'medium')
        DATA_CACHE.clear()
        import time
        time.sleep(1.0)  # Brief sleep timer for calendar/data fetching visual window
        data = fetch_data()
        DATA_CACHE['latest'] = data
        
        score = calculate_score(data)
        streak_info = update_productivity_streak(score)
        roast = roast_user(data, intensity=intensity)
        # Check for calendar/productivity issues
        calendar_data = data.get("calendar", {})
        calendar_issues = (
            calendar_data.get("events_skipped", 0) > 0 or
            calendar_data.get("lazy_count", 0) > 0
        )

        # Check for email/communication velocity issues
        gmail_data = data.get("gmail", {})
        email_issues = (
            gmail_data.get("total_unread", 0) > 0 or
            gmail_data.get("older_than_3d_unreplied", 0) > 0
        )

        fixes = ""
        if calendar_issues:
            fixes += (
                '<div class="st-info-box">'
                '📅 <strong>Calendar & Focus Override</strong><br>'
                'Your data shows a buildup of stagnant or unproductive tasks dragging down your metrics. '
                'Don\'t just blindly complete them—clean up your schedule by deleting the low-value \'lazy\' items '
                'and blocking out a strict 45-minute focus window specifically for your high-priority objectives.'
                '</div>'
            )
        if email_issues:
            fixes += (
                '<div class="st-info-box">'
                '📧 <strong>Communication Velocity Correction</strong><br>'
                'Your communication velocity has dipped, meaning passive procrastination is catching up to you. '
                'Stop letting unread messages stack up; clear out the critical threads in one quick burst so you can get back to deep work.'
                '</div>'
            )
        if not calendar_issues and not email_issues:
            fixes = (
                '<div class="st-success-box">'
                '✅ <strong>All Systems Nominal</strong><br>'
                'No corrections are needed.'
                '</div>'
            )

        return jsonify({
            "success": True,
            "score": score,
            "current_streak": streak_info["current_streak"],
            "roast": roast,
            "fixes": fixes,
            "data": data,
            "last_week": get_last_week_summary()
        })
    except Exception as e:
        print(f"Error executing audit pipeline: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/score', methods=['GET'])
def score():
    """Returns productivity score and stats breakdown."""
    data = DATA_CACHE.get('latest') or fetch_data()
    DATA_CACHE['latest'] = data
    score_val = calculate_score(data)
    streak_info = update_productivity_streak(score_val)
    return jsonify({
        "success": True,
        "score": score_val,
        "current_streak": streak_info["current_streak"],
        "unread": data.get("gmail", {}).get("total_unread", 0),
        "events_this_week": data.get("calendar", {}).get("total_events_this_week", 0),
        "events_skipped": data.get("calendar", {}).get("events_skipped", 0),
        "completed_cleared_count": data.get("calendar", {}).get("completed_cleared_count", 0),
        "best_day": data.get("calendar", {}).get("best_day", "Wednesday"),
        "worst_day": data.get("calendar", {}).get("worst_day", "Friday"),
        "last_week": get_last_week_summary()
    })

@app.route('/again', methods=['POST'])
def again():
    """Generates a fresh roast from existing cached collector data."""
    try:
        req_json = request.get_json(silent=True) or {}
        intensity = req_json.get('intensity', 'medium')
        data = DATA_CACHE.get('latest') or fetch_data()
        DATA_CACHE['latest'] = data
        
        fresh_roast = roast_user(data, intensity=intensity)
        return jsonify({"success": True, "roast": fresh_roast})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/deeper', methods=['POST'])
def deeper():
    """Generates a hyper-focused roast on the worst metric."""
    try:
        data = DATA_CACHE.get('latest') or fetch_data()
        DATA_CACHE['latest'] = data
        worst_metric = identify_worst_metric(data)
        
        focused_roast = roast_user(data, intensity='savage', focus_metric=worst_metric)
        return jsonify({
            "success": True,
            "worst_metric": worst_metric,
            "roast": focused_roast
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    print("Starting Premium Audit Me Flask Server on http://localhost:5000")
    print("Running startup Gmail unread query...")
    fetch_gmail_unread_count_startup()
    app.run(host='0.0.0.0', port=5000, debug=True)
