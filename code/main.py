import pygame, sys, time
from settings import *
from sprites import *

class App():

    def __init__(self):
        # setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock()
        self.active = True

        # sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        # scale factors
        bg_height = pygame.image.load('../graphics/environment/background.png').get_height()
        self.scale_factor = WINDOW_HEIGHT / bg_height

        # sprite setup
        BG(self.all_sprites, self.scale_factor)
        Ground([self.all_sprites, self.collision_sprites], self.scale_factor)
        self.player = Player(self.all_sprites, self.scale_factor / 4.5)
        

        # timer
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 900)

        # menu

        self.menu_surf = pygame.image.load('../graphics/ui/tap.png').convert_alpha()
        self.menu_rect = self.menu_surf.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

        # Text

        self.font = pygame.font.Font('../others/font.ttf', 30)
        self.score = 0
        Ground([self.all_sprites, self.collision_sprites], self.scale_factor)

    def Score_display(self):
        if self.active:
            self.score = round(pygame.time.get_ticks() // 1000)

        score_surf = self.font.render(str(self.score), False, 'white')
        score_rect = score_surf.get_rect(midtop = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 10))
        self.display_surface.blit(score_surf, score_rect)

    def collisions(self):
        if pygame.sprite.spritecollide(self.player, self.collision_sprites, False, pygame.sprite.collide_mask)\
        or self.player.rect.top <= 0:
            self.active = False

    def run(self):
        last_time = time.time()
        while True:

            # delta time
            dt = time.time() - last_time
            last_time = time.time()

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.player.jump()
                if event.type == self.obstacle_timer:
                    Obstacles([self.all_sprites, self.collision_sprites], self.scale_factor)
            # game logic

            self.display_surface.fill('white')
            self.all_sprites.update(dt)
            if self.active:
                self.collisions()
            else:
                self.display_surface.blit(self.menu_surf, self.menu_rect)
            self.all_sprites.draw(self.display_surface)
            self.Score_display()

            pygame.display.update()
            self.clock.tick(FRAMERATE)
        
        

if __name__ == '__main__':
    app = App()
    app.run()