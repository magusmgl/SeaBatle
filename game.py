# Внешняя логика игры
import random

from SeaBatle.sea_battle import Board, Ship, Dot


class Player():
    """Класс игрока в игру"""

    def __init__(self, own_board: object, enemy_board: object):
        self.own_board = own_board
        self.enemy_board = enemy_board

    @classmethod
    def ask(self):
        pass

    def move(self) -> bool:
        """Метод, который делает ход в игре"""
        res = None
        try:
            grid_coordinate = self.ask()
            res = self.enemy_board.shot(grid_coordinate)
        except Exception as e:
            print(e)
        return res == "hit"


class AI(Player):
    def ask(self):
        """Cпрашивает игрока, в какую клетку он делает выстрел"""
        return Dot(random.randint(0, 5), random.randint(0, 5))


class User(Player):
    def ask(self):
        """Выбор случайной точки на доске"""
        return Dot(map(int, input("Введите координаты клетки: ").split()))


class Game:
    """Класс игры"""
    SHIP_LENGTHS = [3, 2, 2, 1, 1, 1, 1]

    def __init__(self):
        self.user_board = self._random_board()
        self.ai_board = self._random_board()

        self.player_user = User(own_board=self.user_board, enemy_board=self.ai_board)
        self.player_ai = AI(own_board=self.ai_board, enemy_board=self.user_board)

    @classmethod
    def _random_board(self):
        """Метод генерирует случайную доску"""
        flag = True
        while flag:
            new_board = Board(list_of_ships=[], number_of_live_ships=7)
            for ship_length in self.SHIP_LENGTHS:
                for _ in range(1000):
                    try:
                        curr_ship = Ship(length=ship_length, start_dot=Dot(random.randint(0, 5), random.randint(0, 5)),
                                         direction=random.randint(0, 1),
                                         number_of_lives=ship_length)
                        new_board.add_ship(curr_ship)
                    except Exception:
                        continue
                    else:
                        new_board.list_of_ships.append(curr_ship)
                        break
            if len(new_board.list_of_ships) == 7:
                flag = False
        return new_board

    def greet(self):
        """Метод, который в консоли приветствует пользователя и рассказывает о формате ввода"""
        pass

    def loop(self):
        """Метод с самим игровым циклом"""
        pass

    def start(self):
        """Запуск игры"""
        self.greet()
        self.loop()


start = Game()

start.user_board.hid == True
start.user_board.display_board()
print()
start.ai_board.display_board()
