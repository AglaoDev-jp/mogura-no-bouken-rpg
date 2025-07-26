# item_effects.py
# ----------------------------------------
# アイテムの効果・購入・パラメータ補助関数を管理
# ----------------------------------------

from status import player_status

# --- アイテムの種類（種別管理） ---
ITEM_KINDS = {
    "ごちサンド": "consumable",   # 使うたび減る
    "トロッコ": "consumable",
    "スコップ": "weapon",       # 装備1回限り
    "ヘルメット": "armor",
}

# --- 装備によるステータス補正値 ---
ITEM_STATUS_BONUS = {
    "スコップ": {"atk": 5},
    "ヘルメット": {"def_": 5},
}

# --- 各アイテムの効果処理（個別関数） ---
def heal_hp(status=None):
    """
    ごちサンドの効果（HP30回復）。
    status: 回復対象のステータス(dict)。省略時はplayer_status。
    """
    if status is None:
        status = player_status
    max_hp = status.get("max_hp", 100)
    recovery = 30
    old_hp = status["hp"]
    status["hp"] = min(status["hp"] + recovery, max_hp)
    return f"HPを {status['hp'] - old_hp} 回復した！"

def escape_dungeon(status=None):
    """
    トロッコの効果を実行します。
    ダンジョン内で使用した場合、呼び出し元で町へ強制帰還させる必要があります。

    【戻り値】
      - dict型：{"result": "escape_dungeon", "message": "トロッコで一瞬で町に戻った！"}

    呼び出し例：
      result = escape_dungeon()
      if result.get("result") == "escape_dungeon":
          # ここで町へ戻す処理を記述

    トロッコの効果：ダンジョンから町へ強制帰還。
    呼び出し元（scenes/inventory.py → main.py）でシーン遷移を行うこと！

    """
    # ※インベントリ減算はuse_item()で行います。
    return {"result": "escape_dungeon", "message": "トロッコで一瞬で町に戻った！"}


def equip_weapon():
    """
    スコップを装備。
    """
    if player_status.get("weapon") == "スコップ":
        return "スコップはすでに装備しています。"
    player_status["weapon"] = "スコップ"
    return "スコップを装備した！"


def equip_armor():
    """
    ヘルメットを装備。
    """
    if player_status.get("armor") == "ヘルメット":
        return "ヘルメットはすでに装備しています。"
    player_status["armor"] = "ヘルメット"
    return "ヘルメットを装備した！"

# --- アイテム名→処理関数のマッピング ---
item_effects = {
    "ごちサンド": heal_hp,
    "トロッコ": escape_dungeon,
    "スコップ": equip_weapon,
    "ヘルメット": equip_armor,
}

# --- アイテム使用時の共通処理 ---
# use_item()より
def use_item(item_name, context="dungeon", player=None, sound_manager=None):
    """
    アイテム使用時の挙動。戦闘中はplayer（dict）で管理、マップ時はplayer_statusで管理。
    :param item_name: 使用するアイテム名
    :param context: 'dungeon' or 'battle'
    :param player: 戦闘中バトル用ステータス(dict)。省略時は player_status を使う
    :param sound_manager: SoundManager インスタンス。Noneの場合は音なし
    """
    # --- ステータス対象を決定 ---
    status = player if player is not None else player_status

    # --- ごちサンドの特別処理 ---
    if item_name == "ごちサンド":
        # ● 効果音
        if sound_manager:
            sound_manager.play_se("heal")
        # ● 回復量
        heal_amount = 20
        before = status["hp"]
        status["hp"] = min(status["hp"] + heal_amount, status["max_hp"])
        healed = status["hp"] - before
        # ● アイテム減算
        items = status.setdefault("items", {})
        if items.get(item_name, 0) > 0:
            items[item_name] -= 1
            if items[item_name] <= 0:
                del items[item_name]
        return f"ごちサンドでHPが{healed}回復！"

    # --- トロッコはダンジョン内限定 ---
    if item_name == "トロッコ" and context != "dungeon":
        return f"{item_name}は今は使えない…"
    # --- スコップを戦闘中に使えないようにする ---
    if item_name == "スコップ" and context != "dungeon":
        # 戦闘中(context="battle")や町(context="town")では使えない
       return f"{item_name}は今は使えない…"
    # --- ヘルメットを戦闘中に使えないようにする ---
    if item_name == "ヘルメット" and context != "dungeon":
        # 戦闘中(context="battle")や町(context="town")では使えない
       return f"{item_name}は今は使えない…"
    
    # --- 装備品（weapon/armor）は減算せず関数呼び出しのみ ---
    kind = ITEM_KINDS.get(item_name, "consumable")
    if kind in ["weapon", "armor"]:
        return item_effects[item_name]()

    # --- 所持チェック ---
    items = status.setdefault("items", {})
    if items.get(item_name, 0) <= 0:
        return f"{item_name}を持っていません。"

    # 使用制限
    result = item_effects[item_name](status)
    items[item_name] -= 1
    if items[item_name] <= 0:
        del items[item_name]
    return result

# --- アイテム購入時の処理 ---
def buy_item(item_name, price):
    """
    アイテム購入処理
    item_name: アイテム名
    price: 金額
    """
    if player_status["gold"] < price:
        
        return "お金が足りないよ！"

    kind = ITEM_KINDS.get(item_name, "consumable")
    items = player_status.setdefault("items", {})

    if kind == "weapon":
        # すでに装備中なら却下
        if player_status["equip"].get("weapon") == item_name:
            return f"{item_name}はすでに装備してるよ。"
        # itemsリストにも追加
        items[item_name] = items.get(item_name, 0) + 1
        # 装備状態に反映
        player_status["equip"]["weapon"] = item_name
        player_status["gold"] -= price
        return f"{item_name}を装備しました！"

    elif kind == "armor":
        if player_status["equip"].get("armor") == item_name:
            return f"{item_name}はすでに装備してるよ。"
        items[item_name] = items.get(item_name, 0) + 1
        player_status["equip"]["armor"] = item_name
        player_status["gold"] -= price
        return f"{item_name}を装備しました！"

    else:
        # 通常アイテム
        items[item_name] = items.get(item_name, 0) + 1
        player_status["gold"] -= price
        return f"{item_name}を手に入れた！"


# --- 装備補正を加味した攻撃力・防御力取得 ---
def get_current_atk():
    """
    装備補正込みの攻撃力を返す
    """
    base = player_status.get("atk", 0)
    weapon = player_status.get("weapon")
    bonus = ITEM_STATUS_BONUS.get(weapon, {}).get("atk", 0)
    return base + bonus

def get_current_def():
    """
    装備補正込みの防御力を返す
    """
    base = player_status.get("def_", 0)
    armor = player_status.get("armor")
    bonus = ITEM_STATUS_BONUS.get(armor, {}).get("def_", 0)
    return base + bonus