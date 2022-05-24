# Внутренняя логика игры — корабли, игровая доска и вся логика связанная с ней
from SeaBatle.my_Exception import ShipLengthException, ShipLivesException, ShipDirectionException, DortCordsException


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
            self.__validate_length_ship(length_ship)
            self.__validate_num_lives(number_of_lives)
            self.__validate_direction_ship(ship_direction)
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
    def __validate_num_lives(cls, arg):
        if not isinstance(arg, int) or not 0 <= arg <= 3:
            raise ShipLivesException(arg)

    @classmethod
    def __validate_direction_ship(cls, arg: str):
        if arg.lower() != "r" or arg.lower() != "h":
            raise ShipDirectionException(arg)

    def dots(self):
        """Возвращает список всех точек коробля"""
        if self.length == 1:
            return self.start_dot
        else:
            pass


class Board:
    def __init__(self, ship_list, number_of_live_ships, hid=False):
        self.board = [[" O "] * 6 for _ in range(6)]
        self.ship_list = ship_list
        self.hid = hid
        self.number_of_live_ships = number_of_live_ships

    def __str__(self):
        print("  | 1 | 2 | 3 | 4 | 5 | 6|")
        print("-" * 25)
        for i, row in enumerate(self.board):
            print(f"{i}|{'|'.join(row)}|")
            print("-" * 25)

    @property
    def ship_list(self):
        return []

    @ship_list.setter
    def ship_list(self, ship):
        self.ship_list.append(ship)

    @property
    def number_of_live_ships(self):
        return self.number_of_live_ships

    @number_of_live_ships.setter
    def number_of_live_ships(self):
        return len(self.ship_list)

    def add_ship(self, ship):
        """ ставит корабль на доску (если ставить не получается, выбрасываем исключения)"""
        pass

    def contour(self):
        """который обводит корабль по контуру. Он будет полезен и в ходе самой игры,
        и в при расстановке кораблей (помечает соседние точки, где корабля по правилам быть не может)."""

    def display_board(self, hid):
        """выводит доску в консоль в зависимости от параметра hid"""
        pass

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
