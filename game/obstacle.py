from typing import Any
import pygame

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, pos:(int, int), size:(int, int), group:pygame.sprite.Group):
        super().__init__(group)

        self.image = pygame.Surface(size)
        self.image.fill('gray')
        self.rect = self.image.get_rect(topleft = pos)

    def update(self, world_shift: int):
        self.rect.x += world_shift