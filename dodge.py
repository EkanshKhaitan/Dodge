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

# IMAGES

play_again = pygame.image.load('assets/playagain.png').convert_alpha()
play_again = pygame.transform.smoothscale(play_again, (400, 200))

# Sounds

pop = pygame.mixer.Sound('assets/pop.mp3')

# CLASSES

class Enemy:
    def __init__(self):
        self.reset()

    def tick(self, screen, dt):
        self.pos.x -= self.velocity * dt
        pygame.draw.circle(screen, 'red', self.pos, 40)
        pygame.draw.circle(screen, 'white', self.pos, 40, width=3)
        if self.pos.x <= 40:
            pop.play()
            self.reset()


    def reset(self):
        self.pos = pygame.Vector2(random.randint(WIDTH - 200, WIDTH - 40), random.randint(40, HEIGHT - 40))
        
        self.velocity = random.randint(600, 1400)


    def get_rect(self):
        return pygame.Rect(self.pos.x - 40, self.pos.y - 40, 80, 80)




font = pygame.font.Font('assets/pirkkala.ttf', 50)
largefont = pygame.font.Font('assets/pirkkala.ttf', 200)


player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

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

    timer += dt


    
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

        if playagain_rect.colliderect(mouse_rect):
            if any(pygame.mouse.get_pressed()):
                timer = 0
                enemy1.reset()
                enemy2.reset()
                enemy3.reset()

    else:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player_pos.y -= 300 * dt
        if keys[pygame.K_s]:
            player_pos.y += 300 * dt
        if keys[pygame.K_a]:
            player_pos.x -= 300 * dt
        if keys[pygame.K_d]:
            player_pos.x += 300 * dt

    if player_pos.x <= 40:
        player_pos.x = 40
    if player_pos.x >= 300:
        player_pos.x = 300
    if player_pos.y >= HEIGHT - 40:
        player_pos.y = HEIGHT - 40
    if player_pos.y <= 40:
        player_pos.y = 40

    pygame.display.flip()
    dt = clock.tick(120) / 1000

pygame.quit()