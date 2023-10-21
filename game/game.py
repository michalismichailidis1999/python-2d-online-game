import pygame, sys
from game.map import Map
from game.settings import Settings

class Game:
	def __init__(self):
		pygame.init()
		self.settings = Settings('./game/settings.json')
		self.screen = pygame.display.set_mode((self.settings.screen['width'], self.settings.screen['height']))
		pygame.display.set_caption(self.settings.screen['caption'])
		self.clock = pygame.time.Clock()
		self.map = Map(self.settings)
		
	def display(self):
		self.map.run()
		
	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
					
			self.map.run()
			pygame.display.update()
			self.clock.tick(60)