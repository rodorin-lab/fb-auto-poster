#!/usr/bin/env python3
"""Post SCORPION BRAIN 38K-word mega article to coding4beginners group"""
import os, time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

PROFILE = os.path.expanduser("~/.config/google-chrome")
GROUP_URL = "https://www.facebook.com/groups/coding4beginners/"
ARTICLE_PATH = "/home/rodorin/fb-auto-poster/scorpion-brain-article-en.txt"

# Load the full article
with open(ARTICLE_PATH, "r") as f:
    POST_TEXT = f.read()

print(f"Article loaded: {len(POST_TEXT)} chars")

def main():
    # Clean up Chrome lock files
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
    
    print("[1/4] Navigating to coding4beginners...")
    driver.get(GROUP_URL)
    time.sleep(6)

    # STEP 1: Click the post box
    print("[2/4] Clicking post box...")
    clicked = driver.execute_script("""
        const btns = document.querySelectorAll('[role="button"]');
        for (const b of btns) {
            const t = b.textContent || '';
            if (t.includes('Write something') || t.includes('What') || t.includes('start') || t.includes('text')) {
                b.click();
                return 'CLICKED: ' + t.substring(0, 30);
            }
        }
        // Try div-based clickable areas
        const divs = document.querySelectorAll('div[role="button"]');
        for (const d of divs) {
            const t = d.textContent || '';
            if (t.includes('something') || t.includes('What')) {
                d.click();
                return 'CLICKED (div): ' + t.substring(0, 30);
            }
        }
        return 'NOT FOUND';
    """)
    print(f"   {clicked}")
    time.sleep(4)

    # STEP 2: Fill the FULL 38K article via execCommand
    print(f"[3/4] Filling {len(POST_TEXT)} chars...")
    result = driver.execute_script("""
        const editors = document.querySelectorAll('[contenteditable="true"]');
        const editor = editors[editors.length - 1];
        if (editor && editor.isConnected) {
            editor.focus();
            editor.innerHTML = '';
            document.execCommand('insertText', false, arguments[0]);
            return 'FILLED: ' + arguments[0].substring(0, 50) + '... (' + arguments[0].length + ' chars)';
        }
        return 'NO EDITOR';
    """, POST_TEXT)
    print(f"   {result}")
    time.sleep(4)

    # STEP 3: Post via Ctrl+Enter
    print("[4/4] Posting (Ctrl+Enter)...")
    body = driver.find_element("tag name", "body")
    body.send_keys(Keys.CONTROL + Keys.ENTER)
    print("   Ctrl+Enter sent!")
    time.sleep(8)

    # Screenshot
    driver.save_screenshot("/home/rodorin/fb-auto-poster/screenshots/coding4beginners_mega_post.png")
    
    # Check
    check = driver.execute_script("""
        const text = document.body.textContent;
        const count = (text.match(/SCORPION BRAIN/gi) || []).length;
        return 'SCORPION BRAIN appears ' + count + ' times on page';
    """)
    print(f"\nCheck: {check}")
    
    posted = "appears" in check and int(check.split("appears")[1].strip().split()[0]) >= 1
    print(f"{'SUCCESS! Mega article posted!' if posted else 'Check screenshot to confirm.'}")

    print("\nBrowser stays open for verification. Will close in 15 seconds...")
    time.sleep(15)
    driver.quit()

if __name__ == "__main__":
    main()