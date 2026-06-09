#!/usr/bin/env python3
"""THE REAL ONE - Dismiss anonymous dialog, then post normally."""
import os, time
from selenium import webdriver

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
    
    # CLICK post box
    print("[*] Opening post composer...")
    driver.execute_script("""
        const btns = document.querySelectorAll('[role="button"]');
        for (const b of btns) {
            const t = b.textContent || '';
            if (t.includes('テキストを入力')) {
                b.click();
                return 'Clicked!';
            }
        }
        return 'Not found';
    """)
    time.sleep(3)
    
    # DISMISS anonymous dialog if present
    print("[*] Handling dialogs...")
    driver.execute_script("""
        // Click 'Cancel' on anonymous dialog if showing
        const allBtns = document.querySelectorAll('[role="button"]');
        for (const b of allBtns) {
            if (b.textContent.includes('キャンセル') || b.textContent.includes('Cancel')) {
                b.click();
                return 'Dismissed anonymous dialog';
            }
        }
        return 'No dialog to dismiss';
    """)
    time.sleep(2)
    
    # FILL content
    print("[*] Filling content...")
    result = driver.execute_script("""
        const editor = document.querySelector('[contenteditable="true"]');
        if (editor) {
            editor.focus();
            editor.textContent = '';
            document.execCommand('insertText', false, arguments[0]);
            return 'Content filled!';
        }
        // Try the div[role="dialog"] div[contenteditable]
        const inDialog = document.querySelector('div[role="dialog"] [contenteditable="true"]');
        if (inDialog) {
            inDialog.focus();
            inDialog.textContent = '';
            document.execCommand('insertText', false, arguments[0]);
            return 'Content filled in dialog!';
        }
        return 'No editor found';
    """, POST)
    print(f"[*] {result}")
    time.sleep(2)
    
    # CLICK Post button
    print("[*] Clicking Post...")
    result = driver.execute_script("""
        const btns = document.querySelectorAll('[role="button"]');
        for (const b of btns) {
            const label = b.getAttribute('aria-label') || '';
            if (label.includes('投稿') || label.includes('Post')) {
                b.click();
                return 'POSTED via aria-label!';
            }
        }
        // Try by text
        for (const b of btns) {
            const text = b.textContent || '';
            if (text.includes('投稿') && !text.includes('匿名')) {
                b.click();
                return 'POSTED via text!';
            }
        }
        // Submit the whole form
        const form = document.querySelector('form');
        if (form) { form.submit(); return 'Form submitted!'; }
        return 'No post button';
    """)
    print(f"[*] {result}")
    time.sleep(4)
    
    driver.save_screenshot("/home/rodorin/fb-auto-poster/screenshots/real_one.png")
    posted = "POSTED" in result
    status = "✅✅✅ POSTED SUCCESSFULLY!" if posted else "❌ Check screenshot"
    print(f"\n=== {status} ===")
    
    input("Press Enter...")
    driver.quit()

if __name__ == "__main__":
    main()