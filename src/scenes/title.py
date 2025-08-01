# scenes/title.py
import pygame
from pathlib import Path
from scenes.save_load import save_file_exists

title_state = {
    "selected": 0,
    "options": ["初めから", "続きから"],
    "bg": None,  # 背景画像
}
# クリア済みフラグ（仮）
cleared = False  # クリア時にTrueにする

def update_options():
    # optionsリストを状況に応じて動的に変更
    # どれかひとつでもセーブがあれば「続きから」を出す
    has_any_save = any(save_file_exists(slot) for slot in [1, 2, 3])
    if cleared:
        if has_any_save:
            return ["初めから", "続きから", "あとがき"]
        else:
            return ["初めから", "あとがき"]
    else:
        if has_any_save:
            return ["初めから", "続きから"]
        else:
            return ["初めから"]

    
def handle_event(event, state):
    state["options"] = update_options()  # ここで毎回更新
    n = len(state["options"])
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            state["selected"] = (state["selected"] - 1) % n
        elif event.key == pygame.K_DOWN:
            state["selected"] = (state["selected"] + 1) % n
        elif event.key == pygame.K_RETURN:
            if state["selected"] == 0:
                return "start"
            elif state["selected"] == 1:
                return "continue"
            elif n >= 3 and state["selected"] == 2:
                return "afterword"  # あとがきシーンへ
    return None

def draw(screen, font, WIDTH, HEIGHT, state):
    # ===== 画像の初回ロード =====
    if state["bg"] is None:
        BASE_DIR = Path(__file__).resolve().parent.parent
        bg_path = BASE_DIR / "assets" / "images" / "title_bg.png"
        try:
            bg_img = pygame.image.load(str(bg_path)).convert()
            bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
        except Exception:
            bg_img = pygame.Surface((WIDTH, HEIGHT))
            bg_img.fill((80, 60, 120))
        state["bg"] = bg_img

    screen.blit(state["bg"], (0, 0))

    # ===== 選択肢を表示 =====
    center_x = 490
    base_y = 430

    for i, opt in enumerate(state["options"]):
        color = (255, 255, 0) if i == state["selected"] else (255, 255, 255)
        txt = font.render(opt, True, color)
        txt_rect = txt.get_rect(center=(center_x, base_y + i * 50))
        screen.blit(txt, txt_rect)

    # ヒントも下中央に
    hint = font.render("↑↓:選択 Enter:決定", True, (255, 255, 255))
    hint_rect = hint.get_rect(center=(center_x, HEIGHT - 25))
    screen.blit(hint, hint_rect)
