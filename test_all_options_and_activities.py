import urllib.request
import urllib.parse
import json
import time
from pathlib import Path

BASE_URL = "http://127.0.0.1:8000"
PROJECT_DIR = Path("C:/Users/logap/Desktop/ComicCraft")

def run_full_activity_test():
    print("=" * 70)
    print("      COMICCRAFT AI - DEEP MULTI-OPTION & ACTIVITY AUDIT      ")
    print("=" * 70)

    # 1. Test Combinations Matrix (Different Settings, Tones, Styles)
    test_scenarios = [
        {
            "name": "Scenario A: Cyberpunk Detective (City + Action + Comic Book)",
            "prompt": "A cyber detective navigates neon alleys pursuing a rogue android",
            "char": "Detective Jax",
            "setting": "City",
            "tone": "Action",
            "style": "Comic Book"
        },
        {
            "name": "Scenario B: Cosmic Star Odyssey (Space + Dramatic + Anime)",
            "prompt": "An astronaut investigates a dormant alien starship orbiting Saturn",
            "char": "Captain Sol",
            "setting": "Space",
            "tone": "Dramatic",
            "style": "Anime"
        },
        {
            "name": "Scenario C: Enchanted Forest Sorcery (Forest + Poetic + Dark Noir)",
            "prompt": "A druid protects an ancient glowing world tree from dark shadow beasts",
            "char": "Elara",
            "setting": "Forest",
            "tone": "Poetic",
            "style": "Dark Noir"
        },
        {
            "name": "Scenario D: Superpower Academy (School + Funny + Pixel Art)",
            "prompt": "A young telekinetic student accidentally levitates the entire cafeteria",
            "char": "Toby",
            "setting": "School",
            "tone": "Funny",
            "style": "Pixel Art"
        }
    ]

    all_passed = True

    print("\n--- 1. Testing Multiple Story Settings, Tones & Visual Styles ---")
    for idx, sc in enumerate(test_scenarios, start=1):
        t0 = time.time()
        form_data = urllib.parse.urlencode({
            "prompt": sc["prompt"],
            "character_name": sc["char"],
            "setting": sc["setting"],
            "tone": sc["tone"],
            "style": sc["style"]
        }).encode("utf-8")

        try:
            req = urllib.request.Request(f"{BASE_URL}/generate", data=form_data, method="POST")
            with urllib.request.urlopen(req) as resp:
                html = resp.read().decode("utf-8")
                status = resp.getcode()
                has_5_panels = all(f"PANEL {p}:" in html for p in range(1, 6))
                has_pdf = "DOWNLOAD FULL COMIC AS PDF" in html
                
                if status == 200 and has_5_panels and has_pdf:
                    print(f"[PASS] {sc['name']} -> 200 OK (5 Panels + PDF generated in {time.time()-t0:.2f}s)")
                else:
                    print(f"[FAIL] {sc['name']} -> Missing panels or PDF link")
                    all_passed = False
        except Exception as e:
            print(f"[FAIL] {sc['name']} -> Error: {e}")
            all_passed = False

    print("\n--- 2. Testing Interactive Panel Re-Roll Activity (POST /regenerate-panel) ---")
    try:
        regen_payload = {
            "prompt": "Hero unleashing glowing energy shield against dark forces",
            "panel_index": 4,
            "title": "Energy Climax",
            "dialogue": 'Hero: "This shield will hold until backup arrives!"',
            "setting": "Space"
        }
        req_regen = urllib.request.Request(
            f"{BASE_URL}/regenerate-panel",
            data=json.dumps(regen_payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req_regen) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            assert data["status"] == "success"
            assert data["panel_index"] == 4
            # Verify file exists on disk
            img_file = PROJECT_DIR / data["image_path"].lstrip("/")
            assert img_file.exists() and img_file.stat().st_size > 1000
            print(f"[PASS] Re-Roll Activity -> Generated new image {img_file.name} ({img_file.stat().st_size} bytes)")
    except Exception as e:
        print(f"[FAIL] Re-roll Activity -> Error: {e}")
        all_passed = False

    print("\n--- 3. Testing JSON REST API Activity (POST /generate-comic/json) ---")
    try:
        api_payload = {
            "prompt": "Mythic warrior claims the sunblade from the mountaintop",
            "character_name": "Valen",
            "setting": "Forest",
            "tone": "Action",
            "style": "Comic Book"
        }
        req_api = urllib.request.Request(
            f"{BASE_URL}/generate-comic/json",
            data=json.dumps(api_payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req_api) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            assert data["status"] == "success"
            assert len(data["layout"]) == 5
            pdf_path = PROJECT_DIR / data["pdf_path"].lstrip("/")
            assert pdf_path.exists() and pdf_path.stat().st_size > 10000
            print(f"[PASS] JSON API Activity -> 5 Panels & Valid PDF ({pdf_path.stat().st_size} bytes)")
    except Exception as e:
        print(f"[FAIL] JSON API Activity -> Error: {e}")
        all_passed = False

    print("\n--- 4. Testing Export Confirmation & PDF Download Activity ---")
    try:
        req_exp = urllib.request.urlopen(f"{BASE_URL}/export-success?pdf=/static/exports/test_comic.pdf")
        html_exp = req_exp.read().decode("utf-8")
        assert req_exp.getcode() == 200
        assert "COMIC EXPORTED SUCCESSFULLY!" in html_exp
        assert "VIEW PDF DOCUMENT" in html_exp
        print("[PASS] Export Confirmation Screen -> 200 OK & All Action Buttons Verified")
    except Exception as e:
        print(f"[FAIL] Export Screen -> Error: {e}")
        all_passed = False

    print("\n--- 5. Testing Report Documents & Local Assets ---")
    docx1 = PROJECT_DIR / "ComicCraft_Naan_Mudhalvan_Project_Report.docx"
    docx2 = PROJECT_DIR / "REPORT.docx"
    md1 = PROJECT_DIR / "REPORT.md"
    bat1 = PROJECT_DIR / "run.bat"
    ps1 = PROJECT_DIR / "run.ps1"

    for f, label in [(docx1, "Official Word Report (.docx)"), (docx2, "REPORT.docx"), (md1, "REPORT.md"), (bat1, "run.bat"), (ps1, "run.ps1")]:
        if f.exists() and f.stat().st_size > 0:
            print(f"[PASS] {label} -> Exists ({f.stat().st_size} bytes)")
        else:
            print(f"[FAIL] {label} -> Missing or empty")
            all_passed = False

    print("\n" + "=" * 70)
    if all_passed:
        print("[SUCCESS] ALL OPTIONS, STYLES, ENDPOINTS & USER ACTIVITIES VERIFIED 100% OPERATIONAL!")
    else:
        print("[WARNING] Some activities encountered issues. Please check the logs above.")
    print("=" * 70)

if __name__ == "__main__":
    run_full_activity_test()
