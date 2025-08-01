import pygame
from pathlib import Path
from status import player_status
import copy  
from status import player_status, get_exp_to_next_level, is_max_level

castle_states = {
    "gameover": {
        "dialog": [
            "「またやられてしまったか…」",
            "「休んで行け！HPを回復してやろう。」",
            "「気をつけていくのじゃぞ！」"
        ],
        "dialog_index": 0,
        "in_dialog": True,
        "message": "",
        "result": None,
        "voice_played": False,  # 音声フラグ
    },
    "default": {
        "dialog": [
            "「よく無事で帰ってきたな、もぐらよ！」",
            "「冒険の進み具合はどうじゃ？」",
            "「無理せず冒険を楽しんでいくのじゃぞ！」"
        ],
        "dialog_index": 0,
        "in_dialog": True,
        "message": "",
        "result": None,
        "voice_played": False,
    }
}

castle_bg = None

# ◆セリフ順に対応する音声ファイル（最大4つ目が経験値）
castle_voice_map = {
    "gameover": [
        "castle_gameover_00.mp3.enc",
        "castle_gameover_01.mp3.enc",
        "castle_exp.mp3.enc",      # 経験値(数字問わず)
        "castle_gameover_02.mp3.enc",
    ],
    "default": [
        "castle_default_00.mp3.enc",
        "castle_default_01.mp3.enc",
        "castle_exp.mp3.enc",      # 経験値(数字問わず)
        "castle_default_02.mp3.enc",
    ],
    "max_level": "castle_max.mp3.enc", # レベル最大時の特別音声
}

def init_state(key="gameover"):
    state = copy.deepcopy(castle_states[key])
    state["voice_played"] = False
    exp_needed = get_exp_to_next_level()
    if is_max_level():
        exp_msg = "「これ以上強くなれぬようじゃ。見事じゃ！」"
    else:
        exp_msg = f"「次のレベルまであと{exp_needed}の経験が必要じゃ。がんばるのじゃぞ！」"
    state["dialog"].insert(2, exp_msg)
    return state

def handle_event(event, state):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            if state["in_dialog"]:
                if state["dialog_index"] < len(state["dialog"]) - 1:
                    state["dialog_index"] += 1
                    state["voice_played"] = False  # メッセージ進行時にフラグリセット
                    return None
                else:
                    return "town"
            return "town"
        elif event.key == pygame.K_ESCAPE:
            return "town"
    return None

def draw(screen, font, WIDTH, HEIGHT, state, sound_manager=None, key="default"):
    global castle_bg
    if castle_bg is None:
        BASE_DIR = Path(__file__).resolve().parent.parent
        castle_bg_path = BASE_DIR / "assets" / "images" / "castle_bg.png"
        try:
            castle_bg = pygame.image.load(str(castle_bg_path)).convert()
            castle_bg = pygame.transform.scale(castle_bg, (WIDTH, HEIGHT))
        except:
            castle_bg = pygame.Surface((WIDTH, HEIGHT))
            castle_bg.fill((80, 80, 160))
    screen.blit(castle_bg, (0, 0))
    draw_status_bar(screen, font, player_status)
    window_rect = pygame.Surface((WIDTH - 100, 150), pygame.SRCALPHA)
    window_rect.fill((0, 0, 0, 180))
    screen.blit(window_rect, (50, HEIGHT - 180))
    npc_label = font.render("王様", True, (255, 255, 255))
    screen.blit(npc_label, (60, HEIGHT - 170))
    if state["in_dialog"]:
        dialog = state["dialog"][state["dialog_index"]]
        lines = wrap_text(dialog, font, WIDTH - 150)
        for i, line in enumerate(lines):
            dialog_text = font.render(line, True, (255, 255, 255))
            screen.blit(dialog_text, (60, HEIGHT - 130 + i * 40))
        # ---- 音声再生部分（1メッセージごと1回だけ）----
        if sound_manager is not None and not state.get("voice_played", False):
            idx = state["dialog_index"]
            # 経験値メッセージ判定
            if "これ以上強くなれぬ" in dialog:
                sound_manager.play_voice(castle_voice_map["max_level"])
            elif "次のレベルまであと" in dialog:
                sound_manager.play_voice(castle_voice_map[key][2])  # 共通経験値音声
            else:
                # 通常メッセージ（keyに応じてindexで再生）
                if idx < len(castle_voice_map[key]):
                    sound_manager.play_voice(castle_voice_map[key][idx])
            state["voice_played"] = True
    elif state.get("message"):
        lines = wrap_text(state["message"], font, WIDTH - 150)
        for i, line in enumerate(lines):
            msg_text = font.render(line, True, (255, 255, 255))
            screen.blit(msg_text, (60, HEIGHT - 130 + i * 40))
    hint = font.render("Enter:次へ  Esc:戻る ", True, (255, 255, 255))
    screen.blit(hint, (WIDTH - 350, HEIGHT - 50))

def wrap_text(text, font, max_width):
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
    hp_text = f"HP: {status['hp']} / {status['max_hp']}"
    gold_text = f"G: {status['gold']}"
    hp_surface = font.render(hp_text, True, (255, 255, 255))
    gold_surface = font.render(gold_text, True, (255, 255, 0))
    screen.blit(hp_surface, (20, 20))
    screen.blit(gold_surface, (20, 60))
