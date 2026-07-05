## Kaggle Capstone Project Submission: Audit-Me 
## 1. The Problem We Are Solving
Modern productivity tracking applications suffer from a critical architectural flaw: they are either visually unengaging logs that fail to drive real behavioral modification, or they introduce massive data liabilities. To provide personalized feedback, traditional tools scrape and store raw, unencrypted user text strings—such as descriptive calendar titles and private email contents. This creates a severe privacy vulnerability, forcing users to choose between workspace optimization and data sovereignty.

## 2. Our Solution
**Audit-Me** resolves this paradigm by engineering a local feedback workspace that balances engaging behavioral conditioning with security. The system splits responsibilities across two distinct components:
* **The Tactical Critic (Groq Engine):** Analyzes categorized activity telemetry and event summaries to deliver sharp, real-time accountability reviews ("roasts") to confront productivity leaks.
* **The Strategic Coach (Local Rule-Based & Gemini Foundation):** Although a Gemini-powered coaching agent is defined to process structured telemetry, the active Flask application serves targeted, rule-based productivity fixes directly from the server depending on whether calendar or email metrics fall below nominal thresholds.

## 3. System Architecture
The application runs entirely as a local production-ready web framework using **Flask**, initialized seamlessly via the terminal. The core architecture relies on two critical system layers to handle execution and privacy:
* **Client-Side Data Collector (`data_pipeline.py`):** Before data payloads hit downstream external APIs, calendar events are retrieved via Google Calendar API and locally categorized into "lazy" or "productive" lists using keyword matching (e.g., matching Netflix, Gaming, or Study). Email metrics are kept secure by querying only inbox count metadata via the Gmail API, ensuring raw email body text never leaves the local machine.
* **Dynamic UI View Toggling (`templates/index.html`):** The front-end layout integrates a native JavaScript action listener on the "Fix Me" trigger button. Clicking the button dynamically alters the DOM layout state—instantly hiding the critique container card (`display: none;`) so that the remediation panel expands to occupy the primary canvas completely to present targeted action items without distraction.

## 4. Our Project's Journey
The repository lifecycle was built from day one to be completely native to the **Antigravity Workspace Environment**. The structural layout—separating core routing logic, local data scrubbers, and responsive view layers—was iteratively optimized to ensure flawless sandboxed execution. By strictly avoiding hardcoded file paths or rigid host OS configurations, the codebase achieved total cross-platform environment portability, ensuring that any evaluator can clone, spin up, and verify the live interactive dashboard instantly without runtime drift or dependency fragmentation.
