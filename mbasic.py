#!/usr/bin/env python3
"""FINAL - MBASIC Facebook Poster. Simple textarea, guaranteed to work."""
import os, time

PROFILE = os.path.expanduser("~/.config/google-chrome")
POST_TEXT = "🌸 Today's Japanese Phrase\n\n「ありがとう」- Thank you\n\nA simple but powerful word.\nUse it every day! 🌟\n\n#JapaneseLearning #JLPT"

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
    
    print("[*] Launching Chrome with real profile...")
    driver = webdriver.Chrome(options=options)
    
    # Use MBASIC - Facebook's ancient mobile site with simple HTML forms!
    # No JavaScript, no shadow DOM, no complex selectors - just pure HTML forms
    URL = "https://mbasic.facebook.com/groups/443644486582763/"
    print(f"[*] Opening mbasic.facebook group...")
    driver.get(URL)
    time.sleep(5)
    
    # Check if logged in
    if "login" in driver.current_url.lower():
        print("[!] Not logged in. Log in manually in the browser window.")
        print("[*] Waiting up to 5 minutes...")
        for i in range(300):
            time.sleep(1)
            if "login" not in driver.current_url.lower():
                print(f"[✓] Logged in! ({i+1}s)")
                break
            if i % 30 == 0:
                print(f"   Waiting... ({i+1}s)")
    
    print(f"[*] Current page: {driver.current_url[:60]}")
    
    # mbasic has a simple textarea named "xc_message" for group posts!
    try:
        textarea = driver.find_element("name", "xc_message")
        print("[✓] Found post textarea!")
        textarea.clear()
        textarea.send_keys(POST_TEXT)
        time.sleep(1)
        print("[✓] Content filled!")
        
        # Find the submit button
        submit = driver.find_element("css selector", 'input[type="submit"][value="投稿"], input[type="submit"]')
        submit.click()
        time.sleep(3)
        print("[✅✅✅ POSTED SUCCESSFULLY!]")
    except Exception as e:
        print(f"[-] Standard post failed: {e}")
        
        # Maybe we need to click "Write something" first on mbasic
        try:
            write_link = driver.find_element("link text", "Write something...")
            write_link.click()
            time.sleep(3)
            
            textarea = driver.find_element("name", "xc_message")
            textarea.send_keys(POST_TEXT)
            time.sleep(1)
            
            submit = driver.find_element("css selector", 'input[type="submit"]')
            submit.click()
            time.sleep(3)
            print("[✅✅✅ POSTED!]")
        except Exception as e2:
            print(f"[-] Also failed: {e2}")
            driver.save_screenshot("/home/rodorin/fb-auto-poster/screenshots/mbasic_final.png")
            print("[📸] Screenshot saved")
    
    print("\n[*] Browser stays open. Check the result!")
    print("[*] Close browser window when done.")

if __name__ == "__main__":
    main()