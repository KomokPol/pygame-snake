import os
import sys
import pygame

from snake_core import Snake, UP, DOWN, LEFT, RIGHT
from bot import STRATEGIES

WIDTH = 20
HEIGHT = 15
CELL = 30
FPS = 7
START_LENGTH = 3
TOP_BAR = 40

BG_COLOR = (30, 30, 30)
GRID_COLOR = (45, 45, 45)
SNAKE_COLOR = (80, 200, 80)
HEAD_COLOR = (140, 230, 140)
FOOD_COLOR = (220, 70, 70)
TEXT_COLOR = (230, 230, 230)


def draw_grid(screen):
    for x in range(WIDTH):
        for y in range(HEIGHT):
            rect = pygame.Rect(x * CELL, TOP_BAR + y * CELL, CELL, CELL)
            pygame.draw.rect(screen, GRID_COLOR, rect, 1)


def draw_food(screen, food):
    if food is None:
        return
    fx, fy = food
    rect = pygame.Rect(fx * CELL + 3, TOP_BAR + fy * CELL + 3, CELL - 6, CELL - 6)
    pygame.draw.rect(screen, FOOD_COLOR, rect)


def draw_snake(screen, snake):
    for i in range(len(snake.body)):
        x, y = snake.body[i]
        if i == 0:
            color = HEAD_COLOR
        else:
            color = SNAKE_COLOR
        rect = pygame.Rect(x * CELL + 1, TOP_BAR + y * CELL + 1, CELL - 2, CELL - 2)
        pygame.draw.rect(screen, color, rect)


def draw_score(screen, snake, font):
    text = "Счет: " + str(snake.get_score()) + "   Шаги: " + str(snake.steps)
    image = font.render(text, True, TEXT_COLOR)
    screen.blit(image, (10, 8))


def draw_game_over(screen, snake, font):
    if snake.won:
        message = "Победа!"
    else:
        message = "Игра окончена"
    big_font = pygame.font.SysFont("arial", 56)
    big_image = big_font.render(message, True, TEXT_COLOR)
    hint_image = font.render("R: начать заново,  S: скриншот", True, TEXT_COLOR)

    center_x = WIDTH * CELL // 2
    center_y = TOP_BAR + HEIGHT * CELL // 2
    screen.blit(big_image, big_image.get_rect(center=(center_x, center_y - 20)))
    screen.blit(hint_image, hint_image.get_rect(center=(center_x, center_y + 30)))


def save_screenshot(screen):
    if not os.path.exists("results"):
        os.makedirs("results")
    path = "results/screenshot.png"
    pygame.image.save(screen, path)
    print("скриншот сохранен в", path)


def get_bot_function():
    if len(sys.argv) < 2:
        return None
    name = sys.argv[1]
    if name not in STRATEGIES:
        print("Неизвестная стратегия:", name)
        print("Можно выбрать только random, greedy, astar или без аргумента, чтобы сыграть самому")
        sys.exit(1)
    return STRATEGIES[name]


def main():
    bot_function = get_bot_function()

    pygame.init()
    screen = pygame.display.set_mode((WIDTH * CELL, TOP_BAR + HEIGHT * CELL))
    if bot_function is None:
        pygame.display.set_caption("Змейка")
    else:
        pygame.display.set_caption("Змейка - бот: " + sys.argv[1])
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 24)

    snake = Snake(WIDTH, HEIGHT, START_LENGTH)
    next_direction = snake.direction

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and bot_function is None:
                    next_direction = UP
                elif event.key == pygame.K_DOWN and bot_function is None:
                    next_direction = DOWN
                elif event.key == pygame.K_LEFT and bot_function is None:
                    next_direction = LEFT
                elif event.key == pygame.K_RIGHT and bot_function is None:
                    next_direction = RIGHT
                elif event.key == pygame.K_r:
                    snake = Snake(WIDTH, HEIGHT, START_LENGTH)
                    next_direction = snake.direction
                elif event.key == pygame.K_s:
                    save_screenshot(screen)
                elif event.key == pygame.K_ESCAPE:
                    running = False

        if snake.alive:
            if bot_function is not None:
                next_direction = bot_function(snake)
            snake.step(next_direction)

        screen.fill(BG_COLOR)
        draw_grid(screen)
        draw_food(screen, snake.food)
        draw_snake(screen, snake)
        draw_score(screen, snake, font)
        if not snake.alive:
            draw_game_over(screen, snake, font)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
