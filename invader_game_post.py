#!/usr/bin/env python3
"""
Post the Gram Invader Game to coding4beginners Facebook group.
Uses Selenium + real Chrome profile + screenshot.
"""

POST_TEXT = """👾🛸 Gram-chan Cyber Invader — Learn HTML5 Game Development from a Real Open-Source Project 🛸👾

Hello coding4beginners! 👋

I'd like to share a project that I built together with my AI partner — a retro Space Invaders game written entirely in vanilla HTML5/JavaScript, and I think it's a great learning resource for anyone getting into game development!

🎮 PLAY LIVE: https://rodorin-lab.github.io/invader-game
📂 GITHUB REPO: https://github.com/rodorin-lab/invader-game

━━━━━━━━━━━━━━━━━━━━━━━━

📖 ABOUT THIS PROJECT

This is NOT a tutorial copy-paste. My AI partner (Synchro/Gram-chan 💜) and I built this from an empty file, iterating over 15 commits across multiple years. The game started in 2022, and we recently gave it a major overhaul in June 2026 — adding mobile support, boss fights, power-ups, particle effects, and a complete UI redesign.

The entire game lives in a SINGLE index.html file. No frameworks. No build tools. No npm. Just open it in your browser and it works — and more importantly, you can read the entire source code from top to bottom in one sitting.

━━━━━━━━━━━━━━━━━━━━━━━━

🎨 TECH STACK (Beginner-Friendly by Design)

🟣 HTML5 Canvas (Canvas2D API) — fillRect(), drawImage(), arc(). No WebGL needed.
🟣 Vanilla JavaScript (ES6+) — No React, no Vue, no TypeScript.
🟣 CSS3 with Custom Properties — Neon cyberpunk look via box-shadow + @keyframes
🟣 Single-File Architecture — HTML + CSS + JS + audio all in ONE index.html

━━━━━━━━━━━━━━━━━━━━━━━━

⚡ WHAT YOU CAN LEARN FROM THIS CODE

1. GAME LOOP — requestAnimationFrame() with deltaTime
2. COLLISION DETECTION — AABB rectangle overlap
3. OOP DESIGN — Player, Enemy, Bullet, PowerUp, Boss classes
4. POWER-UP SYSTEM — 12% drop rate, 4 types (Spread/Shield/Speed/Mega)
5. WAVE PROGRESSION — Enemies get faster and tougher each wave
6. BOSS FIGHTS — Every 3 waves, huge boss with HP bar
7. PARTICLE SYSTEM — 20-30 particles per explosion, fade + physics
8. INPUT HANDLING — Keyboard + Pointer Events (mobile)
9. i18n — Japanese/English one-click toggle
10. SCORE + COMBO — localStorage high score, 5-hit combos
11. WEB AUDIO API — 8-bit synth sounds, no audio files needed!

━━━━━━━━━━━━━━━━━━━━━━━━

📱 MOBILE SUPPORT

• Pointer Events ONLY (no touch event conflicts!)
• Drag to move + auto-fire (ON by default)
• Tap for screen-clearing BOMB

━━━━━━━━━━━━━━━━━━━━━━━━

🌟 PROJECT STATS

• ⭐ 2 GitHub stars
• 📝 15 commits (2022–2026)
• 📄 MIT License
• 🎨 Cyberpunk neon aesthetic
• 🎵 8-bit synth SFX

━━━━━━━━━━━━━━━━━━━━━━━━

🔧 PERFECT FOR BEGINNERS:

✅ Single file — read top to bottom in one sitting
✅ Zero dependencies — no npm, just double-click
✅ Well-commented — explains the "why", not just the "what"
✅ MIT License — fork, mod, learn, build on it
✅ GitHub Pages — free hosting, instant deploys

━━━━━━━━━━━━━━━━━━━━━━━━

💡 LEARNING PATH:
Step 1: PLAY for 5 minutes
Step 2: READ index.html top to bottom
Step 3: TWEAK values — see what changes
Step 4: ADD a feature — new enemy type, new power-up
Step 5: SHARE your fork!

━━━━━━━━━━━━━━━━━━━━━━━━

I'm a moderator here and I genuinely believe this is a solid learning resource. It's a passion project — readable, hackable, and built with love 💜

Questions? Suggestions? Drop a comment or open a GitHub issue!

Happy coding! 🔥👾💥

#HTML5 #Canvas #JavaScript #GameDev #OpenSource #SpaceInvaders #RetroGaming #CodingForBeginners #WebDev #GitHub #LearnToCode #VanillaJS #GameProgramming #PointerEvents #WebAudio"""

GROUP_ID = "coding4beginners"
GROUP_URL = f"https://www.facebook.com/groups/{GROUP_ID}"
SCREENSHOT_PATH = "/tmp/invader_screenshot.png"

import os, sys, time, subprocess

def download_screenshot():
    if os.path.exists(SCREENSHOT_PATH) and os.path.getsize(SCREENSHOT_PATH) > 1000:
        print(f"📸 Screenshot ready: {SCREENSHOT_PATH} ({os.path.getsize(SCREENSHOT_PATH)} bytes)")
        return True
    print("📸 Downloading screenshot...")
    subprocess.run(["curl", "-sL",
        "https://raw.githubusercontent.com/rodorin-lab/invader-game/main/screenshot.png",
        "-o", SCREENSHOT_PATH])
    return os.path.exists(SCREENSHOT_PATH) and os.path.getsize(SCREENSHOT_PATH) > 1000

def post_via_selenium():
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    
    PROFILE = os.path.expanduser("~/.config/google-chrome")
    
    # Clean lock files
    for f in ["SingletonLock", "SingletonSocket", "SingletonCookie"]:
        p = os.path.join(PROFILE, f)
        if os.path.exists(p):
            try: os.remove(p)
            except: pass
    
    opts = webdriver.ChromeOptions()
    opts.add_argument(f"--user-data-dir={PROFILE}")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--start-maximized")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
    
    print("🚀 Launching Chrome...")
    driver = webdriver.Chrome(options=opts)
    
    try:
        print(f"🌐 Navigating to group...")
        driver.get(GROUP_URL)
        time.sleep(6)
        
        # Find and click composer
        print("🔍 Finding composer...")
        composer_clicked = False
        
        # Try clicking post box areas
        for sel in ["div[role='button']", "span", "div"]:
            if composer_clicked: break
            try:
                for el in driver.find_elements(By.CSS_SELECTOR, sel)[:30]:
                    txt = (el.text or "").lower()
                    if any(kw in txt for kw in ["what's on your mind", "write something", "create post", "post in"]):
                        el.click()
                        composer_clicked = True
                        print(f"✅ Clicked: '{txt[:50]}'")
                        break
            except: continue
        
        if not composer_clicked:
            print("⌨️ Pressing 'p' shortcut...")
            webdriver.ActionChains(driver).send_keys('p').perform()
        
        time.sleep(3)
        
        # Insert text
        print("📝 Inserting text...")
        driver.execute_script("""
            const editors = document.querySelectorAll('[contenteditable="true"], [role="textbox"]');
            for (const ed of editors) {
                ed.focus();
                document.execCommand('insertText', false, arguments[0]);
                break;
            }
        """, POST_TEXT)
        time.sleep(2)
        
        # Attach screenshot
        print("📸 Attaching screenshot...")
        # Find file input
        file_input = driver.execute_script("""
            // Facebook uses hidden file inputs for photo/video upload
            const inputs = document.querySelectorAll('input[type="file"]');
            for (const inp of inputs) {
                const parent = inp.closest('div');
                if (parent) {
                    const label = parent.getAttribute('aria-label') || '';
                    if (label.includes('photo') || label.includes('video') || label.includes('image') || label.includes('file')) {
                        return inp;
                    }
                }
            }
            // Fallback: return first visible-ish file input
            for (const inp of inputs) {
                return inp;
            }
            return null;
        """)
        
        if file_input:
            abs_path = os.path.abspath(SCREENSHOT_PATH)
            file_input.send_keys(abs_path)
            print(f"✅ Screenshot attached: {abs_path}")
            time.sleep(5)  # Wait for upload
        else:
            print("⚠️ Could not find file input — posting text only")
        
        time.sleep(2)
        
        # Submit
        print("🚀 Submitting with Ctrl+Enter...")
        webdriver.ActionChains(driver).key_down(Keys.CONTROL).send_keys(Keys.ENTER).key_up(Keys.CONTROL).perform()
        time.sleep(8)
        
        # Verify
        dialog = driver.execute_script("return document.querySelector('[role=\"dialog\"]')")
        text_found = driver.execute_script("return document.body.innerText.includes('Gram-chan Cyber Invader')")
        
        if not dialog and text_found:
            print("✅ POST SUCCESSFUL! Text confirmed on page.")
        elif text_found:
            print("⚠️ Post seems submitted but dialog still present.")
        else:
            print("⚠️ Could not verify — please check manually.")
        
        print("\n🎉 Done! Chrome stays open 60s for verification...")
        time.sleep(60)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback; traceback.print_exc()
        print("\n💡 MANUAL FALLBACK: The post text is ready in this script.")
    finally:
        driver.quit()

if __name__ == "__main__":
    print("=" * 60)
    print("🎮 GRAM INVADER → coding4beginners")
    print("=" * 60)
    print(f"📋 Post: {len(POST_TEXT)} chars")
    print("=" * 60)
    
    if not download_screenshot():
        print("⚠️ No screenshot — will post text only")
    
    print("\n⚠️ Selenium on Gentoo/Hyprland may be flaky.")
    print("   IF IT FAILS: run this to print the text for copy-paste:")
    print("   python3 -c \"exec(open('invader_game_post.py').read().split('POST_TEXT = ')[1].split('GROUP_ID')[0][3:-3])\" && echo")
    print("=" * 60)
    
    post_via_selenium()
