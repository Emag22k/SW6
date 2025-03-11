import random

class Ship:
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.hits = set()

    def is_hit(self, shot):
        if shot in self.coordinates:
            self.hits.add(shot)
            return True
        return False

    def is_sunk(self):
        return set(self.coordinates) == self.hits

class Board:
    SIZE = 10 # Размер поля (При желании можно увеличить)

    def __init__(self):
        self.ships = []
        self.shots = {}

    def place_ships_manually(self):
        """ Позволяет игроку вручную расставить корабли. """
        self.ships.clear()
        ship_sizes = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]  # Размеры кораблей

        print("\nРучная расстановка кораблей.")
        self.display(show_ships=True)

        for size in ship_sizes:
            while True:
                try:
                    print(f"\nРазместите корабль размером {size} клеток.")
                    x, y = map(int, input("Введите начальные координаты (x y): ").split())
                    direction = input("Введите направление (H - горизонтально, V - вертикально): ").strip().upper()

                    # Список координат для корабля
                    if direction == "H":
                        ship_cells = [(x + i, y) for i in range(size)]
                    elif direction == "V":
                        ship_cells = [(x, y + i) for i in range(size)]
                    else:
                        print("Некорректное направление! Используйте 'H' или 'V'.")
                        continue

                    # Можно ли разместить корабль
                    ship = Ship(ship_cells)
                    if len(ship_cells) == size and self.can_place_ship(ship):
                        self.place_ship(ship)
                        self.display(show_ships=True)  # Показываем поле после каждого добавления
                        break
                    else:
                        print("Ошибка: корабль выходит за границы или пересекается с другим!")
                except ValueError:
                    print("Некорректный ввод. Введите координаты заново.")

    def auto_place_ships(self):
        self.ships.clear()
        ship_sizes = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        for size in ship_sizes:
            self.place_ship_correctly(size)

    def can_place_ship(self, ship):
        for x, y in ship.coordinates:
            if not (0 <= x < self.SIZE and 0 <= y < self.SIZE):
                return False
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    if (x + dx, y + dy) in [cell for s in self.ships for cell in s.coordinates]:
                        return False
        return True

    def place_ship(self, ship):
        self.ships.append(ship)

    def place_ship_correctly(self, size):
        attempts = 100
        while attempts > 0:
            x = random.randint(0, self.SIZE - 1)
            y = random.randint(0, self.SIZE - 1)
            direction = random.choice(["H", "V"])

            if direction == "H":
                ship_cells = [(x + i, y) for i in range(size) if x + i < self.SIZE]
            else:
                ship_cells = [(x, y + i) for i in range(size) if y + i < self.SIZE]

            if len(ship_cells) == size:
                ship = Ship(ship_cells)
                if self.can_place_ship(ship):
                    self.place_ship(ship)
                    return
            attempts -= 1

        self.ships.clear()
        self.auto_place_ships()

    def receive_shot(self, x, y):
        for ship in self.ships:
            if ship.is_hit((x, y)):
                self.shots[(x, y)] = "hit" if not ship.is_sunk() else "sink"
                return True
        self.shots[(x, y)] = "miss"
        return False

    def all_ships_sunk(self):
        return all(ship.is_sunk() for ship in self.ships)

    def display(self, show_ships=True):
        """ Отображает поле в консоли """
        print("  " + "  ".join(str(i) for i in range(self.SIZE)))
        for y in range(self.SIZE):
            row = []
            for x in range(self.SIZE):
                if (x, y) in self.shots:
                    row.append("X" if self.shots[(x, y)] == "hit" else "#" if self.shots[(x, y)] == "sink" else "o")
                elif show_ships and any((x, y) in ship.coordinates for ship in self.ships):
                    row.append("■")
                else:
                    row.append(".")
            print(f"{y} " + "  ".join(row))
