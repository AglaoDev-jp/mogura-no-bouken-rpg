# scenes/save_load.py
import json
import sys
from pathlib import Path  
from status import player_status # 必要なグローバル変数をインポート
from scenes import dungeon  # ボス撃破情報を管理しているdungeon.pyをインポート

def get_save_path(slot=1):
    """スロット番号に応じたファイルパスを返す（例：save1.json, save2.json, ...）"""
    filename = f"save{slot}.json"
    if hasattr(sys, '_MEIPASS'):
        base_dir = Path(sys.executable).parent
    else:
        base_dir = Path(__file__).resolve().parent.parent
    return str(base_dir / filename)

def save_game(slot=1):
    """スロット指定でセーブします"""
    # --- プレイヤー情報の保存 ---
    save_data = {"player_status": player_status}
    # --- ボス撃破情報の保存 ---
    save_data["boss_defeated_flags"] = dungeon.boss_defeated_flags.copy()
    # ★将来拡張する場合はここに他の変数も追加

    file_path = get_save_path(slot)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(save_data, f, ensure_ascii=False, indent=2)
    print(f"セーブが完了しました。（{file_path}）")

def save_file_exists(slot=1):
    """指定したスロットのセーブデータが存在するか判定します"""
    file_path = get_save_path(slot)
    return Path(file_path).exists()

def load_game(slot=1):
    """スロット指定でロードします。ファイルがなければFalseを返す"""
    global player_status
    file_path = get_save_path(slot)
    if not Path(file_path).exists():
        print(f"セーブデータが存在しません: {file_path}")
        return False  # ←これが肝
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            save_data = json.load(f)
        player_status.clear()
        player_status.update(save_data["player_status"])
        dungeon.boss_defeated_flags = save_data.get(
            "boss_defeated_flags", {"K": False, "D": False, "F": False}
        ).copy()
        dungeon.clear_defeated_boss_tiles()
        print(f"ロードが完了しました。（{file_path}）")
        return True  # 成功時True
    except Exception as e:
        print(f"ロードに失敗しました: {e}")
        return False


SAVE_FILE = get_save_path()  # セーブデータの保存先





