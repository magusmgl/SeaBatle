# Внутренняя логика игры — корабли, игровая доска и вся логика связанная с ней
from SeaBatle.my_Exception import *


class CheckCoordDort:
    # data descriptor для класса Dot
    @classmethod
    def validate_coord(cls, value):
        if not isinstance(value, int) or not 0 <= value <= 5:
            raise DortCordsException(value)

    def __set_name__(self, owner, name):
        self.name = '_' + name

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        try:
            self.validate_coord(value)
        except DortCordsException as e:
            print(e)
        else:
            setattr(instance, self.name, value)


class Dot:
    x = CheckCoordDort()
    y = CheckCoordDort()

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Ship:
    "в конструктор передаём информацию о его положении на доске\
    кораблей: 1 корабль на 3 клетки, 2 корабля на 2 клетки, 4 корабля на одну клетку."

    def __init__(self, length_ship: int, start_dot: object, ship_direction: str, number_of_lives: int):
        try:
            self.validate_length_ship(length_ship)
            self.validate_num_lives(number_of_lives)
            self.validate_direction_ship(ship_direction)
        except ShipLengthException as e:
            print(e)
        except ShipLivesException as e:
            print(e)
        except ShipDirectionException as e:
            print(e)
        else:
            self.length_ship = length_ship
            self.start_dot = start_dot
            self.ship_direction = ship_direction
            self.number_of_lives = number_of_lives

    @classmethod
    def validate_length_ship(cls, arg):
        if not isinstance(arg, int) or not 1 <= arg <= 3:
            raise ShipLengthException(arg)

    @classmethod
    def validate_num_lives(cls, arg):
        if not isinstance(arg, int) or not 0 <= arg <= 3:
            raise ShipLivesException(arg)

    @classmethod
    def validate_direction_ship(cls, arg: str):
        if arg != "v" and arg != "h":
            raise ShipDirectionException(arg)

    @property
    def dots(self):
        """Возвращает список всех точек коробля"""
        list_of_dots = []
        for i in range(self.length_ship):
            if self.ship_direction == "v":
                list_of_dots.append((self.start_dot.x + i, self.start_dot.y))
            else:
                list_of_dots.append((self.start_dot.x, self.start_dot.y + i))
        return list_of_dots


class Board:
    def __init__(self, list_of_ships: list, number_of_live_ships, hid=False):
        self.board = [[" O "] * 6 for _ in range(6)]
        self.list_of_ships = list_of_ships
        self.number_of_live_ships = number_of_live_ships
        self.hid = hid

    def add_ship(self, ship: object):
        """ ставит корабль на доску (если ставить не получается, выбрасываем исключения)"""
        for x, y in ship.dots:
            if any([x > len(self.board) - 1, y > len(self.board[0]) - 1]):
                raise BoardOutException(x, y)
            if self.board[x][y] != " O ":
                raise BoardOccupiedCage(x, y)
            self.board[x][y] = " ■ "

    def contour(self):
        """который обводит корабль по контуру. Он будет полезен и в ходе самой игры,
        и в при расстановке кораблей (помечает соседние точки, где корабля по правилам быть не может)."""

    def display_board(self):
        """выводит доску в консоль в зависимости от параметра hid"""
        print("  | 1 | 2 | 3 | 4 | 5 | 6|")
        print("-" * 25)
        if self.hid == False:
            for i, row in enumerate(self.board):
                print(f"{i}|{'|'.join(row)}|")
                print("-" * 25)

    def out(self, dort):
        """для точки (объекта класса Dot) возвращает True,
        если точка выходит за пределы поля, и False, если не выходит."""
        pass

    def shot(self):
        """
        делает выстрел по доске (если есть попытка выстрелить за пределы
         и в использованную точку, нужно выбрасывать исключения).
        :return:
        """

# a1 = Dot(1, 1)
# sh_1 = Ship(3, a1, "v", 3)
# a2 = Dot(4, 3)
# sh_2 = Ship(2, a2, "h", 2)
# print(sh_2.dots)
# sh_3 = Ship(3, a1, "v", 3)
# list_ship = [sh_1, sh_2, sh_3]
# board_1 = Board(list_ship, 1, False)
#
# board_1.add_ship(sh_1)
# board_1.add_ship(sh_2)
# board_1.add_ship(sh_3)
# board_1.display_board()
