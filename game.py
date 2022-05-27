# Внешняя логика игры
from SeaBatle.sea_battle import Board, Ship, Dot


class Player(Dot):
    def __init__(self, own_board: object, enemy_board: object):
        self.own_board = own_board
        self.enemy_board = enemy_board

    @classmethod
    def ask(self):
        """Cпрашивает игрока, в какую клетку он делает выстрел"""
        pass
        # return map(int, input("Введите координаты: ").split())

    def move(self):
        res = None
        """метод, который делает ход в игре"""
        try:
            x, y = self.ask()
            coord_for_shoot = Dot(x, y)
            res = self.enemy_board.shot(coord_for_shoot)
        except Exception as e:
            print(e)
        return res == "hit"


class Game:
    def __init__(self, playe_user):
        self.playe_user = playe_user


# кораблей: 1 корабль на 3 клетки, 2 корабля на 2 клетки, 4 корабля на одну клетку."
try:
    sh_one_cage_1 = Ship(1, Dot(0, 0), "h", 1)
    sh_one_cage_2 = Ship(1, Dot(0, 5), "h", 1)
    sh_one_cage_3 = Ship(1, Dot(5, 0), "h", 1)
    sh_one_cage_4 = Ship(1, Dot(5, 4), "h", 1)

    sh_two_cage_1 = Ship(2, Dot(0, 2), "v", 2)
    sh_two_cage_2 = Ship(2, Dot(2, 5), "v", 2)

    sh_three_cage_1 = Ship(3, Dot(3, 1), "h", 3)

    list_ship_ai = [sh_one_cage_1, sh_one_cage_2, sh_one_cage_3, sh_one_cage_4, sh_two_cage_1, sh_two_cage_2,
                    sh_three_cage_1]
    list_ship_player = []

    ai_board = Board(list_ship_ai, 1, False)
    player_board = Board(list_ship_ai, 1, False)

    for ship in list_ship_ai:
        ai_board.contour(ship)
        ai_board.add_ship(ship)

    ai_board.display_board()

    player = Player(own_board=player_board, enemy_board=ai_board)
    print(player.move())
except Exception as e:
    print(e)
