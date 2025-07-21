# scenes/inventory.py
import pygame
from pathlib import Path
from collections import Counter
from status import player_status
from status import EQUIPMENT_TABLE, equip_item, unequip   
from item_effects import use_item
import item_effects

cursor_index = 0
message = ""  # 効果メッセージ表示用

# ダンジョン脱出用の状態フラグ
escape_pending = False

# --- 背景画像を一度だけロード ---
item_bg = None

def load_images():
    global item_bg
    if item_bg is None:
        base = Path(__file__).resolve().parent.parent / "assets" / "images"
        try:
            item_bg = pygame.image.load(str(base / "item_bg.png")).convert()
            item_bg = pygame.transform.scale(item_bg, (800, 600))
        except Exception:
            item_bg = None  # 画像がなければNone

def is_equipment(item_name):
    """装備品かどうか判定"""
    return item_name in EQUIPMENT_TABLE

def handle_event(event, sound_manager, context="dungeon"):
    global cursor_index, message, escape_pending
    # --- 1) まず脱出待ちフラグ優先処理 ---
    if escape_pending:
         if event.type == pygame.KEYDOWN and event.key in [pygame.K_RETURN, pygame.K_z]:
             escape_pending = False
             message = ""
             return "escape_dungeon"
         return None

    # --- 2) 脱出待ちでなければ、改めてアイテムリストを取得 ---
    item_list = get_item_list()

    # リストが空、またはカーソル位置が範囲外なら0にリセット(バグ防止)
    if not item_list:
        cursor_index = 0 # リセット。
        return "戻る"
    elif cursor_index >= len(item_list):
        cursor_index = max(0, len(item_list) - 1) # カーソルがリスト末尾を超えていたら「最後の項目」に合わせる

     # ── ここからは item_list が空でない前提 ──
     # 現在選択中のアイテム
    selected_item = item_list[cursor_index][0]

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_DOWN:
            sound_manager.play_se("cursor")
            cursor_index = (cursor_index + 1) % len(item_list)
        elif event.key == pygame.K_UP:
            sound_manager.play_se("cursor")
            cursor_index = (cursor_index - 1) % len(item_list)
        elif event.key in [pygame.K_RETURN, pygame.K_z]:
            # ----装備品分岐----
            if is_equipment(selected_item):
                kind = EQUIPMENT_TABLE[selected_item]["kind"]
                # すでに装備中なら「外す」
                if player_status["equip"].get(kind) == selected_item:
                    sound_manager.play_se("equip")                    
                    message = unequip(kind)
                else:
                    sound_manager.play_se("unequip")
                    message = equip_item(selected_item)
            else:
                result = use_item(selected_item, context=context, sound_manager=sound_manager)
                if (
                    isinstance(result, dict)
                    and result.get("result") == "escape_dungeon"
                ):
                    if context != "dungeon":
                        # トロッコは町では使えないように制限
                        message = "ここではトロッコは使えない！"
                        sound_manager.play_se("cancel")
                    else:
                        sound_manager.play_se("warp")
                        message = result.get("message", "トロッコで脱出！")
                        escape_pending = True # ←ここで脱出待ちフラグを立てる
                else:
                    message = result # 通常アイテムの効果メッセージ
        elif event.key == pygame.K_ESCAPE:
            sound_manager.play_se("cancel")
            message = ""
            return "戻る"
    return None


def draw(screen, font, WIDTH, HEIGHT):
    load_images()
    # --- 背景画像 ---
    if item_bg:
        screen.blit(item_bg, (0, 0))
    else:
        screen.fill((40, 40, 60))

    # タイトル
    title = font.render("=== アイテム ===", True, (255, 255, 255))
    screen.blit(title, (WIDTH // 2 - 140, 40))

    item_list = get_item_list()
    if not item_list:
        text = font.render("所持アイテムはありません。", True, (255, 200, 200))
        screen.blit(text, (60, 120))
    else:
        for i, (name, count) in enumerate(item_list):
            prefix = "▶ " if i == cursor_index else "   "
            color = (255, 255, 0) if i == cursor_index else (255, 255, 255)
            # 装備品なら装備中マークを付与
            equip_mark = ""
            if is_equipment(name):
                kind = EQUIPMENT_TABLE[name]["kind"]
                if player_status["equip"].get(kind) == name:
                    equip_mark = " ★装備中"
            label = font.render(f"{prefix}{name} × {count}{equip_mark}", True, color)
            screen.blit(label, (60, 120 + i * 40))

    # 効果メッセージ表示（下部に大きめ＆目立つ色で表示）
    if message:
        msg_surface = font.render(message, True, (100, 255, 100))
        screen.blit(msg_surface, (60, HEIGHT - 120))

    # 操作ヒント
    guide = font.render("↑↓:選択 Enter:決定 Esc:戻る", True, (200, 200, 100))
    screen.blit(guide, (WIDTH // 2 - 45, HEIGHT // 2 + 250))

def get_item_list():
    # 所持数が 1 以上のものだけ返す
    from collections import Counter
    return [(name, cnt) for name, cnt in Counter(player_status["items"]).items() if cnt > 0]
