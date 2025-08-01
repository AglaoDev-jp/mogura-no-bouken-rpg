# scenes/dungeon.py

import pygame
import random
import copy
from pathlib import Path
from status import ENEMY_TABLE

# ==============================
# グローバル変数（状態保持）
# ==============================
step_counter = 0                  # 歩数カウント
exclamation_timer = -1            # びっくりマーク演出タイマー（-1は非表示）
last_battle_pos = None            # 直前エンカウント座標
last_battle_tile = None           # 直前エンカウント敵ID
last_player_pos = None            # 直前プレイヤー座標
encounter_locked = False          # エンカ防止フラグ

# ==============================
# ボス撃破状況フラグ
# セーブデータに保存することで、撃破後は復活しなくなる
# save_load.pyで保存/復元されることに注意
# ==============================
BLOCKING_ENEMY_TILES = ["K", "D", "F"]
boss_defeated_flags = {
    "K": False,   # ごちミミズ
    "D": False,   # ふかふかダンゴ
    "F": False,   # しゅごもぐら
}

# 移動可能タイル
MOVABLE_TILES = ".E><M"  # "K", "B3"は除外

# 画像リソース
BASE_DIR = Path(__file__).resolve().parent.parent
floor_tile_images = [
    {  # B1用
        "#": pygame.image.load(str(BASE_DIR / "assets" / "images" / "wall_b1.png")),
        ".": pygame.image.load(str(BASE_DIR / "assets" / "images" / "floor_b1.png")),
        ">": pygame.image.load(str(BASE_DIR / "assets" / "images" / "stairs_down.png")),
        "<": pygame.image.load(str(BASE_DIR / "assets" / "images" / "stairs_up.png")),
        "E": pygame.image.load(str(BASE_DIR / "assets" / "images" / "exit.png")),
        "K": pygame.image.load(str(BASE_DIR / "assets" / "images" / "enemy_k.png")),
    },
    {  # B2用
        "#": pygame.image.load(str(BASE_DIR / "assets" / "images" / "wall_b2.png")),
        ".": pygame.image.load(str(BASE_DIR / "assets" / "images" / "floor_b2.png")),
        ">": pygame.image.load(str(BASE_DIR / "assets" / "images" / "stairs_down.png")),
        "<": pygame.image.load(str(BASE_DIR / "assets" / "images" / "stairs_up.png")),
        "E": pygame.image.load(str(BASE_DIR / "assets" / "images" / "exit.png")),
        "D": pygame.image.load(str(BASE_DIR / "assets" / "images" / "enemy_d.png")),
    },
    {  # B3用
        "#": pygame.image.load(str(BASE_DIR / "assets" / "images" / "wall_b3.png")),
        ".": pygame.image.load(str(BASE_DIR / "assets" / "images" / "floor_b3.png")),
        ">": pygame.image.load(str(BASE_DIR / "assets" / "images" / "stairs_down.png")),
        "<": pygame.image.load(str(BASE_DIR / "assets" / "images" / "stairs_up.png")),
        "E": pygame.image.load(str(BASE_DIR / "assets" / "images" / "exit.png")),
        "F": pygame.image.load(str(BASE_DIR / "assets" / "images" / "enemy_f.png")),
    },
]

# player_image = pygame.image.load(str(BASE_DIR / "assets" / "images" / "mogura.png"))
exclamation_img = pygame.image.load(str(BASE_DIR / "assets" / "images" / "exclamation.png"))

# ==============================
# マップ定義
# ==============================
# ==== ダンジョンマップ ====
dungeon_b1_map = [
    "########################",
    "#...........#..........#",
    "#E######.#####.######..#",
    "#.#.............#......#",
    "#.#.###########.#.####.#",
    "#...#.......#...#......#",
    "###.#.#####.#.#####.####",
    "#...#.#.....#.....#....#",
    "#.###.#.#########.#.####",
    "#.#...#.....#.....#....#",
    "#.#.#####.#.#.#####.##.#",
    "#.#.....#.#.#.....#....#",
    "#.#####.#.#.#####.####.#",
    "#.....#.#.#.....#......#",
    "#.###.#.#.###.#.######.#",
    "#.#...#.#.....#.......K#",
    "#.#.###.##############>#",
    "########################"
]
dungeon_b2_map = [
    "########################",
    "#<........#............#",
    "#.#######.#####.########",
    "#.#.............#......#",
    "#.#.###########.#.####.#",
    "#...#.......#...#......#",
    "###.#.#####.#.#####.####",
    "#...#.#.....#.....#....#",
    "#.###.#.#########.#.####",
    "#.#...#.....#.....#....#",
    "#.#.#####.#.#.#####.##.#",
    "#.#.....#.#.#.....#....#",
    "#.#####.#.#.#####.####.#",
    "#.....#.#.#.....#......#",
    "#.###.#.#.###.#.######.#",
    "#.#...#D#.....#........#",
    "#.#.###>##############E#",
    "########################"
]
dungeon_b3_map = [
    "########################",
    "#<.....................#",
    "#.######################",
    "#.#.............#......#",
    "#.#.###########.#.####.#",
    "#...#.......#...#......#",
    "###.#.#####.#.#####.####",
    "#...#.#.....#.....#....#",
    "#.###.#.#########.#.####",
    "#.#...#.....#.....#....#",
    "#.#.#####.#.#.#####.##.#",
    "#.#.....#.#.#.....#....#",
    "#.#####.#.#.#####.####.#",
    "#.....#.#.#.....#......#",
    "#.###.#.#.###.#.######.#",
    "#.#...#.#.....#.......F#",
    "#.#.###.################",
    "########################"
]
dungeon_maps = [dungeon_b1_map, dungeon_b2_map, dungeon_b3_map]

def reset_dungeon_maps():
    """
    ボスなどを含むマップの状態を最初に戻す（ゲーム初期化時用）
    """
    global dungeon_maps
    dungeon_maps = copy.deepcopy(original_dungeon_maps)

original_dungeon_maps = [
    dungeon_b1_map[:],
    dungeon_b2_map[:],
    dungeon_b3_map[:]
]

current_floor = 0
player_pos = [1, 1]
move_cooldown = 0
stairs_locked = False

# ==============================
# タイル探索ヘルパー
# ==============================
def find_tile_on_map(map_data, target):
    for y, row in enumerate(map_data):
        for x, t in enumerate(row):
            if t == target:
                return [x, y]
    return [1, 1]

# ==============================
# 描画処理（タイルごとに画像を割り当てる）
# ==============================
def draw(screen, font, WIDTH, HEIGHT, player):
    """
    マップ・プレイヤー・びっくり演出の描画
    Draw map, player, and exclamation effect with tile images.
    """
    cur_map = dungeon_maps[current_floor]
    tile_images = floor_tile_images[current_floor] 
    MAP_ROWS = len(cur_map)
    MAP_COLS = len(cur_map[0])
    TILE_SIZE = min(WIDTH // MAP_COLS, HEIGHT // MAP_ROWS)
    offset_x = (WIDTH - (TILE_SIZE * MAP_COLS)) // 2
    offset_y = (HEIGHT - (TILE_SIZE * MAP_ROWS)) // 2

    screen.fill((0, 0, 0))  # 背景を黒で塗りつぶし（Clear background）

    # --- マップタイル画像描画 ---
    for y, row in enumerate(cur_map):
        for x, tile in enumerate(row):
            # タイル画像が登録されていれば貼る
            if tile in tile_images:
                img = pygame.transform.scale(tile_images[tile], (TILE_SIZE, TILE_SIZE))
                screen.blit(img, (offset_x + x * TILE_SIZE, offset_y + y * TILE_SIZE))
            elif tile in BLOCKING_ENEMY_TILES and not boss_defeated_flags.get(tile, False):
                # ボス用の特殊画像や色
                pygame.draw.rect(
                    screen, (255, 120, 120),
                    (offset_x + x * TILE_SIZE, offset_y + y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                )
            else:
                # その他は薄いグレーで描画
                pygame.draw.rect(
                    screen, (150, 150, 150),
                    (offset_x + x * TILE_SIZE, offset_y + y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                )

    # --- プレイヤー画像描画 ---
    px, py = player_pos
    player_img = pygame.transform.scale(player.get_current_image(), (TILE_SIZE, TILE_SIZE))
    screen.blit(player_img, (offset_x + px * TILE_SIZE, offset_y + py * TILE_SIZE))

    # --- びっくりマーク演出 ---
    global exclamation_timer
    if exclamation_timer > 0:
        mark_img = pygame.transform.scale(exclamation_img, (TILE_SIZE, TILE_SIZE))
        mark_x = offset_x + px * TILE_SIZE
        mark_y = offset_y + py * TILE_SIZE - TILE_SIZE // 2
        screen.blit(mark_img, (mark_x, mark_y))
        exclamation_timer -= 1

    # --- フロア表示 ---
    floor_label = font.render(f"B{current_floor+1}F", True, (255,255,0))
    screen.blit(floor_label, (offset_x + 10, offset_y + 5))

# ==============================
# ボスに話しかけた判定
# ==============================
def check_boss_encounter(events):
    """
    主人公が隣接マスのボスに向かって
    「Z」または「Enter」キーで話しかけた時に発火。
    返り値として "boss_event_k" や "boss_event_f" などの文字列を返す。
    """
    px, py = player_pos
    cur_map = dungeon_maps[current_floor]
    for event in events:
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_z, pygame.K_RETURN):
            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                nx, ny = px + dx, py + dy
                if 0 <= nx < len(cur_map[0]) and 0 <= ny < len(cur_map):
                    tile = cur_map[ny][nx]
                    print(f"隣接タイル: {tile}, boss_defeated_flags: {boss_defeated_flags}")
                    # --- Fボス判定 ---
                    if (tile == "F" and not boss_defeated_flags.get("F", False)):
                        print("ボスFエンカウント発生！")
                        return "boss_event_f"
                    # --- Dボス判定---
                    if tile == "D" and not boss_defeated_flags.get("D", False):
                        print("ボスDエンカウント発生！")
                        return "boss_event_d"
                    # --- Kボス判定 ---
                    if (tile == "K" and not boss_defeated_flags.get("K", False)):
                        print("ボスKエンカウント発生！")
                        return "boss_event_k"

    return None

def clear_defeated_boss_tiles():
    """
    boss_defeated_flagsに従い、各マップのボス記号を消す
    """
    global dungeon_maps, boss_defeated_flags
    for floor, boss_char in enumerate(["K", "D", "F"]):
        if boss_defeated_flags.get(boss_char, False):
            # マップ上から該当のボスタイルを消す
            new_map = []
            for row in dungeon_maps[floor]:
                new_map.append(row.replace(boss_char, "."))  # K→., D→., F→.
            dungeon_maps[floor] = new_map
            
# ==============================
# ダンジョンのメインロジック
# ==============================
def update(keys, events, sound_manager):
    """
    ダンジョン内ロジック
    - 通常移動・階段移動
    - ボス話しかけ・エンカウント判定
    - 各種状態リセット
    """
    global move_cooldown, current_floor, player_pos, stairs_locked
    global encounter_locked, step_counter, exclamation_timer
    global last_battle_pos, last_battle_tile, last_player_pos

    # びっくりマーク演出中はエンカウント
    if exclamation_timer > 0:
        return "encounter"
    elif exclamation_timer == 0:
        exclamation_timer = -1
        return "battle"

    cur_map = dungeon_maps[current_floor]
    MAP_ROWS = len(cur_map)
    MAP_COLS = len(cur_map[0])

    # クールタイム
    if move_cooldown > 0:
        move_cooldown -= 1
        return None

    # 階段ワープ直後の移動ロック
    if stairs_locked:
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:  dx = -1
        elif keys[pygame.K_RIGHT]: dx = 1
        elif keys[pygame.K_UP]:    dy = -1
        elif keys[pygame.K_DOWN]:  dy = 1
        if dx != 0 or dy != 0:
            new_x = player_pos[0] + dx
            new_y = player_pos[1] + dy
            if 0 <= new_y < MAP_ROWS and 0 <= new_x < MAP_COLS:
                next_tile = cur_map[new_y][new_x]
                if next_tile in MOVABLE_TILES:
                    player_pos = [new_x, new_y]
                    move_cooldown = 8
                    stairs_locked = False
        return None

    # エンカウントロック（1回のみ無効）
    if encounter_locked:
        encounter_locked = False
        return None

    # 出入り口・階段処理
    y, x = player_pos[1], player_pos[0]
    now_tile = cur_map[y][x]
    if now_tile == "E":
        sound_manager.play_se("stairs") 
        current_floor = 0
        player_pos = [1, 1]
        return "town"
    if now_tile == ">" and current_floor < len(dungeon_maps) - 1:
        sound_manager.play_se("stairs") 
        current_floor += 1
        player_pos = find_tile_on_map(dungeon_maps[current_floor], "<")
        stairs_locked = True
        return None
    if now_tile == "<" and current_floor > 0:
        sound_manager.play_se("stairs") 
        current_floor -= 1
        player_pos = find_tile_on_map(dungeon_maps[current_floor], ">")
        stairs_locked = True
        return None

    # 通常移動
    dx, dy = 0, 0
    if keys[pygame.K_LEFT]:  dx = -1
    elif keys[pygame.K_RIGHT]: dx = 1
    elif keys[pygame.K_UP]:    dy = -1
    elif keys[pygame.K_DOWN]:  dy = 1

    if dx != 0 or dy != 0:
        new_x = player_pos[0] + dx
        new_y = player_pos[1] + dy
        if 0 <= new_x < MAP_COLS and 0 <= new_y < MAP_ROWS:
            next_tile = cur_map[new_y][new_x]
            if (next_tile in BLOCKING_ENEMY_TILES and not boss_defeated_flags.get(next_tile, False)):
                pass  # ボス未撃破なら進入不可
            elif next_tile in MOVABLE_TILES:
                player_pos = [new_x, new_y]
                move_cooldown = 8

                # 歩数カウント＆ランダムエンカウント
                step_counter += 1
                ENCOUNTER_RATE = 0.05  # 5%
                if random.random() < ENCOUNTER_RATE:
                    encounter_locked = True
                    # モンスターリスト（階層別）
                    floor_enemy_ids = [
                        ["A"],            # B1階
                        ["C","M"],        # B2階
                        ["P","S"],        # B3階
                    ]
                    ids = floor_enemy_ids[current_floor]
                    enemy_id = random.choice(ids)
                    from scenes import battle
                    battle.reset_battle(ENEMY_TABLE[enemy_id])
                    last_battle_pos = player_pos[:]
                    last_battle_tile = enemy_id
                    last_player_pos = player_pos[:]
                    exclamation_timer = 15
                    sound_manager.play_se("encounter")
                    return "encounter"

    # --- ここでボス話しかけイベントの判定 ---
    result = check_boss_encounter(events)
    if result:  # "boss_event_k" など
        return result

    return None
