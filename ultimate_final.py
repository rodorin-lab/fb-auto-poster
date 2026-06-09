#!/usr/bin/env python3
"""THE ULTIMATE FINAL - Cancel anon, click again for normal post."""
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
    driver.get("https://www.facebook.com/groups/443644486582763/")
    time.sleep(6)
    
    # Step 1: Click post box (this opens anonymous dialog)
    print("[1/5] Clicking post box...")
    driver.execute_script("""
        const btns = document.querySelectorAll('[role="button"]');
        for (const b of btns) {
            const t = b.textContent || '';
            if (t.includes('テキストを入力') && !t.includes('匿名')) {
                b.click();
                return 'Clicked!';
            }
        }
        return 'Not found';
    """)
    time.sleep(2)
    
    # Step 2: Cancel the anonymous dialog
    print("[2/5] Cancelling anonymous dialog...")
    driver.execute_script("""
        // Find and click Cancel
        const btns = document.querySelectorAll('[role="button"]');
        for (const b of btns) {
            const t = b.textContent || '';
            if (t.includes('キャンセル') || t.includes('Cancel')) {
                const rect = b.getBoundingClientRect();
                if (rect.width > 0 && rect.height > 0) {
                    b.click();
                    return 'Cancelled!';
                }
            }
        }
        return 'No cancel found';
    """)
    time.sleep(2)
    
    # Step 3: NOW press keyboard shortcut 'p' to open NORMAL composer
    print("[3/5] Pressing 'p' keyboard shortcut for normal composer...")
    ActionChains(driver).send_keys('p').perform()
    time.sleep(3)
    
    # Step 4: Fill content in NORMAL composer
    print("[4/5] Writing content...")
    result = driver.execute_script("""
        const editor = document.querySelector('[contenteditable="true"]');
        if (editor) {
            editor.focus();
            editor.textContent = '';
            document.execCommand('insertText', false, arguments[0]);
            return 'Content filled!';
        }
        return 'No editor';
    """, POST)
    print(f"   {result}")
    time.sleep(2)
    
    # Step 5: Post
    print("[5/5] Posting...")
    result = driver.execute_script("""
        const btns = document.querySelectorAll('[role="button"]');
        for (const b of btns) {
            const label = b.getAttribute('aria-label') || '';
            if (label.includes('投稿') || label.includes('Post')) {
                const rect = b.getBoundingClientRect();
                if (rect.width > 0 && rect.height > 0) {
                    b.click();
                    return 'POSTED!';
                }
            }
        }
        return 'Button not found';
    """)
    print(f"   {result}")
    time.sleep(5)
    
    driver.save_screenshot("/home/rodorin/fb-auto-poster/screenshots/ultimate_final.png")
    posted = "POSTED" in result
    print(f"\n{'='*40}")
    print(f"{'✅✅✅ POSTED!' if posted else '❌ Failed'}")
    print(f"{'='*40}")
    print("\n[*] Browser stays open. Check it!")

if __name__ == "__main__":
    main()