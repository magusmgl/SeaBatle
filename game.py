import random


class BoardException(Exception):
    def __init__(self, *args):
        self.message = args


class BoardOutException(BoardException):
    """Класс исключения, который  используется чтобы отлавливать ошибки,
     когда игрок пытается выстрелить в клетку за пределами игрового поля. """

    def __str__(self):
        return f"Точка с координатами ({self.message[0]},{self.message[1]}) находится за пределами  игрового поля."


class BoardOccupiedCage(BoardException):
    def __str__(self):
        return f"Точка с координатами ({self.message[0]},{self.message[1]}) занята."


class BoardShotUsedCage(BoardException):
    def __str__(self):
        return f"В точку с координатами ({self.message[0]},{self.message[1]}) уже был сделан выстрел."


class DortException(Exception):
    def __init__(self, *args):
        self.message = args[0] if args else None


class DortCordsException(DortException):
    def __str__(self):
        return f"Ошибка: '{self.message}' координаты задаются целыми числами от 0 до 5."


class DortSignException(DortException):
    def __str__(self):
        return f"Ошибка: '{self.message}' неверный знак для точки."


class ShipParamException(Exception):
    def __init__(self, *args):
        self.message = args[0] if args else None


class ShipLengthException(ShipParamException):
    def __str__(self):
        return f"Ошибка: длина коробля не может принимать значение '{self.message}'."


class ShipLivesException(ShipParamException):
    def __str__(self):
        return f"Ошибка: Число жизней '{self.message}' должно принимать значение от 0 до 3."


class ShipDirectionException(ShipParamException):
    def __str__(self):
        return f"Ошибка: Введенное положение корабля '{self.message}' должно принимать значение 'v'/'h'."


class GameSettings():
    """Настройка игры"""
    # Список кораблей и их длины
    SHIP_LENGTHS = [3, 2, 2, 1, 1, 1, 1]

    # Размер доски
    BOARD_SIZE = 6

    MAX_NUM_SHIP_CELLS = max(SHIP_LENGTHS)
    MIN_NUM_SHIP_CELLS = min(SHIP_LENGTHS)
    MAX_NUM_SHIP_LIVES = max(SHIP_LENGTHS)


# Внешняя логика игры
class Dot:
    """Класс точек на поле"""
    _x = None
    _y = None
    _sign = None

    def __init__(self, x, y, sign=" O "):
        self.x = x
        self.y = y
        self.sign = sign

    @classmethod
    def _validate_coord(cls, value):
        if not isinstance(value, int):
            raise DortCordsException(value)

    @classmethod
    def _validate_sign(cls, sign):
        if isinstance(sign, str) and sign not in [" X ", " O ", " T ", " - ", " ■ "]:
            raise DortSignException(sign)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._validate_coord(value)
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._validate_coord(value)
        self._y = value

    @property
    def sign(self):
        return self._sign

    @sign.setter
    def sign(self, value):
        self._validate_sign(value)
        self._sign = value


class Ship(GameSettings):
    """Корабль на игровом поле"""

    def __init__(self, length: int, start_dot: Dot, direction: str, health: str):
        self._validate_length_ship(length)
        self._validate_num_lives(health)
        self._validate_direction_ship(direction)

        self.length = length
        self.start_dot = start_dot
        self.direction = direction
        self.health = health

    @classmethod
    def _validate_length_ship(cls, value: int) -> None:
        """Проверяет значение длины корaбля (число от min до max)"""
        if not all([isinstance(value, int),
                    cls.MIN_NUM_SHIP_CELLS <= value <= cls.MAX_NUM_SHIP_CELLS]):
            raise ShipLengthException(value)

    @classmethod
    def _validate_num_lives(cls, value: int) -> None:
        """Проверяет значение жизней коробля (число от 0 до max)"""
        if not all([isinstance(value, int),
                    0 <= value <= cls.MAX_NUM_SHIP_LIVES]):
            raise ShipLivesException(value)

    @classmethod
    def _validate_direction_ship(cls, value: str) -> None:
        """Проверяет значение направление корабля ('v' и 'h')"""
        if value != "v" and value != "h":
            raise ShipDirectionException(value)

    @property
    def dots(self) -> list:
        """Возвращает список всех точек коробля"""
        list_of_dots = []
        for i in range(self.length):
            if self.direction == "v":
                list_of_dots.append(Dot(self.start_dot.x + i, self.start_dot.y))
            else:
                list_of_dots.append(Dot(self.start_dot.x, self.start_dot.y + i))
        return list_of_dots

    @property
    def name(self):
        if self.length == 3:
            name = "Крейсер"
        if self.length == 2:
            name = "Эсминец"
        if self.length == 1:
            name = "Катер"
        return name


class Board(GameSettings):
    """Игровая доска"""
    _hid = None

    def __init__(self, list_of_ships: list, number_of_live_ships: int, hid=False):
        self.list_dots_on_board = [[Dot(i, j) for j in range(self.BOARD_SIZE)] for i in
                                   range(self.BOARD_SIZE)]
        self.list_of_ships = list_of_ships
        self.number_of_live_ships = number_of_live_ships
        self.hid = hid

    @property
    def hid(self):
        return self._hid

    @hid.setter
    def hid(self, value):
        if isinstance(value, bool):
            self._hid = value

    def add_ship(self, ship: Ship) -> None:
        """Ставит корабль на доску (если ставить не получается, выбрасывает исключения)"""
        for dot in ship.dots:
            if self._out(dot):
                raise BoardOutException(dot.x, dot.y)
            if self.list_dots_on_board[dot.x][dot.y].sign != " O ":
                raise BoardOccupiedCage(dot.x, dot.y)
            self.list_dots_on_board[dot.x][dot.y].sign = " ■ "
        self.contour(ship)
        self.list_of_ships.append(ship)

    def contour(self, ship: Ship) -> None:
        """Обводит корабль по контуру"""
        x_0 = ship.start_dot.x - 1
        y_0 = ship.start_dot.y - 1

        if ship.length == 1:
            k, m = 3, 3
        else:
            k, m = (ship.length + 2, 3) if ship.direction == "v" else (3, ship.length + 2)

        for i in range(k):
            for j in range(m):
                curr_dot = Dot(i + x_0, j + y_0)
                if not self._out(curr_dot) and curr_dot not in ship.dots:
                    self.list_dots_on_board[x_0 + i][y_0 + j].sign = " - "

    def display_board(self) -> None:
        """ Выводит доску в консоль в зависимости от параметра hid"""
        board = f" | {' | '.join([str(i) for i in range(self.BOARD_SIZE)])} |\n"
        board += f" {'-' * self.BOARD_SIZE * 4} \n"
        if self.hid:
            for i, row in enumerate(self.list_dots_on_board):
                board += f"{i}|{'|'.join(list(map(lambda x: ' O ' if x.sign == ' ■ ' else x.sign, row)))}|\n"
                board += f" {'-' * self.BOARD_SIZE * 4} \n"
        else:
            for i, row in enumerate(self.list_dots_on_board):
                board += f"{i}|{'|'.join(list(map(lambda x: x.sign, row)))}|\n"
                board += f" {'-' * self.BOARD_SIZE * 4} \n"
        print(board)

    def _out(self, dot: Dot) -> bool:
        """Для точки (объекта класса Dot) возвращает True,
        если точка выходит за пределы поля, и False, если не выходит."""
        for row in self.list_dots_on_board:
            for item in row:
                if item == dot:
                    return False
        return True

    def shot(self, dot: Dot) -> str:
        """ Делает выстрел по доске (если есть попытка выстрелить за пределы
         и в использованную точку, нужно выбрасывать исключения).
        """
        if self._out(dot):
            raise BoardOutException(dot.x, dot.y)

        if self.list_dots_on_board[dot.x][dot.y].sign in [" T ", " X "]:
            raise BoardShotUsedCage(dot.x, dot.y)

        if self.list_dots_on_board[dot.x][dot.y].sign == " ■ ":
            for ship in self.list_of_ships:
                for ship_dot in ship.dots:
                    if dot == ship_dot:
                        if ship.health == 1:
                            print(f"Потоплен {ship.name}!  - {dot.x, dot.y}")
                            ship.health -= 1
                            self.number_of_live_ships -= 1
                            self.list_of_ships.remove(ship)
                        else:
                            print(f"Попал! - {dot.x, dot.y}")
                            ship.health -= 1

                        self.list_dots_on_board[dot.x][dot.y].sign = " X "

            return True

        else:
            self.list_dots_on_board[dot.x][dot.y].sign = " T "
            print(f"Мимо!- {dot.x, dot.y}")
        return False


class Player():
    """Класс игрока в игру"""

    def __init__(self, own_board: Board, enemy_board: Board):
        self.own_board = own_board
        self.enemy_board = enemy_board

    def _ask(self):
        pass

    def move(self):
        pass


class AI(Player):
    def _ask(self):
        """Cпрашивает игрока, в какую клетку он делает выстрел"""
        return Dot(random.randint(0, 5), random.randint(0, 5))

    def move(self) -> bool:
        """Метод, который делает ход в игре"""
        try:
            grid_coordinate = self._ask()
            res = self.enemy_board.shot(grid_coordinate)
        except BoardException as e:
            return False
        return res


class User(Player):
    def _ask(self):
        """Выбор случайной точки на доске"""
        x, y = list(map(int, input("Введите координаты клетки: ").split()))
        return Dot(x, y)

    def move(self) -> bool:
        """Метод, который делает ход в игре"""
        try:
            grid_coordinate = self._ask()
            res = self.enemy_board.shot(grid_coordinate)
        except Exception as e:
            print(e)
            return True
        return res


class Game(GameSettings):
    """Класс игры"""

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
                    except BoardException:
                        continue
                    else:
                        break
            if len(new_board.list_of_ships) == len(self.SHIP_LENGTHS):
                for row in new_board.list_dots_on_board:
                    for dot in row:
                        if dot.sign == " - ":
                            dot.sign = " O "
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
     
          | 0 | 1 | 2 | 3 | 4 | 5 |

        0 | О | О | О | О | О | О |

        1 | О | О | О | О | О | О |

        2 | О | О | О | О | О | О |

        3 | О | О | О | О | О | О |

        4 | О | О | О | О | О | О |

        5 | О | О | О | О | О | О |


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
        turn_order = "user"

        while True:
            print("Ваша доска: ")
            self.user_board.display_board()
            print("^" * 26)
            print("Доска компьютера: ")
            self.ai_board.hid = True
            self.ai_board.display_board()

            if turn_order == "user":
                print()
                print("Ваш ход.", end=" ")
                if self.player_user.move():
                    if self.ai_board.number_of_live_ships == 0:
                        print("Вы выиграли!")
                        break
                    else:
                        continue
                else:
                    turn_order = "ai"
                    continue
            if turn_order == "ai":
                print()
                print("Ход компьютера.", end="")
                if self.player_ai.move():
                    if self.user_board.number_of_live_ships == 0:
                        print("Вы проиграли!")
                        break
                    else:
                        continue
                else:
                    turn_order = "user"
                    continue

    def start(self):
        """Запуск игры"""
        self.greet()
        self.loop()


if __name__ == '__main__':
    new_game = Game()
    new_game.start()
