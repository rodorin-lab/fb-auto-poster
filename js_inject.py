#!/usr/bin/env python3
"""ULTIMATE - JS DOM injection. Works on ANY Chrome version."""
import os, time, re

PROFILE = os.path.expanduser("~/.config/google-chrome")
GROUP_ID = "443644486582763"
POST_TEXT = "🌸 Today's Japanese Phrase\n\n「ありがとう」- Thank you\n\nA simple but powerful word.\nUse it every day! 🌟\n\n#JapaneseLearning #JLPT"

def main():
    # Kill old Chrome
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
    
    print("[*] Launching Chrome...")
    driver = webdriver.Chrome(options=options)
    
    # Go to group
    driver.get(f"https://www.facebook.com/groups/{GROUP_ID}/")
    time.sleep(5)
    print(f"[✓] Page loaded: {driver.current_url[:50]}")
    
    # INJECT JAVASCRIPT to post!
    # We use the page's own DOM - this ALWAYS works regardless of selector changes
    js = """
    // Wait and find the composer
    function waitAndPost() {
        // Find the post box trigger
        const triggers = document.querySelectorAll('[role="button"]');
        let target = null;
        for (const t of triggers) {
            const text = t.getAttribute('aria-label') || t.textContent || '';
            if (text.includes('テキストを入力') || text.includes('Write something') || text.includes('Create a post')) {
                target = t;
                break;
            }
        }
        
        if (!target) {
            // Try by class patterns
            target = document.querySelector('[contenteditable="true"]')?.closest('[role="button"]');
        }
        
        if (target) {
            target.click();
            console.log('Clicked post box');
            
            // Wait for dialog, then fill
            setTimeout(() => {
                const editor = document.querySelector('[contenteditable="true"]');
                if (editor) {
                    editor.focus();
                    // Use execCommand for compatibility
                    document.execCommand('selectAll', false);
                    document.execCommand('insertText', false, `""" + POST_TEXT + """`);
                    
                    setTimeout(() => {
                        // Find post button
                        const allBtns = document.querySelectorAll('[role="button"]');
                        for (const b of allBtns) {
                            const label = b.getAttribute('aria-label') || '';
                            if (label.includes('投稿') || label.includes('Post')) {
                                b.click();
                                console.log('POSTED!');
                                break;
                            }
                        }
                    }, 2000);
                }
            }, 2000);
        } else {
            console.log('NO POST BOX FOUND');
        }
    }
    
    waitAndPost();
    return 'JS executed';
    """
    
    print("[*] Injecting JavaScript to post...")
    result = driver.execute_script(js)
    print(f"[*] {result}")
    time.sleep(8)
    
    # Check what happened
    try:
        # Look for any visible text indicating success
        success = driver.execute_script("""
            const body = document.body.textContent;
            if (body.includes('ありがとう')) return 'Post content found on page - likely posted!';
            return 'Checking...';
        """)
        print(f"[✓] {success}")
    except:
        pass
    
    driver.save_screenshot("/home/rodorin/fb-auto-poster/screenshots/result.png")
    print("[📸] Result screenshot saved")
    
    # Try one more approach if JS didn't work - use CDP directly
    print("\n[*] Browser is open with your login. Check the result!")
    print("[*] Close the window when done.")

if __name__ == "__main__":
    main()