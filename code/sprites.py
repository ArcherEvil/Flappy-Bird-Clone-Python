import pygame
from settings import *
from random import choice, randint, randrange

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
        self.pos.x -= 50 * dt

        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)

class Ground(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        ground_surf = pygame.image.load('../graphics/environment/ground.png').convert_alpha()
        self.image = pygame.transform.scale(ground_surf, pygame.math.Vector2(ground_surf.get_size()) * scale_factor)
        self.rect = self.image.get_rect(bottomleft= (0,WINDOW_HEIGHT))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        # mask

        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.pos.x -= 200 * dt

        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)

class Player(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        
        # image
        self.import_frames(scale_factor)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        # rect 
        self.rect = self.image.get_rect(midleft = (WINDOW_WIDTH / 20, WINDOW_HEIGHT/2))

        self.pos = pygame.math.Vector2(self.rect.topleft)

        # movement
        self.gravity = 1700
        self.direction = 0
    
        # mask

        self.mask = pygame.mask.from_surface(self.image)
    
    def import_frames(self, scale_factor):
        self.frames = []
        for n in range(2):
            surf = pygame.image.load(f'../graphics/plane/0{n + 1}.png').convert_alpha()
            scaled_surface = pygame.transform.scale(surf, pygame.math.Vector2(surf.get_size()) * scale_factor)
            self.frames.append(scaled_surface)

    def apply_gravity(self, dt):
        self.direction += self.gravity * dt
        self.pos.y += self.direction * dt
        self.rect.y = round(self.pos.y)
        if self.direction >= 100:
            self.image = self.frames[0]

    def jump(self):
        self.direction = -500
        self.image = self.frames[1]


    def update(self, dt):
        self.apply_gravity(dt)

class Obstacles(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)

        color = randint(0,9)

        orientation = choice(('up', 'down'))
        surf = pygame.image.load(f'../graphics/obstacles/0{color}.png').convert_alpha()
        self.image = pygame.transform.scale(surf, pygame.math.Vector2(surf.get_size()) * scale_factor * 1.6)
        
        x = WINDOW_WIDTH + randint(40, 100)

        # mask

        self.mask = pygame.mask.from_surface(self.image)

        if orientation == 'up':
            y = WINDOW_HEIGHT * 1.4 + randrange(-70, 120, 30)
            self.rect = self.image.get_rect(midbottom = (x,y))

        elif orientation == 'down':
            y = -WINDOW_HEIGHT / 2 + randrange(-70, 120, 30)
            self.image = pygame.transform.flip(self.image, False, True)

            self.rect = self.image.get_rect(midtop = (x,y))
    
        self.pos = pygame.math.Vector2(self.rect.topleft)

    def update(self, dt):
        self.pos.x -= 400 * dt
        self.rect.x = round(self.pos.x)
        if self.rect.right <= -100:
            self.kill()


