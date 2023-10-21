import re
import pygame
from game.obstacle import Obstacle
from game.settings import Settings
from game.keyboard import Keyboard, ClassicKeyboard
from game.util import import_folder_images
from game.constants import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos:(int, int), settings:Settings, keyboard:Keyboard = None):
        super().__init__()

        self._load()

        self.settings = settings

        self.direction = pygame.math.Vector2()
        self.speed = settings.player['speed']

        self.is_left = False

        self.shooting = False
        self.can_shoot = True

        self.is_sliding = False
        self.can_slide = False

        self.jump_speed = settings.player['jumpSpeed']
        self.gravity = settings.player['gravity']
        self.on_ground = False
        self.jumps = 0
        self.max_jumps = settings.player['maxJumps']

        self.frame_index = 0
        self.animation_speed = settings.player['animationSpeed']
        self.animation_cooldown = 0
        self.status = self._get_status()

        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

        if keyboard == None:
            keyboard = ClassicKeyboard()

        self.keyboard = keyboard

    def _load(self):
        keys = [
            'idle',
            'duck',
            'hurt',
            'jump',
            'run',
            'run-shoot',
            'shoot',
            'slide'
        ]

        has_not_rotation = set([])

        self.animations = {}

        player_path = './game/graphics/player/'

        for key in keys:
            if key in has_not_rotation:
                self.animations[key] = import_folder_images(player_path + key, 2)
            else:
                self.animations['right_' + key] = import_folder_images(player_path + key, 2)
                self.animations['left_' + key] = import_folder_images(player_path + key, 2, True)

    #region Movement

    def _input(self):
        keys = pygame.key.get_pressed()

        if keys[self.keyboard.up] and self.jumps < self.max_jumps and not self.shooting:
            self._jump()

        idleShooting = self.status == (('left_' if self.is_left else 'right_') +  SHOOT)

        if not self.is_sliding:
            if keys[self.keyboard.left] and not idleShooting:
                self.direction.x = -1
                self.is_left = True
            elif keys[self.keyboard.right] and not idleShooting:
                self.direction.x = 1
                self.is_left = False
            else:
                self.direction.x = 0

        if keys[self.keyboard.slide] and not self.shooting and self.on_ground and self.can_slide:
            self._slide()

        if keys[self.keyboard.shoot] and self.on_ground and self.can_shoot:
            self._shoot()

    def _apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def _slide(self):
        self.is_sliding = True
        self.can_slide = False
        self.direction.x *= 1.2
        self.animation_cooldown = self.settings.player['slideCooldown']

    def _jump(self):
        if self.jumps == 0:
            self.direction.y = self.jump_speed
            self.jumps += 1
            self.animation_cooldown = self.settings.player['jumpCooldown']
        elif self.jumps == 1 and self.animation_cooldown <= 0:
            self.direction.y = self.direction.y + self.jump_speed * 0.65 if self.direction.y < 0 else self.jump_speed
            self.jumps += 1

        self.on_ground = False

    def _check_horizontal_collision(self, objects:pygame.sprite.Group):
        for objSprite in objects.sprites():
            if objSprite.rect.colliderect(self.rect):
                if self.direction.x > 0:
                    self.rect.right = objSprite.rect.left
                    break
                elif self.direction.x < 0:
                    self.rect.left = objSprite.rect.right
                    break

    def _check_vertical_collision(self, objects:pygame.sprite.Group):
        for objSprite in objects.sprites():
            if objSprite.rect.colliderect(self.rect):
                if self.direction.y > 0:
                    self.rect.bottom = objSprite.rect.top
                    self.direction.y = 0
                    self.on_ground = True
                    self.jumps = 0
                    if not self.shooting:
                        self.animation_cooldown = 0
                    break
                elif self.direction.y < 0:
                    self.rect.top = objSprite.rect.bottom
                    self.direction.y = 0
                    break

    def _apply_horizontal_movement(self, objects:pygame.sprite.Group):
        self.rect.x += self.direction.x * self.speed
        self._check_horizontal_collision(objects)

    def _apply_vertical_movement(self, objects:pygame.sprite.Group):
        self._apply_gravity()
        self._check_vertical_collision(objects)

    def _update_cooldowns(self):
        if self.animation_cooldown >= 1:
            self.animation_cooldown -= 1

        if self.animation_cooldown <= 0:
            if self.shooting:
                self.can_shoot = True
                self.shooting = False
                self.frame_index = 0
            elif self.is_sliding:
                self.is_sliding = False
                self.frame_index = 0

            self.animation_cooldown = 0

    def _shoot(self):
        self.shooting = True
        self.can_shoot = False
        self.animation_cooldown = self.settings.player['shootCooldown']

    #endregion

    #region animation

    def _get_status(self) -> str:
        status = IDLE

        if not self.on_ground:
            status = JUMP
        elif self.is_sliding:
            status = SLIDE
        elif self.direction.x != 0:
            status = RUN
        
        if self.shooting:
            status = SHOOT if status == IDLE else RUN_AND_SHOOT

        key = 'right_' + status if not self.is_left else 'left_' + status

        if key not in self.animations: return status

        return key

    def _animate(self):
        prev_status = self.status

        status = self._get_status()

        if re.sub('left_|right_', '', status) != re.sub('left_|right_', '', prev_status): self.frame_index = 0

        self.frame_index += self.animation_speed

        total_frames = len(self.animations[status])

        idx = int(self.frame_index)

        dir_key = 'left_' if self.is_left else 'right_'
        
        if status == dir_key + JUMP:
            idx = 0 if self.direction.y <= 0 else 1
            self.frame_index = idx
        elif idx > total_frames - 1:
            self.frame_index = 0 if not self.shooting else total_frames - 1
            idx = 0 if not self.shooting else total_frames - 1

        try:
            img = self.animations[status][idx]
        except IndexError:
            img = self.animations[status][0]

        self.image = img
        self.status = status
    #endregion

    def update(self, objects:pygame.sprite.Group):
        self._input()

        self._update_cooldowns()

        self._animate()

        self._apply_horizontal_movement(objects)
        self._apply_vertical_movement(objects)
        