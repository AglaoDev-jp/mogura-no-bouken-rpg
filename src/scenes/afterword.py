# scenes/afterword.py
import pygame
from pathlib import Path

def init_state():
    """
    あとがき用の状態を初期化して返す関数
    """
    return {
        "text_index": 0,
        "in_dialog": True,
        "bg_images": None,
    }

# 初期状態（mainからimport時にも使う）
state = init_state()

# あとがきで使う背景画像
bg_files = [
    "afterword.png",  
] * 12  # 12枚分繰り返し表示（行数に応じて増やしてもOK）

script = [
    "はじめまして。作者の AglaoDev-jp です。",
    "このたびは拙作のRPGを最後まで観ていただいて、ありがとうございました。",
    "本作は「モジュール構成」「状態管理」「クラスベースの記述」を意識して、Pythonで自作フレームワークのRPGを構築してみました。",
    "（といってもほぼすべてChatGPTがコードを書いていますが…）",
    "GUIで動かすし、LLM（大規模言語モデル）の力も借りられるし、「シンプルなRPGなら何とかなるだろう」と思って始めたのですが、まったく簡単ではありませんでした。",
    "システム、演出、セーブ・ロードなど、いろんな要素が複雑に絡み合っていて、これまでRPGを作ってきた人たちってどんだけすごいんだと痛感する日々となりました。",
    "これからRPGを作りたい方には、既存フレームワークを活用することをおすすめしますよ。",
    "とはいえ、このコードもベースに使えるようにGitHubにて公開しています。素材やライセンス情報、READMEを含む詳細な説明もすべてGitHubに掲載しています。",
    "オリジナル作品づくりに利用していただければ幸いです。",
    "いつかプロンプト一回とかでRPGが作られる未来が来るんでしょうかね……。",
    "また何か作るかもしれませんので、そのときはどうぞよろしくお願いします。",
    "それでは、またいつか。",
]

def load_bg_images():
    BASE_DIR = Path(__file__).resolve().parent.parent
    images = []
    for fname in bg_files:
        img_path = BASE_DIR / "assets" / "images" / fname
        try:
            img = pygame.image.load(str(img_path)).convert_alpha()
            img = pygame.transform.scale(img, (800, 600))
        except Exception:
            img = pygame.Surface((800, 600))
            img.fill((30, 30, 30))
        images.append(img)
    return images

def handle_event(event, state):
    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
        if state["in_dialog"]:
            if state["text_index"] < len(script) - 1:
                state["text_index"] += 1
            else:
                state["in_dialog"] = False
        else:
            # 「Enter:スタート」でタイトルに戻る
            return "title"
    return None

def wrap_text(text, font, max_width):
    lines = []
    line = ''
    for char in text:
        test_line = line + char
        if font.size(test_line)[0] <= max_width:
            line = test_line
        else:
            lines.append(line)
            line = char
    if line:
        lines.append(line)
    return lines

def draw(screen, font, WIDTH, HEIGHT, state):
    if state["bg_images"] is None:
        state["bg_images"] = load_bg_images()
    bg = state["bg_images"][state["text_index"] % len(state["bg_images"])]
    screen.blit(bg, (0, 0))

    # 下部ウィンドウ
    dialog_box = pygame.Surface((WIDTH - 120, 180), pygame.SRCALPHA)
    dialog_box.fill((0, 0, 0, 180))
    screen.blit(dialog_box, (50, HEIGHT - 210))

    if state["in_dialog"]:
        dialog = script[state["text_index"]]
        lines = wrap_text(dialog, font, WIDTH - 140)
        for i, line in enumerate(lines):
            text_surface = font.render(line, True, (255, 255, 255))
            screen.blit(text_surface, (70, HEIGHT - 210 + i * 40))

        hint = font.render("Enter: 次へ", True, (255, 255, 255))
        screen.blit(hint, (WIDTH - 180, HEIGHT - 50))
    else:
        end_msg = font.render("Enter: タイトルへ戻る", True, (255, 255, 255))
        screen.blit(end_msg, (WIDTH // 2 - 160, HEIGHT - 120))
