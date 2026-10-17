"""Run a 20-loop end-to-end M3 API verification against the user's local PostgreSQL-backed server."""
import os, time, uuid
from datetime import date, timedelta
import requests

API = os.getenv("SKIN_API", "http://127.0.0.1:8000")
LOOPS = 20
email = os.getenv("M3_TEST_EMAIL", f"m3_verify_{uuid.uuid4().hex[:10]}@example.com")
password = os.getenv("M3_TEST_PASSWORD", "M3Verify@123")


def req(method, path, **kwargs):
    r = requests.request(method, API + path, timeout=15, **kwargs)
    if not r.ok:
        raise RuntimeError(f"{method} {path} -> {r.status_code}: {r.text[:500]}")
    return r.json()

print(f"Testing {API} for {LOOPS} loops")
# Create a dedicated verification user.
r = requests.post(API + "/auth/register", json={"name":"M3 Verification","email":email,"password":password}, timeout=15)
if not r.ok and r.status_code != 400:
    raise RuntimeError(f"registration failed: {r.status_code} {r.text[:500]}")
login = requests.post(API + "/auth/login", data={"username":email,"password":password}, timeout=15)
login.raise_for_status()
token = login.json()["access_token"]
headers={"Authorization":f"Bearer {token}"}

# M1/M2 prerequisites.
profile = requests.get(API+"/user/skin-profile",headers=headers,timeout=15)
if profile.status_code == 404:
    req("POST","/user/skin-profile",headers=headers,json={"skin_type":"combination","acne":True,"dryness":False,"pigmentation":True,"sensitivity":False})
assessment = requests.get(API+"/user/skin-assessment",headers=headers,timeout=15)
if assessment.status_code == 404:
    req("POST","/user/skin-assessment",headers=headers,json={"skin_type":"combination","acne_level":"medium","dryness_level":"low","pigmentation_level":"medium","sensitivity_level":"low","additional_concerns":"acne,pigmentation"})

for i in range(1, LOOPS+1):
    ingredient = req("POST","/user/ingredients/analyze",headers=headers,json={"ingredients":["Niacinamide","Hyaluronic Acid","Retinol"]})
    assert ingredient["matched_count"] == 3
    suitability = req("POST","/user/ingredients/suitability",headers=headers,json={"ingredients":["Niacinamide","Retinol"]})
    assert suitability["matched_count"] == 2
    products = req("POST","/user/products/recommendations",headers=headers,json={"category":"Serum","budget":800,"goal":"pigmentation","limit":5})
    assert "recommendations" in products
    progress = req("POST","/user/progress",headers=headers,json={"log_date":(date.today()-timedelta(days=LOOPS-i)).isoformat(),"skin_score":70+i,"routine_adherence":60+i,"notes":f"M3 verification loop {i}"})
    assert progress["user_id"]
    analytics = req("GET","/user/analytics/dashboard",headers=headers)
    assert analytics["progress_entries"] >= i
    print(f"Loop {i:02d}/20: OK | products={len(products['recommendations'])} | latest_score={analytics['latest_skin_score']}")

history = req("GET","/user/ingredients/history",headers=headers)
recommendation_history = req("GET","/user/products/recommendation-history",headers=headers)
progress_history = req("GET","/user/progress",headers=headers)
assert len(history) >= LOOPS
assert len(recommendation_history) >= LOOPS
assert len(progress_history) >= LOOPS
print("\n20/20 LOOPS PASSED")
print(f"Ingredient history rows: {len(history)}")
print(f"Recommendation history rows: {len(recommendation_history)}")
print(f"Progress rows: {len(progress_history)}")
print("PostgreSQL persistence was verified through the running API.")
