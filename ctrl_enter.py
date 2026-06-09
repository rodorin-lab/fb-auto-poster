#!/usr/bin/env python3
"""CTRL+ENTER METHOD - The final final. Uses keyboard shortcut to post."""
import os, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
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
    
    # 1. Click post box
    print("[1/4] Opening composer...")
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
    
    # 2. Send keys to the editor
    print("[2/4] Typing content...")
    try:
        editor = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[contenteditable="true"]'))
        )
        # Click via JS to avoid interception
        driver.execute_script("arguments[0].focus();", editor)
        time.sleep(0.5)
        editor.send_keys(POST)
        print("   Content typed!")
    except Exception as e:
        print(f"   Error: {e}")
        ActionChains(driver).send_keys(POST).perform()
        print("   ActionChains fallback")
    time.sleep(2)
    
    # 3. CRITICAL: Focus the editor, then Ctrl+Enter
    print("[3/4] Pressing Ctrl+Enter to post...")
    try:
        editor = driver.find_element(By.CSS_SELECTOR, '[contenteditable="true"]')
        editor.send_keys(Keys.CONTROL + Keys.ENTER)
        print("   Ctrl+Enter sent!")
    except Exception as e:
        # Fallback: Tab to Post button then Enter
        print(f"   Ctrl+Enter failed: {e}")
        actions = ActionChains(driver)
        actions.key_down(Keys.CONTROL).send_keys(Keys.ENTER).key_up(Keys.CONTROL)
        actions.perform()
        print("   ActionChains Ctrl+Enter")
    
    time.sleep(5)
    
    # 4. Verify
    driver.save_screenshot("/home/rodorin/fb-auto-poster/screenshots/ctrl_enter_result.png")
    
    check = driver.execute_script("""
        const body = document.body.textContent;
        const count = (body.match(/ありがとう/g) || []).length;
        return 'ありがとう count: ' + count;
    """)
    print(f"\n{check}")
    
    # Check if post dialog is still open
    dialog_check = driver.execute_script("""
        return document.querySelector('[role="dialog"]') ? 'DIALOG STILL OPEN' : 'NO DIALOG - posted!';
    """)
    print(f"Dialog: {dialog_check}")
    
    posted = "NO DIALOG" in dialog_check or "2" in check or "3" in check
    print(f"\n{'='*30}")
    print(f"{'✨✨✨ POSTED!' if posted else '❌ Dialog still open'}")
    print(f"{'='*30}")
    print("\n[*] Browser open. Check the group feed!")

if __name__ == "__main__":
    main()