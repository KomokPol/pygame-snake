import heapq
import random

from snake_core import ALL_DIRECTIONS


def is_cell_safe(snake, cell):
    x, y = cell
    if x < 0 or x >= snake.width:
        return False
    if y < 0 or y >= snake.height:
        return False
    body_without_tail = snake.body[:-1]
    if cell in body_without_tail:
        return False
    return True


def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def random_bot(snake):
    safe_directions = []
    for direction in ALL_DIRECTIONS:
        head_x, head_y = snake.body[0]
        next_cell = (head_x + direction[0], head_y + direction[1])
        if is_cell_safe(snake, next_cell):
            safe_directions.append(direction)

    if len(safe_directions) == 0:
        return snake.direction
    return random.choice(safe_directions)


def greedy_bot(snake):
    head_x, head_y = snake.body[0]
    food = snake.food

    best_direction = None
    best_distance = None

    for direction in ALL_DIRECTIONS:
        next_cell = (head_x + direction[0], head_y + direction[1])
        if not is_cell_safe(snake, next_cell):
            continue

        if food is None:
            distance = 0
        else:
            distance = manhattan_distance(next_cell, food)

        if best_direction is None or distance < best_distance:
            best_direction = direction
            best_distance = distance

    if best_direction is None:
        return snake.direction
    return best_direction


def find_path_astar(snake, start, goal):
    width = snake.width
    height = snake.height
    blocked = set(snake.body[:-1])

    open_set = []
    heapq.heappush(open_set, (manhattan_distance(start, goal), 0, start))

    came_from = {start: None}
    cost_so_far = {start: 0}

    while len(open_set) > 0:
        priority, cost, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        for direction in ALL_DIRECTIONS:
            nx = current[0] + direction[0]
            ny = current[1] + direction[1]
            if nx < 0 or nx >= width or ny < 0 or ny >= height:
                continue
            neighbor = (nx, ny)
            if neighbor in blocked and neighbor != goal:
                continue

            new_cost = cost + 1
            old_cost = cost_so_far.get(neighbor)
            if old_cost is None or new_cost < old_cost:
                cost_so_far[neighbor] = new_cost
                came_from[neighbor] = current
                priority = new_cost + manhattan_distance(neighbor, goal)
                heapq.heappush(open_set, (priority, new_cost, neighbor))

    return None


def astar_bot(snake):
    if snake.food is None:
        return greedy_bot(snake)

    head = snake.body[0]
    path = find_path_astar(snake, head, snake.food)

    if path is None or len(path) < 2:
        return greedy_bot(snake)

    next_cell = path[1]
    dx = next_cell[0] - head[0]
    dy = next_cell[1] - head[1]
    return (dx, dy)

