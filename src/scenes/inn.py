# scenes/inn.py
import pygame
from pathlib import Path
from status import player_status

# ==============
# 宿屋ステート（状態管理変数）
# ==============
inn_state = {
    "dialog": ["いらっしゃいませ、旅のお方。", "今晩、お休みになりますか？"],
    "dialog_index": 0,
    "in_dialog": True,
    "message": "",
    "healed": False,
    "select_mode": False,      # 「はい／いいえ」選択中か
    "cursor": 0,               # 0: はい, 1: いいえ
    "finished": False,         # 処理が終わったかどうか
    "key_up_pressed": False,   # UPキーの押下状態
    "key_down_pressed": False, # DOWNキーの押下状態
}

inn_bg = None  # 背景画像（初回のみ読み込み）

# ==============
# イベント処理
# ==============
def handle_event(event, state, sound_manager):
    # --- 状態: 通常会話から選択へ ---
    if state["in_dialog"] and not state["select_mode"]:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            state["dialog_index"] += 1
            if state["dialog_index"] >= len(state["dialog"]):
                state["select_mode"] = True
            return None

    # --- 状態: 選択肢モード（はい/いいえ） ---
    elif state["select_mode"]:
        # 上下カーソル制御
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                sound_manager.play_se("cursor")
                state["cursor"] = 1 - state["cursor"]
            elif event.key == pygame.K_RETURN:
                # はい
                if state["cursor"] == 0:
                    if player_status["gold"] >= 10:
                        player_status["gold"] -= 10
                        player_status["hp"] = player_status["max_hp"]
                        # 回復メッセージ表示→「またのご利用～」表示→戻るへ
                        state["message"] = "ゆっくり休めた！HPが全回復した"
                        sound_manager.play_se("roostercry")
                        state["flow"] = "healed"  # flow状態で会話進行管理
                    else:
                        state["message"] = "お金が足りないようですね…"
                        state["flow"] = "fail"
                # いいえ
                else:
                    sound_manager.play_se("cancel")
                    state["message"] = "またのご利用をお待ちしております。"
                    state["flow"] = "no"
                state["select_mode"] = False
                state["in_dialog"] = False
                return None

    # --- 状態: メッセージ進行 ---
    elif not state["in_dialog"] and not state["select_mode"]:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            # 回復成功時
            if state.get("flow") == "healed" and state["message"] == "ゆっくり休めた！HPが全回復した":
                # 次のメッセージへ
                state["message"] = "またのご利用をお待ちしております。"
                return None
            # 失敗・いいえ・「またのご利用」後は町へ戻る
            else:
                # 状態リセット
                state["dialog_index"] = 0
                state["in_dialog"] = True
                state["select_mode"] = False
                state["cursor"] = 0
                state["message"] = ""
                state["flow"] = None
                state["healed"] = False
                state["finished"] = False
                return "town"
    return None


    # ----- 通常会話（Enterで次へ） -----
    if state["in_dialog"] and not state["select_mode"] and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
        state["dialog_index"] += 1
        if state["dialog_index"] >= len(state["dialog"]):
            # 会話文が終わったら「はい／いいえ」選択モードへ
            state["select_mode"] = True
        return None

    # ----- 終了処理・町に戻る -----
    if not state["in_dialog"] and event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        # 宿屋の状態リセット
        state["dialog_index"] = 0
        state["in_dialog"] = True
        state["select_mode"] = False
        state["cursor"] = 0
        state["message"] = ""
        state["healed"] = False
        state["finished"] = False
        state["key_up_pressed"] = False
        state["key_down_pressed"] = False
        return "town"

    return None

# ==============
# 描画処理
# ==============
def draw(screen, font, WIDTH, HEIGHT, state):
    global inn_bg
    # 背景画像の初回読み込み
    if inn_bg is None:
        BASE_DIR = Path(__file__).resolve().parent.parent
        inn_bg_path = BASE_DIR / "assets" / "images" / "inn_bg.png"
        inn_bg = pygame.image.load(str(inn_bg_path)).convert()
        inn_bg = pygame.transform.scale(inn_bg, (WIDTH, HEIGHT))
    screen.blit(inn_bg, (0, 0))

    # ステータス表示バー
    hp_text = f"HP: {player_status['hp']} / {player_status['max_hp']}"
    gold_text = f"G: {player_status['gold']}"
    hp_surface = font.render(hp_text, True, (255, 255, 255))
    gold_surface = font.render(gold_text, True, (255, 255, 0))
    screen.blit(hp_surface, (20, 20))
    screen.blit(gold_surface, (20, 60))

    # 会話ウィンドウ
    window_rect = pygame.Surface((WIDTH - 100, 180), pygame.SRCALPHA)
    window_rect.fill((0, 0, 0, 180))
    screen.blit(window_rect, (50, HEIGHT - 210))

    # NPC名
    npc_label = font.render("宿屋の主人", True, (255, 255, 255))
    screen.blit(npc_label, (60, HEIGHT - 200))

    if state["in_dialog"] and not state["select_mode"]:
        # 通常会話表示
        dialog = state["dialog"][state["dialog_index"]]
        dialog_text = font.render(dialog, True, (255, 255, 255))
        screen.blit(dialog_text, (60, HEIGHT - 160))
        hint = font.render("Enter:次へ", True, (255, 255, 255))
        screen.blit(hint, (WIDTH - 200, HEIGHT - 60))

    elif state["select_mode"]:
        # 「はい／いいえ」選択表示
        screen.blit(font.render("一泊：10G", True, (255, 255, 255)), (60, HEIGHT - 170))
        options = ["はい", "いいえ"]
        for i, opt in enumerate(options):
            color = (255, 255, 0) if i == state["cursor"] else (255, 255, 255)
            prefix = "▶ " if i == state["cursor"] else "   "
            txt = font.render(f"{prefix}{opt}", True, color)
            screen.blit(txt, (100, HEIGHT - 120 + i * 40))
        hint = font.render("↑↓:選択  Enter:決定", True, (255, 255, 255))
        screen.blit(hint, (WIDTH - 350, HEIGHT - 60))

    elif state["message"]:
        # 結果・メッセージ表示
        msg = font.render(state["message"], True, (255, 255, 255))
        screen.blit(msg, (60, HEIGHT - 150))
        hint = font.render("Enter:戻る", True, (255, 255, 255))
        screen.blit(hint, (WIDTH - 200, HEIGHT - 60))
