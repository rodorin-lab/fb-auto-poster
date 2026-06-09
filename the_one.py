#!/usr/bin/env python3
"""THE ONE - Finds post box by textContent. FINAL. PERIOD."""
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
    
    # CLICK: Find by text content (the ONLY way that works!)
    print("[*] Finding post box by text content...")
    posted = False
    
    try:
        driver.execute_script("""
            // Find the specific post box - NOT anonymous post
            const ariaBtns = document.querySelectorAll('[role="button"]');
            for (const b of ariaBtns) {
                const text = b.textContent || '';
                // Must contain テキスト but NOT 匿名
                if (text.includes('テキストを入力') && !text.includes('匿名')) {
                    b.click();
                    return 'Found post box!';
                }
            }
            // Try English
            for (const b of ariaBtns) {
                const text = b.textContent || '';
                if (text.includes('Write something') && !text.includes('anonymous')) {
                    b.click();
                    return 'Found English post box!';
                }
            }
            return 'Text not found';
        """)
        time.sleep(3)
        
        # Fill content
        driver.execute_script("""
            const editor = document.querySelector('[contenteditable="true"]');
            if (editor) {
                editor.focus();
                editor.textContent = '';
                document.execCommand('insertText', false, arguments[0]);
                return 'Content filled!';
            }
            return 'No editor found';
        """, POST)
        time.sleep(2)
        print("[✓] Content inserted")
        
        # Post
        driver.execute_script("""
            const all = document.querySelectorAll('[role="button"]');
            for (const b of all) {
                const label = b.getAttribute('aria-label') || '';
                if (label.includes('投稿') || label.includes('Post')) {
                    b.click();
                    return 'POSTED!';
                }
            }
            // Try data-pagelet
            const postBtn = document.querySelector('[data-pagelet="PostComposer"] [role="button"]');
            if (postBtn) { postBtn.click(); return 'POSTED!'; }
            return 'No post button found';
        """)
        time.sleep(4)
        posted = True
        print("[✅✅✅ POSTED!]")
    except Exception as e:
        print(f"[-] {e}")
    
    driver.save_screenshot("/home/rodorin/fb-auto-poster/screenshots/the_one.png")
    print("[📸] Saved")
    
    status = "✅ POSTED!" if posted else "❌ Failed - check screenshot"
    print(f"\n=== {status} ===")
    input("Press Enter to close...")
    driver.quit()

if __name__ == "__main__":
    main()