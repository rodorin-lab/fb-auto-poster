#!/usr/bin/env python3
"""日本語グループ初投稿 - AIパワーアップ宣言 + 参加型ポスト"""
import os, time
from selenium import webdriver

PROFILE = os.path.expanduser("~/.config/google-chrome")

POST = """みなさん、お久しぶりです！🌟

このグループを再始動します！

実はここ数ヶ月、AIの世界にどっぷり浸かっていました。そして気づいたんです——AIって日本語学習の最強パートナーになるって。

たとえば：
📝 24時間いつでも添削してくれるAI先生
🗣️ 発音チェックしてくれるAI会話相手
📚 JLPT対策問題を無限に作れるAI

これからこのグループで、AIを使った新しい日本語学習のアイデアをどんどんシェアしていきます！

まずはみなさんに質問です👇

① 今の日本語レベルは？
② どんなコンテンツが見たい？（文法 / 会話 / JLPT対策 / アニメで学ぶ / AI活用法）

コメントで教えてください！一緒に楽しく学びましょう✨"""

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
    
    print("🚀 Launching Chrome...")
    driver = webdriver.Chrome(options=opts)
    driver.get("https://www.facebook.com/groups/443644486582763/")
    time.sleep(6)
    
    # STEP 1: Click the post box
    print("[1/3] Clicking post box...")
    result = driver.execute_script("""
        const btns = document.querySelectorAll('[role="button"]');
        for (const b of btns) {
            const t = b.textContent || '';
            if (t.includes('テキストを入力') || t.includes('Write something')) {
                b.click();
                return 'CLICKED';
            }
        }
        return 'NOT FOUND';
    """)
    print(f"   ✅ {result}")
    time.sleep(4)
    
    # STEP 2: Fill the editor using execCommand for React compatibility
    print("[2/3] Filling content...")
    result = driver.execute_script("""
        const editors = document.querySelectorAll('[contenteditable="true"]');
        const editor = editors[editors.length - 1];
        if (editor && editor.isConnected) {
            editor.focus();
            editor.innerHTML = '';
            document.execCommand('insertText', false, arguments[0]);
            return 'FILLED';
        }
        return 'NO EDITOR';
    """, POST)
    print(f"   ✅ {result}")
    time.sleep(3)
    
    # STEP 3: Post via Ctrl+Enter (most reliable)
    print("[3/3] Submitting via Ctrl+Enter...")
    driver.execute_script("""
        const editors = document.querySelectorAll('[contenteditable="true"]');
        const editor = editors[editors.length - 1];
        if (editor) {
            editor.focus();
            const e = new KeyboardEvent('keydown', {
                key: 'Enter', code: 'Enter', ctrlKey: true,
                bubbles: true, cancelable: true
            });
            editor.dispatchEvent(e);
            return 'SENT';
        }
        return 'FAIL';
    """)
    time.sleep(6)
    
    # FINAL check
    driver.save_screenshot("/home/rodorin/fb-auto-poster/screenshots/jl_first_post.png")
    
    check = driver.execute_script("""
        const body = document.body.textContent;
        const count = body.split('再始動').length - 1;
        return '再始動 appears ' + count + ' times on page';
    """)
    print(f"\n🔍 Feed check: {check}")
    print("✅ Done! Check the screenshot.")
    print("\n💡 Browser stays open — check the group!")

if __name__ == "__main__":
    main()
