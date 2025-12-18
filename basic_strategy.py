"""
Blackjack Basic Strategy Engine
Perfect basic strategy for S17 and H17 variations
Includes strategy for hard hands, soft hands, pairs, and surrender
"""

from enum import Enum
from typing import Optional
from blackjack_engine import Hand, Card, GameRules


class Action(Enum):
    """Possible player actions"""
    HIT = "H"
    STAND = "S"
    DOUBLE = "D"
    SPLIT = "SP"
    SURRENDER = "SR"
    DOUBLE_OR_HIT = "DH"  # Double if allowed, otherwise hit
    DOUBLE_OR_STAND = "DS"  # Double if allowed, otherwise stand
    SPLIT_IF_DAS = "SPD"  # Split if double after split allowed


class BasicStrategy:
    """
    Perfect basic strategy for blackjack
    Optimized for 6-deck S17 and H17 variations
    """

    def __init__(self, dealer_hits_soft_17: bool = False,
                 can_surrender: bool = True,
                 double_after_split: bool = True):
        self.dealer_hits_soft_17 = dealer_hits_soft_17
        self.can_surrender = can_surrender
        self.double_after_split = double_after_split

        # Initialize strategy tables
        self._init_hard_totals()
        self._init_soft_totals()
        self._init_pair_splitting()
        self._init_surrender()

    def _init_hard_totals(self):
        """Initialize hard total strategy table"""
        # Hard totals strategy (player total, dealer upcard)
        # Format: {player_total: {dealer_upcard: action}}

        self.hard_strategy = {
            # 5-8: Always hit
            5: {2: Action.HIT, 3: Action.HIT, 4: Action.HIT, 5: Action.HIT, 6: Action.HIT,
                7: Action.HIT, 8: Action.HIT, 9: Action.HIT, 10: Action.HIT, 11: Action.HIT},
            6: {2: Action.HIT, 3: Action.HIT, 4: Action.HIT, 5: Action.HIT, 6: Action.HIT,
                7: Action.HIT, 8: Action.HIT, 9: Action.HIT, 10: Action.HIT, 11: Action.HIT},
            7: {2: Action.HIT, 3: Action.HIT, 4: Action.HIT, 5: Action.HIT, 6: Action.HIT,
                7: Action.HIT, 8: Action.HIT, 9: Action.HIT, 10: Action.HIT, 11: Action.HIT},
            8: {2: Action.HIT, 3: Action.HIT, 4: Action.HIT, 5: Action.HIT, 6: Action.HIT,
                7: Action.HIT, 8: Action.HIT, 9: Action.HIT, 10: Action.HIT, 11: Action.HIT},

            # 9: Double on 3-6, otherwise hit
            9: {2: Action.HIT, 3: Action.DOUBLE_OR_HIT, 4: Action.DOUBLE_OR_HIT,
                5: Action.DOUBLE_OR_HIT, 6: Action.DOUBLE_OR_HIT, 7: Action.HIT,
                8: Action.HIT, 9: Action.HIT, 10: Action.HIT, 11: Action.HIT},

            # 10: Double on 2-9, hit on 10/A
            10: {2: Action.DOUBLE_OR_HIT, 3: Action.DOUBLE_OR_HIT, 4: Action.DOUBLE_OR_HIT,
                 5: Action.DOUBLE_OR_HIT, 6: Action.DOUBLE_OR_HIT, 7: Action.DOUBLE_OR_HIT,
                 8: Action.DOUBLE_OR_HIT, 9: Action.DOUBLE_OR_HIT, 10: Action.HIT, 11: Action.HIT},

            # 11: Double on 2-10, hit on A (S17) or double on all (H17)
            11: {2: Action.DOUBLE_OR_HIT, 3: Action.DOUBLE_OR_HIT, 4: Action.DOUBLE_OR_HIT,
                 5: Action.DOUBLE_OR_HIT, 6: Action.DOUBLE_OR_HIT, 7: Action.DOUBLE_OR_HIT,
                 8: Action.DOUBLE_OR_HIT, 9: Action.DOUBLE_OR_HIT, 10: Action.DOUBLE_OR_HIT,
                 11: Action.DOUBLE_OR_HIT if self.dealer_hits_soft_17 else Action.HIT},

            # 12: Stand on 4-6, hit on 2-3, 7-A
            12: {2: Action.HIT, 3: Action.HIT, 4: Action.STAND, 5: Action.STAND,
                 6: Action.STAND, 7: Action.HIT, 8: Action.HIT, 9: Action.HIT,
                 10: Action.HIT, 11: Action.HIT},

            # 13-16: Stand on 2-6, hit on 7-A
            13: {2: Action.STAND, 3: Action.STAND, 4: Action.STAND, 5: Action.STAND,
                 6: Action.STAND, 7: Action.HIT, 8: Action.HIT, 9: Action.HIT,
                 10: Action.HIT, 11: Action.HIT},
            14: {2: Action.STAND, 3: Action.STAND, 4: Action.STAND, 5: Action.STAND,
                 6: Action.STAND, 7: Action.HIT, 8: Action.HIT, 9: Action.HIT,
                 10: Action.HIT, 11: Action.HIT},
            15: {2: Action.STAND, 3: Action.STAND, 4: Action.STAND, 5: Action.STAND,
                 6: Action.STAND, 7: Action.HIT, 8: Action.HIT, 9: Action.HIT,
                 10: Action.HIT, 11: Action.HIT},
            16: {2: Action.STAND, 3: Action.STAND, 4: Action.STAND, 5: Action.STAND,
                 6: Action.STAND, 7: Action.HIT, 8: Action.HIT, 9: Action.HIT,
                 10: Action.HIT, 11: Action.HIT},

            # 17+: Always stand
            17: {2: Action.STAND, 3: Action.STAND, 4: Action.STAND, 5: Action.STAND,
                 6: Action.STAND, 7: Action.STAND, 8: Action.STAND, 9: Action.STAND,
                 10: Action.STAND, 11: Action.STAND},
            18: {2: Action.STAND, 3: Action.STAND, 4: Action.STAND, 5: Action.STAND,
                 6: Action.STAND, 7: Action.STAND, 8: Action.STAND, 9: Action.STAND,
                 10: Action.STAND, 11: Action.STAND},
            19: {2: Action.STAND, 3: Action.STAND, 4: Action.STAND, 5: Action.STAND,
                 6: Action.STAND, 7: Action.STAND, 8: Action.STAND, 9: Action.STAND,
                 10: Action.STAND, 11: Action.STAND},
            20: {2: Action.STAND, 3: Action.STAND, 4: Action.STAND, 5: Action.STAND,
                 6: Action.STAND, 7: Action.STAND, 8: Action.STAND, 9: Action.STAND,
                 10: Action.STAND, 11: Action.STAND},
            21: {2: Action.STAND, 3: Action.STAND, 4: Action.STAND, 5: Action.STAND,
                 6: Action.STAND, 7: Action.STAND, 8: Action.STAND, 9: Action.STAND,
                 10: Action.STAND, 11: Action.STAND},
        }

    def _init_soft_totals(self):
        """Initialize soft total strategy table"""
        # Soft totals (A,2 through A,9)

        self.soft_strategy = {
            # Soft 13-14 (A,2 - A,3): Double on 5-6, otherwise hit
            13: {2: Action.HIT, 3: Action.HIT, 4: Action.HIT, 5: Action.DOUBLE_OR_HIT,
                 6: Action.DOUBLE_OR_HIT, 7: Action.HIT, 8: Action.HIT, 9: Action.HIT,
                 10: Action.HIT, 11: Action.HIT},
            14: {2: Action.HIT, 3: Action.HIT, 4: Action.HIT, 5: Action.DOUBLE_OR_HIT,
                 6: Action.DOUBLE_OR_HIT, 7: Action.HIT, 8: Action.HIT, 9: Action.HIT,
                 10: Action.HIT, 11: Action.HIT},

            # Soft 15-16 (A,4 - A,5): Double on 4-6, otherwise hit
            15: {2: Action.HIT, 3: Action.HIT, 4: Action.DOUBLE_OR_HIT, 5: Action.DOUBLE_OR_HIT,
                 6: Action.DOUBLE_OR_HIT, 7: Action.HIT, 8: Action.HIT, 9: Action.HIT,
                 10: Action.HIT, 11: Action.HIT},
            16: {2: Action.HIT, 3: Action.HIT, 4: Action.DOUBLE_OR_HIT, 5: Action.DOUBLE_OR_HIT,
                 6: Action.DOUBLE_OR_HIT, 7: Action.HIT, 8: Action.HIT, 9: Action.HIT,
                 10: Action.HIT, 11: Action.HIT},

            # Soft 17 (A,6): Double on 3-6, otherwise hit
            17: {2: Action.HIT, 3: Action.DOUBLE_OR_HIT, 4: Action.DOUBLE_OR_HIT,
                 5: Action.DOUBLE_OR_HIT, 6: Action.DOUBLE_OR_HIT, 7: Action.HIT,
                 8: Action.HIT, 9: Action.HIT, 10: Action.HIT, 11: Action.HIT},

            # Soft 18 (A,7): Stand on 2,7,8, Double on 3-6, Hit on 9-A
            18: {2: Action.STAND if not self.dealer_hits_soft_17 else Action.DOUBLE_OR_STAND,
                 3: Action.DOUBLE_OR_STAND, 4: Action.DOUBLE_OR_STAND,
                 5: Action.DOUBLE_OR_STAND, 6: Action.DOUBLE_OR_STAND,
                 7: Action.STAND, 8: Action.STAND, 9: Action.HIT, 10: Action.HIT,
                 11: Action.HIT if not self.dealer_hits_soft_17 else Action.HIT},

            # Soft 19-21: Always stand
            19: {2: Action.STAND, 3: Action.STAND, 4: Action.STAND, 5: Action.STAND,
                 6: Action.STAND, 7: Action.STAND, 8: Action.STAND, 9: Action.STAND,
                 10: Action.STAND, 11: Action.STAND},
            20: {2: Action.STAND, 3: Action.STAND, 4: Action.STAND, 5: Action.STAND,
                 6: Action.STAND, 7: Action.STAND, 8: Action.STAND, 9: Action.STAND,
                 10: Action.STAND, 11: Action.STAND},
            21: {2: Action.STAND, 3: Action.STAND, 4: Action.STAND, 5: Action.STAND,
                 6: Action.STAND, 7: Action.STAND, 8: Action.STAND, 9: Action.STAND,
                 10: Action.STAND, 11: Action.STAND},
        }

    def _init_pair_splitting(self):
        """Initialize pair splitting strategy table"""
        # Pair splitting strategy

        self.pair_strategy = {
            # 2,2 and 3,3: Split on 2-7
            '2': {2: Action.SPLIT if self.double_after_split else Action.HIT,
                  3: Action.SPLIT if self.double_after_split else Action.HIT,
                  4: Action.SPLIT, 5: Action.SPLIT, 6: Action.SPLIT, 7: Action.SPLIT,
                  8: Action.HIT, 9: Action.HIT, 10: Action.HIT, 11: Action.HIT},
            '3': {2: Action.SPLIT if self.double_after_split else Action.HIT,
                  3: Action.SPLIT if self.double_after_split else Action.HIT,
                  4: Action.SPLIT, 5: Action.SPLIT, 6: Action.SPLIT, 7: Action.SPLIT,
                  8: Action.HIT, 9: Action.HIT, 10: Action.HIT, 11: Action.HIT},

            # 4,4: Split on 5-6 if DAS, otherwise hit
            '4': {2: Action.HIT, 3: Action.HIT, 4: Action.HIT,
                  5: Action.SPLIT if self.double_after_split else Action.HIT,
                  6: Action.SPLIT if self.double_after_split else Action.HIT,
                  7: Action.HIT, 8: Action.HIT, 9: Action.HIT, 10: Action.HIT, 11: Action.HIT},

            # 5,5: Never split, treat as 10
            '5': {2: Action.DOUBLE_OR_HIT, 3: Action.DOUBLE_OR_HIT, 4: Action.DOUBLE_OR_HIT,
                  5: Action.DOUBLE_OR_HIT, 6: Action.DOUBLE_OR_HIT, 7: Action.DOUBLE_OR_HIT,
                  8: Action.DOUBLE_OR_HIT, 9: Action.DOUBLE_OR_HIT, 10: Action.HIT, 11: Action.HIT},

            # 6,6: Split on 2-6 (with DAS)
            '6': {2: Action.SPLIT if self.double_after_split else Action.HIT,
                  3: Action.SPLIT, 4: Action.SPLIT, 5: Action.SPLIT, 6: Action.SPLIT,
                  7: Action.HIT, 8: Action.HIT, 9: Action.HIT, 10: Action.HIT, 11: Action.HIT},

            # 7,7: Split on 2-7
            '7': {2: Action.SPLIT, 3: Action.SPLIT, 4: Action.SPLIT, 5: Action.SPLIT,
                  6: Action.SPLIT, 7: Action.SPLIT, 8: Action.HIT, 9: Action.HIT,
                  10: Action.HIT, 11: Action.HIT},

            # 8,8: Always split
            '8': {2: Action.SPLIT, 3: Action.SPLIT, 4: Action.SPLIT, 5: Action.SPLIT,
                  6: Action.SPLIT, 7: Action.SPLIT, 8: Action.SPLIT, 9: Action.SPLIT,
                  10: Action.SPLIT, 11: Action.SPLIT},

            # 9,9: Split on 2-9 except 7, stand on 7,10,A
            '9': {2: Action.SPLIT, 3: Action.SPLIT, 4: Action.SPLIT, 5: Action.SPLIT,
                  6: Action.SPLIT, 7: Action.STAND, 8: Action.SPLIT, 9: Action.SPLIT,
                  10: Action.STAND, 11: Action.STAND},

            # 10,10: Never split
            '10': {2: Action.STAND, 3: Action.STAND, 4: Action.STAND, 5: Action.STAND,
                   6: Action.STAND, 7: Action.STAND, 8: Action.STAND, 9: Action.STAND,
                   10: Action.STAND, 11: Action.STAND},
            'J': {2: Action.STAND, 3: Action.STAND, 4: Action.STAND, 5: Action.STAND,
                  6: Action.STAND, 7: Action.STAND, 8: Action.STAND, 9: Action.STAND,
                  10: Action.STAND, 11: Action.STAND},
            'Q': {2: Action.STAND, 3: Action.STAND, 4: Action.STAND, 5: Action.STAND,
                  6: Action.STAND, 7: Action.STAND, 8: Action.STAND, 9: Action.STAND,
                  10: Action.STAND, 11: Action.STAND},
            'K': {2: Action.STAND, 3: Action.STAND, 4: Action.STAND, 5: Action.STAND,
                  6: Action.STAND, 7: Action.STAND, 8: Action.STAND, 9: Action.STAND,
                  10: Action.STAND, 11: Action.STAND},

            # A,A: Always split
            'A': {2: Action.SPLIT, 3: Action.SPLIT, 4: Action.SPLIT, 5: Action.SPLIT,
                  6: Action.SPLIT, 7: Action.SPLIT, 8: Action.SPLIT, 9: Action.SPLIT,
                  10: Action.SPLIT, 11: Action.SPLIT},
        }

    def _init_surrender(self):
        """Initialize surrender strategy"""
        # Surrender strategy (only for initial two cards)
        # Format: {player_total: [dealer_upcards_to_surrender_against]}

        self.surrender_strategy = {
            15: [10] if self.can_surrender else [],  # Surrender 15 vs 10
            16: [9, 10, 11] if self.can_surrender else [],  # Surrender 16 vs 9,10,A
            17: [11] if self.can_surrender and self.dealer_hits_soft_17 else [],  # Surrender 17 vs A (H17 only)
        }

    def get_action(self, hand: Hand, dealer_upcard: Card,
                   can_double: bool = True, can_split: bool = True,
                   can_surrender: bool = True) -> Action:
        """
        Get the correct basic strategy action for a hand

        Args:
            hand: Player's hand
            dealer_upcard: Dealer's visible card
            can_double: Whether doubling is allowed
            can_split: Whether splitting is allowed
            can_surrender: Whether surrender is allowed

        Returns:
            The optimal action according to basic strategy
        """
        dealer_value = dealer_upcard.value()
        player_value = hand.value()

        # Check for surrender first (only on initial two cards)
        if can_surrender and len(hand.cards) == 2 and not hand.is_soft():
            if player_value in self.surrender_strategy:
                if dealer_value in self.surrender_strategy[player_value]:
                    return Action.SURRENDER

        # Check for pair splitting
        if can_split and hand.is_pair():
            rank = hand.cards[0].rank
            action = self.pair_strategy.get(rank, {}).get(dealer_value, Action.HIT)

            # Handle conditional actions
            if action == Action.SPLIT:
                return Action.SPLIT
            # If not splitting, fall through to hard/soft strategy

        # Check if hand is soft
        if hand.is_soft() and player_value <= 21:
            action = self.soft_strategy.get(player_value, {}).get(dealer_value, Action.STAND)
        else:
            # Hard total
            action = self.hard_strategy.get(player_value, {}).get(dealer_value, Action.STAND)

        # Handle conditional actions based on what's allowed
        if action == Action.DOUBLE_OR_HIT:
            return Action.DOUBLE if can_double else Action.HIT
        elif action == Action.DOUBLE_OR_STAND:
            return Action.DOUBLE if can_double else Action.STAND

        return action

    def get_action_string(self, action: Action) -> str:
        """Convert action to readable string"""
        action_map = {
            Action.HIT: "Hit",
            Action.STAND: "Stand",
            Action.DOUBLE: "Double Down",
            Action.SPLIT: "Split",
            Action.SURRENDER: "Surrender",
            Action.DOUBLE_OR_HIT: "Double (or Hit)",
            Action.DOUBLE_OR_STAND: "Double (or Stand)",
        }
        return action_map.get(action, str(action))

    def is_correct_action(self, hand: Hand, dealer_upcard: Card,
                         player_action: Action,
                         can_double: bool = True,
                         can_split: bool = True,
                         can_surrender: bool = True) -> bool:
        """
        Check if player's action matches basic strategy

        Returns:
            True if action is correct, False otherwise
        """
        correct_action = self.get_action(hand, dealer_upcard, can_double,
                                        can_split, can_surrender)

        # Handle equivalent actions
        if player_action == correct_action:
            return True

        # DOUBLE_OR_HIT accepts both DOUBLE and HIT
        if correct_action == Action.DOUBLE_OR_HIT:
            return player_action in [Action.DOUBLE, Action.HIT]

        # DOUBLE_OR_STAND accepts both DOUBLE and STAND
        if correct_action == Action.DOUBLE_OR_STAND:
            return player_action in [Action.DOUBLE, Action.STAND]

        return False
