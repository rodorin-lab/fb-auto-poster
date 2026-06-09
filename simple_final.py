#!/usr/bin/env python3
"""SIMPLE - Anonymous OFF, so just click+type+post. 3 steps."""
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
    
    # STEP 1: Click the post box (NO MORE anonymous dialog!)
    print("[1/3] Clicking post box...")
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
    time.sleep(4)  # Wait for composer to fully open
    
    # STEP 2: Find the editor and fill it
    print("[2/3] Filling content...")
    result = driver.execute_script("""
        // Get ALL contenteditable elements
        const editors = document.querySelectorAll('[contenteditable="true"]');
        console.log('Editors found:', editors.length);
        
        // Use the LAST one (the active composer)
        const editor = editors[editors.length - 1];
        if (editor && editor.isConnected) {
            editor.focus();
            // Clear existing content
            editor.innerHTML = '';
            // Insert text
            const text = arguments[0];
            // Use textContent for plain text
            editor.textContent = text;
            return 'FILLED: ' + text.substring(0, 20);
        }
        return 'NO EDITOR';
    """, POST)
    print(f"   {result}")
    time.sleep(3)
    
    # STEP 3: Find and click Post button
    print("[3/3] Clicking Post...")
    result = driver.execute_script("""
        // Look for Post button in the dialog
        const dialog = document.querySelector('[role="dialog"]');
        if (!dialog) return 'NO DIALOG';
        
        const btns = dialog.querySelectorAll('[role="button"]');
        for (const b of btns) {
            const label = b.getAttribute('aria-label') || '';
            const text = b.textContent || '';
            if (label.includes('投稿') || label.includes('Post') || text.includes('投稿')) {
                b.click();
                return 'POSTED!';
            }
        }
        // Try outside dialog too
        const allBtns = document.querySelectorAll('[role="button"]');
        for (const b of allBtns) {
            const label = b.getAttribute('aria-label') || '';
            if (label.includes('投稿') || label.includes('Post')) {
                b.click();
                return 'POSTED (outside dialog)!';
            }
        }
        return 'NO POST BUTTON';
    """)
    print(f"   {result}")
    time.sleep(5)
    
    # FINAL screenshot
    driver.save_screenshot("/home/rodorin/fb-auto-poster/screenshots/simple_result.png")
    
    # Check if it worked
    check = driver.execute_script("""
        const body = document.body.textContent;
        // If our post content appears in the feed, it worked!
        const phrases = body.split('ありがとう').length - 1;
        return 'ありがとう appears ' + phrases + ' times on page';
    """)
    print(f"\n🔍 Feed check: {check}")
    posted = "POSTED" in result or ('appears 2' in check)
    print(f"{'✅✅✅ SUCCESS!' if posted else '❌ Check screenshot'}")
    print("\n[*] Browser open. Check the group!")

if __name__ == "__main__":
    main()