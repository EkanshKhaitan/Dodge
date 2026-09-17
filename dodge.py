import pygame
import random

pygame.init()
pygame.font.init()

WIDTH = 1280
HEIGHT = 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
dt = 0
enemyvel = 600

font = pygame.font.Font('pirkkala.ttf', 50)
largefont = pygame.font.Font('pirkkala.ttf', 200)


player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
enemy1_pos = pygame.Vector2(random.randint(500, WIDTH - 40), random.randint(40, HEIGHT - 40))
enemy2_pos = pygame.Vector2(random.randint(500, WIDTH - 40), random.randint(40, HEIGHT - 40))
enemy3_pos = pygame.Vector2(random.randint(500, WIDTH - 40), random.randint(40, HEIGHT - 40))


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("purple")
    player_rect = pygame.Rect(player_pos.x - 40, player_pos.y - 40, 80, 80)

    if enemy1_pos.x <= 40:
        enemy1_pos = pygame.Vector2(random.randint(500, WIDTH - 40), random.randint(40, HEIGHT - 40))
    enemy1_pos.x -= enemyvel * dt
    enemy1_rect = pygame.Rect(enemy1_pos.x - 40, enemy1_pos.y - 40, 80, 80)

    if enemy2_pos.x <= 40:
        enemy2_pos = pygame.Vector2(random.randint(500, WIDTH - 40), random.randint(40, HEIGHT - 40))
    enemy2_pos.x -= enemyvel * dt
    enemy2_rect = pygame.Rect(enemy2_pos.x - 40, enemy2_pos.y - 40, 80, 80)

    if enemy3_pos.x <= 40:
        enemy3_pos = pygame.Vector2(random.randint(500, WIDTH - 40), random.randint(40, HEIGHT - 40))
    enemy3_pos.x -= enemyvel * dt
    enemy3_rect = pygame.Rect(enemy3_pos.x - 40, enemy3_pos.y - 40, 80, 80)


    pygame.draw.circle(screen, 'green', enemy1_pos, 40)
    pygame.draw.circle(screen, 'green', enemy2_pos, 40)
    pygame.draw.circle(screen, 'green', enemy3_pos, 40)
    

    pygame.draw.circle(screen, "red", player_pos, 40)

    if enemy1_rect.colliderect(player_rect) or enemy2_rect.colliderect(player_rect) or enemy3_rect.colliderect(player_rect):
        enemyvel = 0
        screen.fill('black')
        lose_text = largefont.render(f'YOU LOST', True, 'red')
        screen.blit(lose_text , (WIDTH / 6, HEIGHT / 6))

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
    dt = clock.tick(60) / 1000

pygame.quit()