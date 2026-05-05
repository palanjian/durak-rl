from collections import deque
import random
import logging

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __repr__(self):
        return f"<{self.rank_repr()}{self.suit_repr()}>"

    def rank_repr(self):
        faces = ["J", "Q", "K", "A"]
        if self.rank <= 10: return str(self.rank)
        return faces[self.rank-11]
    
    def suit_repr(self):
        suits = {"Hearts":"♥","Diamonds":"♦","Clubs":"♣","Spades":"♠"}
        return suits[self.suit]

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
        self.attack_pile, self.defend_pile = [], []

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
                hand.append(card)
            self.hands.append(hand)
        
        self.attacker = attacker
        self.defender = (attacker+1) % self.num_players

    def get_next_attacker(self):
        """Returns None if round is over (all players have thrown cards)"""
        attacker = (self.attacker + 1) % self.num_players
        if attacker == self.defender: 
            return None
        
        logging.log(f"Next attacker is {attacker}")
        return attacker

    def attack(self, card: Card):
        """Returns True if legal, False if illegal (too many cards or rank doesn't match)"""
        assert card
        # make sure # attacking hands <= # defender's cards
        if len(self.attack_pile) + 1 > len(self.hands[self.defender]) + len(self.defend_pile):
            logging.log(f"Too many cards. Cannot throw {card}")
            return False
        
        # make sure rank exists on the current board
        if card.rank not in {c.rank for c in self.attack_pile} and \
            card.rank not in {c.rank for c in self.defend_pile}:
            logging.log(f"Cannot throw {card}. {card.rank} does not exist in defender hands: \
                        {self.defend_pile} or attacker hands: {self.attack_pile}")
            return False
        
        logging.log(f"Appended {card} to the attacking pile")
        self.attack_pile.append(card)
        self.hands[self.attacker].remove(card)

        return True

    def defend(self, card: Card, index : int):
        """Returns True if legal, False if illegal (index invalid, suit not equivalent, rank not larger)"""
        assert card
        # ensure card at index exists
        if index < 0 or index >= len(self.attack_pile):
            return False
        
        to_defend_against = self.attack_pile[index]

        if card.rank < to_defend_against.rank:
            logging.log(f"Can not defend {to_defend_against} with a {card}. Rank too low.")
            return False

        # if defender is defending with a trump card, suit doesn't matter, only rank
        if card.suit != to_defend_against.suit and card.suit != self.trump_suit:
            logging.log(f"Can not defend {to_defend_against} with a {card}. Suit not equivalent.")
            return False
        
        self.defend_pile.append(card)
        self.hands[self.defender].remove(card)

        return True


    def bita(self):
        # clear hands on board and pass out new cards in order
        pass

    def get_legal_throws(self):
        # for RL
        pass

    def __repr__(self):
        title_str = f"<Durak {self.num_cards}-card | trump: {self.trump_suit} | deck size: {len(self.deck)}>"
        hands_str = "\n".join(
            f"  P{i} {'[ATK]' if i == self.attacker else '[DEF]' if i == self.defender else '     '}: "
            f"{self.hands[i]}"
            for i in range(self.num_players)
        )
        piles_str = "I need to repr attacker & defender piles"
        return f"{title_str}\n{hands_str}\n{piles_str}"
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    game = Durak(num_cards=36, num_players=4)
    print(game)


    

