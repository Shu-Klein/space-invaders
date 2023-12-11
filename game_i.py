from manager_i import Manager


class Game:
    def __init__(self):
        self.manager = Manager()


game = Game()
game.manager.run()
