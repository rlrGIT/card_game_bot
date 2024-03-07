import card, csv, random
from card import Card

class Deck:
    DECK_SIZE = 0
    CARD_TEXT = 1

    def __init__(self):
        self.cards = []

    def build_deck(self, file_name : str, red_cards : bool=False):
        with open(file_name, 'r') as card_info:
            reader = csv.reader(card_info, delimiter=';')
            for row in reader:
                if row:
                    self.cards.append(Card(row[self.CARD_TEXT], red_cards))
                    self.DECK_SIZE += 1
        return self

    def place_at_bottom(self, card : card.Card):
        self.cards.append(card)

    def draw_card(self):
        try:
            return self.cards.pop(0)

        except IndexError as out_of_cards:
            print(out_of_cards)

    def get_random_pair(self):
        index_0 = random.randrange(self.DECK_SIZE)
        index_1 = random.randrange(self.DECK_SIZE)
        return (index_0, index_1)

    def shuffle(self):
        assert(self.DECK_SIZE > 0)
        for i in range(self.DECK_SIZE):
            i, j = self.get_random_pair()
            self.cards[i], self.cards[j] = self.cards[j], self.cards[i]
        return self

    def __str__(self):
        output = "{\n"
        for card in self.cards:
            output += card.text
        output += "\n}\n"
        return output
