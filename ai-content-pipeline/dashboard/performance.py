"""Read-only HubSpot Performance view. Access locally via /performance."""
from flask import Blueprint, render_template, request

from pipeline.hubspot_reporting import HubSpotReporting
from pipeline.hubspot_live import HubSpotIntegrationError

performance_bp = Blueprint("performance", __name__)


@performance_bp.get("/performance")
def performance():
    days = request.args.get("days", default=90, type=int)
    if days not in (30, 90, 180):
        days = 90
    report = None
    error = None
    try:
        report = HubSpotReporting().get_report(days)
    except HubSpotIntegrationError as exc:
        error = str(exc)
    return render_template("performance.html", report=report, days=days, error=error)
