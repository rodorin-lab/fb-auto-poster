#!/usr/bin/env python3
"""FB Auto Poster - Selenium with REAL Chrome profile + m.facebook.com"""
import os, time, json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

PROFILE = os.path.expanduser("~/.config/google-chrome")
POST_TEXT = """🌸 Today's Japanese Phrase

「ありがとう」- Thank you

A simple but powerful word.
Use it every day! 🌟

#JapaneseLearning #JLPT"""

def main():
    # Kill existing Chrome
    os.system("kill -9 $(ps aux | grep chrome | grep -v grep | grep -v crashpad | awk '{print $2}') 2>/dev/null")
    time.sleep(2)
    
    # Remove lock files
    for f in ["SingletonLock", "SingletonSocket", "SingletonCookie"]:
        p = f"{PROFILE}/{f}"
        if os.path.exists(p):
            os.remove(p)
    
    # Setup Chrome with REAL profile
    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-data-dir={PROFILE}")
    options.add_argument("--no-sandbox")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    
    print("[*] Starting Chrome with your REAL profile...")
    print(f"[*] Profile: {PROFILE}")
    driver = webdriver.Chrome(options=options)
    
    # Navigate to mobile Facebook group (simpler UI)
    GROUP_URL = "https://m.facebook.com/groups/443644486582763/"
    print(f"[*] Navigating to group...")
    driver.get(GROUP_URL)
    time.sleep(5)
    
    # Take screenshot
    driver.save_screenshot("/home/rodorin/fb-auto-poster/screenshots/selenium_status.png")
    
    # Check if logged in
    if "login" in driver.current_url.lower():
        print("[!] NOT LOGGED IN!")
        print("[*] Browser is open - please log in manually")
        print("[*] Waiting up to 5 minutes...")
        for i in range(300):
            time.sleep(1)
            if "login" not in driver.current_url.lower():
                print(f"[✓] Logged in! ({i+1}s)")
                break
            if i % 30 == 0:
                print(f"   Waiting... ({i+1}s)")
    
    # Try to find the post box
    print("[*] Looking for post box...")
    try:
        # Desktop: aria-label
        post_box = driver.find_element(By.CSS_SELECTOR, '[aria-label="テキストを入力..."]')
        post_box.click()
        time.sleep(2)
        
        # Find the actual text input
        editor = driver.find_element(By.CSS_SELECTOR, 'div[contenteditable="true"]')
        editor.send_keys(POST_TEXT)
        time.sleep(1)
        
        # Post
        post_btn = driver.find_element(By.CSS_SELECTOR, '[aria-label="投稿"]')
        post_btn.click()
        print(f"[✓] POSTED!")
    except Exception as e:
        print(f"[-] Desktop selectors failed: {e}")
        
        # Try mobile version selectors
        try:
            print("[*] Trying mobile selectors...")
            textarea = driver.find_element(By.NAME, "xc_message")
            textarea.send_keys(POST_TEXT)
            time.sleep(1)
            
            submit_btn = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
            submit_btn.click()
            print(f"[✓] POSTED via mobile!")
        except Exception as e2:
            print(f"[-] Mobile selectors also failed: {e2}")
            driver.save_screenshot("/home/rodorin/fb-auto-poster/screenshots/debug_selenium.png")
            print(f"[📸] Debug screenshot saved")
    
    print("\n[*] Browser stays open. Close it when done.")
    input("Press Enter to close browser...")
    driver.quit()

if __name__ == "__main__":
    os.makedirs("/home/rodorin/fb-auto-poster/screenshots", exist_ok=True)
    main()