from disnake.ext import commands
import asyncio
from player import Player
from deck import Deck

# pretty sure this has to be an async cog...
"""
    Ok, so I'm pretty sure we need to use tasks and cogs now,
    because the bot is essentially abstracting some kind of 
    event loop

"""
class GameState:
    WHITE_CARD_MAX = 4
    RED_CARD_MAX = 3

    def __init__(self):
        self.players = {} # name : str -> Player()
        self.red_cards = Deck()
        self.white_cards = Deck()

    def load_cards(self) -> None:
        self.red_cards.build_deck('red_cards.csv', True).shuffle()
        print('Red cards:\n')
        for card in self.red_cards.cards:
            print(card.text)

        self.white_cards.build_deck('white_cards.csv').shuffle()
        print('White cards:\n') 
        for card in self.white_cards.cards:
            print(card.text)

    def deal_hand(self, player : Player) -> None:
        for i in range(0, self.WHITE_CARD_MAX):
            wcard = self.white_cards.draw_card()
            wcard.owner = player.name
            player.add_to_hand(wcard) 

        for i in range(0, self.RED_CARD_MAX):
            rcard = self.red_cards.draw_card()
            rcard.owner = player.name
            player.add_to_hand(rcard)

        print('Hands delt!')

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
