import pygame
from sys import exit
from random import randint, choice


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_surface1 = pygame.image.load('player ani/playerA.png').convert_alpha()
        player_surface2 = pygame.image.load('player ani/playerB.png').convert_alpha()
        self.player_walk = [player_surface1, player_surface2]
        self.player_index = 0
        self.player_jump = pygame.image.load('player ani/playerC.png').convert_alpha()
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(50, 325))
        self.gravity = 0
        self.jump_sound = pygame.mixer.Sound('pop_sound.mp3')
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 325:
            self.gravity = -20
            self.jump_sound.play()
        if keys[pygame.MOUSEBUTTONDOWN] and self.rect.bottom >= 325:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 325:
            self.rect.bottom = 325

    def animation_state(self):
        if self.rect.bottom < 325:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'fly':
            flypoo1 = pygame.image.load('poop/flypoop/flypoo1.png').convert_alpha()
            flypoo2 = pygame.image.load('poop/flypoop/flypoo2.png').convert_alpha()
            self.frames = [flypoo1, flypoo2]
            y_pos = 170
        else:
            poop_move1 = pygame.image.load('poop/dung original/dung1.png').convert_alpha()
            poop_move2 = pygame.image.load('poop/dung original/dung2.png').convert_alpha()
            poop_move3 = pygame.image.load('poop/dung original/dung3.png').convert_alpha()
            self.frames = [poop_move1, poop_move2, poop_move3]
            y_pos = 322

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

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
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'SCORE : {current_time}', False, (20, 20, 20))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):

        collide_Sound.play()
        obstacle_group.empty()
        return False
    else:
        return True


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Poopilicious')
clock = pygame.time.Clock()
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('bg_sound.mp3')
bg_music.set_volume(0.3)
bg_music.play(loops=-1)

collide_Sound = pygame.mixer.Sound('collision sound.mp3')

# GROUPS
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

# importing assets
test_font = pygame.font.Font('poopfont1.otf', 30)
score_font = pygame.font.Font('poopfont2.ttf', 30)

background_surface = pygame.image.load('bg3.png').convert_alpha()

text_surf = test_font.render('POOPilicious', False, 'white').convert_alpha()
text_rect = text_surf.get_rect(topleft=(0, 0))

# intro screen
# player_stand = pygame.image.load('poop/poop_idel/idelpoo1.png').convert_alpha()
# player_stand = pygame.transform.scale2x(player_stand)
# player_stand_rect = player_stand.get_rect(center=(400, 200))
p_sprite = [pygame.image.load('poop/poop_idel/idelpoo1.png').convert_alpha(),
            pygame.image.load('poop/poop_idel/idelpoo2.png').convert_alpha(),
            pygame.image.load('poop/poop_idel/idelpoo3.png').convert_alpha(),
            pygame.image.load('poop/poop_idel/idelpoo4.png').convert_alpha(),
            pygame.image.load('poop/poop_idel/idelpoo5.png').convert_alpha(),
            pygame.image.load('poop/poop_idel/idelpoo6.png').convert_alpha(),
            pygame.image.load('poop/poop_idel/idelpoo7.png').convert_alpha()]

pindex = 0
# if pindex >= len(p_sprite):
#     pindex = 0
p_surf = p_sprite[pindex]
p_rect = p_surf.get_rect(center=(400, 200))
screen.fill((94, 129, 162))
screen.blit(p_surf, p_rect)
# pindex += 1


# intro screen text
game_name = test_font.render('POOPilicious', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(400, 80))

game_message = test_font.render('press space to run', False, (20, 20, 20))
game_message_rect = game_message.get_rect(center=(400, 320))

# timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'poop', 'poop', 'poop'])))

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

    if game_active:
        screen.blit(background_surface, (0, 0))
        score = display_score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision_sprite()

    else:
        screen.fill((1, 169, 155))
        screen.blit(p_surf, p_rect)
        title_surf = pygame.image.load('heading.png').convert_alpha()
        game_name_rect = title_surf.get_rect(center=(400, 80))
        score_message = test_font.render(f'Your score : {score}', False, (20, 20, 20))
        score_message_rect = score_message.get_rect(center=(400, 300))
        screen.blit(title_surf, game_name_rect)

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)
