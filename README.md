# Snake - pygame

Учебный проект «Змейка»

## Установка

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Запуск игры (для человека)

```bash
python game.py
```

Управление:
- **Стрелки** - направление змейки
- **R** - рестарт после смерти
- **S** - сохранить скриншот в `results/screenshot.png`
- **Esc** - выход

## Посмотреть, как играет бот

```bash
python game.py random    # случайный бот
python game.py greedy    # жадный бот
python game.py astar     # бот с поиском пути A*
```

Стрелки в этом режиме отключены, но **R** (перезапуск), **S** (скриншот) и **Esc** (выход) работают. Скорость регулируется параметром `FPS` в начале файла `game.py`.

## Запуск симуляций

```bash
python simulate.py
```

Проводятся три эксперимента и сохраняются CSV в `results/`:
- `sim_size.csv` - жадный бот на полях 10×10…50×50, по 100 прогонов на каждый размер
- `sim_histogram.csv` - жадный бот на 20×15, 500 прогонов
- `sim_histogram_astar.csv` - A* бот на 20×15, 500 прогонов
- `sim_strategies.csv` - random / greedy / A* на 20×15, по 200 прогонов

## Построение графиков

```bash
python analyze.py
```

Читаем CSV и строим три PNG в `results/`:
- `plot_size.png` — зависимость длины от размера поля
- `plot_histogram.png` — распределение финальной длины
- `plot_strategies.png` — сравнение трех стратегий бота

## Файлы

| Файл | Что делает |
|------|------------|
| `snake_core.py` | Логика змейки: поле, движение, столкновения, еда |
| `game.py` | Сама игра |
| `bot.py` | Три стратегии: `random_bot`, `greedy_bot`, `astar_bot` |
| `simulate.py` | Прогон симуляций, запись CSV |
| `analyze.py` | Построение графиков из CSV |
| `report.md` | Отчет с описанием, графиками и выводами |
