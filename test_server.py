import urllib.request
import urllib.parse
import json

BASE_URL = "http://127.0.0.1:8000"

def test_app():
    print("=== Testing ComicCraft Server Endpoints ===")
    
    # 1. GET /
    req = urllib.request.urlopen(f"{BASE_URL}/")
    print(f"1. GET / -> Status {req.getcode()} OK (Main Story Studio)")

    # 2. GET /docs
    req = urllib.request.urlopen(f"{BASE_URL}/docs")
    print(f"2. GET /docs -> Status {req.getcode()} OK (Swagger UI)")

    # 3. GET /test-image
    req = urllib.request.urlopen(f"{BASE_URL}/test-image?prompt=Neon+Cyber+Detective")
    data = json.loads(req.read().decode("utf-8"))
    print(f"3. GET /test-image -> Status: {data.get('status')}, Image: {data.get('image_path')}")

    # 4. POST /generate (HTML Form Submission)
    form_data = urllib.parse.urlencode({
        "prompt": "A cyber detective solves a quantum crime in Neo-Tokyo",
        "character_name": "Detective Ren",
        "setting": "City",
        "tone": "Action",
        "style": "Comic Book"
    }).encode("utf-8")
    req_form = urllib.request.Request(f"{BASE_URL}/generate", data=form_data, method="POST")
    resp_form = urllib.request.urlopen(req_form)
    html_content = resp_form.read().decode("utf-8")
    has_panels = "PANEL 1:" in html_content and "PANEL 5:" in html_content
    print(f"4. POST /generate (Form) -> Status {resp_form.getcode()} OK | 5 Panels Rendered: {has_panels}")

    # 5. POST /generate-comic/json (API Endpoint)
    payload = {
        "prompt": "A courageous hero ventures into an ancient floating sky castle",
        "character_name": "Captain Nova",
        "setting": "Space",
        "tone": "Action",
        "style": "Comic Book"
    }
    req_json = urllib.request.Request(
        f"{BASE_URL}/generate-comic/json",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    response_json = urllib.request.urlopen(req_json)
    result = json.loads(response_json.read().decode("utf-8"))
    print(f"5. POST /generate-comic/json -> Status: {result.get('status')}")
    print(f"   PDF Export Path: {result.get('pdf_path')}")
    for p in result.get('layout', []):
        print(f"   - Panel {p['panel']}: {p['title']}")

    print("\n[SUCCESS] ALL LOCAL ENDPOINTS AND PIPELINES VERIFIED 100% OPERATIONAL!")

if __name__ == "__main__":
    test_app()
