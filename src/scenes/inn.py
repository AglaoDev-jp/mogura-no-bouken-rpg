import pygame
from pathlib import Path
from status import player_status

# ============== 宿屋ステート ==============
inn_state = {
    "dialog": ["いらっしゃいませ、旅のお方。", "今晩、お休みになりますか？"],
    "dialog_index": 0,
    "in_dialog": True,
    "message": "",
    "healed": False,
    "select_mode": False,      # 「はい／いいえ」選択中か
    "cursor": 0,               # 0: はい, 1: いいえ
    "finished": False,
    "key_up_pressed": False,
    "key_down_pressed": False,
    "flow": None,
    "voice_played": False,     # 音声再生フラグ
}

inn_bg = None  # 背景画像（初回のみ読み込み）

# ◆ dialogに対応する音声ファイル名
voice_files = [
    "inn_voice_00.mp3.enc",  # いらっしゃいませ、旅のお方。
    "inn_voice_01.mp3.enc",  # 今晩、お休みになりますか？
]

# ============== イベント処理 ==============
def handle_event(event, state, sound_manager):
    """
    宿屋でのキー入力・会話進行などを管理します。
    会話・分岐に合わせて音声再生フラグも制御します。
    """
    # --- 通常会話 ---
    if state["in_dialog"] and not state["select_mode"]:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            state["dialog_index"] += 1
            state["voice_played"] = False  # 次のセリフで再生
            if state["dialog_index"] >= len(state["dialog"]):
                state["select_mode"] = True
            return None

    # --- はい／いいえ選択肢 ---
    elif state["select_mode"]:
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
                        state["message"] = "ゆっくり休めた！HPが全回復した"
                        sound_manager.play_se("roostercry")
                        state["flow"] = "healed"
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
                state["voice_played"] = False  # メッセージ音声再生のためリセット
                return None

    # --- 結果メッセージ表示中 ---
    elif not state["in_dialog"] and not state["select_mode"]:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            # 回復成功時（「またのご利用～」に進む）
            if state.get("flow") == "healed" and state["message"] == "ゆっくり休めた！HPが全回復した":
                state["message"] = "またのご利用をお待ちしております。"
                state["voice_played"] = False  # 次のメッセージで音声再生
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
                state["voice_played"] = False
                return "town"
    return None

# ============== 描画処理 ==============
def draw(screen, font, WIDTH, HEIGHT, state, sound_manager=None):
    """
    宿屋の画面・会話・選択肢・メッセージの表示と、音声再生を行います。
    """
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

    # --- 通常会話（dialog） ---
    if state["in_dialog"] and not state["select_mode"]:
        dialog = state["dialog"][state["dialog_index"]]
        # ◆ 音声再生（未再生時のみ）
        if (not state.get("voice_played", False)) and sound_manager is not None:
            if state["dialog_index"] < len(voice_files):
                filename = voice_files[state["dialog_index"]]
                sound_manager.play_voice(filename)
                state["voice_played"] = True
        # テキスト描画
        dialog_text = font.render(dialog, True, (255, 255, 255))
        screen.blit(dialog_text, (60, HEIGHT - 160))
        hint = font.render("Enter:次へ", True, (255, 255, 255))
        screen.blit(hint, (WIDTH - 200, HEIGHT - 60))

    # --- 選択肢モード ---
    elif state["select_mode"]:
        screen.blit(font.render("一泊：10G", True, (255, 255, 255)), (60, HEIGHT - 170))
        options = ["はい", "いいえ"]
        for i, opt in enumerate(options):
            color = (255, 255, 0) if i == state["cursor"] else (255, 255, 255)
            prefix = "▶ " if i == state["cursor"] else "   "
            txt = font.render(f"{prefix}{opt}", True, color)
            screen.blit(txt, (100, HEIGHT - 120 + i * 40))
        hint = font.render("↑↓:選択  Enter:決定", True, (255, 255, 255))
        screen.blit(hint, (WIDTH - 350, HEIGHT - 60))

    # --- メッセージ表示（回復・失敗など） ---
    elif state["message"]:
        msg = font.render(state["message"], True, (255, 255, 255))
        screen.blit(msg, (60, HEIGHT - 150))
        hint = font.render("Enter:戻る", True, (255, 255, 255))
        screen.blit(hint, (WIDTH - 200, HEIGHT - 60))
        # ◆ メッセージごとに音声再生（未再生時のみ）
        if (not state.get("voice_played", False)) and sound_manager is not None:
            voice_map = {
                "ゆっくり休めた！HPが全回復した": "inn_heal.mp3.enc",
                "お金が足りないようですね…": "inn_no_money.mp3.enc",
                "またのご利用をお待ちしております。": "inn_thankyou.mp3.enc",
            }
            if state["message"] in voice_map:
                sound_manager.play_voice(voice_map[state["message"]])
                state["voice_played"] = True

