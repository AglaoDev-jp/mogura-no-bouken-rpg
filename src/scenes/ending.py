# scenes/ending.py
import pygame
from pathlib import Path

# ◆エンディングシーン状態変数
state = {
    "text_index": 0,
    "in_dialog": True,
    "bg_images": None,
    "voice_played": False,
}

bg_files = [
    "ending_bg_00.png", 
    "ending_bg_00.png", 
    "ending_bg_00.png", 
    "ending_bg_00.png",
    "ending_bg_00.png", 
    "ending_bg_03.png", # 城へ帰る
    "ending_bg_05.png", 
    "ending_bg_06.png",
    "ending_bg_06.png", 
    "ending_bg_07.png",
    "ending_bg_07.png", 
    "ending_bg_08.png",
    "ending_bg_08.png", 
    "ending_bg_08.png",
    "ending_bg_09.png", 
    "ending_bg_09.png", 
    "ending_bg_09.png", 
    "ending_bg_09.png",
    "ending_bg_10.png", 
    "ending_bg_11.png", 
    "endroll_bg.png",
    "endroll_bg.png",
]

voice_files = [
    "ending_voice_00.mp3", "ending_voice_01.mp3", "ending_voice_02.mp3", "ending_voice_03.mp3", "ending_voice_04.mp3",
    "ending_voice_05.mp3", "ending_voice_06.mp3", "ending_voice_07.mp3", "ending_voice_08.mp3", "ending_voice_09.mp3",
    "ending_voice_10.mp3", "ending_voice_11.mp3", "ending_voice_12.mp3", "ending_voice_13.mp3", "ending_voice_14.mp3",
    "ending_voice_15.mp3", "ending_voice_16.mp3", "ending_voice_17.mp3", "ending_voice_18.mp3", "ending_voice_19.mp3",
    "ending_voice_20.mp3", "ending_voice_21.mp3",
]

# ◆エンディングシナリオ
script = [
    "もぐら：「やった。勝った。」",
    "しゅごもぐら：「うそん……負けた……。もぐらくん、君がここまで強いとは思わなかったよ……。」",
    "もぐら：「道すがら“ごちサンド”いっぱい食べてきたんだ。パワーでたねぇ。」",
    "しゅごもぐら：「そ、そうだったのか……。僕も勇者に会いたかったなぁ……。会ったらよろしくいっといてよ。」",
    "もぐら：「わかった。」",
    
    "かくして“テカテカのたま”を手に入れたもぐらくん。どうやらお城に帰ってきたようですよ。",

    "もぐら：「ただいま、王様。テカテカのたまとってきたよ。」",

    "王様：「おおっ、よくぞやったもぐらよ！　これで世界は救われる…っ、が…それどころではないのだ！」",

    "もぐら：「どしたんすか、王様？　そんなに慌てて。」",
    "王様：「そ、それが…伝説の勇者殿が……寝込んでしまわれたのだ！」",

    "もぐら：「へ！？　何があったんです？」",
    "王様：「わしが…もぐら達に作らせた料理をふるまったら…どうやらお腹に合わなかったようでのぅ…」",

    "もぐら：「あーあ、王様。もぐらの料理を旅人に出すもんじゃないっすよ。そりゃ無茶ってもんですよ。」",
    "王様：「うう…どうしよう、勇者殿は世界を救うお方なのに…」",
    "もぐら：「いーけないんだー、王様のせいで世界が終わりますよー」",
    "王様：「そ、そんな…わしはただ…」",
    "もぐら：「王様のせいで世界が滅びた！なんて言われちゃいますよ？自分だけ勇者にいい顔しようとした罰ですかねー。」",
    "王様：「うぅ…そんなつもりじゃ…良かれと思ったんじゃ…！」",

    "もぐら：「ま、いいや。ダンジョンで“ごちサンド”たくさん食べたし、ちょっと腹ごなしに出かけてきますよ。」",
    "王様：「ど、どこへ行くのだ、こんな大変なときに！」",

    "もぐら：「…魔王退治っす！」",

    "こうして、もぐらくんの新たな冒険が始まるのでした――"
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
            img.fill((0, 0, 0))
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
    screen.blit(bg_images[bg_idx], (0, 0)) if bg_images else screen.fill((0, 0, 0))
    
    window_rect = pygame.Surface((WIDTH - 100, 180), pygame.SRCALPHA)
    window_rect.fill((0, 0, 0, 180))
    screen.blit(window_rect, (50, HEIGHT - 210))

    if state["in_dialog"]:
        idx = min(state["text_index"], len(script) - 1)
        dialog = script[idx]
        npc, text = extract_npc_and_text(dialog)

        # ---- 音声再生（未再生時のみ）----
        if (not state.get("voice_played", False)) and (sound_manager is not None):
            filename = voice_files[state["text_index"]]
            sound_manager.play_voice(filename)
            state["voice_played"] = True

        if npc:
            npc_label = font.render(npc, True, (255, 255, 255))
            screen.blit(npc_label, (70, HEIGHT - 200))
        lines = wrap_text(text, font, WIDTH - 140)
        y0 = HEIGHT - 170
        for i, line in enumerate(lines):
            dialog_surface = font.render(line, True, (255, 255, 255))
            screen.blit(dialog_surface, (70, y0 + i * 40))
        hint = font.render("Enter: 次へ", True, (255, 255, 255))
        screen.blit(hint, (WIDTH - 180, HEIGHT - 50))

def handle_event(event, state, sound_manager=None):
    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
        if state["in_dialog"]:
            if state["text_index"] < len(script) - 1:
                state["text_index"] += 1
                state["voice_played"] = False  # 次のテキストで再生可能に
            else:
                # 終了直前に音声停止（お好みで）
                if sound_manager:
                    sound_manager.stop_voice()

                return "endroll" # 最後の一文のEnterでスタッフロールへ
    return None
