import pygame
import os
from collections import deque

pygame.init()
pygame.font.init()

# Game Setup
WIDTH, HEIGHT = 900, 500
GRID_SIZE = 50
ROWS, COLS = HEIGHT // GRID_SIZE, WIDTH // GRID_SIZE
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spaceship AI with BFS + Bullets")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Assets
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 40, 40
YELLOW_SPACESHIP = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "spaceship_yellow.png")), (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
RED_SPACESHIP = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "spaceship_red.png")), (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
BG = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "space.png")), (WIDTH, HEIGHT))

# Fonts
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 80)

# Constants
FPS = 60
PLAYER_VEL = 5
BULLET_VEL = 7
AI_MOVE_INTERVAL = 500  # milliseconds
MAX_BULLETS = 5

def draw_window(player, ai, bullets, ai_health):
    WIN.blit(BG, (0, 0))
    WIN.blit(YELLOW_SPACESHIP, (player.x, player.y))
    WIN.blit(RED_SPACESHIP, (ai.x, ai.y))

    for bullet in bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    ai_health_text = HEALTH_FONT.render(f"AI Health: {ai_health}", 1, WHITE)
    WIN.blit(ai_health_text, (WIDTH - ai_health_text.get_width() - 10, 10))

    pygame.display.update()

def player_movement(keys, player):
    if keys[pygame.K_a] and player.x - PLAYER_VEL > 0:
        player.x -= PLAYER_VEL
    if keys[pygame.K_d] and player.x + PLAYER_VEL + player.width < WIDTH:
        player.x += PLAYER_VEL
    if keys[pygame.K_w] and player.y - PLAYER_VEL > 0:
        player.y -= PLAYER_VEL
    if keys[pygame.K_s] and player.y + PLAYER_VEL + player.height < HEIGHT:
        player.y += PLAYER_VEL

def bfs(start, goal):
    queue = deque()
    queue.append((start, [start]))
    visited = set()
    visited.add(start)

    while queue:
        (x, y), path = queue.popleft()
        if (x, y) == goal:
            return path

        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < COLS and 0 <= ny < ROWS and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append(((nx, ny), path + [(nx, ny)]))

    return []

def move_ai(ai, player):
    ai_grid = (ai.x // GRID_SIZE, ai.y // GRID_SIZE)
    player_grid = (player.x // GRID_SIZE, player.y // GRID_SIZE)
    path = bfs(ai_grid, player_grid)
    if len(path) > 1:
        next_cell = path[1]
        ai.x = next_cell[0] * GRID_SIZE
        ai.y = next_cell[1] * GRID_SIZE

def handle_bullets(bullets, ai):
    for bullet in bullets[:]:
        bullet.x += BULLET_VEL
        if ai.colliderect(bullet):
            bullets.remove(bullet)
            return True  # AI got hit
        elif bullet.x > WIDTH:
            bullets.remove(bullet)
    return False

def draw_winner(text):
    winner_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2,
                           HEIGHT // 2 - winner_text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(3000)

def main():
    clock = pygame.time.Clock()
    player = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    ai = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    ai_health = 5

    bullets = []
    ai_timer = pygame.time.get_ticks()

    run = True
    while run:
        clock.tick(FPS)
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_LCTRL:
                if len(bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(player.x + player.width, player.y + player.height // 2 - 2, 10, 5)
                    bullets.append(bullet)

        keys = pygame.key.get_pressed()
        player_movement(keys, player)

        if current_time - ai_timer >= AI_MOVE_INTERVAL:
            move_ai(ai, player)
            ai_timer = current_time

        if handle_bullets(bullets, ai):
            ai_health -= 1

        if ai_health <= 0:
            draw_winner("You Win!")
            break

        draw_window(player, ai, bullets, ai_health)

    pygame.quit()

if __name__ == "__main__":
    main()
