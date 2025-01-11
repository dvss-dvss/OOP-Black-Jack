# Модуль games
# Демонструе створення модуля

def ask_yes_no(question):
    """Задае питання з вiдповiддю (y/n)"""
    response = None
    while response not in ("y", "n"):
        response = input(question + ' (y/n)? '.lower())
    return response

def ask_number(question, low, hight):
    """Просить ввести число iз заданого дiапазону."""
    response = None
    while response not in range(low, hight + 1):
        response = int(input(question))
    return response

class Card:
    """Гральна карта."""
    RANKS = ["Т", "2", "3", "5", "6", "7",
             "8", "9", "10", "В", "Д", "К"]
    
    SUITS = [u'\u2660', u'\u2663', u'\u2665', u'\u2666']

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        rep = self.rank + self.suit
        return rep

class Unprintble_Card(Card):
    
    def __str__(self):
        return "<не можна надрукувати>"
    
class Positionable_Card(Card):
    """Карта, яку можна покласти
      обличчям або сорочкою вгору."""
    
    def __init__(self, rank, suit, face_up = True):
        super().__init__(rank, suit)
        self.is_face_up = face_up

    def __str__(self):
        if self.is_face_up:
            rep = super().__str__()
        else:
            rep = "XX"
        return rep
    def flip(self):
        self.is_face_up = not self.is_face_up

class Hand:
    """Рука: набір карт на руках одного гравця."""

    def __init__(self):
        self.cards = []

    def __str__(self):
        if self.cards:
            rep = ""
            for card in self.cards:
                rep+= str(card) + "\t"
        else:
            rep = "<пусто>"
        return rep
    
    def clear(self):
        self.cards = []

    def add(self, card):
        self.cards.append(card)

    def give(self, card, other_hand):
        self.cards.remove(card)
        other_hand.add(card)

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

if __name__ == "__main__":
    print("Ви запустили модуль games, "
          "а не iмпортували його (import games).")
    
    card1 = Card("Т", Card.SUITS[0])
    card2 = Unprintble_Card("Т", Card.SUITS[1])
    card3 = Positionable_Card("Т", Card.SUITS[2])
    print("Об'ект Card:", card1)
    print("Об'ект Unpritable_Card:", card2)
    print("Об'ект Positionable_Card:", card3)
    card3.flip()
    print("Перевертаю Об'ект Positionable_Card:", card3)
    deck1= Deck()
    print("\nСтворено нову колоду:", deck1)
    deck1.populate()
    print("У колоди з'явилися карти:", deck1, sep="\n")
    deck1.shuffle()
    print("Колода перемишана:", deck1, sep="\n")
    hand1 = Hand()
    hand2 = Hand()
    deck1.deal(hands=(hand1, hand2), per_hand = 5)
    print("\nРоздано по 5 карт.")
    print("Рука1:", hand1)
    print("Рука2:", hand2)
    print("Залишилось у колоди", deck1, sep="\n")
    deck1.clear()
    print("Колода очищена:", deck1)