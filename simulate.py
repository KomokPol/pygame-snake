import csv
import os
import random

from snake_core import Snake
from bot import STRATEGIES

RESULTS_DIR = "results"


def run_one_game(bot_function, width, height, seed):
    random.seed(seed)
    snake = Snake(width, height, start_length=3)
    max_steps = 20000
    while snake.alive and snake.steps < max_steps:
        direction = bot_function(snake)
        snake.step(direction)
    return snake.get_score(), snake.steps


def save_csv(path, rows, column_names):
    file = open(path, "w", newline="", encoding="utf-8")
    writer = csv.writer(file)
    writer.writerow(column_names)
    for row in rows:
        writer.writerow(row)
    file.close()
    print("Файл готов", path)


def experiment_size():
    print()
    print("Эксперимент 1: влияние размера поля на жадного бота")
    sizes = [10, 20, 30, 40, 50]
    runs_per_size = 100
    bot_function = STRATEGIES["greedy"]
    rows = []

    for size in sizes:
        print("поле", str(size) + "x" + str(size) + "...", end=" ", flush=True)
        for run_id in range(1, runs_per_size + 1):
            seed = 420000 + size * 1000 + run_id
            length, steps = run_one_game(bot_function, size, size, seed)
            rows.append([size, run_id, length, steps])
        print("готово")

    save_csv(
        os.path.join(RESULTS_DIR, "sim_size.csv"),
        rows,
        ["size", "run_id", "length", "steps"],
    )


def experiment_histogram():
    print()
    print("Эксперимент 2: распределение финальной длины жадного бота (поле 20x15)")
    runs = 500
    bot_function = STRATEGIES["greedy"]
    rows = []

    for run_id in range(1, runs + 1):
        seed = 10000 + run_id
        length, steps = run_one_game(bot_function, 20, 15, seed)
        rows.append([run_id, length, steps])

    save_csv(
        os.path.join(RESULTS_DIR, "sim_histogram.csv"),
        rows,
        ["run_id", "length", "steps"],
    )


def experiment_histogram_astar():
    print()
    print("Эксперимент 2b: распределение финальной длины бота A* (поле 20x15)")
    runs = 500
    bot_function = STRATEGIES["astar"]
    rows = []

    for run_id in range(1, runs + 1):
        seed = 30000 + run_id
        length, steps = run_one_game(bot_function, 20, 15, seed)
        rows.append([run_id, length, steps])

    save_csv(
        os.path.join(RESULTS_DIR, "sim_histogram_astar.csv"),
        rows,
        ["run_id", "length", "steps"],
    )


def experiment_strategies():
    print()
    print("Эксперимент 3: сравнение стратегий (поле 20x15)")
    strategy_names = ["random", "greedy", "astar"]
    runs_per_strategy = 200
    rows = []

    for name in strategy_names:
        bot_function = STRATEGIES[name]
        print(name + "...", end=" ", flush=True)
        for run_id in range(1, runs_per_strategy + 1):
            seed = 20000 + run_id
            length, steps = run_one_game(bot_function, 20, 15, seed)
            rows.append([name, run_id, length, steps])
        print("готово")

    save_csv(
        os.path.join(RESULTS_DIR, "sim_strategies.csv"),
        rows,
        ["strategy", "run_id", "length", "steps"],
    )


def main():
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)

    experiment_size()
    experiment_histogram()
    experiment_histogram_astar()
    experiment_strategies()

    print()
    print("Симуляции завершены. Запустите analyze.py для построения графиков")


if __name__ == "__main__":
    main()
