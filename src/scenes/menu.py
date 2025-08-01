# scenes/menu.py
import pygame
from pathlib import Path
from status import player_status
from status import get_total_status
from scenes.save_load import save_game, load_game
from pathlib import Path
import json
from scenes.save_load import get_save_path
from scenes.save_load import save_game, load_game, save_file_exists


# ======== 画像読み込み（初回のみ）========
menu_bg = None
status_bg = None
# item_bg = None アイテムの画像読み込みは"scenes/inventory.py"にあります。
save_bg = None
load_bg = None

def load_images():
    global menu_bg, status_bg, save_bg, load_bg
    if menu_bg is None:
        base = Path(__file__).resolve().parent.parent / "assets" / "images"
        menu_bg = pygame.image.load(str(base / "menu_bg.png")).convert()
        menu_bg = pygame.transform.scale(menu_bg, (800, 600))
        # セーブ画面用
        if (base / "save_bg.png").exists():
            save_bg = pygame.image.load(str(base / "save_bg.png")).convert()
            save_bg = pygame.transform.scale(save_bg, (800, 600))
        else:
            save_bg = menu_bg
        # ロード画面用
        if (base / "load_bg.png").exists():
            load_bg = pygame.image.load(str(base / "load_bg.png")).convert()
            load_bg = pygame.transform.scale(load_bg, (800, 600))
        else:
            load_bg = menu_bg
        # ステータス画面用
        if (base / "status_bg.png").exists():
            status_bg = pygame.image.load(str(base / "status_bg.png")).convert()
            status_bg = pygame.transform.scale(status_bg, (800, 600))
        else:
            status_bg = menu_bg

# ===============================
# メニューのモード管理
# ===============================
MODE_MENU = 0          # メインメニュー
MODE_STATUS = 1        # ステータス画面
MODE_SAVE_SELECT = 2   # セーブスロット選択
MODE_LOAD_SELECT = 3   # ロードスロット選択
MODE_SAVE_MSG = 4      # セーブ完了メッセージ
MODE_LOAD_MSG = 5      # ロード完了メッセージ
MODE_LOAD_ERROR = 6    # セーブデータが存在しない場合のメッセージ
MODE_VOLUME = 7        # 音量設定モード

mode = MODE_MENU

last_mode = MODE_MENU  # 初期値をメニューに

# --- 各カーソルインデックス ---
menu_index = 0        # メニュー選択用
slot_index = 0        # セーブ／ロードスロット選択用

volume_index = 0  # 0:BGM, 1:SE, 2:Voice
volume_names = ["BGM音量", "効果音音量", "音声音量"]

# --- メニュー項目 ---
menu_items = [
    "ステータスを見る",
    "アイテムを見る",
    "セーブする",
    "ロードする",
    "音量設定", 
]

save_slots = [
    "スロット1にセーブ",
    "スロット2にセーブ",
    "スロット3にセーブ",
    "キャンセル"
]
load_slots = [
    "スロット1からロード",
    "スロット2からロード",
    "スロット3からロード",
    "キャンセル"
]

def get_slot_info(slot_no):
    """
    指定スロットのセーブデータから「名前」と「レベル」を取得
    Returns: (name, level)  例: ("もぐら", 3) / セーブなしなら ("---", "-")
    """
    file_path = Path(get_save_path(slot=slot_no))
    if not file_path.exists():
        return ("---", "-")
    try:
        with file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        p = data.get("player_status", {})
        name = p.get("name", "---")
        lv = p.get("lv", "-")
        return (str(name), str(lv))
    except Exception:
        return ("???", "?")

# --- 完了メッセージ ---
message = ""

def handle_event(event, sound_manager):
    """キー入力イベント処理"""
    global mode, last_mode, menu_index, slot_index, message, volume_index
    # 先頭で前回のmodeを記録（イベントごとに必ず更新）
    prev_mode = mode

    if mode == MODE_MENU:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                menu_index = (menu_index + 1) % len(menu_items)
                sound_manager.play_se("cursor")
            elif event.key == pygame.K_UP:
                menu_index = (menu_index - 1) % len(menu_items)
                sound_manager.play_se("cursor")
            elif event.key == pygame.K_RETURN:
                selected = menu_items[menu_index]
                if selected == "音量設定":
                    sound_manager.play_se("select")
                    mode = MODE_VOLUME
                    volume_index = 0
                elif selected == "ステータスを見る":
                    sound_manager.play_se("select")
                    mode = MODE_STATUS
                elif selected == "セーブする":
                    sound_manager.play_se("select")
                    slot_index = 0
                    mode = MODE_SAVE_SELECT
                elif selected == "ロードする":
                    sound_manager.play_se("select")
                    slot_index = 0
                    mode = MODE_LOAD_SELECT
                elif selected == "アイテムを見る":
                    sound_manager.play_se("select")
                    return "アイテム"  # 必要に応じて切り替え
                
            elif event.key == pygame.K_ESCAPE:
                sound_manager.play_se("cancel")
                return "戻る"

    elif mode == MODE_STATUS:
        if event.type == pygame.KEYDOWN and (event.key in [pygame.K_ESCAPE, pygame.K_RETURN]):
            sound_manager.play_se("cancel")
            mode = MODE_MENU

    elif mode in (MODE_SAVE_SELECT, MODE_LOAD_SELECT):
        slot_list = save_slots if mode == MODE_SAVE_SELECT else load_slots
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                sound_manager.play_se("cursor")
                slot_index = (slot_index + 1) % len(slot_list)
            elif event.key == pygame.K_UP:
                sound_manager.play_se("cursor")
                slot_index = (slot_index - 1) % len(slot_list)
            elif event.key == pygame.K_RETURN:
                # キャンセル選択で戻る
                if slot_index == 3:
                    sound_manager.play_se("cancel")
                    mode = MODE_MENU
                    return
                slot_no = slot_index + 1
                if mode == MODE_SAVE_SELECT:
                    sound_manager.play_se("save")
                    save_game(slot=slot_no)
                    message = f"スロット{slot_no}にセーブしました！（Enter/Escで戻る）"
                    mode = MODE_SAVE_MSG
                else:
                    # ★ここで空スロットならエラー画面に遷移
                    if not save_file_exists(slot_no):
                        sound_manager.play_se("error")
                        message = "セーブデータが存在しません"
                        mode = MODE_LOAD_ERROR
                        return
                    sound_manager.play_se("load")
                    load_game(slot=slot_no)
                    message = f"スロット{slot_no}からロードしました！（Enter/Escで戻る）"
                    mode = MODE_LOAD_MSG
            elif event.key == pygame.K_ESCAPE:
                sound_manager.play_se("cancel")
                mode = MODE_MENU
                
    elif mode == MODE_VOLUME:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                volume_index = (volume_index + 1) % 3
                sound_manager.play_se("cursor")
            elif event.key == pygame.K_UP:
                volume_index = (volume_index - 1) % 3
                sound_manager.play_se("cursor")
            elif event.key == pygame.K_RIGHT:
                if volume_index == 0:
                    sound_manager.set_bgm_volume(sound_manager.bgm_volume + 0.05)
                elif volume_index == 1:
                    sound_manager.set_se_volume(sound_manager.se_volume + 0.05)
                elif volume_index == 2:
                    sound_manager.set_voice_volume(sound_manager.voice_volume + 0.05)
                sound_manager.apply_volume()
                sound_manager.save_settings()
                sound_manager.play_se("select")
            elif event.key == pygame.K_LEFT:
                if volume_index == 0:
                    sound_manager.set_bgm_volume(sound_manager.bgm_volume - 0.05)
                elif volume_index == 1:
                    sound_manager.set_se_volume(sound_manager.se_volume - 0.05)
                elif volume_index == 2:
                    sound_manager.set_voice_volume(sound_manager.voice_volume - 0.05)
                sound_manager.apply_volume()
                sound_manager.save_settings()
                sound_manager.play_se("select")
            elif event.key in [pygame.K_RETURN, pygame.K_ESCAPE]:
                sound_manager.play_se("cancel")
                mode = MODE_MENU
                # 変更を保存
                sound_manager.save_settings()
    # ★エラー時はEnter/Escでスロット選択画面に戻す
    elif mode == MODE_LOAD_ERROR:
        if event.type == pygame.KEYDOWN and event.key in [pygame.K_RETURN, pygame.K_ESCAPE]:
            sound_manager.play_se("cancel")
            message = ""
            mode = MODE_LOAD_SELECT  # ロードスロット選択に戻す

    elif mode in (MODE_SAVE_MSG, MODE_LOAD_MSG):
        if event.type == pygame.KEYDOWN and (event.key in [pygame.K_ESCAPE, pygame.K_RETURN]):
            sound_manager.play_se("cancel")
            mode = MODE_MENU
    # 最後でlast_modeを更新
    last_mode = prev_mode

    return None

def draw(screen, font, WIDTH, HEIGHT, sound_manager):
    """メニュー画面描画"""
    load_images()
    global mode, menu_index, slot_index, message, volume_index

    if mode == MODE_MENU:
        # メインメニュー描画
        screen.blit(menu_bg, (0, 0))
        title = font.render("=== メニュー ===", True, (255, 255, 255))
        screen.blit(title, (WIDTH // 2 - 200, HEIGHT // 2 - 150))
        for i, item in enumerate(menu_items):
            prefix = "▶ " if i == menu_index else "   "
            color = (255, 255, 0) if i == menu_index else (255, 255, 255)
            label = font.render(prefix + item, True, color)
            screen.blit(label, (WIDTH // 2 - 200, HEIGHT // 2 - 80 + i * 40))
        # サブステータス表示
        hp_text = f"HP: {player_status['hp']} / {player_status['max_hp']}"
        lv_text = f"Lv: {player_status.get('lv', 1)}"
        gold_text = f"G: {player_status['gold']}"
        hp_surface = font.render(hp_text, True, (255, 255, 255))
        lv_surface = font.render(lv_text, True, (255, 255, 255))
        gold_surface = font.render(gold_text, True, (255, 255, 0))
        screen.blit(hp_surface, (20, 20))
        screen.blit(lv_surface, (20, 50))
        screen.blit(gold_surface, (20, 80))
        guide = font.render("↑↓:選択 Enter:決定 Esc:戻る", True, (200, 200, 100))
        screen.blit(guide, (WIDTH // 2 - 45, HEIGHT // 2 + 250))

    elif mode == MODE_STATUS:
        # ステータス画面描画
        screen.blit(status_bg, (0, 0))
        title = font.render("=== ステータス ===", True, (100, 255, 255))
        screen.blit(title, (WIDTH // 2 - 200, HEIGHT // 2 - 180))
        total = get_total_status()
        name = player_status.get("name", "")
        lv = f"レベル: {player_status.get('lv', 1)}"
        hp = f"HP: {player_status['hp']} / {player_status['max_hp']}"
        atk = f"攻撃力: {total['atk']}"
        if player_status["equip"].get("weapon"):
            atk += f"（{player_status['equip']['weapon']}装備）"
        defense = f"防御力: {total['def_']}"
        if player_status["equip"].get("armor"):
            defense += f"（{player_status['equip']['armor']}装備）"
        gold = f"G: {player_status['gold']}"
        exp = f"経験値: {player_status.get('exp', 0)}"
        status_lines = [
            f"名前: {name}", lv, hp, atk, defense, gold, exp,
        ]
        for i, line in enumerate(status_lines):
            text = font.render(line, True, (255, 255, 255))
            screen.blit(text, (WIDTH // 2 - 200, HEIGHT // 2 - 120 + i * 40))
        info = font.render("EnterまたはEscでメニューへ戻る", True, (200, 200, 100))
        screen.blit(info, (WIDTH // 2 - 90, HEIGHT // 2 + 250))

    elif mode in (MODE_SAVE_SELECT, MODE_LOAD_SELECT):
        # ★セーブ／ロード画面ごとに背景を変える
        if mode == MODE_SAVE_SELECT:
            screen.blit(save_bg, (0, 0))
        else:
            screen.blit(load_bg, (0, 0))
        is_save = (mode == MODE_SAVE_SELECT)
        title_str = "=== セーブスロット選択 ===" if is_save else "=== ロードスロット選択 ==="
        title = font.render(title_str, True, (0, 255, 255))
        screen.blit(title, (WIDTH // 2 - 210, HEIGHT // 2 - 150))
        slots = save_slots if is_save else load_slots
        for i, item in enumerate(slots):
            is_selected = (i == slot_index)
            color = (0, 255, 0) if is_selected else (255, 255, 255)
            info_color = (0, 255, 0) if is_selected else (180, 180, 180)
            prefix = "▶ " if is_selected else "   "
            label = font.render(prefix + item, True, color)
            screen.blit(label, (WIDTH // 2 - 330, HEIGHT // 2 - 60 + i * 40))
            if i < 3:
                name, lv = get_slot_info(i+1)
                info_text = f"名前: {name} / Lv: {lv}"
                info_label = font.render(info_text, True, info_color)
                screen.blit(info_label, (WIDTH // 2 + 30, HEIGHT // 2 - 60 + i * 40))
        guide = font.render("↑↓:選択 Enter:決定 Esc:戻る", True, (200, 200, 100))
        screen.blit(guide, (WIDTH // 2 - 45, HEIGHT // 2 + 250))

    elif mode == MODE_LOAD_ERROR:
        # エラーメッセージ画面
        screen.blit(menu_bg, (0, 0))
        msg = font.render(message, True, (255, 180, 80))
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 40))
        guide = font.render("Enterで戻る", True, (200, 200, 100))
        screen.blit(guide, (WIDTH // 2 - guide.get_width() // 2, HEIGHT // 2 + 30))

    elif mode == MODE_SAVE_MSG:
        screen.blit(menu_bg, (0, 0))
        msg = font.render(message, True, (0, 255, 0))
        screen.blit(msg, (WIDTH // 20, HEIGHT // 2 - 40))
        guide = font.render("EnterまたはEscでメニューへ戻る", True, (200, 200, 100))
        screen.blit(guide, (WIDTH // 2 - 90, HEIGHT // 2 + 250))

    elif mode == MODE_LOAD_MSG:
        screen.blit(menu_bg, (0, 0))
        msg = font.render(message, True, (0, 255, 0))
        screen.blit(msg, (WIDTH // 20, HEIGHT // 2 - 40))
        guide = font.render("EnterまたはEscでメニューへ戻る", True, (200, 200, 100))
        screen.blit(guide, (WIDTH // 2 - 90, HEIGHT // 2 + 250))
    
    elif mode == MODE_VOLUME:
        # 音量設定画面描画
        screen.blit(menu_bg, (0, 0))
        # タイトル
        title_surf = font.render("=== 音量設定 ===", True, (255, 255, 255))
        screen.blit(title_surf, ((WIDTH - title_surf.get_width()) // 2, HEIGHT // 2 - 160))
        # 各項目と現在値を表示
        for i, name in enumerate(volume_names):
            prefix = "▶ " if i == volume_index else "   "
            color  = (255, 255, 0) if i == volume_index else (255, 255, 255)
            # 現在の音量（0.0〜1.0）をパーセンテージに
            if i == 0:
                vol = sound_manager.bgm_volume
            elif i == 1:
                vol = sound_manager.se_volume
            else:
                vol = sound_manager.voice_volume
            vol_percent = int(vol * 100)
            text = f"{prefix}{name}: {vol_percent}%"
            label = font.render(text, True, color)
            screen.blit(label, (WIDTH // 2 - 200, HEIGHT // 2 - 80 + i * 50))
        # 操作ガイド
        guide = font.render("↑↓:選択  ←→:調整  Enter/Esc:戻る", True, (200, 200, 100))
        screen.blit(guide, (WIDTH // 2 - 130, HEIGHT // 2 + 250))
