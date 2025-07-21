# sound_manager.py
import pygame
from pathlib import Path

# BGM（音楽）は容量が大きいため、再生時にファイル名で都度ロードして使用しています。
# SE（効果音）は短く軽量なため、事前にSoundオブジェクトとして事前にメモリに読み込んでおくことで、
# 即時再生・レスポンス向上を図っています。
# ※この方式はPygameに限らず、一般的なゲーム開発でもよく用いられる手法のようです。

# サウンド管理クラス
class SoundManager:
    def __init__(self, base_path):
        # サウンドのパスを保存
        self.bgm_path = base_path / "bgm"
        self.se_path = base_path / "se"
        self.current_bgm = None

        # 効果音ファイルの読み込み（辞書で管理）
        self.se = {
            "cursor": pygame.mixer.Sound(str(self.se_path / "カーソル移動11.mp3")),       # カーソル移動
            "select": pygame.mixer.Sound(str(self.se_path / "カーソル移動10.mp3")),       # 決定・選択
            "cancel": pygame.mixer.Sound(str(self.se_path / "キャンセル4.mp3")),          # キャンセル
            "item_get": pygame.mixer.Sound(str(self.se_path / "金額表示.mp3")),          # アイテム入手
            "attack": pygame.mixer.Sound(str(self.se_path / "小キック.mp3")),            # 攻撃
            "damage": pygame.mixer.Sound(str(self.se_path / "小パンチ.mp3")),            # ダメージ
            "victory": pygame.mixer.Sound(str(self.se_path / "ジャジャーン.mp3")),        # 勝利
            "levelup": pygame.mixer.Sound(str(self.se_path / "ラッパのファンファーレ.mp3")),       # レベルアップ
            "encounter": pygame.mixer.Sound(str(self.se_path / "ひらめく1.mp3")),        # エンカウント
            "runok": pygame.mixer.Sound(str(self.se_path / "ピューンと逃げる.mp3")),      #逃げる成功
            "runfail": pygame.mixer.Sound(str(self.se_path / "間抜け2.mp3")),            #逃げるの失敗
            "defeat": pygame.mixer.Sound(str(self.se_path / "間抜け5.mp3")),             # 敗北
            "roostercry": pygame.mixer.Sound(str(self.se_path / "ニワトリの鳴き声1.mp3")),  # 宿屋で使う朝の目覚め
            "save": pygame.mixer.Sound(str(self.se_path / "成功音.mp3")),                 # セーブ
            "load": pygame.mixer.Sound(str(self.se_path / "ニワトリの鳴き声1.mp3")),       # ロード
            "error": pygame.mixer.Sound(str(self.se_path / "間抜け2.mp3")),               # ロード失敗
            "equip": pygame.mixer.Sound(str(self.se_path / "可愛い動作.mp3")),               # 装備する
            "unequip": pygame.mixer.Sound(str(self.se_path / "ぷよん.mp3")),             # 装備を外す
            "heal": pygame.mixer.Sound(str(self.se_path / "ステータス治療1.mp3")),        # 回復
            "warp": pygame.mixer.Sound(str(self.se_path / "ヒューンと落下.mp3")),         # ワープ
        }

    # BGM再生
    def play_bgm(self, filename, loop=True):
        full_path = str(self.bgm_path / filename)
        # すでに再生中ならスキップ
        if self.current_bgm == full_path:
            return
        pygame.mixer.music.stop()
        pygame.mixer.music.load(full_path)
        pygame.mixer.music.play(-1 if loop else 0)
        self.current_bgm = full_path

    # BGM停止
    def stop_bgm(self):
        pygame.mixer.music.stop()
        self.current_bgm = None

    # BGMフェードアウト（msはミリ秒、デフォルトは1000ms = 1秒）
    def fadeout_bgm(self, ms=1000):
        pygame.mixer.music.fadeout(ms)
        self.current_bgm = None
        
    # 効果音再生
    def play_se(self, key):
        if key in self.se:
            self.se[key].play()

# サウンドマネージャの初期化例
sound_manager = SoundManager(Path(__file__).resolve().parent / "assets" / "sounds")




