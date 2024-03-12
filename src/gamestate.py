from disnake.ext import commands
import asyncio
from player import Player
from deck import Deck

class GameState:
    WHITE_CARD_MAX = 4
    RED_CARD_MAX = 3

    def __init__(self) -> None:
        self.players = {} # name : str -> Player()
        self.red_cards = Deck()
        self.white_cards = Deck()


    def load_cards(self) -> None:
        self.red_cards.build_deck('red_cards.csv', True).shuffle()
        self.white_cards.build_deck('white_cards.csv').shuffle()


    def deal_hand(self, player : Player) -> None:
        for i in range(0, self.WHITE_CARD_MAX):
            wcard = self.white_cards.draw_card()
            wcard.owner = player.name
            player.add_to_hand(wcard) 

        for i in range(0, self.RED_CARD_MAX):
            rcard = self.red_cards.draw_card()
            rcard.owner = player.name
            player.add_to_hand(rcard)


    def add_player(self, name : str) -> Player:
        if name not in self.players:
            self.players[name] = Player(name)
            return self.players[name]
        return None


    def remove_player(self, name : str) -> Player:
        if name not in self.players:
            return None

        tmp = self.players[name]
        del self.players[name]
        return tmp
