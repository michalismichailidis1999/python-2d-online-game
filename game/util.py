import pygame
from os import walk

def import_folder_images(path, scale=1, flip=False):
	surface_list = []

	for _,__,img_files in walk(path):
		for image in img_files:
			full_path = path + '/' + image
			image_surf = pygame.image.load(full_path).convert_alpha()
			
			if scale != 1:
				rect = image_surf.get_rect()
					
				image_surf = pygame.transform.scale(image_surf, (rect.width * scale, rect.height * scale))
		
				if flip:
					image_surf = pygame.transform.flip(image_surf, True, False)
				
			surface_list.append(image_surf)

	return surface_list