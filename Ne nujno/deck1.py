from hand import Hand
from cards1 import Card
class Deck(Hand):
    """ Колода гральних карт. """

    def populate(self):
        for suit in Card.SUITS:
            for rank in Card.RANKS:
                self.add(Card(rank, suit))

    def shuffle(self):
        import random
        random.shuffle(self.cards)

    def add_new_deck(self):
        self.populate()
        self.shuffle()

    def deal(self, hands, per_hand = 1):
        for rounds in range(per_hand):
            for hand in hands:
                # Перевирка на нявнисть карт у колоди
                if self.cards:
                    self.add_new_deck()
                top_card = self.cards[0]
                self.give(top_card, hand)