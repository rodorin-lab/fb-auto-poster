#!/usr/bin/env python3
"""FB Group Auto Poster - ULTIMATE EDITION - Uses REAL Chrome profile"""
from playwright.sync_api import sync_playwright
from datetime import datetime
import json, sys, os, time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
now = datetime.now()

POST_CONTENT = f"""🌸 Today's Japanese Phrase

「ありがとう」- Thank you

A simple but powerful word.
Use it every day! 🌟

#JapaneseLearning #JLPT"""

class UltimatePoster:
    def __init__(self):
        p = sync_playwright().start()
        
        # Use the user's REAL Chrome profile to keep login!
        REAL_CHROME_PROFILE = os.path.expanduser("~/.config/google-chrome")
        
        print(f"[*] Using REAL Chrome profile: {REAL_CHROME_PROFILE}")
        print(f"[*] Launching browser with your saved login...")
        
        self.context = p.chromium.launch_persistent_context(
            user_data_dir=REAL_CHROME_PROFILE,
            headless=False,
            args=[
                "--start-maximized",
                "--remote-allow-origins=*",
            ]
        )
        self.page = self.context.pages[0] if self.context.pages else self.context.new_page()
        
        # First check if logged in
        self.ensure_logged_in()
        
        # Then post!
        self.post_to_groups()

    def ensure_logged_in(self):
        """Check login status and wait if needed"""
        self.page.goto("https://www.facebook.com/")
        time.sleep(3)
        
        url = self.page.url
        if "login" in url.lower():
            print("[!] NOT logged in. Please log in now in the browser window.")
            print("[*] I'll wait up to 5 minutes...")
            for i in range(300):
                time.sleep(1)
                current = self.page.url
                if "login" not in current.lower() and "facebook.com" in current.lower():
                    print(f"[✓] Logged in! ({i+1}s)")
                    break
                if i % 30 == 0:
                    print(f"   Waiting... ({i+1}s)")
        else:
            print("[✓] Already logged in!")

    def post_to_groups(self):
        groups = self.load_groups()
        print(f"[*] Groups to post: {[g['name'] for g in groups]}")
        
        for group in groups:
            print(f"\n[*] === {group['name']} ===")
            try:
                self.page.goto(f"https://www.facebook.com/groups/{group['username']}")
                time.sleep(5)
                
                # Screenshot to debug
                os.makedirs(f"{PROJECT_ROOT}/screenshots", exist_ok=True)
                self.page.screenshot(path=f"{PROJECT_ROOT}/screenshots/{group['username']}.png")
                print(f"   📸 Screenshot saved")
                
                # Find post box - try multiple selectors
                clicked = False
                selectors = [
                    '[aria-label="テキストを入力..."]',
                    '[aria-label="Write something..."]',
                    '[aria-label="Create a post"]',
                    '[aria-label="投稿を作成"]',
                    '//span[contains(text(), "Write something")]',
                    '//span[contains(text(), "テキストを入力")]',
                ]
                
                for sel in selectors:
                    try:
                        if sel.startswith("//"):
                            self.page.wait_for_selector(sel, timeout=3000).click()
                        else:
                            self.page.wait_for_selector(sel, timeout=3000).click()
                        print(f"   [+] Post box clicked! ({sel[:30]})")
                        clicked = True
                        break
                    except:
                        continue
                
                if not clicked:
                    print("   [-] Could not find post box")
                    continue
                
                time.sleep(2)
                
                # Fill content
                try:
                    self.page.wait_for_selector("div[role='dialog'] div[contenteditable='true']", timeout=5000)
                    self.page.fill("div[role='dialog'] div[contenteditable='true']", POST_CONTENT)
                    print("   [+] Content filled!")
                except:
                    print("   [-] Could not fill content")
                    continue
                
                time.sleep(2)
                
                # Post!
                try:
                    self.page.wait_for_selector('[aria-label="投稿"]', timeout=5000).click()
                except:
                    try:
                        self.page.wait_for_selector('[aria-label="Post"]', timeout=5000).click()
                    except:
                        print("   [-] Could not click Post")
                        continue
                
                time.sleep(3)
                print(f"   ✅ POSTED to {group['name']}!")
                
            except Exception as e:
                print(f"   ❌ Error: {e}")

    def load_groups(self):
        with open(f"{PROJECT_ROOT}/groups.json", "r") as f:
            return json.load(f)


if __name__ == "__main__":
    UltimatePoster()