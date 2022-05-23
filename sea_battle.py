"""
Внутренняя логика игры — корабли, игровая доска и вся логика связанная с ней
"""


class Ship:
    "в конструктор передаём информацию о его положении на доске\
    кораблей: 1 корабль на 3 клетки, 2 корабля на 2 клетки, 4 корабля на одну клетку."

    def __init__(self, length, start_dot, ship_direction, number_of_lives):
        self.length = length
        self.start_dot = start_dot
        self.ship_direction = ship_direction
        self.number_of_lives = number_of_lives

    def dot(self):
        """Возвращает список всех точек коробля"""
        if self.length == 1:
            return self.start_dot


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



class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    @property
    def cord(self):
        return self.x, self.y


"""Внешняя логика игры — пользовательский интерфейс, искусственный интеллект, игровой контроллер, который считает побитые корабли.

1. В начале имеет смысл написать классы исключений, которые будет использовать наша программа. Например, когда игрок пытается выстрелить
 в клетку за пределами поля, во внутренней логике должно выбрасываться соответствующее исключение BoardOutException,
  а потом отлавливаться во внешней логике, выводя сообщение об этой ошибке пользователю.
2.Далее нужно реализовать класс Dot — класс точек на поле. Каждая точка описывается параметрами:


"""
