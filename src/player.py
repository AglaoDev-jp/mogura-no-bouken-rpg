# player.py
import pygame
from pathlib import Path

class Player:
    def __init__(self, start_pos, base_dir):
        self.pos = pygame.Vector2(start_pos)
        self.speed = 6
        self.direction = "down"
        self.frame_index = 0
        self.frame_timer = 0
        self.frame_interval = 10  # フレーム切り替え速度

        # プレイヤー画像読み込み
        self.images = self.load_images(base_dir / "assets" / "images" / "player")
        self.image = self.images[self.direction][self.frame_index]
        self.rect = self.image.get_rect(center=self.pos)

    def load_images(self, folder):
        """
        ★将来的なメモ★
        アニメーション画像の枚数が増えた場合、以下のように glob を使えばファイル数を自動で検出可能。
        import glob を使うと load_images を修正せずに画像を自由に追加できる。
        例:
        pattern = str(folder / f"{dir}_*.png")
        file_paths = sorted(glob.glob(pattern))
        ※今は range(2) で手動指定。モジュール数をこれ以上増やしたくないので保留。
        """
        directions = ["down", "up", "left", "right"]
        images = {}
        for dir in directions:
            dir_images = []
            # キャラのフレーム数
            for i in range(2): # たとえば5枚使いたいときは range(5)
                path = folder / f"{dir}_{i}.png"
                img = pygame.image.load(str(path)).convert_alpha()
                img = pygame.transform.scale(img, (48, 48))
                dir_images.append(img)
            images[dir] = dir_images
        return images

    def update(self, keys):
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -self.speed
            self.direction = "left"
        elif keys[pygame.K_RIGHT]:
            dx = self.speed
            self.direction = "right"
        elif keys[pygame.K_UP]:
            dy = -self.speed
            self.direction = "up"
        elif keys[pygame.K_DOWN]:
            dy = self.speed
            self.direction = "down"

        moved = dx != 0 or dy != 0
        if moved:
            self.pos.x += dx
            self.pos.y += dy
            self.frame_timer += 1
            if self.frame_timer >= self.frame_interval:
                self.frame_index = (self.frame_index + 1) % len(self.images[self.direction])
                self.frame_timer = 0
        else:
            self.frame_index = 1  # 立ち止まり時は中央の画像

        self.image = self.images[self.direction][self.frame_index]
        self.rect = self.image.get_rect(center=self.pos)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def get_current_image(self):
        """
        現在のアニメーションフレームの画像（Surface）を返します。
        dungeon.draw() 内でスプライトを描画したいときに使われます。
        """
        # もし self.image 属性に常に最新のフレームを保持しているならこれでOK
        return self.image

        # もしフレームリストとインデックスで管理しているなら、例えば：
        # return self.images[self.direction][self.frame_index]

    def get_center(self):
        return (int(self.pos.x), int(self.pos.y))

    def set_center(self, x, y):
        self.pos.update(x, y)
        self.rect.center = (x, y)
