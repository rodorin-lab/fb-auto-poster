#!/usr/bin/env python3
"""Delete the last comment that was accidentally posted"""
import os, time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

PROFILE = os.path.expanduser("~/.config/google-chrome")
GROUP_URL = "https://www.facebook.com/groups/coding4beginners/"

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
    
    print("[1/3] Navigating to coding4beginners...")
    driver.get(GROUP_URL)
    time.sleep(6)

    # Find the comment we posted (contains "SCORPION BRAIN" in a comment context)
    print("[2/3] Looking for our comment...")
    
    # Find the comment's "..." menu and click it
    found = driver.execute_script("""
        // Look for our comment text
        const allText = document.querySelectorAll('[role="article"]');
        for (const article of allText) {
            const text = article.textContent || '';
            if (text.includes('SCORPION BRAIN') && text.includes('No Monthly Fees')) {
                // Find the "..." button in this article/comment
                const buttons = article.querySelectorAll('[role="button"]');
                for (const btn of buttons) {
                    const aria = btn.getAttribute('aria-label') || '';
                    if (aria.includes('More') || aria.includes('Action') || aria.includes('その他')) {
                        btn.click();
                        return 'CLICKED_MENU';
                    }
                }
            }
        }
        return 'NOT_FOUND';
    """)
    print(f"   Menu: {found}")
    time.sleep(3)

    # Click "Delete" in the dropdown
    print("[3/3] Clicking Delete...")
    deleted = driver.execute_script("""
        // Look for delete option in dropdown menu
        const menus = document.querySelectorAll('[role="menu"], [role="listbox"], [role="menu"]');
        for (const menu of menus) {
            const items = menu.querySelectorAll('[role="menuitem"]');
            for (const item of items) {
                const text = item.textContent || '';
                if (text.includes('Delete') || text.includes('Remove') || text.includes('削除')) {
                    item.click();
                    return 'CLICKED_DELETE: ' + text;
                }
            }
        }
        // Also try span-based menus
        const spans = document.querySelectorAll('span');
        for (const span of spans) {
            if (span.textContent === 'Delete' || span.textContent === 'Remove') {
                span.click();
                return 'CLICKED_DELETE_SPAN';
            }
        }
        return 'NOT_FOUND';
    """)
    print(f"   Delete: {deleted}")
    time.sleep(3)

    # Confirm delete if dialog appears
    confirmed = driver.execute_script("""
        const dialogs = document.querySelectorAll('[role="dialog"]');
        for (const d of dialogs) {
            const buttons = d.querySelectorAll('[role="button"]');
            for (const b of buttons) {
                if (b.textContent.includes('Delete') || b.textContent.includes('Remove') || b.textContent.includes('削除')) {
                    b.click();
                    return 'CONFIRMED_DELETE';
                }
            }
        }
        return 'NO_DIALOG';
    """)
    print(f"   Confirm: {confirmed}")
    time.sleep(5)

    driver.save_screenshot("/home/rodorin/fb-auto-poster/screenshots/deleted_comment.png")
    driver.quit()
    print("\nDone! Check screenshot to verify deletion.")

if __name__ == "__main__":
    main()