#!/usr/bin/env python3
"""KEYBOARD SHORTCUT + DIRECT URL approach. Bypasses anonymous dialog."""
import os, time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

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
    
    # METHOD A: Use the share dialog direct URL (opens post composer directly!)
    print("[*] Using direct share dialog URL...")
    # This URL opens the Facebook share dialog for the group
    driver.get(f"https://www.facebook.com/groups/443644486582763/?__cft__[0]=&__tn__=,O*F")
    time.sleep(3)
    
    # Press 'p' keyboard shortcut - Facebook's native shortcut for "create post"
    print("[*] Pressing 'p' keyboard shortcut...")
    ActionChains(driver).send_keys('p').perform()
    time.sleep(3)
    
    # Check if composer opened
    has_dialog = driver.execute_script("""
        return document.querySelector('[role="dialog"]') !== null;
    """)
    print(f"[*] Dialog open: {has_dialog}")
    
    if has_dialog:
        # Fill content
        driver.execute_script("""
            const editor = document.querySelector('[contenteditable="true"]');
            if (editor) {
                editor.focus();
                editor.textContent = '';
                document.execCommand('insertText', false, arguments[0]);
                return 'Filled!';
            }
            return 'No editor';
        """, POST)
        time.sleep(2)
        
        # Click Post
        driver.execute_script("""
            const btns = document.querySelectorAll('[role="button"]');
            for (const b of btns) {
                const label = b.getAttribute('aria-label') || '';
                if (label.includes('投稿') || label.includes('Post')) {
                    b.click();
                    return 'POSTED!';
                }
            }
            return 'No post button';
        """)
        time.sleep(4)
    
    # METHOD B: If 'p' didn't work, use keyboard shortcut Ctrl+Shift+P
    result = driver.execute_script("""
        return document.querySelector('[contenteditable="true"]') ? 'Editor exists' : 'No editor';
    """)
    print(f"[*] After keyboard: {result}")
    
    # METHOD C: Direct URL to composer (if nothing else works)
    if "No editor" in result:
        print("[*] Trying direct URL composer...")
        driver.get("https://www.facebook.com/sharer/sharer.php?u=https://www.facebook.com/groups/443644486582763/")
        time.sleep(3)
        
        # Type in the share box
        driver.execute_script("""
            const textarea = document.querySelector('textarea, [contenteditable="true"]');
            if (textarea) {
                textarea.focus();
                textarea.value = arguments[0];
                return 'Filled via share!';
            }
            return 'No share box';
        """, POST)
        time.sleep(2)
        
        # Click share
        driver.execute_script("""
            const btns = document.querySelectorAll('[role="button"]');
            for (const b of btns) {
                const t = b.textContent || '';
                if (t.includes('Share') || t.includes('投稿') || t.includes('シェア')) {
                    b.click();
                    return 'Shared!';
                }
            }
            return 'No share button';
        """)
        time.sleep(3)
    
    driver.save_screenshot("/home/rodorin/fb-auto-poster/screenshots/keyboard_approach.png")
    
    # Final check
    final = driver.execute_script("""
        const body = document.body.textContent;
        if (body.includes('ありがとう')) return 'ありがとう found on page - likely posted!';
        return 'Not found on page';
    """)
    print(f"\n✅ {final}")
    print("\n[*] Check the browser window!")

if __name__ == "__main__":
    main()