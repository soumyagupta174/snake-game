import pygame
import random
from collections import deque

# Initialize pygame
pygame.init()

# Screen dimensions and settings
GRID_SIZE = 25
TILE_SIZE = 20
SCREEN_SIZE = GRID_SIZE * TILE_SIZE

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)
WHITE = (255, 255, 255)

# Directions
DIRECTIONS = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0)
}

# Initialize screen
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Advanced Snake Game")

# Clock for controlling frame rate
clock = pygame.time.Clock()
FPS = 10

# Snake and game state initialization
snake = [(random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))]
direction = "UP"
apple = None
apple_color = None

# Function to generate a random apple

def generate_apple():
    while True:
        pos = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
        if pos not in snake:
            color = random.choice([BROWN, BLUE, RED])
            return pos, color

# BFS algorithm for pathfinding

def bfs_path(start, goal):
    queue = deque([(start, [])])
    visited = set()
    while queue:
        (x, y), path = queue.popleft()
        if (x, y) == goal:
            return path
        if (x, y) in visited:
            continue
        visited.add((x, y))
        for dx, dy in DIRECTIONS.values():
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and (nx, ny) not in snake:
                queue.append(((nx, ny), path + [(dx, dy)]))
    return []

# Game loop
running = True
apple, apple_color = generate_apple()
while running:
    screen.fill(BLACK)

    # Draw grid
    for x in range(0, SCREEN_SIZE, TILE_SIZE):
        pygame.draw.line(screen, WHITE, (x, 0), (x, SCREEN_SIZE))
    for y in range(0, SCREEN_SIZE, TILE_SIZE):
        pygame.draw.line(screen, WHITE, (0, y), (SCREEN_SIZE, y))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Find path to apple using BFS
    if apple:
        path = bfs_path(snake[0], apple)
        if path:
            dx, dy = path[0]
            direction = [key for key, value in DIRECTIONS.items() if value == (dx, dy)][0]

    # Move the snake
    dx, dy = DIRECTIONS[direction]
    new_head = (snake[0][0] + dx, snake[0][1] + dy)

    # Check game over conditions
    if (
        new_head in snake
        or not (0 <= new_head[0] < GRID_SIZE)
        or not (0 <= new_head[1] < GRID_SIZE)
    ):
        running = False

    snake.insert(0, new_head)

    # Check if snake eats the apple
    if new_head == apple:
        if apple_color == BROWN:
            snake = snake[: len(snake) // 2]
        elif apple_color == BLUE:
            snake.extend(snake[-1:] * len(snake))
        elif apple_color == RED:
            running = False
        apple, apple_color = generate_apple()
    else:
        snake.pop()

    # Draw apple
    pygame.draw.rect(
        screen, apple_color, (apple[0] * TILE_SIZE, apple[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    )

    # Draw snake
    for segment in snake:
        pygame.draw.rect(
            screen, GREEN, (segment[0] * TILE_SIZE, segment[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        )

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(FPS)

pygame.quit()