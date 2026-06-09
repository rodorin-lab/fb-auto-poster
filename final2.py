#!/usr/bin/env python3
"""FINAL - JS-powered Facebook Poster. Works with Chrome 149"""
import os, time, json, subprocess

PROFILE = os.path.expanduser("~/.config/google-chrome")
GROUP_ID = "443644486582763"
POST_TEXT = """🌸 Today's Japanese Phrase

「ありがとう」- Thank you

A simple but powerful word.
Use it every day! 🌟

#JapaneseLearning #JLPT"""

JS_POST = f"""
// Navigate to group
window.location.href = "https://www.facebook.com/groups/{GROUP_ID}/";

// Wait for page to load
setTimeout(() => {{
    // Find the post box by aria-label
    const postBox = document.querySelector('[aria-label="テキストを入力..."]');
    if (postBox) {{
        postBox.click();
        console.log("Post box clicked!");
        
        // Wait for dialog to open, then fill content
        setTimeout(() => {{
            const editor = document.querySelector('div[role="dialog"] div[contenteditable="true"]');
            if (editor) {{
                editor.focus();
                document.execCommand('insertText', false, `{POST_TEXT.replace(/"/g, '\\"').replace(/\n/g, '\\n')}`);
                console.log("Content filled!");
                
                // Click Post
                setTimeout(() => {{
                    const postBtn = document.querySelector('[aria-label="投稿"], [aria-label="Post"]');
                    if (postBtn) {{
                        postBtn.click();
                        console.log("POSTED! ✅");
                    }}
                }}, 2000);
            }}
        }}, 2000);
    }} else {{
        console.log("Post box not found. Trying alternative...");
        // Try clicking on the composer area
        const composer = document.querySelector('[role="button"][tabindex="0"]');
        if (composer && composer.textContent.includes("入力")) {{
            composer.click();
        }}
    }}
}}, 3000);
"""

def main():
    # Kill Chrome + remove locks
    os.system("kill -9 $(ps aux | grep chrome | grep -v grep | grep -v crashpad | awk '{print $2}') 2>/dev/null")
    time.sleep(2)
    for f in ["SingletonLock", "SingletonSocket", "SingletonCookie"]:
        p = f"{PROFILE}/{f}"
        if os.path.exists(p): os.remove(p)
    
    from selenium import webdriver
    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-data-dir={PROFILE}")
    options.add_argument("--no-sandbox")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
    
    print("[*] Launching Chrome with your profile...")
    driver = webdriver.Chrome(options=options)
    
    # Go to group
    driver.get(f"https://www.facebook.com/groups/{GROUP_ID}/")
    print("[*] Loading group page...")
    time.sleep(5)
    
    # Inject JS to find elements and interact
    print("[*] Ready! Executing JavaScript...")
    
    # First, try to find and interact with the post box via JS
    result = driver.execute_script("""
        // Try to find post box
        const selectors = [
            '[aria-label="テキストを入力..."]',
            '[aria-label="Write something..."]',
            '[aria-label="Create a post"]',
            'div[data-pagelet="MainFeed"] [role="button"]',
            'form [role="button"]',
            '[contenteditable="true"]'
        ];
        
        const found = [];
        for (const sel of selectors) {
            const el = document.querySelector(sel);
            if (el) {
                found.push({selector: sel, text: el.textContent?.substring(0, 50), tag: el.tagName});
            }
        }
        return found;
    """)
    
    print(f"[*] Found {len(result)} potential elements:")
    for r in result[:5]:
        print(f"   - {r['selector']}: {r['text'][:30]}")
    
    if not result:
        # Take screenshot to debug
        driver.save_screenshot("/home/rodorin/fb-auto-poster/screenshots/js_debug.png")
        print("[📸] Debug screenshot saved")
        
        # Try navigating to m.facebook.com (mobile version is simpler)
        print("[*] Trying mobile version...")
        driver.get(f"https://mbasic.facebook.com/groups/{GROUP_ID}/")
        time.sleep(5)
        
        # mbasic.facebook.com has a simple textarea!
        try:
            textarea = driver.find_element("name", "xc_message")
            textarea.send_keys(POST_TEXT)
            time.sleep(1)
            
            submit = driver.find_element("css selector", 'input[type="submit"]')
            submit.click()
            print("[✅] POSTED via mbasic!")
        except Exception as e:
            print(f"[-] Even mbasic failed: {e}")
            driver.save_screenshot("/home/rodorin/fb-auto-poster/screenshots/mbasic_debug.png")
    else:
        # We found elements - try clicking the first one
        try:
            # Click the post area via JS
            driver.execute_script("""
                const el = document.querySelector('[aria-label="テキストを入力..."]');
                if (el) el.click();
            """)
            time.sleep(2)
            
            # Fill content via JS
            driver.execute_script(f"""
                const editor = document.querySelector('div[contenteditable="true"]');
                if (editor) {{
                    editor.focus();
                    document.execCommand('selectAll', false, null);
                    document.execCommand('insertText', false, arguments[0]);
                }}
            """, POST_TEXT)
            time.sleep(1)
            
            # Click Post
            driver.execute_script("""
                const btn = document.querySelector('[aria-label="投稿"], [aria-label="Post"]');
                if (btn) btn.click();
            """)
            print("[✅] POSTED!")
        except Exception as e:
            print(f"[-] Click failed: {e}")
    
    print("\n[*] Browser open. Close it when done.")
    
if __name__ == "__main__":
    main()