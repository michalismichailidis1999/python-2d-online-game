import pygame

class Keyboard:
    def __init__(self):
        self.up = 0
        self.right = 0
        self.left = 0
        self.shoot = 0
        self.slide = 0

class ClassicKeyboard(Keyboard):
    def __init__(self):
        self.up = pygame.K_w
        self.right = pygame.K_d
        self.left = pygame.K_a
        self.shoot = pygame.K_SPACE
        self.slide = pygame.K_LSHIFT

class ArrowKeyboard(Keyboard):
    def __init__(self):
        self.up = pygame.K_UP
        self.right = pygame.K_RIGHT
        self.left = pygame.K_LEFT
        self.shoot = pygame.K_1
        self.slide = pygame.K_2

class CustomKeyboard(Keyboard):
    def __init__(self, up:int, right:int, left:int, shoot:int, slide:int):
        self.up = up
        self.right = right
        self.left = left
        self.shoot = shoot
        self.slide = slide