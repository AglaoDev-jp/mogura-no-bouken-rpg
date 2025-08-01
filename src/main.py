# main.py
"""
Copyright © 2025 AglaoDev-jp

---

Code by AglaoDev-jp © 2025  
Licensed under the MIT License.

Image by AglaoDev-jp © 2025  
Licensed under the Creative Commons Attribution 4.0 International (CC BY 4.0).

Scenario by AglaoDev-jp © 2025  
Licensed under the Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).

---

## Fonts Used

This game uses the "Noto Sans JP" font family (NotoSansJP-Regular.otf).

- **Noto Sans JP**  
  © 2014–2025 Google LLC  
  Licensed under the SIL Open Font License, Version 1.1.  
  See [OFL License](https://scripts.sil.org/OFL) for more information.

---

## External Libraries

- **pygame**  
  Copyright © 2000–2024 Pygame developers  
  Licensed under the LGPL v2.1 License.  
  See LICENSE-pygame.txt or visit:  
  https://www.pygame.org/docs/license.html

- cryptography:  
  Copyright © 2013-2025 The cryptography developers  
  Licensed under the Apache License, Version 2.0 or the BSD 3-Clause License.  
  For full details, see LICENSE-cryptography.txt or visit:  
  [Cryptography License](https://github.com/pyca/cryptography/blob/main/LICENSE)

  This software includes cryptographic components from OpenSSL 3.4.0 (22 Oct 2024), distributed under the Apache License 2.0.  
  For details, see LICENSE-OpenSSL.txt or [OpenSSL License](https://www.openssl.org/source/license.html).  
  Copyright (c) 1998-2025 The OpenSSL Project Authors  
  Copyright (c) 1995-1998 Eric A. Young, Tim J. Hudson  
  All rights reserved.

- Cython
  Cython © 2007-2025 The Cython Project Developers  
  Licensed under the Apache License 2.0.  

Special thanks to all developers and contributors who made this library possible.

---

*This file was created and refined with support from OpenAI’s conversational AI, ChatGPT.*  
*We greatly benefited from its assistance in idea generation, code improvements, and design support.*

"""

import os
print("Current Working Directory:", os.getcwd())
import pygame
import sys
import copy
import traceback
print("=== import直後 ===")

# ================================
# エラー内容をファイルへ保存する関数
# ================================
def save_traceback(e):
    """例外内容を 'error_log.txt' に追記保存します"""
    with open("error_log.txt", "a", encoding="utf-8") as f:
        traceback.print_exc(file=f)

# ================================
# 未処理例外も自動記録（グローバルフック）
# ================================
sys.excepthook = lambda exc_type, exc_value, exc_traceback: (
    print("=== Uncaught Exception ==="),
    traceback.print_exception(exc_type, exc_value, exc_traceback),
    save_traceback(exc_value)
)

from pathlib import Path
# 各シーンのインポート
from scenes import inn, shop, menu, inventory, dungeon, castle
from scenes.castle import castle_states
from scenes.castle import init_state as castle_init_state
from scenes.inn import inn_state, handle_event as inn_handle_event, draw as inn_draw
from scenes.shop import shop_state, handle_event as shop_handle_event, draw as shop_draw
from status import player_status, ENEMY_TABLE
from scenes.opening_event import event_state as opening_state, handle_event as opening_handle_event, draw as opening_draw
from scenes import title
from player import Player
from scenes import boss_event_k   
print("boss_event_kインポート成功:", boss_event_k)
from scenes import boss_event_d
print("boss_event_dインポート成功:", boss_event_d)
from scenes import boss_event_f
print("boss_event_fインポート成功:", boss_event_f)
from scenes import ending
from scenes import endroll
from scenes.save_load import save_game, load_game
from status import initial_player_status
from cryptography.fernet import Fernet

# タイトル画面の状態（管理変数）
title_state = title.title_state

# ========================
# 基本設定
# ========================
WIDTH, HEIGHT = 800, 600
FPS = 60
PLAYER_SPEED = 6
BUILDING_WIDTH, BUILDING_HEIGHT = 240, 200
BLACK, WHITE = (0, 0, 0), (255, 255, 255)

# ========================
# 初期化
# ========================
pygame.init() # 初期化
pygame.mixer.init()  # ← サウンドの初期化
is_fullscreen = False

# ウィンドウモード（800×600）で起動
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen_width, screen_height = screen.get_size()

# 解像度800×600の描画用サーフェスを作成
# 以降の描画はこの game_surface に対して行い、
# 最終的に screen にスケーリングして貼り付けます
game_surface = pygame.Surface((WIDTH, HEIGHT))
pygame.display.set_caption("もぐらの冒険RPG")
clock = pygame.time.Clock()

print("=== リソースロード直前 ===")

# サウンドマネージャのインポート
# pygame.mixer（サウンド機能）は、pygame.mixer.init()を呼ばないと使えません。
from sound_manager import SoundManager # 初期化の後にインポートこれ大事
import scenes.menu as menu # 効果音

# フォント
BASE_DIR = Path(__file__).resolve().parent
font_path = BASE_DIR / "assets" / "fonts" / "NotoSansJP-Regular.ttf"
font = pygame.font.Font(str(font_path), 32)
print("フォントロード成功")

# プレイヤー画像

player = Player(start_pos=(WIDTH // 2, HEIGHT - 100), base_dir=BASE_DIR)
print("プレイヤー画像ロード成功")

# 背景画像
bg_path = BASE_DIR / "assets" / "images" / "town_background.png"
background = pygame.image.load(str(bg_path)).convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
print("背景画像ロード成功")

# サウンドマネージャのインスタンスを作成
sound_manager = SoundManager(BASE_DIR / "assets" / "sounds")
print("サウンドマネージャ成功")

# 建物ラベル/画像/位置
building_labels = {
    "dungeon": "ダンジョン",
    "castle": "お城",
    "inn": "宿屋",
    "shop": "道具屋",
}
building_images = {
    "dungeon": pygame.image.load(str(BASE_DIR / "assets" / "images" / "dungeon.png")).convert_alpha(),
    "castle": pygame.image.load(str(BASE_DIR / "assets" / "images" / "castle.png")).convert_alpha(),
    "inn": pygame.image.load(str(BASE_DIR / "assets" / "images" / "inn.png")).convert_alpha(),
    "shop": pygame.image.load(str(BASE_DIR / "assets" / "images" / "shop.png")).convert_alpha(),
}
building_data = {
    "dungeon": (250, 20),
    "castle": (550, 20),
    "inn": (20, 200),
    "shop": (20, 400),
}
buildings = {name: pygame.Rect(x, y, BUILDING_WIDTH, BUILDING_HEIGHT)
             for name, (x, y) in building_data.items()}
print("建物画像ロード開始")
for name in building_images:
    print(f"  - {name}画像スケーリング前")
    building_images[name] = pygame.transform.scale(building_images[name], (BUILDING_WIDTH, BUILDING_HEIGHT))
    print(f"  - {name}画像スケーリング完了")
print("建物画像ロード・スケーリング全完了")

# ========================
# シーンと状態管理
# ========================
current_scene = "title"      # ゲーム開始時はタイトル
previous_scene = None        # メニュー呼び出し元の保持
from_title = False  # タイトル画面からロードしたかどうかのフラグ
was_load_successful = False # ロード成功判定（タイトル画面のロード）
scene_key = None # ← scene_key の初期化（ゲームオーバーでお城 or 町マップからお城）

def reset_game_state():
    """ゲーム全体の状態を初期化する関数"""
    global player_status
    from status import initial_player_status
    player_status.clear()
    player_status.update(copy.deepcopy(initial_player_status))

    # ダンジョン関係の状態を初期化
    import scenes.dungeon as dungeon
    dungeon.current_floor = 0
    dungeon.player_pos = [1, 1]
    dungeon.last_battle_pos = None
    dungeon.last_battle_tile = None
    dungeon.last_player_pos = None
    dungeon.action_locked = 0
    dungeon.boss_defeated_flags = {
        "K": False,
        "D": False,
        "F": False
    }
    # 🔥 ここが重要：ダンジョンマップ自体を初期状態に戻す！
    from scenes import dungeon
    dungeon.reset_dungeon_maps()

    print("[INFO] ゲーム状態を初期化しました")

# ========================
# メインループ
# ========================
running = True

try:
    print("=== メインループ突入 ===")
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                break

            # F11 でフルスクリーン⇄ウィンドウ切り替え
            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                if is_fullscreen:
                    # ウィンドウモードに戻す（800×600）
                    screen = pygame.display.set_mode((WIDTH, HEIGHT))
                    is_fullscreen = False
                else:
                    # フルスクリーンに戻す
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    is_fullscreen = True
                # 切り替え後は必ずサイズを再取得
                screen_width, screen_height = screen.get_size()
                # 次のイベント処理へ
                continue

        # キー入力取得 キーの長押し判定
        keys = pygame.key.get_pressed()

        # ==== イベント処理 ====
        for event in events:
            # 強制終了
            if event.type == pygame.QUIT:
                running = False
                break

            # タイトル画面
            if current_scene == "title":
                sound_manager.stop_bgm()
                result = title.handle_event(event, title_state)
                if result == "start":
                    sound_manager.play_bgm("お昼のうた.mp3.enc")
                    # オープニング state を初期化（再生フラグをリセット）
                    opening_state["text_index"]   = 0
                    opening_state["in_dialog"]    = True
                    opening_state["voice_played"] = False
                    current_scene = "opening_event"
                    break

                elif result == "continue":
                    # どのスロットにもセーブデータがある可能性を考慮し、ここではチェックしない
                    from_title = True
                    menu.mode = menu.MODE_LOAD_SELECT
                    menu.slot_index = 0
                    current_scene = "load_from_title"
                    break

                elif result == "afterword":
                    sound_manager.play_bgm("私の部屋.mp3.enc")
                    from scenes import afterword # 読み込み
                    afterword.state = afterword.init_state()  # あとがきの初期化（再読用）           
                    # あとがきへ遷移
                    current_scene = "afterword"
                    break

            # タイトルからロード           
            elif current_scene == "load_from_title":
                result = menu.handle_event(event, sound_manager)

                # ★ロード成功したことを記録
                if menu.mode == menu.MODE_LOAD_MSG:
                    was_load_successful = True

                # ----------------------
                # ロード時のプレイヤー復帰処理
                # ----------------------
                # ・セーブデータ内の「scene」と「player_pos」を見て復元
                # ・sceneがtownの場合は町の初期座標、dungeonの場合はマップ座標へ復帰
                # ・"inn", "shop", "castle"等もscene分岐で復帰可能
                # 本RPGは、初期位置にに戻ります。

                if menu.mode == menu.MODE_MENU:
                    if from_title:
                        if was_load_successful:
                            # --- ロード時は必ず町の初期位置から復活する ---
                            # ダンジョンや他の場所でセーブしても、
                            # プレイヤーは町の入口に強制復帰します。
                            # 拡張したい場合はここを分岐制御すればOKです。
                            player.set_center(WIDTH // 2, HEIGHT - 100)
                            current_scene = "town"
                            sound_manager.play_bgm("お昼のうた.mp3.enc")
                            # ── 追加：ダンジョン状態を初期化 ──
                            import scenes.dungeon as dungeon
                            # フロアとプレイヤー位置を最初に
                            dungeon.current_floor = 0
                            dungeon.player_pos    = [1, 1]
                            # ↓拡張したいときはsceneやplayer_statusを使う形に後で変更も可
                            # scene = player_status.get("scene", "town")
                            # pos = player_status.get("player_pos")
                            # if scene == "town":
                            #     if pos:
                            #         player.set_center(*pos)
                            #     else:
                            #         player.set_center(WIDTH // 2, HEIGHT - 100)
                            #     sound_manager.play_bgm("お昼のうた.mp3.enc")
                            #     current_scene = "town"
                        else:
                            current_scene = "title"
                        from_title = False
                        was_load_successful = False
                    break

            # オープニングイベント
            elif current_scene == "opening_event":
                result = opening_handle_event(event, opening_state, sound_manager)
                if result == "end":
                    current_scene = "town"
                    break

            # === ボスイベント（ごちみみず） ===
            elif current_scene == "boss_event_k":
                
                print("  [イベント] boss_event_k: 描画前")
                boss_event_k.draw(game_surface, font, WIDTH, HEIGHT, boss_event_k.state, sound_manager)
                print("  [イベント] boss_event_k: handle_event前")
                result = boss_event_k.handle_event(event, boss_event_k.state, sound_manager)
                if result == "battle":
                    sound_manager.play_bgm("Slapstick_Dance.mp3.enc")
                    print("  [イベント] boss_event_k -> battleへ遷移")
                    # ごちミミズのバトル開始
                    from scenes import battle
                    battle.reset_battle(ENEMY_TABLE["K"])  
                    current_scene = "battle"
                    from scenes import battle, dungeon
                    # プレイヤーの隣接タイルにあるボスの位置を記録
                    px, py = dungeon.player_pos
                    # 上下左右をチェックして "K" を見つけたら座標を保存
                    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                        nx, ny = px + dx, py + dy
                        if 0 <= ny < len(dungeon.dungeon_maps[dungeon.current_floor]) \
                           and 0 <= nx < len(dungeon.dungeon_maps[dungeon.current_floor][0]) \
                           and dungeon.dungeon_maps[dungeon.current_floor][ny][nx] == "K":
                            dungeon.last_battle_pos  = [nx, ny]
                            dungeon.last_battle_tile = "K"
                            dungeon.last_player_pos = [px, py]
                            break
                    # バトル開始処理
                    battle.reset_battle(ENEMY_TABLE["K"])
                    current_scene = "battle"                
                    break

            # === ボスイベント（ふかふかだんご） ===
            elif current_scene == "boss_event_d":
                boss_event_d.draw(game_surface, font, WIDTH, HEIGHT, boss_event_d.state, sound_manager)
                result = boss_event_d.handle_event(event, boss_event_d.state, sound_manager)
                if result == "battle":
                    sound_manager.play_bgm("Slapstick_Dance.mp3.enc") 
                    from scenes import battle, dungeon
                    battle.reset_battle(ENEMY_TABLE["D"])  # ふかふかだんご

                    # ボス位置記録処理
                    px, py = dungeon.player_pos
                    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                        nx, ny = px + dx, py + dy
                        if (0 <= ny < len(dungeon.dungeon_maps[dungeon.current_floor]) and
                            0 <= nx < len(dungeon.dungeon_maps[dungeon.current_floor][0]) and
                            dungeon.dungeon_maps[dungeon.current_floor][ny][nx] == "D"):
                            dungeon.last_battle_pos  = [nx, ny]
                            dungeon.last_battle_tile = "D"
                            dungeon.last_player_pos = [px, py]
                            break

                    current_scene = "battle"
                    break

            # === ボスイベント（しゅごもぐら） ===
            elif current_scene == "boss_event_f":
                # まず描画だけして
                boss_event_f.draw(game_surface, font, WIDTH, HEIGHT, boss_event_f.state, sound_manager)
                # 次にキー入力をチェック
                result = boss_event_f.handle_event(event, boss_event_f.state, sound_manager)
                if result == "battle":
                    sound_manager.play_bgm("Nisemono_Rock.mp3.enc")
                    print("  [イベント] boss_event_f -> battleへ遷移")
                    from scenes import battle, dungeon
                    # バトル初期化
                    battle.reset_battle(ENEMY_TABLE["F"])
                    # 位置情報を保存
                    px, py = dungeon.player_pos
                    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                        nx, ny = px + dx, py + dy
                        if (0 <= ny < len(dungeon.dungeon_maps[dungeon.current_floor]) and
                            0 <= nx < len(dungeon.dungeon_maps[dungeon.current_floor][0]) and
                            dungeon.dungeon_maps[dungeon.current_floor][ny][nx] == "F"):
                            dungeon.last_battle_pos  = [nx, ny]
                            dungeon.last_battle_tile = "F"
                            dungeon.last_player_pos = [px, py]
                            break
                    current_scene = "battle"
                    break

            # メニュー（Mキー）呼び出し
            if current_scene in ["town", "dungeon"] and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    previous_scene = current_scene
                    current_scene = "menu"
                    break

            # 建物進入
            if current_scene == "town" and event.type == pygame.KEYDOWN:
                for name, rect in buildings.items():
                    if player.rect.colliderect(rect):
                        if name == "dungeon":
                            sound_manager.play_se("stairs") 
                            dungeon.player_pos = [1, 1]  # 念のため再入場時にも上書き
                        # お城への進入時は会話状態も必ず初期化
                        if name == "castle":
                            current_castle_state = castle_init_state("default")  # 必ず毎回ここで初期化！
                            scene_key = "default"  # ← scene_key に "default" を設定
                        current_scene = name
                        break

            # 宿屋
            elif current_scene == "inn":
                result = inn_handle_event(event, inn_state, sound_manager)
                sound_manager.play_bgm("昼下がりのおやつ.mp3.enc")
                if result == "town":
                    sound_manager.play_bgm("お昼のうた.mp3.enc")
                    current_scene = "town"
                    player.set_center(WIDTH // 2, HEIGHT - 100)
                    break

            # 道具屋
            elif current_scene == "shop":
                result = shop_handle_event(event, shop_state, sound_manager)
                sound_manager.play_bgm("昼下がりのおやつ.mp3.enc")
                if result == "town":
                    sound_manager.play_bgm("お昼のうた.mp3.enc")
                    current_scene = "town"
                    player.set_center(WIDTH // 2, HEIGHT - 100)
                    break

            elif current_scene == "menu":
                result = menu.handle_event(event, sound_manager)
                sound_manager.play_bgm("起きたくない朝.mp3.enc")
                if result == "戻る":
                    sound_manager.play_bgm("お昼のうた.mp3.enc")
                    current_scene = previous_scene if previous_scene else "town"
                    break
                elif result == "ステータスを見る":
                    print(player_status)
                    break  # ←★ ここ抜けていなかったら止まる可能性あり！
                elif result == "アイテム":
                    sound_manager.play_se("select")
                    current_scene = "inventory"
                    break
                # 「ロードしました！」メッセージが表示されたあと、
                # プレイヤーがEnter/Escで抜けた瞬間だけ町に戻す
                elif (menu.mode == menu.MODE_MENU and 
                    menu.last_mode == menu.MODE_LOAD_MSG):  # ←last_modeをmenu.pyで管理する
                    player.set_center(WIDTH // 2, HEIGHT - 100)
                    player_status["player_pos"] = [WIDTH // 2, HEIGHT - 100]
                    current_scene = "town"
                    sound_manager.play_bgm("お昼のうた.mp3.enc")
                    break
                else:
                    break  # ←★ これがないと result==None で固まる！

            # インベントリ画面
            elif current_scene == "inventory":
                # メニュー画面からインベントリを開いている場合は
                # previous_scene（=元のシーン）を context に渡す
                context_scene = previous_scene if previous_scene is not None else current_scene
                result = inventory.handle_event(event, sound_manager, context=context_scene)
                if result == "戻る":
                    current_scene = "menu"
                    break
                elif result == "escape_dungeon":
                    sound_manager.play_bgm("お昼のうた.mp3.enc")
                    dungeon.current_floor = 0  # フロアを B1(0) にリセット
                    dungeon.player_pos = [1, 1]  # 階数と位置の初期化
                    # ダンジョン脱出
                    current_scene = "town"
                    player.set_center(WIDTH // 2, HEIGHT - 100)   # 町の初期位置に戻す
                    # 必要ならステータスやマップ状態のリセットなども
                    break
                elif result:
                    print(result)


            # 戦闘シーン
            elif current_scene == "battle":
                from scenes import battle, dungeon
                result = battle.handle_event(event, sound_manager)

                if result == "dungeon":
                    # 勝利時の処理
                    if battle.battle_state.get("result") == "victory":
                        if dungeon.last_battle_pos is not None and hasattr(dungeon, "last_battle_tile"):
                            x, y = dungeon.last_battle_pos
                            boss_tile = dungeon.last_battle_tile
                            cur_map = dungeon.dungeon_maps[dungeon.current_floor]
                            if boss_tile in dungeon.boss_defeated_flags:
                                dungeon.boss_defeated_flags[boss_tile] = True
                                row_list = list(cur_map[y])
                                row_list[x] = "."
                                cur_map[y] = "".join(row_list)
                        if dungeon.last_battle_tile == "F":
                            print("ラストボス撃破！エンディングへ遷移")
                            current_scene = "ending"
                            break
                        current_scene = "dungeon"
                        break

                    # 逃走時の処理
                    elif battle.battle_state.get("result") == "run":
                        if dungeon.last_player_pos is not None and dungeon.last_battle_pos is not None:
                            px, py = dungeon.last_player_pos
                            bx, by = dungeon.last_battle_pos
                            dx, dy = px - bx, py - by
                            new_x, new_y = bx + dx, by + dy
                            cur_map = dungeon.dungeon_maps[dungeon.current_floor]
                            if 0 <= new_y < len(cur_map) and 0 <= new_x < len(cur_map[0]) and cur_map[new_y][new_x] in dungeon.MOVABLE_TILES:
                                dungeon.player_pos = [new_x, new_y]
                            else:
                                dungeon.player_pos = dungeon.last_player_pos[:]
                        else:
                            dungeon.player_pos = [1, 1]
                        if not hasattr(dungeon, "action_locked"):
                            dungeon.action_locked = 0
                        dungeon.action_locked = 2
                        current_scene = "dungeon"
                        break

                    elif battle.battle_state.get("result") == "lose":
                        # 敗北時
                        print("バトル敗北: 城(gameover)へ遷移")
                        dungeon.current_floor = 0  # フロアを B1(0) にリセット
                        dungeon.player_pos = [1, 1]  # 階数と位置の初期化
                        current_castle_state = castle_init_state("gameover") # 敗北時は "gameover" をセット
                        scene_key = "gameover"  # ← scene_key に "gameover" を設定
                        player_status["hp"] = player_status["max_hp"]
                        current_scene = "castle"
                        break
        
            # 城シーンの入力処理
            elif current_scene == "castle":
                result = castle.handle_event(event, current_castle_state)
                sound_manager.play_bgm("私の部屋.mp3.enc")
                if result == "town":
                    sound_manager.play_bgm("お昼のうた.mp3.enc")
                    # 町へ
                    current_scene = "town"
                    player.set_center(WIDTH // 2, HEIGHT - 100)
                    break
                elif result == "stay":
                    break
            
            # エンディングシナリオ
            elif current_scene == "ending":
                result = ending.handle_event(event, ending.state, sound_manager)
                sound_manager.play_bgm("お昼のうた.mp3.enc")
                
                if result == "endroll":
                    endroll.init()
                    current_scene = "endroll"
                    break

            # エンドロール
            elif current_scene == "endroll":
                result = endroll.handle_event(event, endroll.state)
                sound_manager.play_bgm("お昼のうた.mp3.enc")
                if result == "title":
                    sound_manager.stop_bgm() # BGMがまだ鳴っていたら止める

                    # あとがきフラグ
                    from scenes import title
                    title.cleared = True

                    reset_game_state() # ゲーム状態をリセット

                    current_scene = "title"
                    break

            # あとがき
            elif current_scene == "afterword":
                from scenes import afterword
                result = afterword.handle_event(event, afterword.state)
                afterword.draw(game_surface, font, WIDTH, HEIGHT, afterword.state)
                if result == "title":
                    
                    current_scene = "title"
                    break

        # ==== 状態・描画処理 ====
        try:
            print(f"[DRAW] シーン: {current_scene}")
            if current_scene == "town":
                # 1) キャラクター移動・アニメーション更新
                player.update(keys)

                # 2) 画面外に出ないように位置をクランプ（プレイヤーの中心座標が
                #    キャラ半幅～WIDTH−半幅、半高さ～HEIGHT−半高さに収まるように）
                cx, cy = player.get_center()
                half_w = player.image.get_width()  // 2
                half_h = player.image.get_height() // 2
                cx = max(half_w, min(WIDTH  - half_w, cx))
                cy = max(half_h, min(HEIGHT - half_h, cy))
                player.set_center(cx, cy)
                player_status["player_pos"] = [cx, cy]

                # 背景・建物・プレイヤー描画
                game_surface.blit(background, (0, 0))
                for name, rect in buildings.items():
                    game_surface.blit(building_images[name], rect.topleft)
                    label = font.render(building_labels[name], True, WHITE)
                    game_surface.blit(label, (rect.x + 10, rect.y + 10))
                # game_surface.blit(player_image, player_rect)
                player.draw(game_surface)

            elif current_scene == "title":
                title.draw(game_surface, font, WIDTH, HEIGHT, title_state)
            
            elif current_scene == "load_from_title":
                print("  [DRAW] タイトルからロード")
                menu.draw(game_surface, font, WIDTH, HEIGHT, sound_manager)

            elif current_scene == "opening_event":
                opening_draw(game_surface, font, WIDTH, HEIGHT, opening_state, sound_manager)
            
            elif current_scene == "inn":
                print("  [DRAW] 宿屋描画")
                inn_draw(game_surface, font, WIDTH, HEIGHT, inn_state, sound_manager)
            elif current_scene == "shop":
                print("  [DRAW] 道具屋描画")
                shop.draw(game_surface, font, WIDTH, HEIGHT, shop_state, sound_manager)
            elif current_scene == "menu":
                print("  [DRAW] メニュー画面描画")
                menu.draw(game_surface, font, WIDTH, HEIGHT, sound_manager)
            elif current_scene == "inventory":
                print("  [DRAW] インベントリ描画")
                inventory.draw(game_surface, font, WIDTH, HEIGHT)
            elif current_scene == "dungeon":
                # ── ダンジョンシーン更新 ──
                print("  [DRAW] ダンジョン描画")
                # 1) マップ移動・イベント処理
                result = dungeon.update(keys, events, sound_manager)
                sound_manager.play_bgm("Royal_Question.mp3.enc")

                # 2) プレイヤーの向き・アニメーションを更新
                player.update(keys)

                tile_size = player.get_current_image().get_width()
                tx, ty = dungeon.player_pos
                px = tx * tile_size + tile_size // 2
                py = ty * tile_size + tile_size // 2
                player.set_center(px, py)

                # 4) ダンジョンとプレイヤーの描画
                dungeon.draw(game_surface, font, WIDTH, HEIGHT, player)
                if result == "town":
                    sound_manager.play_bgm("お昼のうた.mp3.enc")
                    current_scene = "town"
                    player.set_center(WIDTH // 2, HEIGHT - 100)
                elif result == "battle":
                    sound_manager.play_bgm("Slapstick_Dance.mp3.enc")
                    from scenes import battle
                    current_scene = "battle"
                # === ボスイベント（ごちみみず） ===
                elif result == "boss_event_k":
                    sound_manager.play_bgm("お昼のうた.mp3.enc")
                    print("main.py: boss_event_k遷移直前！")
                    # ─ 会話状態を初期化 ─
                    boss_event_k.state["text_index"]   = 0    # 何行目かをリセット
                    boss_event_k.state["in_dialog"]    = True # ダイアログモードへ
                    boss_event_k.state["voice_played"] = False# 音声再生済みフラグをリセット
                    # 背景画像が未ロードならロード
                    if boss_event_k.state["bg_images"] is None:
                        boss_event_k.state["bg_images"] = boss_event_k.load_bg_images()
                    pygame.event.clear()  # 過去のキー入力をクリア
                    current_scene = "boss_event_k"
                    print("main.py: boss_event_kに遷移完了！")
                    continue
                # === ボスイベント（ふかふかダンゴ） ===
                elif result == "boss_event_d":
                    sound_manager.play_bgm("お昼のうた.mp3.enc")
                    print("main.py: boss_event_d遷移直前！")
                    # 状態リセット
                    boss_event_d.state["text_index"] = 0
                    boss_event_d.state["in_dialog"] = True
                    boss_event_d.state["voice_played"] = False 
                    if boss_event_d.state["bg_images"] is None:
                        boss_event_d.state["bg_images"] = boss_event_d.load_bg_images()
                    pygame.event.clear()
                    current_scene = "boss_event_d"
                    print("main.py: boss_event_dに遷移完了！")
                    continue

                # === ボスイベント（しゅごもぐら） ===        
                elif result == "boss_event_f":
                    sound_manager.play_bgm("お昼のうた.mp3.enc")
                    print("main.py: boss_event_f遷移直前！")
                    boss_event_f.state["text_index"] = 0
                    boss_event_f.state["in_dialog"] = True
                    boss_event_f.state["voice_played"] = False
                    if boss_event_f.state["bg_images"] is None:
                        boss_event_f.state["bg_images"] = boss_event_f.load_bg_images()
                    pygame.event.clear()
                    current_scene = "boss_event_f"
                    print("main.py: boss_event_fに遷移完了！")
                    continue

                # action_locked で移動・操作制御
                if hasattr(dungeon, "action_locked") and dungeon.action_locked > 0:
                    dungeon.action_locked -= 1

            elif current_scene == "boss_event_k":
                print("  [DRAW] boss_event_k描画開始")
                boss_event_k.draw(game_surface, font, WIDTH, HEIGHT, boss_event_k.state, sound_manager)
                print("  [DRAW] boss_event_k描画終了")
                
            elif current_scene == "boss_event_f":
                # 描画
                boss_event_f.draw(game_surface, font, WIDTH, HEIGHT, boss_event_f.state, sound_manager)

            elif current_scene == "battle":
                print("  [DRAW] バトル描画")
                from scenes import battle
                battle.draw(game_surface, font, WIDTH, HEIGHT, sound_manager)

            elif current_scene == "castle":
                print("  [DRAW] 城描画")
                castle.draw(game_surface, font, WIDTH, HEIGHT, current_castle_state, sound_manager, key=scene_key)

            elif current_scene == "ending":
                ending.draw(game_surface, font, WIDTH, HEIGHT, ending.state, sound_manager)

            elif current_scene == "endroll":
                # 毎フレームスタッフロールの進行・描画
                endroll.update(endroll.state) # ←毎フレームスクロール！
                endroll.draw(game_surface, font, WIDTH, HEIGHT, endroll.state)

                # ここでフェードアウト処理
                if endroll.state["finished"] and not endroll.state.get("fading"):
                    sound_manager.fadeout_bgm(2000)  # 2秒でフェードアウト
                    endroll.state["fading"] = True  # フェードアウト済みマーク

            elif current_scene == "afterword":
                from scenes import afterword
                afterword.draw(game_surface, font, WIDTH, HEIGHT, afterword.state)

            print("main.py: pygame.display.flip()直前")
            pygame.display.flip()
            print("main.py: pygame.display.flip()直後")
            clock.tick(FPS)
            print("  [DRAW] フレーム更新・スリープ完了")
        except Exception as e:
            print("描画処理でエラー:", e)
            traceback.print_exc()
            with open("error_log.txt", "a", encoding="utf-8") as f:
                traceback.print_exc(file=f)
            running = False
            print("ループ終了: running =", running)

        # --- フルスクリーン表示用スケーリング & 中心表示 ---
        scale = min(screen_width / WIDTH, screen_height / HEIGHT)
        scaled_w = int(WIDTH * scale)
        scaled_h = int(HEIGHT * scale)
        scaled_surface = pygame.transform.scale(game_surface, (scaled_w, scaled_h))

        screen.fill(BLACK)
        x = (screen_width - scaled_w) // 2
        y = (screen_height - scaled_h) // 2
        screen.blit(scaled_surface, (x, y))

        pygame.display.flip()
        clock.tick(FPS)

    print("=== ループ外 ===") 

except Exception as e:
    print("致命的なエラーが発生しました。")
    import traceback
    traceback.print_exc()
    try:
        with open("error_log.txt", "a", encoding="utf-8") as f:
            traceback.print_exc(file=f)
    except Exception as log_e:
        print("error_log.txtへの書き込みでエラー:", log_e)
    import time
    time.sleep(5)  # エラー内容が見えるように5秒だけウィンドウを維持
    running = False
finally:
    print("=== プログラム終了 ===")
    pygame.quit()
    sys.exit()
