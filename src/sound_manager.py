# sound_manager.py
import pygame
from pathlib import Path
import json

# ==========================================
# サウンド管理クラス
# ==========================================
class SoundManager:
    # 音量のデフォルト値
    DEFAULTS = {
        "bgm_volume": 0.6,    # BGMはやや控えめ
        "se_volume": 0.8,     # 効果音は大きめ
        "voice_volume": 1.0,  # ボイス（音声）は最大
    }

    def __init__(self, base_path):
        """
        サウンドマネージャの初期化
        :param base_path: "assets/sounds"を想定したPath
        """
        # サウンド関連のパス設定
        self.bgm_path = base_path / "bgm"
        self.se_path = base_path / "se"
        self.voice_path = base_path / "voice"
        self.settings_path = base_path.parent / "sound_settings.json"  # 設定ファイルの保存先 

        # サウンドチャンネル
        self.voice_channel = pygame.mixer.Channel(3)  # 独立したボイスチャンネルを確保
        self.current_bgm = None  # 再生中BGMのフルパス（重複再生防止用）

        # 音量パラメータ（初期値をセット）
        self.bgm_volume = self.DEFAULTS["bgm_volume"]
        self.se_volume = self.DEFAULTS["se_volume"]
        self.voice_volume = self.DEFAULTS["voice_volume"]

        # 効果音(SE)の辞書
        self.se = {}

        # 効果音の読み込み
        self._load_se()

        # 音量設定ファイル（sound_settings.json）の読み込み（あれば上書き）
        self.load_settings()

        # 読み込んだ音量設定をすべてのサウンドに反映
        self.apply_volume()

    def _load_se(self):
        """効果音ファイルを辞書として読み込む"""
        files = {
            "cursor": "カーソル移動11.mp3",      # カーソル移動
            "select": "カーソル移動10.mp3",      # 決定・選択
            "cancel": "キャンセル4.mp3",         # キャンセル
            "item_get": "金額表示.mp3",          # アイテム購入
            "attack": "小キック.mp3",            # 攻撃
            "damage": "小パンチ.mp3",            # ダメージ
            "victory": "ジャジャーン.mp3",       # 勝利
            "levelup": "ラッパのファンファーレ.mp3", # レベルアップ
            "encounter": "ひらめく1.mp3",        # エンカウント
            "runok": "ピューンと逃げる.mp3",      # 逃げる成功
            "runfail": "間抜け2.mp3",           # 逃げるの失敗
            "defeat": "間抜け5.mp3",            # 敗北
            "roostercry": "ニワトリの鳴き声1.mp3", # 宿屋で使う朝の目覚め
            "save": "成功音.mp3",               # セーブ
            "load": "ニワトリの鳴き声1.mp3",     # ロード
            "error": "間抜け2.mp3",             # ロード失敗
            "equip": "可愛い動作.mp3",          # 装備する
            "unequip": "ぷよん.mp3",            # 装備を外す
            "heal": "ステータス治療1.mp3",      # 回復
            "warp": "ヒューンと落下.mp3",        # ワープ
        }
        self.se = {}
        for key, fname in files.items():
            path = self.se_path / fname
            try:
                sound = pygame.mixer.Sound(str(path))
                sound.set_volume(self.se_volume)  # 初期音量を反映
                self.se[key] = sound
            except Exception as e:
                print(f"[SoundManager] 効果音の読み込み失敗: {fname} ({e})")

    def apply_volume(self):
        """
        現在の音量パラメータをBGM/SE/Voiceに反映
        """
        pygame.mixer.music.set_volume(self.bgm_volume)
        for sound in self.se.values():
            sound.set_volume(self.se_volume)
        self.voice_channel.set_volume(self.voice_volume)

    # BGMの音量設定
    def set_bgm_volume(self, vol):
        self.bgm_volume = max(0.0, min(1.0, vol))
        pygame.mixer.music.set_volume(self.bgm_volume)

    # SEの音量設定
    def set_se_volume(self, vol):
        self.se_volume = max(0.0, min(1.0, vol))
        for sound in self.se.values():
            sound.set_volume(self.se_volume)

    # Voiceの音量設定
    def set_voice_volume(self, vol):
        self.voice_volume = max(0.0, min(1.0, vol))
        self.voice_channel.set_volume(self.voice_volume)

    def save_settings(self):
        """
        現在の音量設定をJSONファイルに保存
        """
        data = {
            "bgm_volume": self.bgm_volume,
            "se_volume": self.se_volume,
            "voice_volume": self.voice_volume,
        }
        try:
            with open(self.settings_path, "w", encoding="utf-8") as f:
                json.dump(data, f)
        except Exception as e:
            print(f"[SoundManager] 音量設定の保存に失敗: {e}")

    def load_settings(self):
        """
        JSONから音量設定を読み込み（なければデフォルト値のまま）
        """
        try:
            with open(self.settings_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.bgm_volume = float(data.get("bgm_volume", self.DEFAULTS["bgm_volume"]))
                self.se_volume = float(data.get("se_volume", self.DEFAULTS["se_volume"]))
                self.voice_volume = float(data.get("voice_volume", self.DEFAULTS["voice_volume"]))
        except Exception:
            # ファイルがなければデフォルト値のまま
            pass

    # ----------------------------
    # BGM（音楽）再生・停止
    # ----------------------------
    def play_bgm(self, filename, loop=True):
        """
        指定BGMファイルの再生。現在のBGMと同じなら何もしない
        """
        full_path = str(self.bgm_path / filename)
        if self.current_bgm == full_path:
            return
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(full_path)
            pygame.mixer.music.set_volume(self.bgm_volume)
            pygame.mixer.music.play(-1 if loop else 0)
            self.current_bgm = full_path
        except Exception as e:
            print(f"[SoundManager] BGM再生失敗: {filename} ({e})")
            self.current_bgm = None

    def stop_bgm(self):
        """BGMを停止"""
        pygame.mixer.music.stop()
        self.current_bgm = None

    def fadeout_bgm(self, ms=1000):
        """BGMをフェードアウトで停止"""
        pygame.mixer.music.fadeout(ms)
        self.current_bgm = None

    # ----------------------------
    # 効果音(SE)再生
    # ----------------------------
    def play_se(self, key):
        """
        効果音を再生。指定キーがなければ何もしない
        """
        if key in self.se:
            self.se[key].play()

    # ----------------------------
    # ボイス（音声）再生・停止
    # ----------------------------
    def play_voice(self, filename):
        """
        ボイス音声（mp3/wav）を再生。
        再生中はstopしてから新たに流す。音量も必ず反映
        """
        self.stop_voice()
        path = str(self.voice_path / filename)
        try:
            sound = pygame.mixer.Sound(path)
            sound.set_volume(self.voice_volume)  # 音量も反映
            self.voice_channel.play(sound)
        except Exception as e:
            print(f"[SoundManager] ボイス再生失敗: {filename} ({e})")

    def stop_voice(self):
        """ボイスチャンネルの音声を停止"""
        self.voice_channel.stop()


# ==========================================
# サウンドマネージャの初期化例
# ==========================================
# このファイルはモジュールとして使う前提なので、
# ゲーム本体(main.pyなどメインスクリプト)で以下のように初期化してください。
# from sound_manager import SoundManager
# sound_manager = SoundManager(Path(__file__).resolve().parent / "assets" / "sounds")
# 必ず**Pygameの初期化後（pygame.mixer.init()後）**にSoundManagerを作ってください。

# BGM（音楽）は容量が大きいため、再生時にファイル名で都度ロードして使用しています。
# SE（効果音）は短く軽量なため、事前にSoundオブジェクトとして事前にメモリに読み込んでおくことで、
# 即時再生・レスポンス向上を図っています。
# ※この方式はPygameに限らず、一般的なゲーム開発でもよく用いられる手法のようです。

