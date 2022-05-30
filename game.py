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
        return res


class AI(Player):
    def ask(self):
        """Cпрашивает игрока, в какую клетку он делает выстрел"""
        return Dot(random.randint(0, 5), random.randint(0, 5))


class User(Player):
    def ask(self):
        """Выбор случайной точки на доске"""
        x, y = list(map(int, input("Введите координаты клетки: ").split()))
        return Dot(x, y)


class Game:
    """Класс игры"""
    SHIP_LENGTHS = [3]

    # SHIP_LENGTHS = [3, 2, 2, 1, 1, 1, 1]

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
            new_board = Board(list_of_ships=[], number_of_live_ships=len(self.SHIP_LENGTHS))
            for ship_length in self.SHIP_LENGTHS:
                for _ in range(1000):
                    try:
                        curr_ship = Ship(length=ship_length, start_dot=Dot(random.randint(0, 5), random.randint(0, 5)),
                                         direction=random.choice(["v", "h"]),
                                         health=ship_length)
                        new_board.add_ship(curr_ship)
                    except Exception:
                        continue
                    else:
                        new_board.list_of_ships.append(curr_ship)
                        break
            if len(new_board.list_of_ships) == len(self.SHIP_LENGTHS):
                flag = False
        return new_board

    def greet(self):
        """Метод, который в консоли приветствует пользователя и рассказывает о формате ввода"""
        str = """
    Морской бой — игра для двух участников, в которой игроки по очереди называют координаты на 
    неизвестной им карте соперника. Если у соперника по этим координатам имеется корабль (координаты заняты),
     то корабль или его часть «топится», а попавший получает право сделать ещё один ход. 
     Цель игрока — первым потопить все корабли противника.
     
     Игровое поле — квадрат 6×6 у каждого игрока, на котором размещается флот кораблей.
     
           | 1 | 2 | 3 | 4 | 5 | 6|

        1 | О | О | О | О | О | О |

        2 | О | О | О | О | О | О |

        3 | О | О | О | О | О | О |

        4 | О | О | О | О | О | О |

        5 | О | О | О | О | О | О |

        6 | О | О | О | О | О | О |


    На поле размещаются:

    1 корабль — ряд из 3 клеток («трёхпалубные»; крейсера)
    2 корабля — ряд из 2 клеток («двухпалубные»; эсминцы)
    4 корабля — 1 клетка («однопалубные»; торпедные катера)
    
    При размещении корабли не могут касаться друг друга сторонами и углами. 
    
    При попадании в корабль противника — на чужом поле ставится крестик (X), 
    при холостом выстреле — буква T. Попавший стреляет ещё раз.
    
    Победителем считается тот, кто первым потопит все 7 кораблей противника.
    
    И так начнем игру. Расставим корабли на вашу доску и доску противника. 
        """
        print(str)

    def loop(self):
        """Метод с самим игровым циклом"""
        pass

    def start(self):
        """Запуск игры"""
        self.greet()
        self.loop()


new_game = Game()
new_game.greet()
new_game.ai_board.hid = False

# new_game.user_board.display_board()
new_game.ai_board.display_board()

# key = True
# while key:
#    new_game.player_user.move()
#    new_game.ai_board.display_board()

# if len(new_game.ai_board.list_of_ships) == 0:
#     key = False
