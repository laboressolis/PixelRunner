import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk1 = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
        player_walk2 = pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()
        self.player_walk = [player_walk1,player_walk2]
        self.player_index = 0
        self.player_jump = pygame.image.load("graphics/player/jump.png").convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.3)


    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()
        if keys[pygame.K_UP]:
            self.gravity = -20
            self.jump_sound.play()
        if keys[pygame.K_LEFT]:
            self.rect.x += 4
        if keys[pygame.K_RIGHT]:
            self.rect.x -= 4
        if keys[pygame.K_d]:
            self.rect.x += 4
        if keys[pygame.K_a]:
            self.rect.x -= 4
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]
    def bounding_box(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= 800:
            self.rect.right = 800
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()
        self.bounding_box()

class Obstacles(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        if type == 'fly':
            fly_frame_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_frame_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_frame_1,fly_frame_2]
            y_pos = 210
        else:
            snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_frame_1,snail_frame_2]
            y_pos = 300
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def display_score():
    current_time = int((pygame.time.get_ticks() / 1000) - start_time)
    score_surf = pixel_font.render(f'Score: {current_time}', False, (64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rect)
    return current_time

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False): 
        obstacle_group.empty()
        return False
    else: return True 

# def progression():
#     global obstacle_interval
#     current_time = int((pygame.time.get_ticks() / 1000) - start_time)
#     if current_time >= 10: obstacle_interval = 500
#     if current_time >= 20: obstacle_interval = 1500
#     if current_time >= 40: obstacle_interval = 1200
#     if current_time >= 60: obstacle_interval = 1000
#     if current_time >= 90: obstacle_interval = 850

    

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Runner')

clock = pygame.time.Clock()
pixel_font = pygame.font.Font('font/Pixeltype.ttf',50)
game_active = False
start_time = 0
score = 0

# Sprites
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

# Background
sky_surface = pygame.image.load('graphics/Sky.png').convert_alpha()
ground_surface = pygame.image.load('graphics/ground.png').convert_alpha()

# Music
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(.5)
bg_music.play(loops = -1)

# For end screen
player_stand = pygame.image.load("graphics/player/player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = pixel_font.render("Pixel Runner", False, (111,196,169))
game_name_rect = game_name.get_rect(center = (400,80))

game_message = pixel_font.render('Press Enter to Start', False,(111,196,169))
game_message_rect = game_message.get_rect(center = (400,330))

obstacle_timer = pygame.USEREVENT + 1
obstacle_interval = 1500
pygame.time.set_timer(obstacle_timer,obstacle_interval)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
        if game_active == False:
            if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)
        
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacles(choice(['fly','notfly','notfly','notfly'])))

    if game_active:
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))

        score = display_score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision_sprite()
        # progression()
    else:
        obstacle_interval = 1500
        screen.fill((94,129,162))

        screen.blit(game_name, game_name_rect)
        screen.blit(player_stand, player_stand_rect)

        score_message = pixel_font.render(f"Your score: {score}", False, (111,196,169))
        score_message_rect = score_message.get_rect(center = (400,330))

        if score == 0: screen.blit(game_message, game_message_rect)
        else: screen.blit(score_message,score_message_rect)
        
    pygame.display.update()
    clock.tick(60) 