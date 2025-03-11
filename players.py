import random
from board import Board

class Player: #Родительский класс Player
    def __init__(self, name):
        self.name = name
        self.board = Board()
        self.enemy_board = Board()
        self.board.auto_place_ships()

    def make_move(self, enemy):
        raise NotImplementedError

class HumanPlayer(Player): #Класс для игрок-человек
    def __init__(self, name):
        super().__init__(name)
        self.shots_made = set()
        self.place_ship_choice()

    def place_ship_choice(self):
        choice = input("Хотите расставить корабли вручную? (y/n): ").strip().lower()
        if choice == "y":
            self.board.place_ships_manually()
        else:
            self.board.auto_place_ships()

    def make_move(self, enemy):
        while True:
            try:
                coords = input(f"{self.name}, ваш ход (формат 'x y'): ").split()
                x, y = map(int, coords)
                if not (0 <= x < Board.SIZE and 0 <= y < Board.SIZE):
                    print("Координаты вне поля.")
                    continue
                if (x, y) in self.shots_made:
                    print("Вы уже стреляли в эту клетку. Попробуйте снова.")
                    continue

                self.shots_made.add((x, y))
                hit = enemy.board.receive_shot(x, y)
                result = enemy.board.shots[(x, y)]
                if result == "hit":
                    print("Попадание!")
                elif result == "sink":
                    print("Корабль потоплен!")
                else:
                    print("Мимо!")
                break
            except ValueError:
                print("Некорректный ввод.")

class BotPlayer(Player): #Класс для ботов
    def __init__(self, name):
        super().__init__(name)
        self.possible_shots = [(x, y) for x in range(Board.SIZE) for y in range(Board.SIZE)]
        random.shuffle(self.possible_shots)

    def make_move(self, enemy):
        print(f"{self.name} делает ход...")
        x, y = self.possible_shots.pop()
        enemy.board.receive_shot(x, y)

        # Выводим обновленное поле противника
        enemy.board.display()
        result = enemy.board.shots[(x, y)]

        # Выводим результат хода
        print(f"{self.name}: Выстрел в ({x}, {y}) – {result}")
        print('------------------------')


class MediumBotPlayer(BotPlayer): #Средний бот
    def __init__(self, name):
        super().__init__(name)
        self.hit_cells = []  # Очередь для добивания

    def make_move(self, enemy):
        print(f"{self.name} делает ход...")

        while True:
            if self.hit_cells:
                x, y = self.hit_cells.pop(0)  # Очередь для добивания Первый - Последний
            else:
                x, y = self.possible_shots.pop(0)

            # Если уже стреляли по этим координатам, пропускаем их
            if (x, y) in enemy.board.shots:
                continue

            enemy.board.receive_shot(x, y)
            result = enemy.board.shots[(x, y)]

            print(f"{self.name}: Выстрел в ({x}, {y}) – {result}")
            print('------------------------')


            if result == "hit":
                self.hit_cells.extend([
                    (x + dx, y + dy)
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                    if 0 <= x + dx < Board.SIZE and 0 <= y + dy < Board.SIZE
                       and (x + dx, y + dy) not in enemy.board.shots  # Не стреляем в уже обстрелянные
                ])
            elif result == "sink":
                self.hit_cells.clear()  # Если потопил – очистить список

            # Если все корабли потоплены, выход из цикла
            if enemy.board.all_ships_sunk():
                print(f"{self.name} победил!")
                break

            return  # Завершение хода


class HardBotPlayer(MediumBotPlayer): #Хард бот (Умеет все)
    def __init__(self, name):
        super().__init__(name)
        self.invalid_shots = set()  # Клетки, куда стрелять бессмысленно

    def mark_invalid_shots(self, x, y, enemy): # клетки вокруг потопленного корабля как бесполезные для стрельбы
        already_marked = set()
        for ship in enemy.board.ships:
            if ship.is_sunk() and tuple(ship.coordinates) not in already_marked:
                for sx, sy in ship.coordinates:
                    for dx in range(-1, 2):
                         for dy in range(-1, 2):
                            nx, ny = sx + dx, sy + dy
                            if 0 <= nx < Board.SIZE and 0 <= ny < Board.SIZE:
                                self.invalid_shots.add((nx, ny))
                            already_marked.add(tuple(ship.coordinates))

    def make_move(self, enemy):
        print(f"{self.name} делает ход (сложный бот)...")

        while True:
            if self.hit_cells:
                x, y = self.hit_cells.pop(0)  # Очередь для добивания Первый - Последний
            else:
                self.possible_shots = [shot for shot in self.possible_shots if shot not in self.invalid_shots]
                x, y = self.possible_shots.pop(0)

            if (x, y) in enemy.board.shots:
                continue  # Пропуск уже обстрелянных клеток

            enemy.board.receive_shot(x, y)
            result = enemy.board.shots[(x, y)]

            print(f"{self.name}: Выстрел в ({x}, {y}) – {result}")
            print('------------------------')

            if result == "hit":
                # Добавляет только те клетки, по которым еще не стреляли
                self.hit_cells.extend([
                    (x + dx, y + dy)
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                    if 0 <= x + dx < Board.SIZE and 0 <= y + dy < Board.SIZE
                       and (x + dx, y + dy) not in enemy.board.shots
                       and (x + dx, y + dy) not in self.invalid_shots
                ])
            elif result == "sink":
                self.mark_invalid_shots(x, y, enemy)
                self.hit_cells.clear()

            if enemy.board.all_ships_sunk():
                print(f"{self.name} победил!")
                break

            return




