import pygame
from game.settings import Settings
from game.util import import_folder_images

class Particle(pygame.sprite.Sprite):
    def __init__(self, pos:(int, int), images_path:str, animation_speed:float, group:pygame.sprite.Group):
        super().__init__(group)

        self._load(images_path)

        self.frame_index = 0
        self.animation_speed = animation_speed

        self.image = self.animations[self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

    def _load(self, path:str):
        self.animations = import_folder_images(path, 2)

    def _animate(self):
        self.frame_index += self.animation_speed

        total_frames = len(self.animations)

        idx = int(self.frame_index)

        if idx > total_frames - 1:
            self.kill()
        else: self.image = self.animations[idx]

    def update(self):
        self._animate()

class BulletParticle(Particle):
    def __init__(self, pos:(int, int), settings:Settings, group:pygame.sprite.Group):
        super().__init__(pos, settings.bullet['imagesPath'] + 'collision', settings.bullet['particleAnimationSpeed'], group)    