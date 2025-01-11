import random
class Card:
    """Представляє окрему карту в колоді."""
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    SUITS = ["\u2660", "\u2663", "\u2665", "\u2666"]
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
    def value(self):
        if self.rank in ['J', 'Q', 'K']:
            return 10
        elif self.rank == 'A':
            return 11  # Буде скориговано при оцінці руки
        else:
            return int(self.rank)
    def __str__(self):
        return f"{self.rank} {self.suit}"
    
class Deck:
    """Представляє колоду карт."""
    def __init__(self):
        self.cards = []
        self.populate()
    def populate(self):
        self.cards = [Card(rank, suit) for rank in Card.RANKS for suit in Card.SUITS]
        self.shuffle()
    def shuffle(self):
        random.shuffle(self.cards)
    def deal(self):
        if not self.cards:
            self.populate()
            print("Колода спорожніла. Нова колода була перетасована.")
        return self.cards.pop()
    
class Player:
    """Представляє гравця у грі."""
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        self.hand = []
        self.bet = 0
        self.doubled_down = False
    def place_bet(self, amount):
        if amount > self.balance:
            raise ValueError("Недостатньо коштів для ставки.")
        self.bet = amount
        self.balance -= amount
    def double_down(self):
        if self.bet > self.balance:
            raise ValueError("Недостатньо коштів для подвоєння ставки.")
        self.balance -= self.bet
        self.bet *= 2
        self.doubled_down = True
    def win_bet(self, multiplier=1):
        self.balance += self.bet * (1 + multiplier)
        self.bet = 0
        self.doubled_down = False
    def lose_bet(self):
        self.bet = 0
        self.doubled_down = False
    def push_bet(self):
        self.balance += self.bet
        self.bet = 0
        self.doubled_down = False
    def add_card(self, card):
        self.hand.append(card)
    def clear_hand(self):
        self.hand = []
        self.doubled_down = False
    def hand_value(self):
        value = sum(card.value() for card in self.hand)
        aces = sum(1 for card in self.hand if card.rank == 'A')
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value
    def is_busted(self):
        return self.hand_value() > 21
    def __str__(self):
        cards = ', '.join(str(card) for card in self.hand)
        return f"{self.name}: {cards} (Значення: {self.hand_value()})"
    
class Dealer(Player):
    """Представляє дилера."""
    def __init__(self):
        super().__init__("Дилер", balance=0)
    def should_hit(self):
        return self.hand_value() < 17
class BlackjackGame:
    """Представляє гру Блекджек."""
    def __init__(self):
        self.deck = Deck()
        self.players = []
        self.dealer = Dealer()
    def add_player(self, name, balance):
        
        self.players.append(Player(name, balance))
    def take_bets(self):
        for player in self.players:
            while True:
                try:
                    bet = int(input(f"{player.name}, у вас є {player.balance} грн. Введіть вашу ставку: "))
                    player.place_bet(bet)
                    break
                except ValueError as e:
                    print(e)

    def deal_initial_cards(self):
        for _ in range(2):
            for player in self.players:
                player.add_card(self.deck.deal())
            self.dealer.add_card(self.deck.deal())

    def player_turns(self):
        for player in self.players:
            print(player)
            while not player.is_busted():
                choice = input(f"{player.name}, бажаєте взяти карту, залишитися чи подвоїти ставку? (y/n/d): ").lower()
                if choice == "h":
                    player.add_card(self.deck.deal())
                    print(player)
                elif choice == "s":
                    break
                elif choice == 'd':
                    try:
                        player.double_down()
                        player.add_card(self.deck.deal())
                        print(player)
                        break
                    except ValueError as e:
                        print(e)
                else:
                    print("Неправильний вибір. Будь ласка, введіть 'h', 's' або 'd'.")
            if player.is_busted():
                print(f"{player.name} програв!")

    def dealer_turn(self):
        print(self.dealer)
        while self.dealer.should_hit():
            self.dealer.add_card(self.deck.deal())
            print(self.dealer)
        if self.dealer.is_busted():
            print("Дилер програв!")

    def settle_bets(self):
        dealer_value = self.dealer.hand_value()
        for player in self.players:
            if player.is_busted():
                player.lose_bet()
            elif self.dealer.is_busted() or player.hand_value() > dealer_value:
                player.win_bet()
                print(f"{player.name} виграв!")
            elif player.hand_value() == dealer_value:
                player.push_bet()
                print(f"{player.name} нічия.")
            else:
                player.lose_bet()
                print(f"{player.name} програв.")

    def reset_hands(self):
        for player in self.players:
            player.clear_hand()
        self.dealer.clear_hand()

    def remove_broke_players(self):
        self.players = [player for player in self.players if player.balance > 0]

    def play_round(self):
        self.take_bets()
        self.deal_initial_cards()
        self.player_turns()
        self.dealer_turn()
        self.settle_bets()
        self.reset_hands()
        self.remove_broke_players()

    def play(self):
        print("Ласкаво просимо до гри Блекджек!")
        num_players = int(input("Скільки гравців грають? "))
        for i in range(num_players):
            name = input(f"Введіть ім'я гравця {i + 1}: ")
            balance = int(input(f"Введіть початковий баланс для {name}: "))
            self.add_player(name, balance)
        while self.players:
            self.play_round()
            if input("Грати ще один раунд? (т/н): ").lower() != 'т':
                break
        print("Гра завершена. Дякуємо за гру!")
if __name__ == "__main__":
    game = BlackjackGame()
    game.play()