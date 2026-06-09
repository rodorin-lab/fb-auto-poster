#!/usr/bin/env python3
"""REACT-FRIENDLY - Uses send_keys for React editor. Works with Facebook."""
import os, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PROFILE = os.path.expanduser("~/.config/google-chrome")
POST = "🌸 Today's Japanese Phrase\n\n「ありがとう」- Thank you\nA simple but powerful word. Use it every day! 🌟"

def main():
    for f in ["SingletonLock", "SingletonSocket", "SingletonCookie"]:
        p = f"{PROFILE}/{f}"
        if os.path.exists(p): os.remove(p)
    
    opts = webdriver.ChromeOptions()
    opts.add_argument(f"--user-data-dir={PROFILE}")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--start-maximized")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
    
    driver = webdriver.Chrome(options=opts)
    driver.get("https://www.facebook.com/groups/443644486582763/")
    time.sleep(6)
    
    # CLICK the post box to open composer
    print("[1/3] Opening composer...")
    driver.execute_script("""
        const btns = document.querySelectorAll('[role="button"]');
        for (const b of btns) {
            const t = b.textContent || '';
            if (t.includes('テキストを入力')) {
                b.click();
                return 'CLICKED';
            }
        }
        return 'NOT FOUND';
    """)
    time.sleep(4)
    
    # NOW use send_keys on the active contenteditable
    print("[2/3] Typing content with send_keys...")
    try:
        editor = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[contenteditable="true"]'))
        )
        editor.click()
        time.sleep(0.5)
        editor.send_keys(POST)
        print("   Content typed!")
    except Exception as e:
        print(f"   send_keys failed: {e}")
        # Fallback: try ActionChains
        from selenium.webdriver.common.action_chains import ActionChains
        actions = ActionChains(driver)
        actions.send_keys(POST)
        actions.perform()
        print("   Used ActionChains fallback")
    
    time.sleep(3)
    
    # CLICK Post button
    print("[3/3] Clicking Post...")
    result = driver.execute_script("""
        const btns = document.querySelectorAll('[role="button"]');
        for (const b of btns) {
            const label = b.getAttribute('aria-label') || '';
            if (label.includes('投稿') || label.includes('Post')) {
                b.click();
                return 'POSTED!';
            }
        }
        return 'NOT FOUND';
    """)
    print(f"   {result}")
    time.sleep(5)
    
    driver.save_screenshot("/home/rodorin/fb-auto-poster/screenshots/react_result.png")
    posted = "POSTED" in result
    status = "✅✅✅ POSTED!" if posted else "❌ Failed"
    print(f"\n{'='*30}")
    print(status)
    print(f"{'='*30}")
    print("\n[*] Browser open. Check the group!")

if __name__ == "__main__":
    main()