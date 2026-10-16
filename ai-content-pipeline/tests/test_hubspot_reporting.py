"""No-credential tests: the live dashboard never substitutes simulated metrics."""
import unittest
from pipeline.hubspot_reporting import HubSpotReporting, normalize_stats
from pipeline.hubspot_live import HubSpotIntegrationError


class StubClient:
    configured = True

    def __init__(self):
        self.calls = []

    def _request(self, method, path, *, params=None, allow_not_found=False, **kwargs):
        self.calls.append((method, path))
        if path.endswith("/statistics/list"):
            return {
                "emails": [123, 123, 456],
                "aggregate": {
                    "counters": {"sent": 210, "delivered": 200, "open": 90, "click": 24},
                    "ratios": {"openratio": 0.45, "clickratio": 0.12},
                },
            }
        if path.endswith("/statistics/histogram"):
            return {
                "results": [{
                    "interval": {"start": "2026-10-01T00:00:00Z"},
                    "aggregations": {"counters": {"delivered": 80},
                                     "ratios": {"openratio": .25, "clickratio": .05}},
                }]
            }
        if path.endswith("/456"):
            return {"name": "Test newsletter 2", "subject": "Subject 2",
                    "publishedAt": "2026-10-09T12:00:00Z", "state": "PUBLISHED",
                    "stats": {"counters": {"delivered": 150}, "ratios": {"clickratio": .11}}}
        if path.endswith("/123"):
            return {"name": "Test newsletter 1", "subject": "Subject 1",
                    "publishedAt": "2026-10-03T12:00:00Z", "state": "PUBLISHED",
                    "stats": {"counters": {"delivered": 50}, "ratios": {"clickratio": .08}}}
        raise AssertionError("Unexpected request: " + path)


class NoTokenStub(StubClient):
    configured = False


class ReportingTests(unittest.TestCase):
    def test_normalizer_keeps_missing_metrics_missing(self):
        stats = normalize_stats({"counters": {"delivered": 10}, "ratios": {}})
        self.assertEqual(stats["delivered"], 10)
        self.assertIsNone(stats["click_rate"])
        self.assertIsNone(stats["open_rate"])

    def test_read_only_live_report(self):
        stub = StubClient()
        report = HubSpotReporting(stub).get_report(30)
        self.assertEqual(report["source"], "LIVE HubSpot API")
        self.assertEqual(report["metrics"]["delivered"], 200)
        self.assertEqual(report["metrics"]["click_rate"], 12.0)
        self.assertEqual(report["campaign_count"], 2)
        self.assertEqual(len(report["emails"]), 2)
        self.assertEqual(report["trend"][0]["click_rate"], 5.0)
        self.assertTrue(all(method == "GET" for method, _ in stub.calls))

    def test_without_token_fails_instead_of_faking_data(self):
        with self.assertRaises(HubSpotIntegrationError):
            HubSpotReporting(NoTokenStub()).get_report(30)

    def test_rejects_unbounded_time_range(self):
        with self.assertRaises(ValueError):
            HubSpotReporting(StubClient()).get_report(365)


if __name__ == "__main__":
    unittest.main()
