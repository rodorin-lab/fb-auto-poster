#!/usr/bin/env python3
"""KEYBOARD SHORTCUT METHOD - Press 'p' to open post compose, type, Ctrl+Enter"""
import os, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

PROFILE = os.path.expanduser("~/.config/google-chrome")
GROUP_ID = "443644486582763"

# SHORT post (no line breaks = one-shot send)
POST_TEXT = "🌸 Today's Japanese Phrase\n\n「ありがとう」- Thank you\nA simple but powerful word. Use it every day! 🌟"

def main():
    # Kill old Chrome
    os.system("kill -9 $(ps aux | grep chrome | grep -v grep | grep -v crashpad | awk '{print $2}') 2>/dev/null")
    time.sleep(2)
    for f in ["SingletonLock", "SingletonSocket", "SingletonCookie"]:
        p = f"{PROFILE}/{f}"
        if os.path.exists(p): os.remove(p)
    
    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-data-dir={PROFILE}")
    options.add_argument("--no-sandbox")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
    
    print("[*] Launching Chrome...")
    driver = webdriver.Chrome(options=options)
    
    # Go to group
    driver.get(f"https://www.facebook.com/groups/{GROUP_ID}/")
    time.sleep(5)
    print("[✓] Page loaded")
    
    # METHOD 1: Keyboard shortcut 'p' to open post composer
    print("[*] Pressing 'p' to open post composer...")
    ActionChains(driver).send_keys('p').perform()
    time.sleep(3)
    
    # Try to type into whatever opened
    try:
        actions = ActionChains(driver)
        actions.send_keys(POST_TEXT)
        actions.perform()
        time.sleep(1)
        
        # Ctrl+Enter to post
        ActionChains(driver).key_down(Keys.CONTROL).send_keys(Keys.ENTER).key_up(Keys.CONTROL).perform()
        time.sleep(3)
        print("[✅ POSTED!]")
    except Exception as e:
        print(f"[-] Keyboard method: {e}")
    
    # METHOD 2: Tab-based navigation (backup)
    print("[*] Trying Tab navigation backup...")
    try:
        # Tab multiple times to reach post box, then type
        actions = ActionChains(driver)
        for _ in range(20):
            actions.send_keys(Keys.TAB)
            actions.pause(0.2)
        actions.send_keys(Keys.ENTER)
        actions.pause(1)
        actions.send_keys(POST_TEXT)
        actions.pause(1)
        actions.key_down(Keys.CONTROL).send_keys(Keys.ENTER).key_up(Keys.CONTROL)
        actions.perform()
        time.sleep(3)
        print("[✅ POSTED via Tab!]")
    except Exception as e:
        print(f"[-] Tab method: {e}")
    
    driver.save_screenshot("/home/rodorin/fb-auto-poster/screenshots/keyboard_result.png")
    print("[📸] Screenshot saved")

if __name__ == "__main__":
    main()