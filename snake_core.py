import random

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

ALL_DIRECTIONS = [UP, DOWN, LEFT, RIGHT]


class Snake:
    def __init__(self, width, height, start_length=3):
        self.width = width
        self.height = height

        center_x = width // 2
        center_y = height // 2
        self.body = []
        for i in range(start_length):
            self.body.append((center_x - i, center_y))

        self.direction = RIGHT
        self.alive = True
        self.won = False
        self.steps = 0
        self.food = None
        self.place_food()

    def get_score(self):
        return len(self.body)

    def get_head(self):
        return self.body[0]

    def place_food(self):
        empty_cells = []
        for x in range(self.width):
            for y in range(self.height):
                if (x, y) not in self.body:
                    empty_cells.append((x, y))

        if len(empty_cells) == 0:
            self.food = None
            self.won = True
            self.alive = False
            return

        self.food = random.choice(empty_cells)

    def step(self, new_direction=None):
        if not self.alive:
            return

        if new_direction is not None:
            old_dx, old_dy = self.direction
            new_dx, new_dy = new_direction
            is_reverse = (new_dx == -old_dx and new_dy == -old_dy)
            if not is_reverse:
                self.direction = new_direction

        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        nx, ny = new_head
        if nx < 0 or nx >= self.width or ny < 0 or ny >= self.height:
            self.alive = False
            self.steps += 1
            return

        will_eat = (new_head == self.food)

        if will_eat:
            body_without_tail = self.body
        else:
            body_without_tail = self.body[:-1]

        if new_head in body_without_tail:
            self.alive = False
            self.steps += 1
            return

        self.body.insert(0, new_head)
        if will_eat:
            self.place_food()
        else:
            self.body.pop()

        self.steps += 1


if __name__ == "__main__":
    random.seed(0)
    snake = Snake(10, 10)
    print("start body:", snake.body)
    print("food:", snake.food)
    for i in range(5):
        snake.step()
        print("step", i + 1, "body:", snake.body, "alive:", snake.alive)
