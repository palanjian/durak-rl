from collections import deque, namedtuple
import random
import logging

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __repr__(self):
        return f"<{self.suit} {self.rank_repr()}>"

    def rank_repr(self):
        faces = ["J", "K", "Q", "A"]
        if self.rank <= 10: return str(self.rank)
        return faces[self.rank-11]
    
class Durak:
    def __init__(self, num_players=2, num_cards=36):
        self.num_players = num_players
        self.num_cards = num_cards

        # Shuffle self.deck & declare self.trump_suit
        self.initialize_deck()

        # Deal each player 6 cards & find first self.defender / self.attacker
        self.hands = []
        self.deal_cards()

        # Define hands on the board
        self.attacker_hands, self.defender_hands = [], []

    def initialize_deck(self):
        assert self.num_cards in (24, 36, 52), \
            "Only 24, 36, or 52 card decks are supported."
        
        lowest = {24: 9, 36: 6, 52: 2}[self.num_cards]

        ranks = range(lowest, 15)  # 6 to Ace (14)
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']

        cards = [Card(suit, rank) for rank in ranks for suit in suits]
        random.shuffle(cards)

        # Durak rules prohibit an Ace from being the bottom card
        while(cards[-1].rank == 14): random.shuffle(cards)

        self.trump_suit = cards[-1].suit
        self.deck = deque(cards)

        logging.info(f"The trump card is: {cards[-1]}")
    
    def deal_cards(self):
        assert self.num_players > 1 and self.num_players <= 6, \
            "Invalid number of players"
        assert self.num_players * 6 <= self.num_cards, \
            "Not enough cards to deal for number of players"

        # Player with the lowest trump card is the first attacker
        lowest, attacker = 15, 0

        for player in range(self.num_players):
            hand = []
            for _ in range(6):
                card = self.deck.pop()
                if card.suit == self.trump_suit and card.rank < lowest:
                    lowest, attacker = card.rank, player
            self.hands.append(hand)
        
        self.attacker = attacker
        self.defender = (attacker+1) % self.num_players

    def attack():
        # put check to make sure # attacking hands <= # defender's cards
        pass

    def defend():
        pass

    def bita():
        # clear hands on board and pass out new cards in order
        pass

    

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    durak = Durak(num_cards=36, num_players=4)
    print(durak.deck)
    

