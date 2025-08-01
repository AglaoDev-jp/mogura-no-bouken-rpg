# scenes/battle.py
import pygame
import random
import copy
from pathlib import Path
from status import get_current_atk, get_current_def, player_status, ENEMIES, ENEMY_TABLE
from item_effects import use_item
from status import check_level_up

# ==============================
# バトルシーン用・状態管理変数
# ==============================

battle_state = {}
enemy_shake_timer = 0
enemy_shake_offsets = [(-2, 0), (2, 0), (0, -2), (0, 2), (0, 0)]
screen_shake_timer = 0
victory_se_timer = 0
global enemy_fade_alpha
enemy_fade_alpha = 255

COMMANDS = ["攻撃", "道具", "逃げる"]
COMMAND_ATTACK, COMMAND_ITEM, COMMAND_RUN = 0, 1, 2

font = None
enemy_image = None
battle_bg = None

def reset_battle(enemy=None):
    """
    戦闘開始時の状態を初期化します。
    """
    global battle_state, enemy_image, battle_bg, enemy_fade_alpha
    battle_state.clear()
    target_enemy = enemy or ENEMIES[0]
    battle_state["enemy"] = copy.deepcopy(target_enemy)
    battle_state["player"] = copy.deepcopy(player_status)
    battle_state["phase"] = "start"
    battle_state["messages"] = ["モンスターが現れた！"]
    battle_state["msg_index"] = 0
    battle_state["command_cursor"] = 0
    battle_state["item_cursor"] = 0
    battle_state["result"] = None
    battle_state["victory_step"] = 0
    battle_state["exp_gained"] = 0
    battle_state["gold_gained"] = 0

    asset_dir = Path(__file__).resolve().parent.parent / "assets" / "images"
    enemy_img_path = asset_dir / target_enemy["img"]
    battle_bg_path = asset_dir / target_enemy["bg"]
    try:
        enemy_image = pygame.image.load(str(enemy_img_path)).convert_alpha()
        enemy_image = pygame.transform.scale(enemy_image, (300, 300))
        battle_bg = pygame.image.load(str(battle_bg_path)).convert()
        battle_bg = pygame.transform.scale(battle_bg, (800, 600))
    except Exception as e:
        print("画像の読み込みエラー:", e)
        enemy_image = None
        battle_bg = None

    enemy_fade_alpha = 255

def get_sorted_items():
    items = None
    if "player" in battle_state and "items" in battle_state["player"]:
        items = battle_state["player"]["items"]
    else:
        items = player_status.get("items", {})
    sorted_keys = []
    if "ごちサンド" in items:
        sorted_keys.append("ごちサンド")
    other_keys = sorted([k for k in items if k != "ごちサンド"])
    sorted_keys.extend(other_keys)
    return [(k, items[k]) for k in sorted_keys]

def handle_event(event, sound_manager):
    # --- 戦闘開始時「モンスターが現れた！」 ---
    if battle_state.get("phase") == "start":
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            battle_state["phase"] = "command"
        return

    # --- コマンド選択 ---
    if battle_state.get("phase") == "command":
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                battle_state["command_cursor"] = (battle_state["command_cursor"] - 1) % len(COMMANDS)
            elif event.key == pygame.K_DOWN:
                battle_state["command_cursor"] = (battle_state["command_cursor"] + 1) % len(COMMANDS)
            elif event.key == pygame.K_RETURN:
                sel = battle_state["command_cursor"]
                # 攻撃
                if sel == COMMAND_ATTACK:
                    player_atk = get_current_atk()
                    enemy = battle_state["enemy"]
                    sound_manager.play_se("attack")
                    dmg = max(1, player_atk - random.randint(0, 2))
                    enemy["hp"] = max(0, enemy["hp"] - dmg)
                    battle_state["messages"] = [
                        f"{player_status['name']}の攻撃！",
                        f"{enemy['name']}に{dmg}ダメージ！"
                    ]
                    battle_state["msg_index"] = 0
                    global enemy_shake_timer
                    enemy_shake_timer = len(enemy_shake_offsets)

                    if enemy["hp"] <= 0:
                        # 勝利フロー開始
                        battle_state["phase"] = "victory"
                        battle_state["messages"] = [f"{enemy['name']}をたおした！"]
                        battle_state["msg_index"] = 0
                        battle_state["exp_gained"] = enemy.get("exp", 0)
                        battle_state["gold_gained"] = enemy.get("gold", 0)
                        global victory_se_timer, enemy_fade_alpha
                        enemy_fade_alpha = 255
                        victory_se_timer = 10
                    else:
                        battle_state["phase"] = "message"
                        battle_state["enemy_turn_ready"] = True

                # アイテム
                elif sel == COMMAND_ITEM:
                    if get_sorted_items():
                        battle_state["phase"] = "item_select"
                        battle_state["item_cursor"] = 0
                    else:
                        battle_state["messages"] = ["アイテムがありません。"]
                        battle_state["msg_index"] = 0
                        battle_state["phase"] = "message"
                        battle_state["enemy_turn_ready"] = False

                # 逃げる
                elif sel == COMMAND_RUN:
                    if random.random() < 0.75:
                        sound_manager.play_se("runok")
                        battle_state["phase"] = "run"
                        battle_state["messages"] = ["うまく逃げられた！"]
                        battle_state["msg_index"] = 0
                    else:
                        sound_manager.play_se("runfail")
                        battle_state["messages"] = ["逃げられなかった！"]
                        battle_state["msg_index"] = 0
                        battle_state["phase"] = "message"
                        battle_state["enemy_turn_ready"] = True

            elif event.key == pygame.K_x or event.key == pygame.K_ESCAPE:
                pass # メニューを閉じるなど

        return

    # --- アイテム選択 ---
    if battle_state.get("phase") == "item_select":
        items = get_sorted_items()
        if not items:
            battle_state["messages"] = ["アイテムがありません。"]
            battle_state["msg_index"] = 0
            battle_state["phase"] = "message"
            battle_state["enemy_turn_ready"] = False
            return
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                battle_state["item_cursor"] = (battle_state["item_cursor"] - 1) % len(items)
            elif event.key == pygame.K_DOWN:
                battle_state["item_cursor"] = (battle_state["item_cursor"] + 1) % len(items)
            elif event.key == pygame.K_RETURN:
                item_name = items[battle_state["item_cursor"]][0]
                # 「ごちサンド」を使ったときに回復のSEを鳴らす
                if item_name == "ごちサンド":
                    sound_manager.play_se("heal")
                msg = use_item(item_name, context="battle", player=battle_state["player"])
                if isinstance(msg, str):
                    battle_state["messages"] = [msg]
                else:
                    battle_state["messages"] = msg
                battle_state["msg_index"] = 0
                battle_state["phase"] = "message"
                battle_state["enemy_turn_ready"] = True
                battle_state["item_cursor"] = 0
            elif event.key == pygame.K_x or event.key == pygame.K_ESCAPE:
                battle_state["phase"] = "command"
                battle_state["item_cursor"] = 0
        return

    # --- プレイヤーアクション後：メッセージ送り ---
    if battle_state.get("phase") == "message":
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            if battle_state["msg_index"] < len(battle_state["messages"]) - 1:
                battle_state["msg_index"] += 1
            else:
                # 敵ターン処理
                if battle_state.get("enemy_turn_ready", False):
                    enemy = battle_state["enemy"]
                    sound_manager.play_se("damage")
                    dmg = max(1, enemy["atk"] - random.randint(0, 2))
                    battle_state["player"]["hp"] = max(0, battle_state["player"]["hp"] - dmg)
                    global screen_shake_timer
                    screen_shake_timer = 5

                    battle_state["messages"] = [
                        f"{enemy['name']}の攻撃！",
                        f"{dmg}のダメージ！"
                    ]
                    battle_state["msg_index"] = 0
                    battle_state["enemy_turn_ready"] = False
                    # HPが0になったら「やられてしまった……」をセットしてphase変更
                    if battle_state["player"]["hp"] <= 0:
                        battle_state["messages"].append("やられてしまった……")
                        
                        battle_state["phase"] = "defeat"  # ←ここで「敗北演出」へ
                else:
                    battle_state["phase"] = "command"
        return

    # --- 敗北演出 ---
    if battle_state.get("phase") == "defeat":
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            # これから表示するmsgが「やられてしまった……」だったらSE
            next_index = battle_state["msg_index"] + 1
            if next_index < len(battle_state["messages"]):
                if battle_state["messages"][next_index] == "やられてしまった……":
                    # BGM を止めてから敗北 SE を再生
                    sound_manager.stop_bgm()
                    sound_manager.play_se("defeat")
            if battle_state["msg_index"] < len(battle_state["messages"]) - 1:
                battle_state["msg_index"] += 1
            else:
                # HPやアイテム進捗も反映
                player_status["hp"] = battle_state["player"]["hp"]
                player_status["items"] = battle_state["player"]["items"].copy()
                battle_state["result"] = "lose"
                return "dungeon"  # main.py側で「城」に遷移させてOK
        return


    # --- 勝利演出 ---
    if battle_state.get("phase") == "victory":
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            if battle_state["msg_index"] < len(battle_state["messages"]) - 1:
                battle_state["msg_index"] += 1
            else:
                # 報酬表示
                battle_state["phase"] = "victory_reward"
                battle_state["messages"] = [f"{battle_state['gold_gained']}Gと{battle_state['exp_gained']}EXPを手に入れた！"]
                battle_state["msg_index"] = 0
        return

    # --- 勝利報酬 → レベルアップ or 終了 ---
    if battle_state.get("phase") == "victory_reward":
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            player_status["hp"] = battle_state["player"]["hp"]
            player_status["items"] = battle_state["player"]["items"].copy()
            player_status["exp"] += battle_state.get("exp_gained", 0)
            player_status["gold"] += battle_state.get("gold_gained", 0)
            up_count = check_level_up()
            if up_count > 0:
                sound_manager.play_se("levelup")
                battle_state["phase"] = "levelup"
                battle_state["messages"] = [
                    f"レベルが {player_status['lv']} に上がった！",
                    "HP/攻撃/防御が上昇！"
                ]
                battle_state["msg_index"] = 0
            else:
                battle_state["result"] = "victory"
                # ★ ここで直接戻る！
                return "dungeon"
        return

    # --- レベルアップ演出 ---
    if battle_state.get("phase") == "levelup":
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            if battle_state["msg_index"] < len(battle_state["messages"]) - 1:
                battle_state["msg_index"] += 1
            else:
                battle_state["result"] = "victory"
                # ★ ここで直接戻る！
                return "dungeon"
        return

    # --- 敗北演出 ---
    if battle_state.get("phase") == "defeat":
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            player_status["hp"] = battle_state["player"]["hp"]
            player_status["items"] = battle_state["player"]["items"].copy()
            battle_state["result"] = "lose"
            return "dungeon"  # ★ ここでdungeonに統一
        return

    # --- 逃走演出 ---
    if battle_state.get("phase") == "run":
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            player_status["hp"] = battle_state["player"]["hp"]
            player_status["items"] = battle_state["player"]["items"].copy()
            battle_state["result"] = "run"      # ★ここでセット！
            return "dungeon"
        return

    # --- バトル終了 ---
    if battle_state.get("phase") == "end":
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            # ★ここでは result はすでにセット済み
            return "dungeon"
        return


def draw(screen, font, WIDTH, HEIGHT, sound_manager):
    game_surface = pygame.Surface((WIDTH, HEIGHT))
    if battle_bg:
        game_surface.blit(battle_bg, (0, 0))
    else:
        game_surface.fill((40, 20, 40))

    if battle_state.get("phase") == "item_select":
        items = get_sorted_items()
        for i, (name, count) in enumerate(items):
            color = (255,255,0) if i == battle_state["item_cursor"] else (200,200,200)
            item_text = font.render(f"{name} ×{count}", True, color)
            game_surface.blit(item_text, (60, HEIGHT - 150 + i*32))
    
    # ★スクリーンシェイク
    global screen_shake_timer
    offset_x, offset_y = 0, 0
    if screen_shake_timer > 0:
        offset_x = random.randint(-3, 3)
        offset_y = random.randint(-3, 3)
        screen_shake_timer -= 1

    screen.blit(game_surface, (offset_x, offset_y))

    # --- 敵画像 ---
    if enemy_image:
        img_w, img_h = enemy_image.get_size()
        img_x = int(WIDTH * 0.57)
        img_y = int(HEIGHT * 0.33)
        global enemy_shake_timer
        if enemy_shake_timer > 0:
            offset = enemy_shake_offsets[len(enemy_shake_offsets) - enemy_shake_timer]
            img_x += offset[0]
            img_y += offset[1]
            enemy_shake_timer -= 1

        if battle_state.get("phase") in ["victory", "victory_reward", "levelup", "end"]:
            global enemy_fade_alpha
            if enemy_fade_alpha > 0:
                enemy_fade_alpha -= 15
            tmp_image = enemy_image.copy()
            tmp_image.set_alpha(enemy_fade_alpha)
            screen.blit(tmp_image, (img_x, img_y))
        else:
            screen.blit(enemy_image, (img_x, img_y))

    enemy = battle_state["enemy"]
    player = battle_state["player"]

    enemy_name = font.render(enemy['name'], True, (255,100,100))
    screen.blit(enemy_name, (500, 60))
    enemy_hp = font.render(f"HP:{enemy['hp']}/{enemy['max_hp']}", True, (255,150,150))
    screen.blit(enemy_hp, (500, 100))
    player_info = font.render(f"{player['name']}  HP:{player['hp']}/{player['max_hp']}", True, (100,255,100))
    screen.blit(player_info, (60, HEIGHT - 180))

    # --- メッセージ ---
    if "messages" in battle_state and "msg_index" in battle_state:
        msg = battle_state["messages"][battle_state["msg_index"]]
    else:
        msg = ""
    msg_render = font.render(msg, True, (255,255,255))
    screen.blit(msg_render, (60, 60))
    
    # --- コマンド選択肢 ---
    if battle_state.get("phase") == "command":
        for i, cmd in enumerate(COMMANDS):
            color = (255,255,0) if i == battle_state["command_cursor"] else (200,200,200)
            cmd_text = font.render(cmd, True, color)
            screen.blit(cmd_text, (60, HEIGHT - 130 + i * 36))
    
    global victory_se_timer
    if victory_se_timer > 0:
        victory_se_timer -= 1
        if victory_se_timer == 0:
            sound_manager.play_se("victory")

def start_battle(enemy=None):
    reset_battle(enemy)
