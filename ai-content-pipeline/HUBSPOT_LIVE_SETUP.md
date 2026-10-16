# HubSpot Live Reporting — Interview Setup

## What is real, and what is simulated?

| Screen | Data source | Writes to HubSpot? |
| --- | --- | --- |
| `/prototype` | Prepared Zip / Shopify / Datadog examples | No |
| `/` (Run pipeline) | Generated content + simulated delivery and engagement | No, when `HUBSPOT_MODE=mock` |
| `/performance` | **Live HubSpot Marketing Email Statistics API** | **No (GET only)** |
| `/` (Sync test contact / Create segment) | Your own HubSpot account | **Yes, only when explicitly clicked** |

The live performance dashboard is **not** a mock report. If your account has no sent marketing emails or the token lacks permissions, it displays an empty or error state. It never substitutes illustrative results.

## Quick setup (Mac)

1. In a HubSpot portal you own or have permission to test, create a **private app**. For the email reporting API, check the current requirement for the **`content`** scope and access to marketing email reporting. For the separate CRM connection-test control, also add contacts-read permissions if desired. CRM property/list creation needs additional write scopes.
2. Copy the private app access token. Keep it **only on your machine**.
3. In a terminal:

   ```bash
   git clone https://github.com/liwelaine/ai-pmm-workflows.git
   cd ai-pmm-workflows/ai-content-pipeline
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   cp .env.example .env
   ```

4. Open `.env` in a local editor. Add:

   ```dotenv
   HUBSPOT_ACCESS_TOKEN=YOUR_PRIVATE_APP_TOKEN
   HUBSPOT_MODE=mock
   ```

   **Keep `HUBSPOT_MODE=mock`** so the old pipeline never attempts CRM live sends. The new read-only performance view uses the token regardless of this switch.

5. Run:

   ```bash
   python dashboard/app.py
   ```

6. Open **http://127.0.0.1:5000/performance** for real HubSpot email metrics. You can switch between last 30, 90, and 180 days. Open **http://127.0.0.1:5000/prototype** to show the example PMM workflow.

## What the live dashboard measures

- HubSpot-reported marketing email delivery, open and click rates;
- aggregated counts and time-bucketed engagement;
- a limited sample of recent email names/subjects and their stats.

These numbers are queried from HubSpot when you open or refresh the page. They are not local campaign simulation and are not cached. The screen is read-only. Missing metrics display as a dash.

**Limitations:** HubSpot portal entitlement and private-app scopes determine availability. One-to-one sales email analytics are outside the Marketing Email API. Email open metrics are affected by image blocking, privacy features and bot filtering. No downstream conversions, qualified leads, revenue attribution, or persona-level lift should be inferred from email opens/clicks.

If your portal has no sent marketing emails, the live dashboard will be empty. To validate a true performance dashboard, you need a legitimate marketing email already sent from that HubSpot account (with appropriate permission and recipient consent). This project **does not send test emails automatically**.

## Security and interview guidance

- Never paste or commit tokens in GitHub, HTML, screenshots or this chat. Your `.env` is excluded by `.gitignore`.
- The Flask app binds to `127.0.0.1` with debug disabled. Do **not** expose it on GitHub Pages or a public server: this version lacks authentication, authorization and CSRF protection for the optional CRM write forms.
- Use `/prototype` for a reliable presentation, then show `/performance` with actual numbers only when you have connected and tested your HubSpot portal.
- Prefer the **read-only** performance screen during interviews. The CRM contact/segment buttons are separate and may change data.

## Troubleshooting

| Message | What it means |
| --- | --- |
| No HubSpot token configured | Add `HUBSPOT_ACCESS_TOKEN` to `.env` and restart |
| 401 | Token is invalid or expired |
| 403 | Token permissions, plan entitlements or feature access are insufficient |
| No sent emails | No marketing emails were reported for that date range |
| No individual email details | Aggregates were available but per-email details are unavailable |
| 429 | API rate limit; retry after a delay |

Documentation:
- [HubSpot Marketing Email API](https://developers.hubspot.com/docs/api-reference/latest/marketing/marketing-emails/emails/get-email)
- [HubSpot official marketing email performance guide](https://knowledge.hubspot.com/marketing-email/analyze-your-marketing-email-campaign-performance)
