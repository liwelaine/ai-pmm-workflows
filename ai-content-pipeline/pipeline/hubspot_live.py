"""Safe, opt-in HubSpot CRM operations for the interview dashboard.

Real operations are intentionally limited to connectivity, a user-submitted
test contact, and an explicitly requested dynamic segment. No email is sent.
Never expose HUBSPOT_ACCESS_TOKEN to the browser or commit it to GitHub.
"""
import re
from urllib.parse import quote

import requests

import config

PERSONA_PROPERTY = "pmm_demo_persona"
EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


class HubSpotIntegrationError(RuntimeError):
    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


class HubSpotLive:
    def __init__(self, token: str | None = None):
        self.token = (config.HUBSPOT_ACCESS_TOKEN if token is None else token).strip()

    @property
    def configured(self) -> bool:
        return bool(self.token)

    def _request(self, method: str, path: str, *, json: dict | None = None,
                 params: dict | None = None, allow_not_found: bool = False) -> dict | None:
        if not self.configured:
            raise HubSpotIntegrationError(
                "HubSpot is not configured. Add HUBSPOT_ACCESS_TOKEN to your local .env file."
            )

        try:
            response = requests.request(
                method, f"{config.HUBSPOT_BASE_URL}{path}",
                headers={"Authorization": f"Bearer {self.token}",
                         "Content-Type": "application/json"},
                json=json, params=params, timeout=20,
            )
        except requests.RequestException as exc:
            raise HubSpotIntegrationError("Could not reach HubSpot. Check your connection.") from exc

        if allow_not_found and response.status_code == 404:
            return None
        if response.status_code >= 400:
            try:
                api_message = response.json().get("message", "")
            except ValueError:
                api_message = ""
            if response.status_code == 401:
                message = "Invalid HubSpot access token (401)."
            elif response.status_code == 403:
                message = "HubSpot permission denied (403). Check the private app scopes."
            elif response.status_code == 429:
                message = "HubSpot rate limit reached (429). Please retry later."
            else:
                message = f"HubSpot returned {response.status_code}: {str(api_message)[:200]}"
            raise HubSpotIntegrationError(message, response.status_code)
        if not response.content:
            return {}
        try:
            return response.json()
        except ValueError as exc:
            raise HubSpotIntegrationError("HubSpot returned a non-JSON response.") from exc

    def test_connection(self) -> dict:
        """Read-only proof that the credentials can access contact records."""
        data = self._request("GET", "/crm/v3/objects/contacts", params={"limit": 1})
        return {"connected": True, "contacts_visible_in_sample": len(data.get("results", []))}

    def ensure_persona_property(self) -> None:
        """Create a dedicated text property once; never overwrite built-in CRM fields."""
        path = f"/crm/v3/properties/contacts/{PERSONA_PROPERTY}"
        existing = self._request("GET", path, allow_not_found=True)
        if existing is not None:
            if existing.get("type") != "string":
                raise HubSpotIntegrationError(
                    "Existing pmm_demo_persona property is not a text field."
                )
            return
        self._request("POST", "/crm/v3/properties/contacts", json={
            "name": PERSONA_PROPERTY,
            "label": "PMM Demo Persona",
            "groupName": "contactinformation",
            "type": "string",
            "fieldType": "text",
            "description": "Test-only persona tag for AI Content Pipeline interviews.",
        })

    def sync_test_contact(self, email: str, persona: str, first_name: str = "") -> dict:
        """Upsert only the email supplied explicitly in the dashboard form."""
        email = email.strip().lower()
        first_name = first_name.strip()
        if not EMAIL_RE.fullmatch(email) or len(email) > 254:
            raise HubSpotIntegrationError("Enter a valid email address that you control.")
        if not re.fullmatch(r"[a-z0-9_]{2,60}", persona):
            raise HubSpotIntegrationError("Invalid demo persona.")
        if len(first_name) > 100:
            raise HubSpotIntegrationError("First name is too long.")

        self.ensure_persona_property()
        search = self._request("POST", "/crm/v3/objects/contacts/search", json={
            "filterGroups": [{"filters": [{
                "propertyName": "email", "operator": "EQ", "value": email
            }]}],
            "limit": 1,
        })
        props = {PERSONA_PROPERTY: persona}
        if first_name:
            props["firstname"] = first_name
        results = search.get("results", [])
        if results:
            record_id = str(results[0]["id"])
            self._request("PATCH", f"/crm/v3/objects/contacts/{quote(record_id, safe='')}",
                          json={"properties": props})
            return {"action": "updated", "id": record_id, "email": email, "persona": persona}

        created = self._request("POST", "/crm/v3/objects/contacts",
                                json={"properties": {"email": email, **props}})
        return {"action": "created", "id": str(created["id"]),
                "email": email, "persona": persona}

    def create_demo_segment(self, persona: str) -> dict:
        """Create one explicitly requested dynamic contact list for a persona."""
        if not re.fullmatch(r"[a-z0-9_]{2,60}", persona):
            raise HubSpotIntegrationError("Invalid demo persona.")
        self.ensure_persona_property()
        payload = {
            "name": f"AI Content Pipeline Demo - {persona}",
            "objectTypeId": "0-1",
            "processingType": "DYNAMIC",
            "filterBranch": {
                "filterBranchType": "OR",
                "filterBranchOperator": "OR",
                "filters": [],
                "filterBranches": [{
                    "filterBranchType": "AND",
                    "filterBranchOperator": "AND",
                    "filterBranches": [],
                    "filters": [{
                        "filterType": "PROPERTY",
                        "property": PERSONA_PROPERTY,
                        "operation": {
                            "operationType": "STRING",
                            "operator": "IS_EQUAL_TO",
                            "value": persona,
                        },
                    }],
                }],
            },
        }
        created = self._request("POST", "/crm/v3/lists", json=payload)
        return {"id": str(created.get("listId", created.get("list", {}).get("listId", ""))),
                "name": payload["name"], "persona": persona}
