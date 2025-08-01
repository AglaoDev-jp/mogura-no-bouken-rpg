# scenes/endroll.py
import pygame
from pathlib import Path

state = {
    "y": 650,
    "finished": False,
    "bg": None,  # 背景画像を保持
    "fading": False  # BGMフェードアウト済み管理用
}

CREDITS = [
    " ~ もぐらの冒険RPG ~ ",
    "",
    " 制作",
    "",
    " プログラム・シナリオ： ",
    " AglaoDev-jp, ChatGPT（AI）",
    "",
    " 画像作成：",
    " ChatGPT 画像生成",
    " Microsoft ペイント",
    "",
    " 使用素材（敬称略）",
    "",
    " 音楽：",
    " フリーBGM DOVA-SYNDROME",
    "",
    "【使用楽曲】",
    "[町,会話シーン] お昼のうた shimtone",
    "[道具屋 宿屋] 昼下がりのおやつ shimtone",
    "[メニュー画面] 起きたくない朝 shimtone",
    "[お城] 私の部屋 Heitaro Ashibe",
    "[ダンジョン] Royal_Question shimtone",
    "[戦闘曲] Slapstick_Dance shimtone",
    "[ラストバトル] Nisemono_Rock shimtone",
    "",        
    " 効果音：",
    " 効果音ラボ",
    "",
    " 音声作成：",
    " CoeFont（コエフォント）",
    " Voiced by https://CoeFont.cloud ",
    " Standardプランを使用 ",
    "",
    "【使用音声】",
    "[ナレーション] あかね大佐*",
    "[王様、宿屋、ショップ] Canel（CV: 森川智之）",
    "[ごちみみず] Ailis Voice 日本語",
    "[しゅごもぐら] パイナップル秀夫お姉さん",
    "[もぐら] ひろゆき",
    "",
    " フォント：",
    " Noto Sans JP",
    " © 2014–2025 Google LLC",
    " licensed under SIL Open Font License, Version 1.1. ",
    "",
    " 使用言語 ",
    "",
    " Python 3.12.5",
    " Copyright © 2001 Python Software Foundation. ",
    " All rights reserved. ",
    "",
    " 外部ライブラリ ",
    "",
    " Pygame",
    " © 2000–2024 Pygame developers ",
    "",
    " 実行ファイル作成：",
    " PyInstaller",
    " Copyright(c)2010–2023,PyInstaller Development Team",
    " Copyright(c)2005–2009,Giovanni Bajo",
    " Based on work(c)2002, McMillan Enterprises,Inc.",
    "",
    " 暗号化：",
    " cryptography ",
    " Copyright (c) Individual contributors. All rights reserved. ",
    "",
    " OpenSSL 3.4.0 ",
    " Copyright (c) 1998-2025 The OpenSSL Project Authors ",
    " Copyright (c) 1995-1998 Eric A. Young, Tim J. Hudson ",
    " All rights reserved. ",
    "",
    " 難読化： ",
    " Cython ",
    " © 2007-2025 The Cython Project Developers ",
    "",
    " 標準モジュール",
    "",
    " os ",
    " pathlib ",
    " sys",
    " copy",
    " traceback",
    " json",
    "",
    " 使用エディター：",
    " Visual Studio Code（VSC）",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    " Thank you for playing!!",
    " Version 2.0（2025年7月）",
    "",
    " © 2025 AglaoDev-jp"
]

# ===============================
# 初期化関数：背景画像を読み込む
# ===============================
def init():
    # プロジェクトのルート（main.pyがあるディレクトリ）を基準に絶対パス取得
    BASE_DIR = Path(__file__).resolve().parent.parent
    bg_path = BASE_DIR / "assets" / "images" / "endroll_bg.png"
    if bg_path.exists():
        state["bg"] = pygame.image.load(str(bg_path)).convert()
        print("[INFO] スタッフロール背景画像ロード成功:", bg_path)
    else:
        print("スタッフロール用背景画像が見つかりません:", bg_path)
        state["bg"] = None  # 念のため

# ===============================
# 描画処理
# ===============================
def draw(screen, font, WIDTH, HEIGHT, state):
    # 背景画像があれば描画、なければ黒背景
    if state["bg"]:
        screen.blit(pygame.transform.scale(state["bg"], (WIDTH, HEIGHT)), (0, 0))
    else:
        screen.fill((0, 0, 0))
    
    y = state["y"]
    for line in CREDITS:
        surface = font.render(line, True, (255, 255, 255))
        screen.blit(surface, (WIDTH//2 - surface.get_width()//2, int(y)))
        y += 40

    if state["finished"]:
        msg = font.render("Enter: タイトルへ", True, (255, 255, 0))
        screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT - 80))

# ===============================
# イベント処理
# ===============================
def handle_event(event, state):
    if state["finished"] and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
        return "title"
    return None

# ===============================
# 更新処理
# ===============================
def update(state):
    if not state["finished"]:
        state["y"] -= 1.0
        if state["y"] < -len(CREDITS) * 40 + 600:
            state["finished"] = True
