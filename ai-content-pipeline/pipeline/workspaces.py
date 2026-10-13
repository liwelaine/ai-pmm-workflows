"""Demo workspace definitions. Persona assumptions are illustrative, not client data."""

BILLABLES_WORKSPACE = {
    "slug": "billables-ai",
    "name": "Billables AI",
    "category": "AI-powered time capture and billing workflows",
    "description": (
        "A product marketing demo workspace for AI-assisted time capture, "
        "billing narratives, and workflow visibility in billable professional services."
    ),
    "website": "https://billables.ai/",
    "status": "Demo / research-based hypotheses",
    "note": (
        "This workspace is an independent portfolio demonstration. It is not "
        "affiliated with Billables AI. Buyer needs, campaign angles, and "
        "persona characteristics are working assumptions to validate with interviews."
    ),
    "value_proposition": (
        "Help billable teams capture more of the work they already do, "
        "reduce manual time-entry effort, and improve visibility into billable activity."
    ),
    "persona": {
        "id": "billables_managing_partner",
        "name": "Managing Partner",
        "subtitle": "Law Firm Owner / Equity Partner",
        "buying_role": "Economic buyer / decision maker (hypothesis)",
        "icp": [
            "Partner-led law firms where fee earners record billable work",
            "Firms that depend on timely, accurate time entries for billing",
            "Leaders responsible for revenue, margin, and practice operations",
        ],
        "jobs": [
            "Protect revenue without adding administrative burden",
            "Improve time-entry completeness across the firm",
            "Understand where billable capacity may be lost",
        ],
        "pain_points": [
            "Billable work can be forgotten or reconstructed too late",
            "Partners lack consistent visibility into capture and billing habits",
            "Manual follow-ups create friction for attorneys and operations teams",
        ],
        "triggers": [
            "Concern about missed billable hours",
            "Growth without a proportional increase in administrative capacity",
            "Pressure to improve billing hygiene and margin visibility",
        ],
        "objections": [
            "Will this add work for attorneys?",
            "How does it fit existing practice-management workflows?",
            "How is confidential client information handled?",
        ],
        "message": "Capture the work. Protect the revenue.",
        "supporting_message": (
            "Reduce reliance on end-of-day reconstruction of billable work "
            "and give firm leaders a more dependable foundation for billing decisions."
        ),
        "cta": "Request a product demo",
        "proof_needed": [
            "Verified customer time-capture results",
            "Security and privacy documentation",
            "Confirmed integration and implementation details",
        ],
    },
    "campaign": {
        "name": "Stop Losing Billable Time",
        "objective": "Drive qualified demo requests",
        "stage": "Awareness to consideration",
        "persona_id": "billables_managing_partner",
        "content_pieces": ["Thought-leadership blog", "Persona-specific email draft", "LinkedIn post"],
        "status": "Brief draft — not published",
    },
}
