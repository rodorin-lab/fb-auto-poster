#!/usr/bin/env python3
"""NO EMOJI - Pure ASCII/BMP only. Works with ChromeDriver."""
import os, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PROFILE = os.path.expanduser("~/.config/google-chrome")

# NO emoji - pure BMP characters only!
POST = 'Today\'s Japanese Phrase\n\n"Arigatou" - Thank you\n\nA simple but powerful word.\nUse it every day!\n\n#JapaneseLearning #JLPT'

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
    
    # 2. Fill content - use JS innerText (no emoji, safe!)
    print("[2/3] Filling content...")
    driver.execute_script("""
        const editors = document.querySelectorAll('[contenteditable="true"]');
        const editor = editors[editors.length - 1];
        if (editor) {
            editor.focus();
            // Clear first
            editor.innerHTML = '';
            // Set text content (no emoji = no BMP issues)
            editor.textContent = arguments[0];
            return 'FILLED';
        }
        return 'NO EDITOR';
    """, POST)
    time.sleep(2)
    
    # 3. Click Post inside the dialog - more specific
    print("[3/3] Clicking Post...")
    result = driver.execute_script("""
        const dialog = document.querySelector('[role="dialog"]');
        if (!dialog) return 'NO DIALOG';
        
        // Get ALL buttons in the dialog
        const btns = dialog.querySelectorAll('[role="button"]');
        console.log('Buttons in dialog:', btns.length);
        
        for (const b of btns) {
            const label = b.getAttribute('aria-label') || '';
            const text = b.textContent || '';
            // Look for exact match on the Post button
            if (label === '投稿' || label === 'Post' || 
                (label.includes('投稿') && text.trim() === '')) {
                b.click();
                return 'POSTED!';
            }
        }
        // Last resort: find by text content
        for (const b of btns) {
            const text = b.textContent.trim();
            if (text === '投稿' || text === 'Post') {
                b.click();
                return 'POSTED by text!';
            }
        }
        // Check if it's a form submit button
        const submitBtn = dialog.querySelector('[type="submit"]');
        if (submitBtn) { submitBtn.click(); return 'POSTED form!'; }
        
        return 'NO POST BTN. Total btns: ' + btns.length;
    """)
    print(f"   {result}")
    time.sleep(5)
    
    # Verify
    driver.save_screenshot("/home/rodorin/fb-auto-poster/screenshots/no_emoji.png")
    
    check = driver.execute_script("""
        const dialog = document.querySelector('[role="dialog"]');
        return dialog ? 'DIALOG STILL OPEN' : 'POSTED - no dialog!';
    """)
    print(f"\n{check}")
    posted = "POSTED" in result or "no dialog" in check.lower()
    print(f"{'✅✅✅ SUCCESS!' if posted else '❌ Failed'}")
    print("\n[*] Check the browser window!")

if __name__ == "__main__":
    main()