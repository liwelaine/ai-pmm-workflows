"""Unit tests for the opt-in HubSpot client; no real network calls."""
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from pipeline.hubspot_live import HubSpotLive, HubSpotIntegrationError


class HubSpotLiveTests(unittest.TestCase):
    def setUp(self):
        self.client = HubSpotLive(token="test-token")

    def test_missing_token_blocks_network(self):
        with self.assertRaises(HubSpotIntegrationError):
            HubSpotLive(token="").test_connection()

    def test_connection_is_read_only(self):
        with patch.object(self.client, "_request", return_value={"results": [{"id": "1"}]}) as call:
            self.assertTrue(self.client.test_connection()["connected"])
            self.assertEqual(call.call_args.args, ("GET", "/crm/v3/objects/contacts"))

    def test_invalid_email_rejected_before_writes(self):
        with patch.object(self.client, "_request") as call:
            with self.assertRaises(HubSpotIntegrationError):
                self.client.sync_test_contact("invalid", "finance_leader")
            call.assert_not_called()

    def test_existing_contact_is_patched_not_duplicated(self):
        def fake_request(method, path, **kwargs):
            if method == "GET": return {"name": "pmm_demo_persona", "type": "string"}
            if path.endswith("/search"): return {"results": [{"id": "123"}]}
            if method == "PATCH": return {}
            raise AssertionError(f"Unexpected request: {method} {path}")
        with patch.object(self.client, "_request", side_effect=fake_request) as request:
            result = self.client.sync_test_contact("demo@example.com", "finance_leader")
            self.assertEqual(result["action"], "updated")
            self.assertEqual([c.args[0] for c in request.call_args_list], ["GET", "POST", "PATCH"])

    def test_list_payload_uses_demo_property(self):
        with patch.object(self.client, "ensure_persona_property"), patch.object(
            self.client, "_request", return_value={"listId": "99"}
        ) as req:
            result = self.client.create_demo_segment("finance_leader")
            self.assertEqual(result["id"], "99")
            payload = req.call_args.kwargs["json"]
            self.assertEqual(payload["filterBranch"]["filterBranches"][0]["filters"][0]["property"], "pmm_demo_persona")


if __name__ == "__main__":
    unittest.main()
