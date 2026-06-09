#!/usr/bin/env python3
"""THE FINAL - Cancel anonymous dialog, then post like a boss."""
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
    
    # STEP 1: Click post box
    print("[1/4] Opening post composer...")
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
    time.sleep(3)
    
    # STEP 2: Cancel anonymous dialog if it shows up
    print("[2/4] Dismissing anonymous dialog if present...")
    driver.execute_script("""
        // Look for Cancel button in any visible dialog
        const btns = document.querySelectorAll('[role="button"]');
        let found = false;
        for (const b of btns) {
            const t = b.textContent || '';
            const a = b.getAttribute('aria-label') || '';
            // Cancel buttons
            if (t.includes('キャンセル') || t.includes('Cancel') || a.includes('キャンセル') || a.includes('Cancel')) {
                // Make sure it's actually visible
                const rect = b.getBoundingClientRect();
                if (rect.width > 0 && rect.height > 0) {
                    b.click();
                    found = true;
                    return 'Cancelled anonymous dialog!';
                }
            }
        }
        if (!found) {
            // Try looking for "通常の投稿" or "Normal post" option
            for (const b of btns) {
                const t = b.textContent || '';
                if (t.includes('通常') || t.includes('Normal') || t.includes('public')) {
                    const rect = b.getBoundingClientRect();
                    if (rect.width > 0 && rect.height > 0) {
                        b.click();
                        return 'Clicked normal post option!';
                    }
                }
            }
        }
        return 'No dialog found - already in normal composer!';
    """)
    time.sleep(3)
    
    # STEP 3: Fill content
    print("[3/4] Writing post content...")
    result = driver.execute_script("""
        // Find the active editor
        const editor = document.querySelector('[contenteditable="true"]');
        if (editor && editor.isConnected) {
            editor.focus();
            editor.textContent = '';
            document.execCommand('insertText', false, arguments[0]);
            return 'Content filled!';
        }
        return 'No editor found';
    """, POST)
    print(f"   {result}")
    time.sleep(2)
    
    # STEP 4: Click Post
    print("[4/4] Clicking Post button...")
    result = driver.execute_script("""
        const btns = document.querySelectorAll('[role="button"]');
        for (const b of btns) {
            const label = b.getAttribute('aria-label') || '';
            if (label.includes('投稿') || label.includes('Post')) {
                b.click();
                return 'POSTED!';
            }
        }
        // Try finding submit in the dialog
        const dialog = document.querySelector('[role="dialog"]');
        if (dialog) {
            const dlgBtns = dialog.querySelectorAll('[role="button"]');
            for (const b of dlgBtns) {
                const t = b.textContent || '';
                if (t.includes('投稿') || t.includes('Post') || t.includes('Share')) {
                    b.click();
                    return 'POSTED via dialog!';
                }
            }
        }
        return 'Post button not found';
    """)
    print(f"   {result}")
    time.sleep(5)
    
    # Verify
    driver.save_screenshot("/home/rodorin/fb-auto-poster/screenshots/final_result.png")
    posted = "POSTED" in result
    print(f"\n{'='*40}")
    print(f"{'✅✅✅ POSTED SUCCESSFULLY!' if posted else '❌ Check screenshot'}")
    print(f"{'='*40}")
    
    # Don't close - let user see
    print("\n[*] Browser stays open. Check the group feed!")
    print("[*] Close the window when done.")

if __name__ == "__main__":
    main()