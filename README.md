# Procrastination Overhaul: Metadata-Driven Analytics & Remediation Engine

### A Privacy-First Analytical Workspace Balancing Automated Behavioral Critiques with Decoupled Action Blueprints

---

## 🎯 Problem & Solution

* **Problem**: Modern professionals face chronic digital distractions, fragmented schedules, and overwhelmed email inboxes, leading to decreased productivity and slower communication velocity. Existing analytics and coaching tools often require invasive access to read the raw body text of personal emails and private calendar event descriptions, compromising user privacy.
* **Solution**: **Audit Me** solves this by implementing a local, privacy-first analytical engine that processes only numerical metadata (such as timestamps, queue counts, and scheduling intervals) client-side. It decouples data gathering from AI analysis through modular pipelines (Schedule Architecture and Inbox Backlog Density), feeding aggregated insights to LLM-powered agents (Roaster & Coach) to provide direct, humorous feedback and actionable "Fix Me" remediation widgets without exposing sensitive communication payloads.

---

## 🛠️ Project Structure / Blueprint

The engine is built as a modular workspace structured as follows:

```text
├── agents/
│   ├── coach.py           # Gemini-powered productivity coaching logic
│   └── roaster.py         # Groq-powered multi-intensity roasting logic
├── app.py                 # Core Flask application entry point and user interface
├── data_pipeline.py       # Data pipelines, Google API fetcher, scoring, & streak calculations
├── requirements.txt       # Python dependencies (including flask, groq, google-generativeai)
├── README.md              # Project documentation
├── .env.example           # Example environment template
└── .gitignore             # Git exclusion rules
```

---

## 📊 System Architecture & Data Flow

<div align="center">
  <img src="Gemini_Generated_Image_kbwschkbwschkbws.png" alt="System Architecture" width="85%">
</div>

### Architectural Mechanics
The system architecture implements a strict unidirectional data flow designed to decouple data ingestion from machine learning logic:
1. **The Ingestion Interface:** The workspace initializes secure OAuth pipelines connecting directly to Google Calendar and Gmail endpoints.
2. **The Privacy Filter (data_pipeline.py):** Raw text payloads are stripped client-side, and only localized numerical metadata is processed to ensure total confidentiality.
3. **Decoupled Agent Orchestration (agents/):** The processed numeric state is dispatched to our decoupled LLM agents (Groq for the roaster engine and Gemini for the coach engine).
4. **Unified State Rendering (app.py):** The individual agent outputs are compiled and pushed straight to the Flask presentation layer.

---


## 🎓 Key Course Concepts

### Agent Skills & Pipeline Decoupling
To enforce a strict separation of concerns, the application decouples data gathering from AI reasoning agents. Data collection is broken down into two distinct, independent pipelines:
- **Schedule Architecture Pipeline**: Evaluates user schedules, logs lazy vs. productive time allocations, and processes skipped calendar events. Progress is communicated in the UI using the loading string `"Evaluating calendar architecture..."`.
- **Inbox Backlog Density Pipeline**: Resolves unread thread counts and measures response latency. Progress is communicated in the UI using the loading string `"Evaluating inbox backlog density..."`.

Once these pipelines run, their output is aggregated into a standardized context state before being dispatched to the downstream AI Roaster and Coach agents.

### Privacy-First Security Framework
Privacy is embedded directly into the data acquisition layer. Instead of scanning raw text payloads, email bodies, or specific event details, the engine pre-processes and quantifies localized numerical metadata (timestamps and queue integers) entirely on the client side. No text content from personal emails or description payloads is sent to external API endpoints, ensuring user communication remains completely confidential.

### Workspace Engineering
The repository and local workflows have been structured and optimized for rapid development, testing, and execution inside the **Antigravity** development environment.

---

## 🎨 UI Features

### Segmented "Fix Me" Alert Panels
When users request diagnostics and remediation advice, the "Fix Me" engine displays isolated, clean alert cards targeted to specific productivity leaks:
- **Calendar & Focus Override Box**: Appears when the Schedule Architecture Pipeline detects skipped calendar events or an imbalance of lazy tasks. It suggests clearing low-value entries and dedicating specific focus blocks.
- **Communication Velocity Correction Box**: Appears when the Inbox Backlog Density Pipeline detects unread backlogs. It advises clearing out unread threads in dedicated bursts to recover response velocity.

---

## 🚀 Local Environment Setup

Follow these steps to run the engine locally on your system.

### Prerequisites
- **Python 3.9** or higher installed.
- A Google Cloud Platform (GCP) Project to configure Google Calendar & Gmail OAuth credentials.
- API keys for **Groq** and **Google Gemini** (optional; mock data profiles are used as fallbacks if missing).

---

### Step 1: Clone the Repository
Clone the repository to your local system and navigate to the project directory:
```bash
git clone https://github.com/tarunthiru06-design/Audit-Me.git
cd "Audit-Me"
```

### Step 2: Install Python Dependencies
Install the required packages (including Flask, Google APIs, and AI integrations) using `pip`:
```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables
1. Copy the example environment file to create a `.env` file:
   ```bash
   copy .env.example .env
   ```
2. Open `.env` and fill in your API credentials:
   - **`GEMINI_API_KEY`**: Your Google Gemini API key.
   - **`GROQ_API_KEY`**: Your Groq API key.
 

### Step 4: Configure Google OAuth Credentials
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project and enable the **Google Calendar API** and the **Gmail API** under the Library.
3. Configure the **OAuth Consent Screen** (User Type: External) and add your email as a **Test User**.
4. Request/add the following scopes:
   - `https://www.googleapis.com/auth/calendar.readonly`
   - `https://www.googleapis.com/auth/gmail.readonly`
5. Under **Credentials**, click **Create Credentials** > **OAuth client ID** and select **Desktop app**.
6. Download the generated client secrets JSON file, rename it to exactly `credentials.json`, and place it in the project root.

### Step 5: Start the App
Launch the Flask interface:
```bash
python app.py
```

### Step 6: Access the Application
Open your web browser and navigate to the URL printed in the terminal (typically **`http://127.0.0.1:5000`**). Connect your Google Account or explore the dashboard with the localized mock profiles.
