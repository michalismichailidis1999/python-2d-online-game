import pygame
from game.particles import BulletParticle
from game.util import import_folder_images
from game.settings import Settings

class GenericSprite(pygame.sprite.Sprite):
    def __init__(self, group:pygame.sprite.Group, image: pygame.Surface, pos:(int, int)):
        super().__init__(group)

        self.image = image
        self.rect = image.get_rect(topleft=pos)

class Obstacle(GenericSprite):
    def __init__(self, pos:(int, int), size:(int, int), group:pygame.sprite.Group):
        image = pygame.Surface(size)
        image.fill('gray')

        super().__init__(group, image, pos)

    def update(self, world_shift: int):
        self.rect.x += world_shift

class Bullet(GenericSprite):
    def __init__(self, pos:(int, int), flip:bool, settings:Settings, group:pygame.sprite.Group):
        self.settings = settings

        self._load(flip)

        self.speed = settings.bullet['speed'] * (-1 if flip else 1)

        self.frame_index = 0
        self.animation_speed = settings.bullet['animationSpeed']

        super().__init__(group, self.animations[self.frame_index], pos)

    def _load(self, flip:bool):
        self.animations = import_folder_images(self.settings.bullet['imagesPath'] + 'instantiate', 2, flip)

    def _animate(self):
        self.frame_index += self.animation_speed

        totalFrames = len(self.animations)

        idx = int(self.frame_index)

        if idx > totalFrames - 1:
            idx = 0
            self.frame_index = 0

        self.image = self.animations[idx]

    def kill_bullet(self, particlesGroup:pygame.sprite.Group):
        BulletParticle((self.rect.x, self.rect.y), self.settings, particlesGroup)
        self.kill()

    def update(self, hitables:list[pygame.sprite.Sprite], obstacles:list[pygame.sprite.Sprite], particlesGroup:pygame.sprite.Group):
        self._animate()

        self.rect.x += self.speed

        collide = False

        for hitable in hitables:
            if hitable.rect.colliderect(self.rect):
                hitable.take_hit()
                collide = True
                break

        if collide: self.kill_bullet(particlesGroup)

        for obstacle in obstacles:
            if obstacle.rect.colliderect(self.rect):
                collide = True
                break

        if collide: self.kill_bullet(particlesGroup)

