class Card:

    def __init__(self, text : str, red_card : bool) -> None:
        self.text = text
        self.red_card = red_card
        self.owner : str = None

    def __str__(self):
        print(self.text)
