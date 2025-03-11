from database import session, GameResult
import time

class Game:
    def __init__(self, player1, player2):
        self.players = [player1, player2]

    # Запуск игры
    def start(self):
        turn = 0
        while True:
            current_player = self.players[turn % 2]
            enemy = self.players[(turn + 1) % 2]
            print(f"\nХод игрока: {current_player.name}")
            enemy.board.display()
            result = current_player.make_move(enemy)
            if enemy.board.all_ships_sunk():
                print(f"\n{current_player.name} победил!")
                self.save_result(current_player.name, turn + 1)
                break
            if result == "miss":
                turn += 1

            time.sleep(1)
            input("\nClick Enter to continue...")

    # Сохранение результата игры в базу данных
    def save_result(self, winner, moves):
        game_result = GameResult(winner=winner, moves=moves)
        session.add(game_result)
        session.commit()
        print("Saved to DB")
