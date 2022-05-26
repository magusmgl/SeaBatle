# Внутренняя логика игры — корабли, игровая доска и вся логика связанная с ней
from SeaBatle.my_Exception import *


class CheckCoordDort:
    # data descriptor для класса Dot
    @classmethod
    def validate_coord(cls, value):
        # if not isinstance(value, int) or not 0 <= value <= 5:
        if not isinstance(value, int):
            raise DortCordsException(value)

    def __set_name__(self, owner, name):
        self.name = '_' + name

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        self.validate_coord(value)
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
    """"""

    def __init__(self, length: int, start_dot: object, direction: str, number_of_lives: int):
        self.validate_length_ship(length)
        self.validate_num_lives(number_of_lives)
        self.validate_direction_ship(direction)

        self.length = length
        self.start_dot = start_dot
        self.direction = direction
        self.number_of_lives = number_of_lives

    @classmethod
    def validate_length_ship(cls, value: int) -> None:
        """Проверяет значение длины корaбля (число от 1 до 3)"""
        if not isinstance(value, int) or not 1 <= value <= 3:
            raise ShipLengthException(value)

    @classmethod
    def validate_num_lives(cls, value: int) -> None:
        """Проверяет значение жизней коробля (число от 0 до 3)"""
        if not isinstance(value, int) or not 0 <= value <= 3:
            raise ShipLivesException(value)

    @classmethod
    def validate_direction_ship(cls, value: str) -> None:
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


class Board(Dot):
    _hid = None

    def __init__(self, list_of_ships: list, number_of_live_ships: int, hid: bool):
        self.board = [[" O "] * 6 for _ in range(6)]
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

    def add_ship(self, ship: object) -> None:
        """Ставит корабль на доску (если ставить не получается, выбрасывает исключения)"""
        for dot in ship.dots:
            if not self.out(dot):
                raise BoardOutException(dot.x, dot.y)
            if self.board[dot.x][dot.y] != " O ":
                raise BoardOccupiedCage(dot.x, dot.y)
            self.board[dot.x][dot.y] = " ■ "

    def contour(self, ship: object) -> None:
        """Обводит корабль по контуру"""
        x_0 = ship.start_dot.x - 1
        y_0 = ship.start_dot.y - 1

        if ship.length == 1:
            for i in range(3):
                for j in range(3):
                    curr_dot = Dot(i + x_0, j + y_0)
                    if self.out(curr_dot) and curr_dot not in ship.dots:
                        self.board[x_0 + i][y_0 + j] = " - "

        if ship.length == 2:
            k, m = (4, 3) if ship.direction == "v" else (3, 4)
            for i in range(k):
                for j in range(m):
                    curr_dot = Dot(i + x_0, j + y_0)
                    if self.out(curr_dot) and curr_dot not in ship.dots:
                        self.board[x_0 + i][y_0 + j] = " - "

        if ship.length == 3:
            k, m = (5, 3) if ship.direction == "v" else (3, 5)
            for i in range(k):
                for j in range(m):
                    curr_dot = Dot(i + x_0, j + y_0)
                    if self.out(curr_dot) and curr_dot not in ship.dots:
                        self.board[x_0 + i][y_0 + j] = " - "

    def display_board(self) -> None:
        """ Выводит доску в консоль в зависимости от параметра hid"""
        print(" | 0 | 1 | 2 | 3 | 4 | 5 |")
        print("-" * 25)
        if self.hid:
            for i, row in enumerate(self.board):
                print(f"{i}| {'|'.join([' O '] * 6)}|")
                print("-" * 25)
        else:
            for i, row in enumerate(self.board):
                print(f"{i}|{'|'.join(row)}|")
                print("-" * 25)

    def out(self, dot: object) -> bool:
        """Для точки (объекта класса Dot) возвращает True,
        если точка выходит за пределы поля, и False, если не выходит."""
        return all([0 <= dot.x < len(self.board), \
                    0 <= dot.y < len(self.board[0])])

    def shot(self, dot: object):
        """
        Делает выстрел по доске (если есть попытка выстрелить за пределы
         и в использованную точку, нужно выбрасывать исключения).
        :return:
        """
        if not self.out(dot):
            raise BoardOutException(dot.x, dot.y)
        if self.board[dot.x][dot.y] == " T " or self.board[dot.x][dot.y] == " X ":
            raise BoardShotUsedCage(dot.x, dot.y)
        if self.board[dot.x][dot.y] == " - " or self.board[dot.x][dot.y] == " O ":
            self.board[dot.x][dot.y] = " T "
        if self.board[dot.x][dot.y] == " ■ ":
            self.board[dot.x][dot.y] = " X "


#
# кораблей: 1 корабль на 3 клетки, 2 корабля на 2 клетки, 4 корабля на одну клетку."
try:
    sh_one_cage_1 = Ship(1, Dot(0, 0), "h", 1)
    sh_one_cage_2 = Ship(1, Dot(0, 5), "h", 1)
    sh_one_cage_3 = Ship(1, Dot(5, 0), "h", 1)
    sh_one_cage_4 = Ship(1, Dot(5, 4), "h", 1)

    sh_two_cage_1 = Ship(2, Dot(0, 2), "v", 2)
    sh_two_cage_2 = Ship(2, Dot(2, 5), "v", 2)

    sh_three_cage_1 = Ship(3, Dot(3, 1), "h", 3)

    list_ship = [sh_one_cage_1, sh_one_cage_2, sh_one_cage_3, sh_one_cage_4, sh_two_cage_1, sh_two_cage_2,
                 sh_three_cage_1]

    test_board = Board(list_ship, 1, False)

    for ship in list_ship:
        test_board.contour(ship)
        test_board.add_ship(ship)
except Exception as e:
    print(e)
else:
    # test_board.display_board()
    test_board.shot(Dot(3, 1))
    test_board.shot(Dot(5, 1))
    test_board.shot(Dot(5, 2))
    test_board.display_board()
