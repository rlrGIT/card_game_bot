from card import Card

class Player:

    def __init__(self, name : str) -> None:
        self.name = name
        self.cards = {}

    def add_to_hand(self, card : Card) -> None:
        self.cards[card.text] = card
        

    def __str__(self) -> str:
        return self.name
