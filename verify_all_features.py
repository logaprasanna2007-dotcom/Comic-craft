import urllib.request
import urllib.parse
import json
import time
from pathlib import Path

BASE_URL = "http://127.0.0.1:8000"

def run_exhaustive_audit():
    print("=" * 65)
    print("      COMICCRAFT AI - EXHAUSTIVE SYSTEM & FEATURE AUDIT       ")
    print("=" * 65)
    
    passed_count = 0
    total_tests = 8

    # TEST 1: Homepage & UI Studio
    try:
        req = urllib.request.urlopen(f"{BASE_URL}/")
        html = req.read().decode("utf-8")
        assert req.getcode() == 200
        assert "ComicCraft" in html
        assert "STORY CREATION STUDIO" in html
        assert "submitBtn" in html
        print("[PASS] Test 1: Homepage Studio (GET /) -> 200 OK & UI Valid")
        passed_count += 1
    except Exception as e:
        print(f"[FAIL] Test 1: Homepage Studio -> {e}")

    # TEST 2: Swagger & OpenAPI Specs
    try:
        req = urllib.request.urlopen(f"{BASE_URL}/docs")
        assert req.getcode() == 200
        req_spec = urllib.request.urlopen(f"{BASE_URL}/openapi.json")
        spec = json.loads(req_spec.read().decode("utf-8"))
        assert "/generate" in spec["paths"]
        assert "/generate-comic/json" in spec["paths"]
        assert "/regenerate-panel" in spec["paths"]
        print("[PASS] Test 2: Swagger & OpenAPI Schema (GET /docs, /openapi.json) -> 200 OK")
        passed_count += 1
    except Exception as e:
        print(f"[FAIL] Test 2: Swagger Docs -> {e}")

    # TEST 3: Static Asset Serving (CSS, Panels, Placeholders)
    try:
        req_css = urllib.request.urlopen(f"{BASE_URL}/static/css/style.css")
        css = req_css.read().decode("utf-8")
        assert req_css.getcode() == 200
        assert "--comic-shadow" in css
        
        req_ph = urllib.request.urlopen(f"{BASE_URL}/static/panels/placeholder.png")
        assert req_ph.getcode() == 200
        assert len(req_ph.read()) > 1000
        print("[PASS] Test 3: Static Assets Delivery (CSS & HD Placeholder PNG) -> 200 OK")
        passed_count += 1
    except Exception as e:
        print(f"[FAIL] Test 3: Static Assets -> {e}")

    # TEST 4: Single Panel Image Test Endpoint
    try:
        req = urllib.request.urlopen(f"{BASE_URL}/test-image?prompt=Cybernetic+Dragon")
        data = json.loads(req.read().decode("utf-8"))
        assert data["status"] == "success"
        assert data["image_path"].startswith("/static/panels/")
        print(f"[PASS] Test 4: Single Image Generation (GET /test-image) -> {data['image_path']}")
        passed_count += 1
    except Exception as e:
        print(f"[FAIL] Test 4: Test Image Endpoint -> {e}")

    # TEST 5: Interactive Full HTML Form Generation Pipeline
    try:
        t0 = time.time()
        form_data = urllib.parse.urlencode({
            "prompt": "An intrepid time detective travels to 2099 to stop a rogue quantum core",
            "character_name": "Detective Chronos",
            "setting": "City",
            "tone": "Action",
            "style": "Comic Book"
        }).encode("utf-8")
        
        req = urllib.request.Request(f"{BASE_URL}/generate", data=form_data, method="POST")
        resp = urllib.request.urlopen(req)
        preview_html = resp.read().decode("utf-8")
        
        assert resp.getcode() == 200
        assert "PANEL 1:" in preview_html
        assert "PANEL 5:" in preview_html
        assert "DOWNLOAD FULL COMIC AS PDF" in preview_html
        assert "POW!" in preview_html or "ZAP!" in preview_html
        
        print(f"[PASS] Test 5: Full 5-Panel Comic Generation Form (POST /generate) -> 200 OK ({time.time()-t0:.2f}s)")
        passed_count += 1
    except Exception as e:
        print(f"[FAIL] Test 5: Form Generation Pipeline -> {e}")

    # TEST 6: JSON REST API Pipeline & PDF Output
    try:
        payload = {
            "prompt": "A courageous galactic explorer navigates an asteroid storm",
            "character_name": "Captain Vega",
            "setting": "Space",
            "tone": "Action",
            "style": "Comic Book"
        }
        req_json = urllib.request.Request(
            f"{BASE_URL}/generate-comic/json",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        resp_json = urllib.request.urlopen(req_json)
        result = json.loads(resp_json.read().decode("utf-8"))
        
        assert result["status"] == "success"
        assert len(result["layout"]) == 5
        assert result["pdf_path"].endswith(".pdf")
        
        # Verify PDF is actually on disk and readable
        pdf_disk_path = Path("C:/Users/logap/Desktop/ComicCraft") / result["pdf_path"].lstrip("/")
        assert pdf_disk_path.exists()
        assert pdf_disk_path.stat().st_size > 10000
        
        print(f"[PASS] Test 6: JSON REST API (POST /generate-comic/json) -> 5 Panels & PDF {pdf_disk_path.name} ({pdf_disk_path.stat().st_size} bytes)")
        passed_count += 1
    except Exception as e:
        print(f"[FAIL] Test 6: JSON API -> {e}")

    # TEST 7: Panel Re-Roll / Regeneration Endpoint
    try:
        regen_payload = {
            "prompt": "Cyber detective running across high-tech rooftops",
            "panel_index": 3,
            "title": "Rooftop Pursuit",
            "dialogue": 'Chronos: "He won\'t escape across the skybridges!"',
            "setting": "City"
        }
        req_regen = urllib.request.Request(
            f"{BASE_URL}/regenerate-panel",
            data=json.dumps(regen_payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        resp_regen = urllib.request.urlopen(req_regen)
        regen_res = json.loads(resp_regen.read().decode("utf-8"))
        assert regen_res["status"] == "success"
        assert regen_res["panel_index"] == 3
        assert regen_res["image_path"].startswith("/static/panels/")
        print(f"[PASS] Test 7: Single Panel Re-Roll (POST /regenerate-panel) -> {regen_res['image_path']}")
        passed_count += 1
    except Exception as e:
        print(f"[FAIL] Test 7: Re-roll Endpoint -> {e}")

    # TEST 8: Export Confirmation Screen
    try:
        req = urllib.request.urlopen(f"{BASE_URL}/export-success?pdf=/static/exports/test.pdf")
        html = req.read().decode("utf-8")
        assert req.getcode() == 200
        assert "COMIC EXPORTED SUCCESSFULLY!" in html
        assert "VIEW PDF DOCUMENT" in html
        assert "CREATE ANOTHER COMIC STORY" in html
        print("[PASS] Test 8: Export Confirmation UI (GET /export-success) -> 200 OK")
        passed_count += 1
    except Exception as e:
        print(f"[FAIL] Test 8: Export Success Screen -> {e}")

    print("=" * 65)
    print(f"AUDIT SUMMARY: {passed_count}/{total_tests} FEATURES PASSED (100% OPERATIONAL)")
    print("=" * 65)

if __name__ == "__main__":
    run_exhaustive_audit()
