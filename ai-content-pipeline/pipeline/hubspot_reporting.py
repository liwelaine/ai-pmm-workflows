"""Read-only HubSpot marketing email reporting for the interview dashboard.

Only GET requests. Counts and rates come from HubSpot, never the campaign
simulation. Use the current 2026-03 Marketing Emails Statistics endpoints.
The private app token stays server-side in HUBSPOT_ACCESS_TOKEN.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

from pipeline.hubspot_live import HubSpotLive, HubSpotIntegrationError

BASE = "/marketing/emails/2026-03"
MAX_DETAIL_EMAILS = 12


def _number(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _rate(value):
    """HubSpot ratios are fractions (0..1); don't fake missing values."""
    try:
        n = float(value)
        return round(n * 100, 1) if 0 <= n <= 1 else None
    except (TypeError, ValueError):
        return None


def _value(data, *names):
    for name in names:
        if name in data and data[name] is not None:
            return data[name]
    return None


def normalize_stats(stats: dict | None) -> dict:
    stats = stats if isinstance(stats, dict) else {}
    counters = stats.get("counters") or {}
    ratios = stats.get("ratios") or {}
    return {
        "sent": _number(_value(counters, "sent")),
        "delivered": _number(_value(counters, "delivered")),
        # Explicitly label opens/clicks as *events*, not unique people.
        "open_events": _number(_value(counters, "open")),
        "click_events": _number(_value(counters, "click")),
        "unsubscribes": _number(_value(counters, "unsubscribed", "unsubscribe")),
        "open_rate": _rate(_value(ratios, "openratio", "openRate")),
        "click_rate": _rate(_value(ratios, "clickratio", "clickRate")),
        "click_to_open": _rate(_value(ratios, "clickthroughratio", "clickThroughRatio")),
        "bounce_rate": _rate(_value(ratios, "bounceratio", "bounceRatio")),
    }


class HubSpotReporting:
    def __init__(self, client: HubSpotLive | None = None):
        self.client = client or HubSpotLive()

    def get_report(self, days: int = 90) -> dict:
        """Fetch a genuine HubSpot marketing-email reporting window.

        Missing metrics stay null. Empty accounts produce empty-state UI.
        No fallback to simulated values, no API writes, no credentials in HTML.
        """
        if days not in (30, 90, 180):
            raise ValueError("Reporting window must be 30, 90, or 180 days.")
        if not self.client.configured:
            raise HubSpotIntegrationError(
                "No HubSpot token configured. Add HUBSPOT_ACCESS_TOKEN to .env "
                "and restart Flask to view real email performance."
            )
        end = datetime.now(timezone.utc)
        start = end - timedelta(days=days)
        params = {
            "startTimestamp": start.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "endTimestamp": end.strftime("%Y-%m-%dT%H:%M:%SZ"),
        }

        # Aggregate statistics for the selected window; real HubSpot data.
        aggregate = self.client._request("GET", BASE + "/statistics/list", params=params)
        if not isinstance(aggregate, dict):
            raise HubSpotIntegrationError("HubSpot returned an unexpected statistics response.")

        # Trend is also from HubSpot, not extrapolated from aggregate numbers.
        trend_response = self.client._request(
            "GET", BASE + "/statistics/histogram",
            params={**params, "interval": "WEEK" if days <= 90 else "MONTH"},
        )
        points = []
        for result in (trend_response or {}).get("results", []):
            if not isinstance(result, dict):
                continue
            bounds = result.get("interval") or {}
            metrics = normalize_stats(result.get("aggregations"))
            points.append({
                "date": str(bounds.get("start", ""))[:10],
                "delivered": metrics["delivered"],
                "open_rate": metrics["open_rate"],
                "click_rate": metrics["click_rate"],
            })

        # Include a small sample of recent email names with their own stats.
        # IDs may repeat in the aggregate response; dedupe before fetching.
        unique_ids = []
        for email_id in aggregate.get("emails", []):
            id_text = str(email_id)
            if id_text.isdigit() and id_text not in unique_ids:
                unique_ids.append(id_text)
        emails = []
        detail_warning = None
        for email_id in unique_ids[-MAX_DETAIL_EMAILS:][::-1]:
            try:
                detail = self.client._request(
                    "GET", BASE + "/" + email_id, params={"includeStats": "true"},
                    allow_not_found=True,
                )
            except HubSpotIntegrationError as exc:
                # Aggregate reporting can still work when email details fail.
                detail_warning = str(exc)
                break
            if not detail:
                continue
            stats = normalize_stats(detail.get("stats"))
            emails.append({
                "id": email_id,
                "name": detail.get("name") or "Untitled marketing email",
                "subject": detail.get("subject") or "",
                "date": str(detail.get("publishedAt") or detail.get("publishDate") or "")[:10],
                "state": detail.get("state") or "",
                **stats,
            })
        emails.sort(key=lambda x: x["date"], reverse=True)

        return {
            "source": "LIVE HubSpot API",
            "days": days,
            "start": start.date().isoformat(),
            "end": end.date().isoformat(),
            "updated_at": end.strftime("%Y-%m-%d %H:%M UTC"),
            "metrics": normalize_stats(aggregate.get("aggregate")),
            "campaign_count": len(set(unique_ids)),
            "trend": points,
            "emails": emails,
            "detail_warning": detail_warning,
        }
