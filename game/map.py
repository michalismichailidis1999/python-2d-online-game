import pygame
from game.settings import Settings
from game.player import Player
from game.obstacle import Obstacle
from game.maps.map0 import map0

class Map:
	def __init__(self, settings:Settings):
		self.settings = settings
		self.display_surface = pygame.display.get_surface()
		self.player = pygame.sprite.GroupSingle()
		self.obstacles = CameraGroup()

		self.world_shift = 0
		
		self._load()

	def _load(self):
		tileSise = self.settings.screen['tileSize']

		for i, row in enumerate(map0):
			for j, col in enumerate(map0[i]):
				pos = (j*tileSise, i*tileSise)
				if col == 'P':
					self.player.add(Player(pos, self.settings))
				elif col == 'X':
					obstacle = Obstacle(pos, (64, 64), self.obstacles)

	def run(self):
		self.display_surface.fill('black')

		self.obstacles.update(self.world_shift)
		self.obstacles.custom_draw(self, self.settings)

		self.player.update(self.obstacles)
		self.player.draw(self.display_surface)
		
class StaticGroup(pygame.sprite.Group):
	def __init__(self):
		super().__init__()

class CameraGroup(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		
	def custom_draw(self, map:Map, settings:Settings):
		player = map.player.sprite

		if player.rect.centerx >= self.display_surface.get_width() - 200 and player.direction.x > 0:
			player.speed = 0
			map.world_shift = -settings.player['speed']
		elif player.rect.centerx <= 200 and player.direction.x < 0:
			player.speed = 0
			map.world_shift = settings.player['speed']
		else:
			player.speed = settings.player['speed']
			map.world_shift = 0

		self.draw(self.display_surface)