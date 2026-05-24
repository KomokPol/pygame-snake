import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

RESULTS_DIR = "results"


def read_csv(path):
    file = open(path, "r", encoding="utf-8")
    reader = csv.reader(file)
    header = next(reader)
    rows = []
    for row in reader:
        rows.append(row)
    file.close()
    return header, rows


def plot_size():
    _, rows = read_csv(os.path.join(RESULTS_DIR, "sim_size.csv"))

    lengths_by_size = {}
    for row in rows:
        size = int(row[0])
        length = int(row[2])
        if size not in lengths_by_size:
            lengths_by_size[size] = []
        lengths_by_size[size].append(length)

    sizes = sorted(lengths_by_size.keys())
    areas = []
    means = []
    maxes = []
    for size in sizes:
        areas.append(size * size)
        means.append(np.mean(lengths_by_size[size]))
        maxes.append(np.max(lengths_by_size[size]))

    plt.figure(figsize=(8, 5))
    plt.plot(areas, means, marker="o", label="Средняя длина")
    plt.plot(areas, maxes, marker="s", label="Максимальная длина")
    plt.xlabel("Площадь поля (клеток)")
    plt.ylabel("Длина змейки в момент смерти")
    plt.title("Жадный бот: длина змейки в зависимости от размера поля")
    plt.grid(True, alpha=0.3)
    plt.legend()

    for i in range(len(sizes)):
        label = str(sizes[i]) + "x" + str(sizes[i])
        plt.annotate(label, (areas[i], means[i]),
                     textcoords="offset points", xytext=(5, 5), fontsize=8)

    out_path = os.path.join(RESULTS_DIR, "plot_size.png")
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close()
    print("Фотка сохранена", out_path)


def plot_histogram():
    _, rows_greedy = read_csv(os.path.join(RESULTS_DIR, "sim_histogram.csv"))
    _, rows_astar = read_csv(os.path.join(RESULTS_DIR, "sim_histogram_astar.csv"))

    greedy_lengths = [int(row[1]) for row in rows_greedy]
    astar_lengths = [int(row[1]) for row in rows_astar]

    greedy_mean = np.mean(greedy_lengths)
    astar_mean = np.mean(astar_lengths)

    plt.figure(figsize=(8, 5))
    plt.hist(greedy_lengths, bins=30, color="#5fa8d3", edgecolor="black",
             alpha=0.6, label="жадный (среднее = " + str(round(greedy_mean, 1)) + ")")
    plt.hist(astar_lengths, bins=30, color="#a8d3a8", edgecolor="black",
             alpha=0.6, label="A* (среднее = " + str(round(astar_mean, 1)) + ")")
    plt.axvline(greedy_mean, color="blue", linestyle="--")
    plt.axvline(astar_mean, color="green", linestyle="--")
    plt.xlabel("Финальная длина змейки")
    plt.ylabel("Количество прогонов")
    plt.title("Распределение финальной длины (поле 20x15, по 500 прогонов)")
    plt.grid(True, alpha=0.3)
    plt.legend()

    out_path = os.path.join(RESULTS_DIR, "plot_histogram.png")
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close()
    print("Фотка сохранена", out_path)


def plot_strategies():
    _, rows = read_csv(os.path.join(RESULTS_DIR, "sim_strategies.csv"))

    lengths_by_strategy = {"random": [], "greedy": [], "astar": []}
    for row in rows:
        name = row[0]
        length = int(row[2])
        lengths_by_strategy[name].append(length)

    russian_names = {"random": "Случайный", "greedy": "Жадный", "astar": "A*"}
    order = ["random", "greedy", "astar"]
    labels = []
    means = []
    for name in order:
        labels.append(russian_names[name])
        means.append(np.mean(lengths_by_strategy[name]))

    colors = ["#d3a8a8", "#a8d3a8", "#a8a8d3"]

    plt.figure(figsize=(8, 5))
    bars = plt.bar(labels, means, color=colors, edgecolor="black")
    for i in range(len(bars)):
        height = bars[i].get_height()
        plt.text(bars[i].get_x() + bars[i].get_width() / 2, height + 1,
                 str(round(means[i], 1)), ha="center", fontsize=11)
    plt.ylabel("Средняя финальная длина")
    plt.title("Сравнение стратегий на поле 20x15 (200 прогонов на стратегию)")
    plt.grid(True, axis="y", alpha=0.3)

    out_path = os.path.join(RESULTS_DIR, "plot_strategies.png")
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close()
    print("Фотка сохранена", out_path)


def main():
    plot_size()
    plot_histogram()
    plot_strategies()


if __name__ == "__main__":
    main()
