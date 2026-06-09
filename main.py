#!/usr/bin/env python3
"""FB Group Auto Poster - For Rodorin's groups (Japanese & coding4beginners)"""
from playwright.sync_api import sync_playwright
from datetime import datetime
from os import path
import json
import sys

PROJECT_ROOT = path.dirname(path.abspath(__file__))
now = datetime.now()

POST_CONTENT = f"""🌸 Today's Japanese Phrase

「ありがとう」- Thank you

A simple but powerful word.
Use it every day! 🌟

#JapaneseLearning #JLPT"""


class FacebookGroupPoster:
    CREATE_SESSION = True  # FIRST TIME - will save cookie

    def __init__(self) -> None:
        p = sync_playwright().start()
        
        # Use persistent context = save login forever!
        self.context = p.chromium.launch_persistent_context(
            user_data_dir=f"{PROJECT_ROOT}/sessions/chrome-profile",
            headless=False,
            args=["--start-maximized"]
        )
        self.page = self.context.pages[0] if self.context.pages else self.context.new_page()

        if self.CREATE_SESSION:
            self.generate_cookie()
        else:
            self.load_cookie()
            self.post_to_groups()

    def post_to_groups(self):
        groups = self.get_sources_list()
        for group in groups:
            print(f"[*] Posting to: {group['name']}")
            try:
                self.page.goto(f"https://facebook.com/groups/{group['username']}")
                self.page.wait_for_timeout(5000)
                
                # Try clicking the post box - Japanese or English
                try:
                    # Japanese: テキストを入力...
                    self.page.wait_for_selector('[aria-label="テキストを入力..."]', timeout=5000).click()
                except:
                    try:
                        # English: Write something...
                        self.page.wait_for_selector('[aria-label="Write something..."]', timeout=5000).click()
                    except:
                        try:
                            # aria-label="Create a post"
                            self.page.wait_for_selector('[aria-label="Create a post"]', timeout=5000).click()
                        except:
                            print("\t[-] Could not find post box!")
                            continue
                
                self.page.wait_for_timeout(2000)
                
                # Type into the contenteditable div inside the dialog
                try:
                    self.page.wait_for_selector("div[role='dialog'] div[contenteditable='true']", timeout=5000).fill(POST_CONTENT)
                except:
                    print("\t[-] Could not find content editor!")
                    continue
                
                self.page.wait_for_timeout(2000)
                
                # Click Post button
                try:
                    self.page.wait_for_selector('[aria-label="投稿"]', timeout=5000).click()
                except:
                    try:
                        self.page.wait_for_selector('[aria-label="Post"]', timeout=5000).click()
                    except:
                        print("\t[-] Could not find Post button!")
                        continue
                
                self.page.wait_for_timeout(5000)
                print(f"\t[+] Posted to {group['name']}!")
                
            except Exception as e:
                print(f"\t[-] Error posting to {group['name']}: {e}")

    def generate_cookie(self):
        self.page.goto("https://facebook.com")
        print("[*] A browser window is open. Please log into Facebook.")
        print("[*] I'll wait for you to log in automatically...")
        
        # Wait for URL to change from login page
        for i in range(300):  # 5 minutes max
            current = self.page.url
            if "login" not in current.lower() and "checkpoint" not in current.lower() and "facebook.com" in current.lower():
                print(f"[✓] Logged in detected! ({i+1}s)")
                break
            import time
            time.sleep(1)
            if i % 30 == 0:
                print(f"   Still waiting... ({i+1}s)")
        
        # Save cookies
        import os
        session_dir = f"{PROJECT_ROOT}/sessions"
        os.makedirs(session_dir, exist_ok=True)
        cookies = self.context.cookies()
        with open(f"{session_dir}/facebook-cookies.json", "w") as f:
            json.dump(cookies, f)
        print(f"[✓] Session saved! ({len(cookies)} cookies)")
        print("[*] Close the browser window to continue.")
        sys.exit(0)

    def load_cookie(self):
        print("[*] Loading saved session...")
        self.page.goto("https://facebook.com")
        self.page.wait_for_timeout(3000)
        print(f"[✓] Current page: {self.page.url[:60]}")

    def get_sources_list(self):
        with open(f"{PROJECT_ROOT}/groups.json", "r") as f:
            return json.load(f)


if __name__ == "__main__":
    mode = "COOKIE GENERATION" if FacebookGroupPoster.CREATE_SESSION else "POSTING"
    print(f"=== FB Group Poster: {mode} ===")
    print(f"Post content: {POST_CONTENT[:50]}...")
    FacebookGroupPoster()