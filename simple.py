"""Simple version - uses NO Chrome profile. Fresh Playwright browser.
Just log in ONCE. That's it. Forever."""
from playwright.sync_api import sync_playwright
from os import path, makedirs
import json, time, sys

BASE = path.dirname(path.abspath(__file__))
SESSION_FILE = f"{BASE}/sessions/fb_login.json"

POST = """🌸 Today's Japanese Phrase

「ありがとう」- Thank you

A simple but powerful word.
Use it every day! 🌟

#JapaneseLearning #JLPT"""

def main():
    p = sync_playwright().start()
    print("[*] Starting browser...")
    
    # Use a FRESH profile only for Playwright (no conflict!)
    PROFILE_DIR = f"{BASE}/sessions/pw-profile"
    
    browser = p.chromium.launch_persistent_context(
        user_data_dir=PROFILE_DIR,
        headless=False,
        args=["--start-maximized"]
    )
    page = browser.pages[0] if browser.pages else browser.new_page()
    
    # Check if we have a login marker
    if path.exists(SESSION_FILE):
        print("[✓] Session found! You're already logged in.")
        print("[*] Navigating to group...")
    else:
        print("[!] FIRST TIME - Please log in now!")
        print("[*] Browser window is open. Log into Facebook.")
        page.goto("https://www.facebook.com/")
        
        for i in range(300):
            time.sleep(1)
            url = page.url.lower()
            if "login" not in url and "checkpoint" not in url:
                print(f"[✓] Logged in! ({i+1}s)")
                # Mark session saved
                with open(SESSION_FILE, "w") as f:
                    json.dump({"saved": True}, f)
                break
            if i % 30 == 0:
                print(f"[*] Waiting for login... ({i+1}s)")
    
    # Now post!
    groups = [
        {"name": "Japanese Learning Group", "id": "443644486582763"},
        {"name": "coding4beginners", "id": "coding4beginners"},
    ]
    
    for g in groups:
        print(f"\n[*] === {g['name']} ===")
        try:
            page.goto(f"https://www.facebook.com/groups/{g['id']}")
            time.sleep(5)
            
            # Click post box
            clicked = False
            for sel in ['[aria-label="テキストを入力..."]', '[aria-label="Write something..."]', '[aria-label="Create a post"]', '[aria-label="投稿を作成"]']:
                try:
                    page.wait_for_selector(sel, timeout=3000)
                    page.click(sel)
                    clicked = True
                    break
                except:
                    continue
            
            if not clicked:
                print("   [-] No post box found. Taking screenshot for debug...")
                page.screenshot(path=f"{BASE}/screenshots/debug_{g['id']}.png")
                continue
            
            time.sleep(2)
            page.fill("div[role='dialog'] div[contenteditable='true']", POST)
            time.sleep(1)
            
            for btn in ['[aria-label="投稿"]', '[aria-label="Post"]']:
                try:
                    page.click(btn)
                    break
                except:
                    continue
            
            time.sleep(3)
            print(f"   ✅ POSTED!")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n✨ Done! Browser stays open. Close it when you want.")

if __name__ == "__main__":
    makedirs(f"{BASE}/sessions", exist_ok=True)
    makedirs(f"{BASE}/screenshots", exist_ok=True)
    main()