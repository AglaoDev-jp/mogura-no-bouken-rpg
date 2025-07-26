# scenes/opening_event.py
import pygame
from pathlib import Path

event_state = {
    "text_index": 0,
    "step": 0,
    "in_dialog": True,
    "bg_images": None,
    "images": [],
    "npc": "王様",  # デフォルト話者
    "voice_played": False,  # 追加（どのindexでも使う）
}
# --- 画像ファイル名（紙芝居型） ---
bg_files = [
    "opening_bg_00.png", "opening_bg_01.png", "castle_bg.png", "castle_bg.png",
    "opening_bg_02.png", "opening_bg_02.png", "opening_bg_03.png", "opening_bg_03.png",
    "opening_bg_03.png", "opening_bg_03.png", "opening_bg_04.png", "opening_bg_04.png",
    "opening_bg_04.png", "opening_bg_05.png", "opening_bg_05.png", "opening_bg_06.png",
    "opening_bg_07.png", "opening_bg_07.png", "opening_bg_08.png",
]

# --- 各セリフに対応するvoiceファイル名 ---
voice_files = [
    "op_voice_00.mp3", "op_voice_01.mp3", "op_voice_02.mp3", "op_voice_03.mp3",
    "op_voice_04.mp3", "op_voice_05.mp3", "op_voice_06.mp3", "op_voice_07.mp3",
    "op_voice_08.mp3", "op_voice_09.mp3", "op_voice_10.mp3", "op_voice_11.mp3",
    "op_voice_12.mp3", "op_voice_13.mp3", "op_voice_14.mp3", "op_voice_15.mp3",
    "op_voice_16.mp3", "op_voice_17.mp3", "op_voice_18.mp3",
]

script = [
    "昔々あるところに、不思議な国がありました。",
    "その国の地中には、なんと人間とおしゃべりできる“もぐら”たちがたくさん暮らしていたのです。",
    "地上では立派なお城がそびえ、賢い王様が国を治めていました。",
    "王様は、地底のもぐらたちがどれほど器用で、どれほどたくましく生きているかをよく知っていました。",
    "そんなある日、地底でいちばんヒマそうな（？）もぐらが、王様に呼び出されます。",
    "もぐら：「こんちわ王様。なんすか？用事って」",
    "王様：「まもなく、この国に伝説の勇者が現れるそうじゃ。その勇者は、“テカテカのたま”を手に入れるために、この地のダンジョンを訪れることになっておる。」",
    "王様：「しかし、そのダンジョンは――地底深く、複雑な迷路となっておる！人間ではとても進めぬ場所も多い。」",
    "王様：「……そこで――だ。もぐらよ、おぬしの出番じゃ！ダンジョンの奥底、誰よりも掘るのが得意な“もぐら”なら、きっと“テカテカのたま”を見つけ出せよう。」",
    "王様：「勇者が来る前に、こっそり取ってきてはくれぬか？」",
    "もぐら：「なんすかその“テカテカのたま”って？」",
    "王様：「ふむ、よい質問じゃ。“テカテカのたま”とは、遥か昔、魔王が現れたとき大地の精霊が封じのために生み出した伝説の宝玉。」",
    "王様：「これがなければ、ダンジョンの最奥――すなわち“魔王の門”は決して開かぬのじゃ。」",
    "もぐら：「へぇ～……でもそういうのって勇者が直接取りにいくもんなんじゃないんすかね？試練的な？」",
    "王様：「う、うむ……確かにそうなのじゃが、なにぶん勇者どのも忙しい身でな。次の勇者業に備えて、体力も温存しておかねばならんしのう……」",
    "もぐら：「ふーん…勇者に忖度してるんすね～。」",
    "王様：「そ、それにだ、おぬしの働きぶりは勇者どのにもきっと良い印象を与えるであろう！なに、国のためじゃ、国のため！頼んだぞ、もぐらよ！」",
    "もぐら：「もぐら搾取じゃん…世知辛いわぁ。まあ、洞窟は得意だし、暇だし、いってきます。」",
    "――こうして、もぐらのちょっと変わった冒険が始まったのでした。",
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
            img.fill((80, 80, 80))
        images.append(img)
    return images

def handle_event(event, state, sound_manager=None):
    if event.type == pygame.KEYDOWN:
        if state["in_dialog"] and event.key == pygame.K_RETURN:
            if state["text_index"] < len(script) - 1:
                state["text_index"] += 1
                # ここで音声再生！
                if sound_manager is not None:
                    # 現在のテキストindexでvoice再生
                    filename = voice_files[state["text_index"]]
                    sound_manager.play_voice(filename)
            else:
                state["in_dialog"] = False
                # 最後のvoiceもstop
                if sound_manager is not None:
                    sound_manager.stop_voice()
        elif not state["in_dialog"] and event.key == pygame.K_RETURN:
            state["text_index"] = 0
            state["in_dialog"] = True
            return "end"
    return None

def wrap_text(text, font, max_width):
    """日本語やスペースのない文でも自動折り返し"""
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
    セリフから「話者名」と本文を分離して返す関数。
    例：「もぐら：「～」」→ ("もぐら", "～")
    会話ラベルがなければ、(None, dialog) を返す。
    """
    if "「" in dialog and dialog.endswith("」"):
        npc, text = dialog.split("「", 1)
        text = text.rstrip("」")
        return npc, "「" + text + "」"
    return None, dialog  # 会話ラベルなし

def draw(screen, font, WIDTH, HEIGHT, state, sound_manager=None):
    # 背景画像の表示
    if state["bg_images"] is None:
        state["bg_images"] = load_bg_images()
    bg_img = state["bg_images"][state["text_index"]]
    screen.blit(bg_img, (0, 0))

    # 下部ウィンドウ
    window_rect = pygame.Surface((WIDTH - 120, 210), pygame.SRCALPHA)
    window_rect.fill((0, 0, 0, 180))
    screen.blit(window_rect, (50, HEIGHT - 250))

    # 会話・ラベル自動抽出
    if state["in_dialog"]:
        dialog = script[state["text_index"]]
        npc, text = extract_npc_and_text(dialog)

        # --- 音声再生（未再生フラグで1回だけ）---
        if (not state.get("voice_played", False)) and (sound_manager is not None):
            filename = voice_files[state["text_index"]]
            sound_manager.play_voice(filename)
            state["voice_played"] = True

        # --- ナレーションの場合はラベル非表示 ---
        if npc:
            npc_label = font.render(npc, True, (255, 255, 255))
            screen.blit(npc_label, (70, HEIGHT - 250))

        # 本文折り返し表示
        max_text_width = WIDTH - 140
        lines = wrap_text(text, font, max_text_width)
        y0 = HEIGHT - 210
        for i, line in enumerate(lines):
            dialog_surface = font.render(line, True, (255, 255, 255))
            screen.blit(dialog_surface, (70, y0 + i * 40))
        hint = font.render("Enter: 次へ", True, (255, 255, 255))
        screen.blit(hint, (WIDTH - 180, HEIGHT - 50))
    else:
        end_msg = font.render("Enter:スタート", True, (255, 255, 255))
        screen.blit(end_msg, (WIDTH // 2 - 120, HEIGHT - 120))

