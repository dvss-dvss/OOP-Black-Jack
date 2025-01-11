# Блек-джек
# Вiд 1 до 7 гравцiв проти дилера

import cards1, games1

class BJ_Card(cards1.Positionable_Card):
    """Карта для гри в Блек-джек."""
    ACE_VALUE = 1

    @property
    def value(self):
        if self.is_face_up:
            v = BJ_Card.RANKS.index(self.rank) + 1
            if v > 10:
                v = 10

            else:
                v = None
            return v
        
class BJ_Deck(cards1.Deck):
    """Колода для гри в Блек-джек"""
    def populate(self):
        for suit in BJ_Card.SUITS:
            for rank in BJ_Card.RANKS:
                self.cards.append(BJ_Card(rank, suit))

class BJ_Hand(cards1.Hand):
    """Рука гравця в Блек_джек."""
    def __init__(self,name):
        super().__init__()
        self.name = name

    def __str__(self):
        rep = self.name + ":\t" + super().__str__()
        if self.total:
            rep += "(" + str(self.total) + ")"
        return rep
    
    @property
    def total(self):
        # якщо value одниейи з карт доривнюе None,
        # то и властивость в цилому доривню None
        for card in self.cards:
            if not card.value:
                return None
            
        # cмуемо очки, рахуючи кожен туз за 1 очко
        # визначаемо, чи е туз на руках у грацвя
        t = 0
        contains_ace = False
        for card in self.cards:
            t += card.value
            if card.value == BJ_Card.ACE_VALUE:
                contains_ace = True
        
        # якщо на руках е туз i сума очок не перевищуе за 11,
        # будемо рахувати туз за 11 очок
        if contains_ace and t <= 11:
            # додати потрiбно лише 10,
            # тому що одиниця вже увiйшла до загальнойи суми
            t += 10

            return t
    def is_busted(self):
        return self.totl > 21
    
class BJ_Player(BJ_Hand):
    """Гравець у Блек-джек. """
    def is_hitting(self):
        response = games1.ask_yes_no("\n" + self.name +
            ", братимете ще карти")
        return response == "y"
    
    def bust(self):
        print(self.name, "перебрав(ла).")
        self.lose()

    def lose(self):
        print(self.name, "прогав(ла).")

    def win(self):
        print(self.name, "виграв(ла).")

    def push(self):
        print(self.name, "зiграв(ла) з дилером внiчию")

class BJ_Dealer(BJ_Hand):
    """Дилер у Блек-джек. """
    def is_hitting(self):
        return self.total < 17
    
    def bust(self):
        print(self.name, "перебрав.")

    def flip_first_card(self):
        first_card = self.cards[0]
        first_card.flip()

class BJ_Game:
    """Гра Блек-джек."""
    def __init__(self, name):
        self.players = []
        for name in names:
            player = BJ_Player(name)
            self.players.append(player)

        self.dealer = BJ_Dealer("Дилер")

        self.deck = BJ_Deck()
        self.deck.populate()
        self.deck.shuffle()
    
    @property
    def still_playing(self):
        for player in self.players:
            if not player.is_busted():
                sp.append(player)
        return sp
    
    def __additional_cards(self, player):
        while not player.is_busted() and player.is_hitting():
            self.deck.deal([player])
            print(player)
            if player.is_busted():
                player.bust()

    def play(self):
        # задача всiм по двi карти
        self.deck.deal(self.players + [self.dealer],
                       per_hand = 2)
        self.dealer.flip_first_card()
        # перша з карт, зданих дилеру, перевертается
        for player in self.players:
            print(player)
        print(self.dealer)

        # роздавання додаткових карт гравцям
        for player in self.players:
            self.__additional_cards(player)
        # перша карта дилера розкривается
        self.dealer.flip_first_card()

        if not self.still_playing:
            # всi гравцi перебрали,
            # покажемо лише "руку" дилера
            print(self.dealer)
        else:
            # роздача додаткових карт дилеру
            print(self.dealer)
            self.__additional_cards(self.dealer)

            if self.dealer.is_busted():
                # виграють усi, хто ще залишився у грi
                for player in self.still_playing:
                    player.win()
            else:
                # порiвнюемо суми очок у дилера
                # та у гравцiв, що залишилися у грi
                for player in self.still_playing:
                    if player.total > self.dealer.total:
                        player.win()
                    elif player.total < self.dealer.total:
                        player.lose()
                    else:
                        player.push()
        # видалення всiх карт
        for player in self.players:
            player.clear()
        self.dealer.clear()

def main():
    print("\t\tЛаскаво просимо до гри Блек-джек!\n")

    names - []
    number = games1.ask_number("Скiльки всього гравцiв? (1-7):",
                                low = 1, high = 7)
    
    for i in range(number):
        name = input("Введiть iм'я гравця № " + str(i + 1) + ":")
        names.append(name)
    print()

    game = BJ_Game(names)

    again = None
    while again != "n":
        game.play()
        again = games1.ask_yes_no("\nБажаэте зiграти ще раз")

main()