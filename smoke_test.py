"""Quick smoke test of the dashboard using Flask's built-in test client.
Run: python smoke_test.py"""
import dashboard.app as a

client = a.app.test_client()

# 1) Homepage renders with prior run data.
r = client.get("/")
html = r.get_data(as_text=True)
assert r.status_code == 200, r.status_code
for needle in ["AI<b>CONTENT</b>", "Segment performance", "AI performance summary",
               "Headline A/B options", "Avg click", "Click rate"]:
    assert needle in html, f"missing: {needle}"
print("GET /            -> 200, all sections present")

# 2) Trigger a run via POST -> should 302 redirect back to /.
r = client.post("/run", data={"topic": "Automating agency onboarding"})
assert r.status_code in (302, 303), r.status_code
print("POST /run        -> 302 redirect (pipeline executed)")

# 3) New campaign now visible.
html = client.get("/").get_data(as_text=True)
assert "Automating agency onboarding" in html
print("GET / (after run)-> new campaign visible")
print("\nDASHBOARD SMOKE TEST PASSED")
