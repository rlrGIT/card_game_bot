from player import Player

class GameState:
    def __init__(self):
        self.players = {} # name x Player()

    def add_player(self, name : str) -> bool:
        if name not in self.players:
            self.players[name] = Player(name)
            return True

        return False

    def remove_player(self, name : str) -> bool:
        if name not in self.players:
            return False

        del self.players[name]
        return True
