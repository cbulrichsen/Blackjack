from random import shuffle
import time

class Player:
    def __init__(self, name: str, money: int):
        self.name = name
        self.money = money
        self.hand = []
        self.bet = 0

    def discard_hand(self):
        self.hand = []

    def receive_card(self, card: tuple):
        self.hand.append(card)

    def get_hand(self):
        return self.hand
    
    def get_name(self):
        return self.name
    
    def bet_money(self, amount: int):
        if amount < 1 or amount > self.money:
            return False
        self.bet = amount
        self.money -= amount
        return amount

    def win_bet(self):
        self.money += self.bet * 2
        return self.bet * 2

    def win_blackjack(self):
        self.money += int(self.bet * 2.5)
        return int(self.bet * 2.5)

    def draw(self):
        self.money += self.bet
    
    def print_hand(self):
        hand = self.hand
        offset = len(f"{self.name}'s hand:")
        print(f"{self.name}'s hand:", end="")
        print(" ___ " * len(hand))
        print(" " * offset, end = "")
        for card in hand:
            print(f"| {card[0]} |", end="")
        print()
        print(" " * offset, end="")
        for card in hand:
            print(f"| {card[1]} |", end="")
        print()
        print(" " * offset + " ‾‾‾ " * len(hand))

    def __str__(self):
        return f"{self.name} has {self.money} dollars"

class CardDeck:
    def __init__(self):
        self.cards = []

    def fill(self):
        self.cards = []
        suits = "DHCS"
        values = "A23456789TJQK"
        for suit in suits:
            for value in values:
                self.cards.append((value, suit))

    def shuffle(self):
        shuffle(self.cards)

    def top_card(self):
        if not self.cards:
            self.fill()
            self.shuffle()
        top_card = self.cards.pop(0)
        return top_card

    def __str__(self):
        return str(self.cards)
    
class Visualizer:
    def __init__(self):
        self.borders = "|_‾"
        #  ___  ___
        # | A || 7 |  the goal :P
        # | S || C |
        #  ‾‾‾  ‾‾‾

    def print_hand(self, player: Player):
        hand = player.get_hand()
        offset = len(f"{player.get_name()}'s hand:")
        print(f"{player.get_name()}'s hand:", end="")
        print(" ___ " * len(hand))
        print(" " * offset, end = "")
        for card in hand:
            print(f"| {card[0]} |", end="")
        print()
        print(" " * offset, end="")
        for card in hand:
            print(f"| {card[1]} |", end="")
        print()
        print(" " * offset + " ‾‾‾ " * len(hand))

            
class BlackjackTable:
    def __init__(self):
        self.deck = CardDeck()
        self.dealer = Player("Dealer", 1)
        self.visualizer = Visualizer()
        self.players = {}

    def add_player(self, name: str, amount: int):
        self.players[name] = Player(name, amount)

    def get_players(self):
        return self.players

    def hand_value(self, player: Player):
        if not player.get_hand():
            return 0
        hand = player.get_hand()
        total = 0
        aces = 0
        for card in hand:
            if card[0] in "TJQK":
                total += 10
            elif card[0] == "A":
                total += 11
                aces += 1
            else:
                total += int(card[0])
        
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1

        return total
    
    def initial_deal(self):
        self.dealer.discard_hand()
        for player in self.players.values():
            player.discard_hand()
        for i in range(2):
            card = self.deck.top_card()
            self.dealer.receive_card(card)
            for player in self.players.values():
                card = self.deck.top_card()
                player.receive_card(card)

    def hit(self, player: Player):
        card = self.deck.top_card()
        player.receive_card(card)

    def print_dealer_hidden(self):
        hand = self.dealer.hand
        offset = len(f"{self.dealer.name}'s hand:")
        print(f"{self.dealer.name}'s hand:", end="")
        print(" ___ " * len(hand))
        print(" " * offset, end = "")
        print(f"| {hand[0][0]} || ? |")
        print(" " * offset, end="")
        print(f"| {hand[0][1]} || ? |")
        print(" " * offset + " ‾‾‾ " * len(hand))

class BlackjackApplication:
    def __init__(self):
        self.table = BlackjackTable()

    def initialize_game(self):
        print("Welcome to the Blackjack table!")
        while True:
            try:
                num_players = int(input("How many will be playing today? "))
                break
            except:
                print("Please type an integer number")
        while True:
            try:
                starting_money = int(input("And how much money will everyone be starting with? "))
                break
            except:
                print("Please type in an integer number")
        for i in range(num_players):
            name = input(f"Player {i+1}'s name: ")
            self.table.add_player(name, starting_money)
        print("Great, let's begin")
        
    def take_bets(self):
        for player in self.table.get_players().values():
            print(player)
            while True:
                try:
                    amount = int(input(f"How much would {player.get_name()} like to bet? ")) 
                except:
                    print("Please type in an integer number")
                    continue
                if not player.bet_money(amount):
                    print("Invalid bet")
                    print(player)
                    continue
                break

    def hit_or_stay(self):
        for player in self.table.get_players().values():
            while True:
                self.table.print_dealer_hidden()
                player.print_hand()
                action = input(f"What would {player.get_name()} like to do? (hit or stay): ")
                if action.lower() == "hit":
                    self.table.hit(player)
                    if self.table.hand_value(player) > 21:
                        player.print_hand()
                        print("Bust! Your bet goes to the house")
                        time.sleep(1)
                        break
                elif action.lower() == "stay":
                    time.sleep(1)
                    break
                else:
                    print("Please type either hit or stay")
                time.sleep(1)

    def dealers_turn(self):
        dealer = self.table.dealer
        while True:
            dealer.print_hand()
            if self.table.hand_value(dealer) >= 17:
                time.sleep(1)
                break
            self.table.hit(dealer)
            time.sleep(2)

    def results(self):
        dealer_bust = self.table.hand_value(self.table.dealer) > 21
        dealer_blackjack = self.table.hand_value(self.table.dealer) == 21 and len(self.table.dealer.get_hand()) == 2

        if dealer_bust:
            print("Dealer busted")
            for player in self.table.get_players().values():
                player_blackjack = self.table.hand_value(player) == 21 and len(player.get_hand()) == 2
                if player_blackjack:
                    winnings = player.win_blackjack()
                    print(f"{player.get_name()} got blackjack and won {winnings} dollars!")
                elif self.table.hand_value(player) < 21:
                    winnings = player.win_bet()
                    print(f"{player.get_name()} won {winnings} dollars")
                else:
                    print(f"{player.get_name()} lost their bet")

        elif dealer_blackjack:
            print("Dealer got blackjack!")
            for player in self.table.get_players().values():
                player_blackjack = self.table.hand_value(player) == 21 and len(player.get_hand()) == 2
                if player_blackjack:
                    player.draw()
                    print(f"{player.get_name()} tied the dealer and got their bet back")
                else:
                    print(f"{player.get_name()} lost their bet")

        else:
            dealers_hand = self.table.hand_value(self.table.dealer)
            for player in self.table.get_players().values():
                player_blackjack = self.table.hand_value(player) == 21 and len(player.get_hand()) == 2
                players_hand = self.table.hand_value(player)
                if player_blackjack:
                    winnings = player.win_blackjack()
                    print(f"{player.get_name()} got blackjack and won {winnings} dollars!")
                elif players_hand > 21 or players_hand < dealers_hand:
                    print(f"{player.get_name()} lost their bet")
                elif players_hand > dealers_hand:
                    winnings = player.win_bet()
                    print(f"{player.get_name()} won {winnings} dollars")
                else:
                    player.draw()
                    print(f"{player.get_name()} tied the dealer and got their bet back")

        print("Current status:")
        losers = []
        for player in self.table.get_players().values():
            if player.money == 0:
                losers.append(player.get_name())
                print(f"{player.get_name()} has lost all their money and left the table")
            else:
                print(player)
        for loser in losers:
            self.table.players.pop(loser)

    def execute(self):
        self.initialize_game()
        while True:
            self.take_bets()
            self.table.initial_deal()
            self.hit_or_stay()
            self.dealers_turn()
            self.results()
            if not self.table.players:
                print("Everyone lost all their money. The game is over")
                break
            keep_going = input("Keep playing? ")
            if keep_going.lower() == "no":
                break
        
        print("Thanks for playing!")
            




app = BlackjackApplication()
app.execute()