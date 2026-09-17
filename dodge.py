import pygame
import random

pygame.init()
pygame.font.init()
pygame.mixer.init()

WIDTH = 1280
HEIGHT = 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

# GAME VARIABLES

dt = 0
enemyvel = 500 
timer = 0
speedpwup_rect = 0
powerup_active_for = 0

# IMAGES

play_again = pygame.image.load('assets/playagain.png').convert_alpha()
play_again = pygame.transform.smoothscale(play_again, (400, 200))
speedpwup = pygame.image.load('assets/2xscore.png').convert_alpha()
speedpwup = pygame.transform.smoothscale(speedpwup, (100, 100))

# Sounds

pop = pygame.mixer.Sound('assets/pop.mp3')

pygame.mixer_music.load('assets/subway.mp3')
pygame.mixer_music.set_volume(0.5)
pygame.mixer_music.play(-1)

# CLASSES

class Enemy:
    def __init__(self):
        self.reset()
        self.just_reset = False

    def tick(self, screen, dt):
        self.just_reset = False
        self.pos.x -= self.velocity * dt
        pygame.draw.circle(screen, 'red', self.pos, 40)
        pygame.draw.circle(screen, 'white', self.pos, 40, width=3)
        if self.pos.x <= 40:
            pop.play()
            self.reset()
            self.just_reset = True

    def reset(self):
        self.pos = pygame.Vector2(random.randint(WIDTH - 200, WIDTH - 40), random.randint(40, HEIGHT - 40))
        
        self.velocity = random.randint(600, 1400)


    def get_rect(self):
        return pygame.Rect(self.pos.x - 40, self.pos.y - 40, 80, 80)

class PowerUp:
    def __init__(self, active=True):
        self.active = active
        self.reset()

    def tick(self, screen, dt):
        if not self.active:
            return
        self.pos.x -= self.velocity * dt
        screen.blit(speedpwup, self.pos)
        if self.pos.x <= 40:
            self.active = False
            pop.play()

    def reset(self):
        self.pos = pygame.Vector2(WIDTH - 40, random.randint(40, HEIGHT-40))
        self.velocity = random.randint(600, 1400)


    def get_rect(self):
        return pygame.Rect(self.pos.x - 40, self.pos.y - 40, 80, 80)




font = pygame.font.Font('assets/pirkkala.ttf', 50)
largefont = pygame.font.Font('assets/pirkkala.ttf', 200)

blit_speed = False

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

powerup = PowerUp(active=False)

enemy1 = Enemy()
enemy2 = Enemy()
enemy3 = Enemy()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")
    player_rect = pygame.Rect(player_pos.x - 40, player_pos.y - 40, 80, 80)
    mouse_rect = pygame.Rect((pygame.mouse.get_pos()), (1, 1))

    enemy1.tick(screen, dt)
    enemy2.tick(screen, dt)
    enemy3.tick(screen, dt)

    if enemy1.just_reset or enemy2.just_reset or enemy3.just_reset:
        pw_chance = random.randint(1, 5)
        if pw_chance == 1:
            if not powerup.active and powerup_active_for is None:
                powerup.active = True
                powerup.reset()

    powerup.tick(screen, dt)

    
    pygame.draw.circle(screen, "green", player_pos, 40)

    timer_text = font.render(f'Time Survived: {round(timer, 2)}', True, 'white')
    screen.blit(timer_text, (50, 50))

    if enemy1.get_rect().colliderect(player_rect) or enemy2.get_rect().colliderect(player_rect) or enemy3.get_rect().colliderect(player_rect):
        enemy1.velocity = 0
        enemy2.velocity = 0
        enemy3.velocity = 0
        screen.fill('black')
        lose_text = largefont.render(f'YOU LOST', True, 'red')
        screen.blit(lose_text , (WIDTH / 5, HEIGHT / 6))

        playagain_rect = pygame.Rect(WIDTH / 1.5, HEIGHT / 1.5, 200, 400)
        screen.blit(play_again, (WIDTH / 1.5, HEIGHT / 1.5))

        lose_time_text = font.render(f'Time Survived: {round(timer, 2)}', True, 'white')
        screen.blit(lose_time_text, (WIDTH / 5, HEIGHT / 2))

        if playagain_rect.colliderect(mouse_rect):
            if any(pygame.mouse.get_pressed()):
                timer = 0
                enemy1.reset()
                enemy2.reset()
                enemy3.reset()

    else:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player_pos.y -= 500 * dt
        if keys[pygame.K_s]:
            player_pos.y += 500 * dt
        if keys[pygame.K_a]:
            player_pos.x -= 500 * dt
        if keys[pygame.K_d]:
            player_pos.x += 500 * dt

        timer += dt

    if player_pos.x <= 40:
        player_pos.x = 40
    if player_pos.x >= 300:
        player_pos.x = 300
    if player_pos.y >= HEIGHT - 40:
        player_pos.y = HEIGHT - 40
    if player_pos.y <= 40:
        player_pos.y = 40

    if powerup.get_rect().colliderect(player_rect) and powerup.active:
        print("PUP!!!")
        powerup.active = False
        powerup_active_for = 5
        enemyvel = enemyvel / 1.5
        enemy1.velocity = enemyvel
        enemy2.velocity = enemyvel
        enemy3.velocity = enemyvel

    if powerup_active_for is not None:
        if powerup_active_for > 0:
            powerup_active_for -= dt
        else:
            powerup_active_for = None
            enemyvel = enemyvel * 1.5
            enemy1.velocity = enemyvel
            enemy2.velocity = enemyvel
            enemy3.velocity = enemyvel

    pygame.display.flip()
    dt = clock.tick(120) / 1000

pygame.quit()