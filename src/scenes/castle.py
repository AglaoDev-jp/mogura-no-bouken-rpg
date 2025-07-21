# scenes/castle.py
import pygame
from pathlib import Path
from status import player_status
import copy  
from status import player_status, get_exp_to_next_level, is_max_level

# 会話パターンの定義 (変更なし)
castle_states = {
    # 敗北時
    "gameover": {
        "dialog": [
            "「またやられてしまったか…」",
            "「休んで行け！HPを回復してやろう。」",
            # 経験値メッセージはここに挿入
            "「気をつけていくのじゃぞ！」"
        ],
        "dialog_index": 0,
        "in_dialog": True,
        "message": "",
        "result": None,
    },
    # 町から入ったとき
    "default": {
        "dialog": [
            "「よく無事で帰ってきたな、もぐらよ！」",
            "「冒険の進み具合はどうじゃ？」",
            # 経験値メッセージはここに挿入
            "「無理せず冒険を楽しんでいくのじゃぞ！」"
        ],
        "dialog_index": 0,
        "in_dialog": True,
        "message": "",
        "result": None,
    }
}


castle_bg = None  # 背景画像キャッシュ

def init_state(key="gameover"):
    """
    ===== 初期状態の取得 =====
    会話パターン内に「次のレベルまで経験値」を差し込む。
    """
    state = copy.deepcopy(castle_states[key])

    # --- 経験値メッセージを自動挿入 ---
    exp_needed = get_exp_to_next_level()
    # ↓ここを修正します！
    if is_max_level():
        exp_msg = "「これ以上強くなれぬようじゃ。見事じゃ！」"
    else:
        exp_msg = f"「次のレベルまであと{exp_needed}の経験が必要じゃ。がんばるのじゃぞ！」"

    # 会話リストの2番目の後に差し込む（お好みで調整）
    state["dialog"].insert(2, exp_msg)
    return state  # deep copy済みのstateを返す

def handle_event(event, state):
    if event.type == pygame.KEYDOWN:
        # Enter：会話進行 or 会話終了後の町戻り
        if event.key == pygame.K_RETURN:
            if state["in_dialog"]:
                # セリフをまだ残しているなら次へ
                if state["dialog_index"] < len(state["dialog"]) - 1:
                    state["dialog_index"] += 1
                    return None
                # 最後のセリフを表示し終えたら
                else:
                    return "town"
            # 万が一 in_dialog が False になっていれば、Enter で町へ
            return "town"

        # Esc：どの段階でも町へ戻る
        elif event.key == pygame.K_ESCAPE:
            return "town"

    return None

def draw(screen, font, WIDTH, HEIGHT, state):
    """
    ===== 画面描画 =====
    背景、ステータス、会話ウィンドウ、セリフ or メッセージ、ヒント を描きます。
    """
    global castle_bg
    # 背景画像のロード＆キャッシュ
    if castle_bg is None:
        BASE_DIR = Path(__file__).resolve().parent.parent
        castle_bg_path = BASE_DIR / "assets" / "images" / "castle_bg.png"
        try:
            castle_bg = pygame.image.load(str(castle_bg_path)).convert()
            castle_bg = pygame.transform.scale(castle_bg, (WIDTH, HEIGHT))
        except:
            # 画像がなければ単色で代用
            castle_bg = pygame.Surface((WIDTH, HEIGHT))
            castle_bg.fill((80, 80, 160))

    # 背景＆ステータスバー
    screen.blit(castle_bg, (0, 0))
    draw_status_bar(screen, font, player_status)

    # 会話ウィンドウ
    window_rect = pygame.Surface((WIDTH - 100, 150), pygame.SRCALPHA)
    window_rect.fill((0, 0, 0, 180))
    screen.blit(window_rect, (50, HEIGHT - 180))

    # NPC 名
    npc_label = font.render("王様", True, (255, 255, 255))
    screen.blit(npc_label, (60, HEIGHT - 170))

    # セリフ or メッセージ表示
    if state["in_dialog"]:
        dialog = state["dialog"][state["dialog_index"]]
        lines = wrap_text(dialog, font, WIDTH - 150)
        for i, line in enumerate(lines):
            dialog_text = font.render(line, True, (255, 255, 255))
            screen.blit(dialog_text, (60, HEIGHT - 130 + i * 40))
    elif state.get("message"):
        lines = wrap_text(state["message"], font, WIDTH - 150)
        for i, line in enumerate(lines):
            msg_text = font.render(line, True, (255, 255, 255))
            screen.blit(msg_text, (60, HEIGHT - 130 + i * 40))

    # ヒント
    hint = font.render("Enter:次へ  Esc:戻る ", True, (255, 255, 255))
    screen.blit(hint, (WIDTH - 350, HEIGHT - 50))

def wrap_text(text, font, max_width):
    """
    指定した幅に収まるようにテキストを自動で折り返す関数
    """
    lines = []
    line = ""
    for char in text:
        test_line = line + char
        if font.size(test_line)[0] > max_width:
            lines.append(line)
            line = char
        else:
            line = test_line
    if line:
        lines.append(line)
    return lines

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
