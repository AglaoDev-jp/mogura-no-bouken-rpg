# scenes/shop.py
import pygame
from pathlib import Path
from status import player_status
from item_effects import buy_item

# 背景画像（初回のみ読み込み）
shop_bg = None

# 商品リスト
items = [
    {"name": "ごちサンド", "price": 10},
    {"name": "トロッコ", "price": 15},
    {"name": "スコップ", "price": 100},
    {"name": "ヘルメット", "price": 150},
]

# shop_state（他ファイルから参照可）
shop_state = {
    "mode": "talk",      # 'talk'(会話)→'select'(選択)→'buymsg'(購入/退出)
    "cursor": 0,         # カーソル位置
    "message": "",       # メッセージ表示用
    "voice_played": False, # 音声再生フラグ（追加）
    "buy_item_name": None,  # 購入時の商品名一時保存
}

# ◆ 会話開始メッセージ用の音声ファイル名
talk_voice = "shop_welcome.mp3.enc"

# ◆ 商品ごとの購入音声
item_voice_map = {
    "ごちサンド": "shop_get_sand.mp3.enc",
    "トロッコ": "shop_get_torocco.mp3.enc",
    "スコップ": "shop_get_scoop.mp3.enc",
    "ヘルメット": "shop_get_helmet.mp3.enc",
}

# ◆ 結果メッセージに対する音声（退出など）
msg_voice_map = {
    "またきてね！": "shop_thankyou.mp3.enc",
}

def handle_event(event, state, sound_manager):
    """
    ショップのキー入力・進行管理
    """
    n_choices = len(items)
    if state["mode"] == "talk":
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            state["mode"] = "select"
            state["message"] = ""
            state["cursor"] = 0
            state["voice_played"] = False  # 音声リセット

    elif state["mode"] == "select":
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                sound_manager.play_se("cursor")
                state["cursor"] = (state["cursor"] + 1) % n_choices
                state["voice_played"] = False
            elif event.key == pygame.K_UP:
                sound_manager.play_se("cursor")
                state["cursor"] = (state["cursor"] - 1) % n_choices
                state["voice_played"] = False
            elif event.key == pygame.K_RETURN:
                idx = state["cursor"]
                item = items[idx]
                msg = buy_item(item["name"], item["price"])
                # --- 購入成功・失敗でSEを分けて再生 ---
                if msg.endswith("を手に入れた！") or msg.endswith("を装備しました！"):
                    sound_manager.play_se("item_get")  # 購入成功SE
                    player_status["items"][item["name"]] = player_status["items"].get(item["name"], 0) + 1
                    state["buy_item_name"] = item["name"]  # 音声用に保存
                elif "お金が足りないよ！" in msg: 
                    sound_manager.play_se("error")
                    state["buy_item_name"] = None
                elif "すでに装備中です" in msg or "すでに装備しています" in msg:
                    sound_manager.play_se("error")
                    state["buy_item_name"] = item["name"]  # 装備品名だけ保存
                else:
                    sound_manager.play_se("error")
                    state["buy_item_name"] = None
                state["message"] = msg
                state["mode"] = "buymsg"
                state["voice_played"] = False
            elif event.key == pygame.K_ESCAPE:
                sound_manager.play_se("cancel")
                state["message"] = "またきてね！"
                state["mode"] = "buymsg"
                state["voice_played"] = False

    elif state["mode"] == "buymsg":
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            if state["message"] == "またきてね！":
                state["mode"] = "talk"
                state["cursor"] = 0
                state["message"] = ""
                state["voice_played"] = False
                return "town"
            else:
                state["mode"] = "select"
                state["message"] = ""
                state["voice_played"] = False
    return None

def draw(screen, font, WIDTH, HEIGHT, state, sound_manager=None):
    """
    ショップの描画処理＋音声再生制御
    """
    global shop_bg
    if shop_bg is None:
        BASE_DIR = Path(__file__).resolve().parent.parent
        shop_bg_path = BASE_DIR / "assets" / "images" / "shop_bg.png"
        shop_bg = pygame.image.load(str(shop_bg_path)).convert()
        shop_bg = pygame.transform.scale(shop_bg, (WIDTH, HEIGHT))

    screen.blit(shop_bg, (0, 0))
    draw_status_bar(screen, font, player_status)

    window_rect = pygame.Surface((WIDTH - 100, 220), pygame.SRCALPHA)
    window_rect.fill((0, 0, 0, 180))
    screen.blit(window_rect, (50, HEIGHT - 250))

    label = font.render("道具屋の店主", True, (255, 255, 255))
    screen.blit(label, (60, HEIGHT - 240))

    if state["mode"] == "talk":
        talk_msg = "いらっしゃい！どれも冒険には必需品だよ！"
        talk_surface = font.render(talk_msg, True, (255, 255, 255))
        screen.blit(talk_surface, (70, HEIGHT - 200))
        hint = font.render("Enter:選択へ", True, (255, 255, 255))
        screen.blit(hint, (WIDTH - 250, HEIGHT - 50))
        # 音声再生（1回のみ）
        if (not state.get("voice_played", False)) and sound_manager is not None:
            sound_manager.play_voice(talk_voice)
            state["voice_played"] = True

    elif state["mode"] == "select":
        y0 = HEIGHT - 200
        x0 = 70
        for i, item in enumerate(items):
            color = (255, 255, 0) if state["cursor"] == i else (255, 255, 255)
            prefix = "▶ " if state["cursor"] == i else "   "
            txt = font.render(f"{prefix}{item['name']} - {item['price']}G", True, color)
            screen.blit(txt, (x0, y0 + i * 40))
        hint1 = font.render("↑↓:選択", True, (255, 255, 255))
        screen.blit(hint1, (WIDTH - 350, HEIGHT - 90))
        hint2 = font.render("Enter:決定 Esc:店を出る", True, (255, 255, 255))
        screen.blit(hint2, (WIDTH - 350, HEIGHT - 50))

    elif state["mode"] == "buymsg":
        msg = font.render(state["message"], True, (255, 255, 255))
        screen.blit(msg, (70, HEIGHT - 150))
        hint = font.render("Enter:次へ", True, (255, 255, 255))
        screen.blit(hint, (WIDTH - 200, HEIGHT - 50))
        # ◆ 購入・装備・失敗・退出などの音声
        if (not state.get("voice_played", False)) and sound_manager is not None:
            # --- 商品入手 or 装備成功 ---
            if ("を手に入れた！" in state["message"]) or ("を装備しました！" in state["message"]):
                # 商品名で判定（全商品対応）
                for item_name in item_voice_map:
                    if state["message"].startswith(item_name):
                        sound_manager.play_voice(item_voice_map[item_name])
                        state["voice_played"] = True
                        break
            # --- すでに装備中（武器・防具共通音声） ---
            elif ("すでに装備してるよ" in state["message"] # 複数パターン
                or "装備しています" in state["message"]
                or "装備中です" in state["message"]):
                sound_manager.play_voice("shop_already_equip.mp3.enc")
                state["voice_played"] = True
            # --- お金が足りないよ！ ---
            elif "お金が足りないよ！" in state["message"]: 
                sound_manager.play_voice("shop_no_money.mp3.enc")
                state["voice_played"] = True
            # --- 退出（またきてね！） ---
            elif state["message"] in msg_voice_map:
                sound_manager.play_voice(msg_voice_map[state["message"]])
                state["voice_played"] = True

def draw_status_bar(screen, font, status):
    """
    画面上部にプレイヤーのHPとゴールドを表示
    """
    hp_text = f"HP: {status['hp']} / {status['max_hp']}"
    gold_text = f"G: {status['gold']}"
    hp_surface = font.render(hp_text, True, (255, 255, 255))
    gold_surface = font.render(gold_text, True, (255, 255, 0))
    screen.blit(hp_surface, (20, 20))
    screen.blit(gold_surface, (20, 60))
