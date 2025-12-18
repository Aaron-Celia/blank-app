"""
Core Blackjack Game Engine
Handles deck, cards, hands, and game logic with full casino rule support
"""

import random
from enum import Enum
from typing import List, Tuple, Optional
from dataclasses import dataclass


class Suit(Enum):
    HEARTS = "♥"
    DIAMONDS = "♦"
    CLUBS = "♣"
    SPADES = "♠"


class Card:
    """Represents a playing card"""

    def __init__(self, rank: str, suit: Suit):
        self.rank = rank
        self.suit = suit

    def value(self) -> int:
        """Returns the blackjack value of the card"""
        if self.rank in ['J', 'Q', 'K']:
            return 10
        elif self.rank == 'A':
            return 11  # Ace is 11 by default, adjusted in hand calculation
        else:
            return int(self.rank)

    def hi_lo_value(self) -> int:
        """Returns the Hi-Lo counting system value"""
        if self.rank in ['2', '3', '4', '5', '6']:
            return 1
        elif self.rank in ['10', 'J', 'Q', 'K', 'A']:
            return -1
        else:  # 7, 8, 9
            return 0

    def __str__(self):
        return f"{self.rank}{self.suit.value}"

    def __repr__(self):
        return str(self)


class Deck:
    """Represents a shoe of multiple decks"""

    def __init__(self, num_decks: int = 6):
        self.num_decks = num_decks
        self.cards: List[Card] = []
        self.discards: List[Card] = []
        self.cut_card_position = 0
        self.reset()

    def reset(self):
        """Create a fresh shoe and shuffle"""
        self.cards = []
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suits = list(Suit)

        for _ in range(self.num_decks):
            for rank in ranks:
                for suit in suits:
                    self.cards.append(Card(rank, suit))

        self.shuffle()
        # Place cut card at 75% through the shoe (typical casino practice)
        self.cut_card_position = int(len(self.cards) * 0.25)
        self.discards = []

    def shuffle(self):
        """Shuffle the deck"""
        random.shuffle(self.cards)

    def deal_card(self) -> Card:
        """Deal one card from the shoe"""
        if len(self.cards) == 0:
            raise Exception("Deck is empty!")
        card = self.cards.pop()
        self.discards.append(card)
        return card

    def cards_remaining(self) -> int:
        """Returns number of cards left in shoe"""
        return len(self.cards)

    def decks_remaining(self) -> float:
        """Returns approximate number of decks remaining"""
        return len(self.cards) / 52.0

    def needs_shuffle(self) -> bool:
        """Check if cut card has been reached"""
        return len(self.cards) <= self.cut_card_position


class Hand:
    """Represents a blackjack hand"""

    def __init__(self):
        self.cards: List[Card] = []
        self.bet: float = 0
        self.is_split: bool = False
        self.is_doubled: bool = False
        self.is_surrendered: bool = False
        self.is_insured: bool = False

    def add_card(self, card: Card):
        """Add a card to the hand"""
        self.cards.append(card)

    def value(self) -> int:
        """Calculate the best value for the hand"""
        total = 0
        aces = 0

        for card in self.cards:
            if card.rank == 'A':
                aces += 1
                total += 11
            else:
                total += card.value()

        # Adjust for aces
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1

        return total

    def is_soft(self) -> bool:
        """Check if hand is soft (has an ace counted as 11)"""
        total = 0
        aces = 0

        for card in self.cards:
            if card.rank == 'A':
                aces += 1
                total += 11
            else:
                total += card.value()

        # If we have an ace and total <= 21, it's soft
        if aces > 0 and total <= 21:
            return True

        return False

    def is_blackjack(self) -> bool:
        """Check if hand is a natural blackjack"""
        return len(self.cards) == 2 and self.value() == 21

    def is_bust(self) -> bool:
        """Check if hand is busted"""
        return self.value() > 21

    def is_pair(self) -> bool:
        """Check if hand is a pair (for splitting)"""
        if len(self.cards) != 2:
            return False

        # Check if both cards have same rank
        return self.cards[0].rank == self.cards[1].rank

    def can_split(self) -> bool:
        """Check if hand can be split"""
        return self.is_pair() and not self.is_split

    def can_double(self) -> bool:
        """Check if hand can be doubled"""
        return len(self.cards) == 2 and not self.is_doubled

    def __str__(self):
        cards_str = ' '.join(str(card) for card in self.cards)
        value = self.value()
        soft = " (soft)" if self.is_soft() and value <= 21 else ""
        return f"{cards_str} = {value}{soft}"

    def __repr__(self):
        return str(self)


@dataclass
class GameRules:
    """Casino blackjack game rules"""
    num_decks: int = 6
    dealer_hits_soft_17: bool = False  # S17 = False, H17 = True
    blackjack_payout: float = 1.5  # 3:2 = 1.5, 6:5 = 1.2
    can_surrender: bool = True
    can_double_after_split: bool = True
    can_resplit_aces: bool = False
    max_splits: int = 3
    min_bet: float = 10.0
    max_bet: float = 500.0
    penetration: float = 0.75  # How deep into shoe before shuffle


class BlackjackGame:
    """Main blackjack game controller"""

    def __init__(self, rules: GameRules = GameRules()):
        self.rules = rules
        self.deck = Deck(rules.num_decks)
        self.player_hands: List[Hand] = []
        self.dealer_hand: Hand = Hand()
        self.current_hand_index: int = 0

    def new_round(self):
        """Start a new round"""
        if self.deck.needs_shuffle():
            self.deck.reset()

        self.player_hands = [Hand()]
        self.dealer_hand = Hand()
        self.current_hand_index = 0

    def place_bet(self, amount: float):
        """Place initial bet"""
        if amount < self.rules.min_bet or amount > self.rules.max_bet:
            raise ValueError(f"Bet must be between {self.rules.min_bet} and {self.rules.max_bet}")
        self.player_hands[0].bet = amount

    def deal_initial_cards(self):
        """Deal initial two cards to player and dealer"""
        # Deal pattern: player, dealer, player, dealer
        self.player_hands[0].add_card(self.deck.deal_card())
        self.dealer_hand.add_card(self.deck.deal_card())
        self.player_hands[0].add_card(self.deck.deal_card())
        self.dealer_hand.add_card(self.deck.deal_card())

    def get_current_hand(self) -> Hand:
        """Get the current player hand being played"""
        return self.player_hands[self.current_hand_index]

    def hit(self) -> Card:
        """Player hits current hand"""
        hand = self.get_current_hand()
        card = self.deck.deal_card()
        hand.add_card(card)
        return card

    def stand(self):
        """Player stands on current hand"""
        self.current_hand_index += 1

    def double_down(self) -> Card:
        """Player doubles down on current hand"""
        hand = self.get_current_hand()
        if not hand.can_double():
            raise ValueError("Cannot double on this hand")

        hand.bet *= 2
        hand.is_doubled = True
        card = self.deck.deal_card()
        hand.add_card(card)
        self.current_hand_index += 1
        return card

    def split(self) -> Tuple[Hand, Hand]:
        """Split current hand into two hands"""
        hand = self.get_current_hand()
        if not hand.can_split():
            raise ValueError("Cannot split this hand")

        if len(self.player_hands) >= self.rules.max_splits + 1:
            raise ValueError("Maximum splits reached")

        # Create new hand with second card
        new_hand = Hand()
        new_hand.add_card(hand.cards.pop())
        new_hand.bet = hand.bet
        new_hand.is_split = True
        hand.is_split = True

        # Deal new cards to both hands
        hand.add_card(self.deck.deal_card())
        new_hand.add_card(self.deck.deal_card())

        # Insert new hand after current hand
        self.player_hands.insert(self.current_hand_index + 1, new_hand)

        return hand, new_hand

    def surrender(self):
        """Player surrenders current hand"""
        hand = self.get_current_hand()
        if len(hand.cards) != 2:
            raise ValueError("Can only surrender on initial hand")

        hand.is_surrendered = True
        self.current_hand_index += 1

    def insure(self):
        """Player takes insurance"""
        if len(self.dealer_hand.cards) != 2 or self.dealer_hand.cards[0].rank != 'A':
            raise ValueError("Insurance only available when dealer shows Ace")

        hand = self.get_current_hand()
        hand.is_insured = True

    def play_dealer_hand(self):
        """Dealer plays their hand according to rules"""
        # Dealer reveals hole card and plays
        while True:
            value = self.dealer_hand.value()

            if value > 21:
                break

            if value > 17:
                break

            if value == 17:
                # Check if dealer hits soft 17
                if self.rules.dealer_hits_soft_17 and self.dealer_hand.is_soft():
                    self.dealer_hand.add_card(self.deck.deal_card())
                else:
                    break
            else:
                self.dealer_hand.add_card(self.deck.deal_card())

    def resolve_hand(self, hand: Hand) -> float:
        """
        Resolve a hand and return profit/loss
        Positive = win, Negative = loss, 0 = push
        """
        if hand.is_surrendered:
            return -hand.bet * 0.5

        player_value = hand.value()
        dealer_value = self.dealer_hand.value()

        # Player busted
        if player_value > 21:
            return -hand.bet

        # Player blackjack
        if hand.is_blackjack():
            if self.dealer_hand.is_blackjack():
                return 0  # Push
            else:
                return hand.bet * self.rules.blackjack_payout

        # Dealer busted
        if dealer_value > 21:
            return hand.bet

        # Dealer blackjack
        if self.dealer_hand.is_blackjack():
            # Check insurance
            if hand.is_insured:
                # Insurance pays 2:1 on half the bet
                insurance_profit = hand.bet * 0.5
                return -hand.bet + insurance_profit  # Lose main bet, win insurance
            return -hand.bet

        # Compare values
        if player_value > dealer_value:
            return hand.bet
        elif player_value < dealer_value:
            return -hand.bet
        else:
            return 0  # Push

    def is_round_complete(self) -> bool:
        """Check if all player hands have been played"""
        return self.current_hand_index >= len(self.player_hands)
