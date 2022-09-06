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
        self.active = False
        self.beggining = True

        # sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        # scale factors
        bg_height = pygame.image.load('../graphics/environment/background.png').get_height()
        self.scale_factor = WINDOW_HEIGHT / bg_height

        # sprite setup
        BG(self.all_sprites, self.scale_factor)
        Ground([self.all_sprites, self.collision_sprites], self.scale_factor)
        #self.player = Player(self.all_sprites, self.scale_factor / 4.5)
        

        # timer
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 900)

        # menu

        self.menu_surf = pygame.image.load('../graphics/ui/tap.png').convert_alpha()
        self.menu_rect = self.menu_surf.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

        # Text

        self.font = pygame.font.Font('../others/font.ttf', 30)
        self.score = 0
        self.start_offset = 0
        Ground([self.all_sprites, self.collision_sprites], self.scale_factor)

        # Title

        self.title_surf = pygame.image.load('../graphics/ui/Title.png').convert_alpha()
        self.title_rect = self.title_surf.get_rect(center= (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

        # Game Over

        self.music = Music()
        game_over = pygame.image.load('../graphics/ui/game_over.png').convert_alpha()
        self.game_over_surf = self.image = pygame.transform.scale(game_over, pygame.math.Vector2(game_over.get_size()) * 0.7)
        self.game_over_rect = self.game_over_surf.get_rect(center= (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 3))

    def Score_display(self):
        if self.active:
            self.score = (pygame.time.get_ticks() - self.start_offset) // 1000
            y = WINDOW_HEIGHT / 10
        else:
            y = WINDOW_HEIGHT / 2 + self.menu_rect.height - 80

        score_surf = self.font.render(str(self.score), False, 'black')
        score_rect = score_surf.get_rect(midtop = (WINDOW_WIDTH / 2, y))
        self.display_surface.blit(score_surf, score_rect)

    def Game_Over(self):
        over = pygame.mixer.Sound('../sounds/game_over.mp3')
        over.set_volume(0.1)
        over.play()
    def collisions(self):
        if pygame.sprite.spritecollide(self.player, self.collision_sprites, False, pygame.sprite.collide_mask)\
        or self.player.rect.top <= 0:
            self.music.Stop()
            self.Game_Over()
            for sprite in self.collision_sprites.sprites():
                if sprite.sprite_type == 'Obstacles':
                    sprite.kill()
            self.active = False
            self.player.kill()


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
                    self.beggining = False
                    if self.active:
                        self.player.jump()
                    else:
                        self.music.Play()
                        self.player = Player(self.all_sprites, self.scale_factor / 4.5)
                        self.active = True
                        self.start_offset = pygame.time.get_ticks()
                if event.type == self.obstacle_timer and self.active:
                    Obstacles([self.all_sprites, self.collision_sprites], self.scale_factor)
            # game logic

            self.display_surface.fill('white')
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.display_surface)
            self.Score_display()
            if self.active and self.beggining == False:
                self.collisions()
            else:
                if self.beggining:
                    self.display_surface.blit(self.title_surf, self.title_rect)
                else:
                    self.display_surface.blit(self.game_over_surf, self.game_over_rect)
                self.display_surface.blit(self.menu_surf,self.menu_rect)
            

            pygame.display.update()
            self.clock.tick(FRAMERATE)
        
        

if __name__ == '__main__':
    app = App()
    app.run()