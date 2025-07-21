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
}

def handle_event(event, state, sound_manager):
    """
    商品リストのみ上下移動、Escで店を出る
    """
    n_choices = len(items)
    if state["mode"] == "talk":
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            state["mode"] = "select"
            state["message"] = ""
            state["cursor"] = 0

    elif state["mode"] == "select":
        if event.type == pygame.KEYDOWN:
            # 上下キーで循環
            if event.key == pygame.K_DOWN:
                sound_manager.play_se("cursor")
                state["cursor"] = (state["cursor"] + 1) % n_choices
            elif event.key == pygame.K_UP:
                sound_manager.play_se("cursor")
                state["cursor"] = (state["cursor"] - 1) % n_choices
            elif event.key == pygame.K_RETURN:
                idx = state["cursor"]
                item = items[idx]
                msg = buy_item(item["name"], item["price"])
                # --- 購入成功・失敗でSEを分けて再生 --- ここちょっとわかりにくいか？
                if msg.endswith("を手に入れた！") or msg.endswith("を装備しました！"):
                    sound_manager.play_se("item_get")  # 購入成功SE
                    # 所持数に反映
                    player_status["items"][item["name"]] = player_status["items"].get(item["name"], 0) + 1
                elif "お金が足りません" in msg: 
                    sound_manager.play_se("error")  # 購入失敗SE
                else:
                    sound_manager.play_se("error")  # その他のエラー等（例：既に装備中）音を別にするのもありかも。
                state["message"] = msg
                state["mode"] = "buymsg"
            elif event.key == pygame.K_ESCAPE:
                sound_manager.play_se("cancel")
                state["message"] = "またきてね！"
                state["mode"] = "buymsg"

    elif state["mode"] == "buymsg":
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            if state["message"] == "またきてね！":
                state["mode"] = "talk"
                state["cursor"] = 0
                state["message"] = ""
                return "town"
            else:
                state["mode"] = "select"
                state["message"] = ""
    return None


def draw(screen, font, WIDTH, HEIGHT, state):
    """
    道具屋の描画処理
    """
    global shop_bg
    if shop_bg is None:
        BASE_DIR = Path(__file__).resolve().parent.parent
        shop_bg_path = BASE_DIR / "assets" / "images" / "shop_bg.png"
        shop_bg = pygame.image.load(str(shop_bg_path)).convert()
        shop_bg = pygame.transform.scale(shop_bg, (WIDTH, HEIGHT))

    screen.blit(shop_bg, (0, 0))
    draw_status_bar(screen, font, player_status)

    # 下部ウィンドウ枠
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

    elif state["mode"] == "select":
        # 商品リストを縦に表示
        y0 = HEIGHT - 200
        x0 = 70
        for i, item in enumerate(items):
            color = (255, 255, 0) if state["cursor"] == i else (255, 255, 255)
            prefix = "▶ " if state["cursor"] == i else "   "
            txt = font.render(f"{prefix}{item['name']} - {item['price']}G", True, color)
            screen.blit(txt, (x0, y0 + i * 40))

        # ヒント2行
        hint1 = font.render("↑↓:選択", True, (255, 255, 255))
        screen.blit(hint1, (WIDTH - 350, HEIGHT - 90))
        hint2 = font.render("Enter:決定 Esc:店を出る", True, (255, 255, 255))
        screen.blit(hint2, (WIDTH - 350, HEIGHT - 50))

    elif state["mode"] == "buymsg":
        msg = font.render(state["message"], True, (255, 255, 255))
        screen.blit(msg, (70, HEIGHT - 150))
        hint = font.render("Enter:次へ", True, (255, 255, 255))
        screen.blit(hint, (WIDTH - 200, HEIGHT - 50))

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
