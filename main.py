from game import Game
from players import HumanPlayer, BotPlayer, MediumBotPlayer, HardBotPlayer

while True: # Запуск Игры
    if __name__ == "__main__":
        difficulty = int(input("Выберите сложность бота (1 - Легкий, 2 - Средний, 3 - Сложный): "))
        bot_class = [BotPlayer, MediumBotPlayer, HardBotPlayer][difficulty - 1]

        player_choice = input("Выберите режим (1 - Человек vs Бот, 2 - Бот vs Бот): ")
        player1 = bot_class("Бот 1") if player_choice == "2" else HumanPlayer("Игрок")
        player2 = bot_class("Бот 2")

        game = Game(player1, player2)
        game.start()

        replay = input("Хотите сыграть ещё раз? (y/n): ").strip().lower() # Повторная игра
        if replay != "y":
            print("Спасибо за игру! До встречи.")
            break

