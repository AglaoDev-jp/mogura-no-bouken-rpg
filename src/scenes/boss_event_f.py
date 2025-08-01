# scenes/boss_event_f.py

print("【DEBUG】boss_event_f.py: import開始")
import pygame
from pathlib import Path
from status import ENEMY_TABLE

# ◆イベントシーンの状態変数
state = {
    "text_index": 0,
    "in_dialog": True,
    "bg_images": None,  
    "voice_played": False,
}

bg_files = [
    "boss_f_bg1.png",  # ボス登場シーン
    "boss_f_bg1.png",
    "boss_f_bg1.png",
    "boss_f_bg2.png", 
    "boss_f_bg1.png",
    "boss_f_bg3.png",
    "boss_f_bg4.png",
    "boss_f_bg4.png",  
]

voice_files = [
    "boss_f_voice_00.mp3.enc",
    "boss_f_voice_01.mp3.enc",
    "boss_f_voice_02.mp3.enc",
    "boss_f_voice_03.mp3.enc",
    "boss_f_voice_04.mp3.enc",
    "boss_f_voice_05.mp3.enc",
    "boss_f_voice_06.mp3.enc",
    "boss_f_voice_07.mp3.enc",
]

script = [
    "もぐら：「やあ、しゅごもぐらくん。……そっか“テカテカのたま”って君が守護してるんだね。」",
    "しゅごもぐら：「もぐらくんじゃないか。こんなところまでどうしたんだ。」",
    "しゅごもぐら：「ここは”テカテカのたま”の祭壇。勇者様の試練の場なんだぞ。きちゃダメなんだぞ。」",
    "もぐら：「なんかさー、王様が勇者にいい顔したいみたいで、テカテカのたま代わりに取りに行けとか言われちゃってさー。」",
    "しゅごもぐら：「な、なんだと！？聖なる”テカテカのたま”をもぐらくんに！？なんとばちあたりな！」",
    "もぐら：「まあ、なんだ、これも効率化の流れじゃない？”テカテカのたま”ちょうだい。」",
    "しゅごもぐら：「なんという適当な！もぐらくん。どうしてもというなら私を倒してからだ！」",
    "もぐら：「うーん。どうしてもってわけでもないけどな～。まあいいか。」",    
]

def load_bg_images():
    """
    背景画像をロードしリストで返します。
    失敗時はグレイの画像で代用します。
    """
    BASE_DIR = Path(__file__).resolve().parent.parent
    images = []
    for fname in bg_files:
        img_path = BASE_DIR / "assets" / "images" / fname
        print("画像ロード確認:", img_path)
        try:
            img = pygame.image.load(str(img_path)).convert_alpha()
            img = pygame.transform.scale(img, (800, 600))
        except Exception as e:
            print(f"画像ロード失敗: {img_path} {e}")
            with open("error_log.txt", "a", encoding="utf-8") as f:
                f.write(f"画像ロード失敗: {img_path} {e}\n")
            img = pygame.Surface((800, 600))
            img.fill((80, 80, 80))
        images.append(img)
    return images

def wrap_text(text, font, max_width):
    """
    指定幅で自動折り返し。日本語対応。
    """
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

def extract_npc_and_text(dialog):
    """
    セリフから話者ラベルを分離（例：「もぐら：「～」」→ ("もぐら", "「～」")）
    """
    if "：「" in dialog and dialog.endswith("」"):
        npc, text = dialog.split("：「", 1)
        text = text.rstrip("」")
        return npc, "「" + text + "」"
    return None, dialog  # 会話ラベルなし

def draw(screen, font, WIDTH, HEIGHT, state, sound_manager=None):
    if state.get("bg_images") is None:
        state["bg_images"] = load_bg_images()
    bg_images = state["bg_images"]
    bg_idx = min(state.get("text_index", 0), len(bg_images) - 1)
    if bg_images and len(bg_images) > 0:
        screen.blit(bg_images[bg_idx], (0, 0))
    else:
        screen.fill((64, 32, 192))

    window_rect = pygame.Surface((WIDTH - 100, 180), pygame.SRCALPHA)
    window_rect.fill((0, 0, 0, 180))
    screen.blit(window_rect, (50, HEIGHT - 210))

    if state["in_dialog"]:
        idx = min(state["text_index"], len(script) - 1)
        dialog = script[idx]
        npc, text = extract_npc_and_text(dialog)
        # 音声再生（未再生時のみ）
        if (not state.get("voice_played", False)) and (sound_manager is not None):
            filename = voice_files[state["text_index"]]
            sound_manager.play_voice(filename)
            state["voice_played"] = True
        if npc:
            npc_label = font.render(npc, True, (255, 255, 255))
            screen.blit(npc_label, (70, HEIGHT - 200))
        max_text_width = WIDTH - 140
        lines = wrap_text(text, font, max_text_width)
        y0 = HEIGHT - 170
        for i, line in enumerate(lines):
            dialog_surface = font.render(line, True, (255, 255, 255))
            screen.blit(dialog_surface, (70, y0 + i * 40))
        hint = font.render("Enter: 次へ", True, (255, 255, 255))
        screen.blit(hint, (WIDTH - 180, HEIGHT - 50))
    else:
        end_msg = font.render("Enter: バトルスタート", True, (255, 255, 255))
        screen.blit(end_msg, (WIDTH // 2 - 120, HEIGHT - 120))

def handle_event(event, state, sound_manager=None):
    """
    イベントの入力処理（文字送り／バトル開始）
    """
    print("【DEBUG】boss_event_f.handle_event() 呼び出し", event)
    if event.type == pygame.KEYDOWN:
        if state["in_dialog"] and event.key == pygame.K_RETURN:
            if state["text_index"] < len(script) - 1:
                state["text_index"] += 1
                state["voice_played"] = False  # 次のセリフで再生できるようリセット
                print("  → text_index:", state["text_index"])
            else:
                state["in_dialog"] = False
                if sound_manager:
                    sound_manager.stop_voice()
                print("  → in_dialog 終了")
        elif not state["in_dialog"] and event.key == pygame.K_RETURN:
            print("  → バトル開始 リクエスト")
            return "battle"
    return None
