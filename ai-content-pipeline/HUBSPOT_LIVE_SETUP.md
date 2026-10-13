# HubSpot Live Demo (safe, opt-in)

The AI Content Pipeline dashboard now contains a separate **HubSpot live connection** section. It is intentionally independent from the main pipeline, whose engagement numbers are simulated.

## Setup

1. Create a HubSpot test/developer account or use a portal where you have permission to create test contacts and lists.
2. Create a HubSpot private app and issue an access token with access to read/write contacts, contact properties/schema, and lists/segments. Actual scope names and subscription availability can vary: verify the current HubSpot UI documentation and grant the minimum scopes that work.
3. From `ai-content-pipeline/`, copy `.env.example` to `.env` and set `HUBSPOT_ACCESS_TOKEN=your-token`. **Do not commit `.env`, paste the token into HTML, or share it during screen share.**
4. Install requirements: `pip install -r requirements.txt`.
5. Start: `python dashboard/app.py`; open `http://127.0.0.1:5000`.
6. Click **Test HubSpot connection** first. It performs a read-only contact query and confirms token validity.
7. For the first write, enter only an email address **you own/control** and click **Sync test contact to HubSpot**. The app will create or update that contact with the `pmm_demo_persona` custom text property.
8. Optionally click **Create demo list in HubSpot** to create a dynamic segment filtered by that persona. List creation needs additional permissions and can create duplicates if repeated.

## Safety and accuracy

- The demo never sends real emails from the new live controls.
- The existing **Run pipeline** still performs mock/real operations according to `HUBSPOT_MODE`. **Keep `HUBSPOT_MODE=mock`** when using the dashboard; the old CRM implementation uses simulated email IDs and is not validated for safe live sending.
- All open/click/unsubscribe analytics currently come from a simulation, not HubSpot reporting.
- HubSpot errors (invalid token, missing permissions, missing plan features) are reported in the dashboard. The full live flow has NOT been tested against your own HubSpot account.
- Local dashboard runs on `127.0.0.1` with Flask debug disabled. Do not expose it publicly without authentication, CSRF protection, secure hosting, and a server-managed secrets system.
- Avoid importing the example contacts to a live portal. The live controls accept one explicitly entered test email at a time.
- For an interview, demo: connection check -> single test contact -> confirm CRM record in HubSpot -> optional persona list.

## Roadmap (not yet implemented)

Build a draft marketing email in HubSpot, opt-in test-send to a verified address using an appropriately licensed API, and import **real** campaign performance metrics separately from the simulation.
