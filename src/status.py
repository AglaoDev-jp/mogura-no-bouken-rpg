# status.py

# ========== プレイヤーステータス ==========
player_status = {
    "name": "もぐら",
    "lv": 1,
    "hp": 10,
    "max_hp": 10,
    "atk": 8,
    "def_": 5,
    "gold": 100,
    "exp": 0,
    "items": {
        "ごちサンド": 2,
        "トロッコ": 1,
        # 装備も「所持アイテム」に入れてOK
    },
    # 各部位に「装備ID or None」
    "equip": {
        "weapon": None,     # 例: "スコップ"
        "armor": None,      # 例: "ヘルメット"
        # 今後「accessory」「ring」なども追加できる
    },
}

# ========== 経験値テーブルとレベル上限 ==========
# LEVEL_EXP_TABLE[レベル] = そのレベルに到達するのに必要な累積経験値
LEVEL_EXP_TABLE = [0, 10, 30, 60, 100, 150, 210, 280, 360, 450, 550]  # Lv1～Lv11
MAX_LV = 10  # レベル10が上限（Lv11には上がらない）

def check_level_up():
    """
    経験値が必要値を超えていればレベルアップ。
    複数回レベルアップや上限(MAX_LV)も考慮。
    LEVEL_EXP_TABLE の定義では、
    LEVEL_EXP_TABLE[1] = 10 が「レベル1→2」に必要な経験値
    LEVEL_EXP_TABLE[2] = 30 が「レベル2→3」に必要な経験値
    …というふうに “現在のレベル” をキーにして参照するつくりです。
    """
    # 現在のレベル lv から次のレベルに上がるのに必要な経験値は LEVEL_EXP_TABLE[lv] です
        
    levelup_count = 0 # ← ここで必ず初期化！

    while player_status["lv"] < MAX_LV:
        current_lv = player_status["lv"]
        # テーブル範囲外なら安全に抜ける
        if current_lv >= len(LEVEL_EXP_TABLE):
            break
        # レベル lv → lv+1 に必要な経験値
        need_exp = LEVEL_EXP_TABLE[current_lv]
        if player_status["exp"] >= need_exp:
            # レベルアップ処理
            player_status["lv"] += 1
            player_status["max_hp"] += 10  # HP+10（お好みで調整可）
            player_status["hp"] = player_status["max_hp"]
            player_status["atk"] += 2
            player_status["def_"] += 1
            levelup_count += 1
        else:
            break
    # 上限到達後も経験値加算は可（無駄にはならない設計）
    return levelup_count


# ========== 装備アイテムのステータス補正値 ==========
EQUIPMENT_TABLE = {
    # 装備ID: 装備の各種情報
    "スコップ": {
        "kind": "weapon",
        "name": "スコップ",
        "desc": "地面を掘る万能道具。攻撃力+10",
        "bonus": {"atk": 10},
        "special": None,        # 今後「特殊効果」などもここで
    },
    "ヘルメット": {
        "kind": "armor",
        "name": "ヘルメット",
        "desc": "地中の危険から身を守る。防御力+8",
        "bonus": {"def_": 8},
        "special": None,
    },
    # ここに新しい装備を**どんどん追加するだけ**でOK！
}

def equip_item(equip_id):
    """
    装備品を装備する関数
    equip_id: EQUIPMENT_TABLEのキー（例："スコップ"）
    """
    equip_info = EQUIPMENT_TABLE.get(equip_id)
    if not equip_info:
        return f"{equip_id} は装備できません。"
    kind = equip_info["kind"]  # "weapon"や"armor"

    # 既に同じものを装備していた場合
    if player_status["equip"].get(kind) == equip_id:
        return f"{equip_info['name']} はすでに装備中です。"

    # 既にその部位に装備しているものを外す
    prev = player_status["equip"].get(kind)
    player_status["equip"][kind] = equip_id
    # もし「装備品を外してインベントリに戻す」等の処理も追加可能

    return f"{equip_info['name']} を装備しました。"

def unequip(kind):
    """
    指定部位(kind: "weapon"や"armor")の装備を外す関数
    """
    if player_status["equip"].get(kind):
        removed = player_status["equip"][kind]
        player_status["equip"][kind] = None
        return f"{removed}を外しました。"
    else:
        return "何も装備していません。"

def get_total_status():
    """
    装備補正込みの現在値を辞書で返す
    """
    atk = player_status["atk"]
    def_ = player_status["def_"]
    for kind, equip_id in player_status["equip"].items():
        if equip_id:
            info = EQUIPMENT_TABLE.get(equip_id)
            if info and "bonus" in info:
                atk += info["bonus"].get("atk", 0)
                def_ += info["bonus"].get("def_", 0)
    return {"atk": atk, "def_": def_}


# ========== 敵キャラクターデータ ==========
ENEMIES = [
    {
        "id": "A",
        "name": "もちもちミミズ",
        "hp": 20,
        "max_hp": 20,
        "atk": 5,
        "img": "enemy_mimizu.png",
        "bg":  "battle_cave_1.png",
        "exp": 5,
        "gold": 10,
    },
    {
        "id": "K",
        "name": "ごちミミズ",
        "hp": 18,
        "max_hp": 18,
        "atk": 6,
        "img": "enemy_gochimimizu.png",
        "bg":  "battle_cave_1.png",
        "exp": 7,
        "gold": 20,
    },
    {
        "id": "C",
        "name": "ぴりからキノコ",
        "hp": 35,
        "max_hp": 35,
        "atk": 10,
        "img": "enemy_kinoko.png",
        "bg":  "battle_cave_2.png",
        "exp": 10,
        "gold": 13,
    },
    {
        "id": "M",
        "name": "ぴょこミント",
        "hp": 40,
        "max_hp": 40,
        "atk": 6,
        "img": "enemy_mint.png",
        "bg":  "battle_cave_2.png",
        "exp": 12,
        "gold": 15,
    },
    {
        "id": "D",
        "name": "ふかふかダンゴ",
        "hp": 80,
        "max_hp": 80,
        "atk": 30,
        "img": "enemy_dango.png",
        "bg":  "battle_cave_2.png",
        "exp": 13,
        "gold": 16,
    },
    {
        "id": "P",
        "name": "カラメルかえる",
        "hp": 80,
        "max_hp": 80,
        "atk": 30,
        "img": "enemy_kaeru.png",
        "bg":  "battle_cave_3.png",
        "exp": 13,
        "gold": 20,
    },
    {
        "id": "S",
        "name": "こうばしみみず",
        "hp": 50,
        "max_hp": 50,
        "atk": 50,
        "img": "enemy_smoke.png",
        "bg":  "battle_cave_3.png",
        "exp": 15,
        "gold": 25,
    },
    {
        "id": "F",
        "name": "しゅごもぐら",
        "hp": 100,
        "max_hp": 100,
        "atk": 40,
        "img": "enemy_shugomogura.png",
        "bg":  "battle_boss2.png",
        "exp": 0,
        "gold": 0,
    },
]

# idから敵データを取得できる便利辞書
ENEMY_TABLE = {enemy["id"]: enemy for enemy in ENEMIES}

# ========== 装備補正を加味した現在の攻撃力・防御力 ==========
def get_current_atk():
    """
    現在の攻撃力（装備補正含む）
    """
    base = player_status["atk"]
    weapon = player_status["equip"].get("weapon")
    bonus = 0
    if weapon and weapon in EQUIPMENT_TABLE:
        bonus = EQUIPMENT_TABLE[weapon]["bonus"].get("atk", 0)
    return base + bonus

def get_current_def():
    """
    現在の防御力（装備補正含む）
    """
    base = player_status["def_"]
    armor = player_status["equip"].get("armor")
    bonus = 0
    if armor and armor in EQUIPMENT_TABLE:
        bonus = EQUIPMENT_TABLE[armor]["bonus"].get("def_", 0)
    return base + bonus

def get_exp_to_next_level():
    """
    次のレベルアップまでに必要な経験値を返します。
    最大レベルの場合は0を返します。
    """
    lv = player_status["lv"]
    exp = player_status["exp"]
    if lv >= MAX_LV:
        return 0  # すでに最大レベル
    next_level_exp = LEVEL_EXP_TABLE[lv]  # lv=1のときはLEVEL_EXP_TABLE[1]=10（Lv2到達に10EXP必要）
    return max(0, next_level_exp - exp)

def is_max_level():
    """現在レベルが最大かどうか"""
    return player_status["lv"] >= MAX_LV 

