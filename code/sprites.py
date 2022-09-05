import pygame
from settings import *

class BG(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        bg_image = pygame.image.load("../graphics/environment/background.png").convert()
        
        resolution = (pygame.image.load("../graphics/environment/background.png").get_width(), 
        pygame.image.load("../graphics/environment/background.png").get_height())
        
        full_height = resolution[1] * scale_factor
        full_width =  resolution[0] * scale_factor
        
        full_sized_image = pygame.transform.scale(bg_image, (full_width, full_height))
        self.image = pygame.Surface((full_width * 2, full_height))
        self.image.blit(full_sized_image, (0,0))
        self.image.blit(full_sized_image, (full_width,0))

        self.rect = self.image.get_rect(topleft = (0,0))
        self.pos = pygame.math.Vector2(self.rect.topleft)

    def update(self, dt):
        self.pos.x -= 150 * dt

        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)