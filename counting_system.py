"""
Card Counting System - Hi-Lo Method
Includes running count, true count conversion, and count-based betting
"""

from typing import List, Optional
from blackjack_engine import Card, Deck, Hand
import math


class HiLoCounter:
    """
    Hi-Lo Card Counting System

    Card Values:
    2-6: +1
    7-9: 0
    10-A: -1
    """

    def __init__(self):
        self.running_count: int = 0
        self.cards_seen: int = 0
        self.starting_decks: int = 6

    def reset(self, num_decks: int = 6):
        """Reset the count for a new shoe"""
        self.running_count = 0
        self.cards_seen = 0
        self.starting_decks = num_decks

    def count_card(self, card: Card) -> int:
        """
        Count a single card and return its value
        Updates the running count
        """
        value = card.hi_lo_value()
        self.running_count += value
        self.cards_seen += 1
        return value

    def count_cards(self, cards: List[Card]) -> int:
        """Count multiple cards"""
        total = 0
        for card in cards:
            total += self.count_card(card)
        return total

    def get_running_count(self) -> int:
        """Get the current running count"""
        return self.running_count

    def get_true_count(self, decks_remaining: float) -> float:
        """
        Convert running count to true count
        True Count = Running Count / Decks Remaining
        """
        if decks_remaining <= 0:
            return 0

        return self.running_count / decks_remaining

    def get_true_count_from_deck(self, deck: Deck) -> float:
        """Get true count from a deck object"""
        return self.get_true_count(deck.decks_remaining())

    def get_decks_remaining_from_cards(self, cards_remaining: int) -> float:
        """Calculate decks remaining from card count"""
        return cards_remaining / 52.0

    def estimate_edge(self, true_count: float) -> float:
        """
        Estimate player edge based on true count
        Each +1 in true count is approximately +0.5% edge
        """
        return true_count * 0.005

    def get_betting_index(self, true_count: float) -> str:
        """
        Get betting recommendation based on true count
        """
        tc = int(true_count)

        if tc <= 0:
            return "MIN_BET"
        elif tc == 1:
            return "MIN_BET"
        elif tc == 2:
            return "2_UNITS"
        elif tc == 3:
            return "4_UNITS"
        elif tc == 4:
            return "6_UNITS"
        elif tc >= 5:
            return "8_UNITS"
        else:
            return "MIN_BET"

    def should_deviate_from_basic_strategy(self, true_count: float,
                                          player_total: int,
                                          dealer_upcard: int,
                                          is_soft: bool) -> Optional[str]:
        """
        Check if we should deviate from basic strategy based on count
        Returns recommended action if deviation suggested, None otherwise

        Common Hi-Lo Index Plays:
        """
        tc = int(true_count)

        # Insurance index: Take insurance at TC +3 or higher
        if dealer_upcard == 11:  # Ace
            if tc >= 3:
                return "INSURE"

        # 16 vs 10: Stand at TC 0 or higher (instead of hitting)
        if player_total == 16 and dealer_upcard == 10 and not is_soft:
            if tc >= 0:
                return "STAND"

        # 15 vs 10: Stand at TC +4 or higher
        if player_total == 15 and dealer_upcard == 10 and not is_soft:
            if tc >= 4:
                return "STAND"

        # 12 vs 3: Stand at TC +2 or higher
        if player_total == 12 and dealer_upcard == 3:
            if tc >= 2:
                return "STAND"

        # 12 vs 2: Stand at TC +3 or higher
        if player_total == 12 and dealer_upcard == 2:
            if tc >= 3:
                return "STAND"

        # 13 vs 2: Stand at TC -1 or higher (almost always)
        if player_total == 13 and dealer_upcard == 2:
            if tc >= -1:
                return "STAND"

        # 10,10 vs 5: Split at TC +5 or higher (very aggressive)
        if player_total == 20 and dealer_upcard == 5:
            if tc >= 5:
                return "SPLIT"

        # 10,10 vs 6: Split at TC +4 or higher (very aggressive)
        if player_total == 20 and dealer_upcard == 6:
            if tc >= 4:
                return "SPLIT"

        return None


class CountingTracker:
    """Track counting performance and accuracy"""

    def __init__(self):
        self.total_counts: int = 0
        self.correct_counts: int = 0
        self.count_errors: List[int] = []
        self.true_count_errors: List[float] = []
        self.time_per_count: List[float] = []

    def record_count_attempt(self, actual_count: int, guessed_count: int,
                            time_taken: float = 0):
        """Record a counting attempt"""
        self.total_counts += 1
        error = abs(actual_count - guessed_count)

        if error == 0:
            self.correct_counts += 1
        else:
            self.count_errors.append(error)

        if time_taken > 0:
            self.time_per_count.append(time_taken)

    def record_true_count_attempt(self, actual_true_count: float,
                                  guessed_true_count: float):
        """Record a true count conversion attempt"""
        error = abs(actual_true_count - guessed_true_count)
        self.true_count_errors.append(error)

    def get_accuracy(self) -> float:
        """Get counting accuracy percentage"""
        if self.total_counts == 0:
            return 0.0
        return (self.correct_counts / self.total_counts) * 100

    def get_average_error(self) -> float:
        """Get average counting error"""
        if len(self.count_errors) == 0:
            return 0.0
        return sum(self.count_errors) / len(self.count_errors)

    def get_average_time(self) -> float:
        """Get average time per count"""
        if len(self.time_per_count) == 0:
            return 0.0
        return sum(self.time_per_count) / len(self.time_per_count)

    def get_average_true_count_error(self) -> float:
        """Get average true count error"""
        if len(self.true_count_errors) == 0:
            return 0.0
        return sum(self.true_count_errors) / len(self.true_count_errors)

    def get_stats(self) -> dict:
        """Get comprehensive statistics"""
        return {
            'total_attempts': self.total_counts,
            'correct': self.correct_counts,
            'accuracy': self.get_accuracy(),
            'average_error': self.get_average_error(),
            'average_time': self.get_average_time(),
            'average_tc_error': self.get_average_true_count_error()
        }

    def reset(self):
        """Reset all statistics"""
        self.total_counts = 0
        self.correct_counts = 0
        self.count_errors = []
        self.true_count_errors = []
        self.time_per_count = []


class BettingStrategy:
    """
    Advanced betting strategies based on true count
    Includes Kelly Criterion and risk management
    """

    def __init__(self, bankroll: float, risk_tolerance: float = 0.5):
        """
        Args:
            bankroll: Total bankroll available
            risk_tolerance: Fraction of Kelly to bet (0.5 = half Kelly, safer)
        """
        self.bankroll = bankroll
        self.risk_tolerance = risk_tolerance
        self.min_bet = 10.0
        self.max_bet = 500.0

    def kelly_criterion_bet(self, true_count: float, min_bet: float) -> float:
        """
        Calculate optimal bet size using Kelly Criterion

        Kelly % = Edge / Variance
        For blackjack: Edge ≈ TC * 0.5%, Variance ≈ 1.33
        """
        if true_count <= 0:
            return min_bet

        # Estimate edge from true count (0.5% per TC)
        edge = true_count * 0.005

        # Blackjack variance is approximately 1.33
        variance = 1.33

        # Kelly percentage
        kelly_pct = edge / variance

        # Apply risk tolerance (typically 0.5 for half-Kelly)
        adjusted_kelly = kelly_pct * self.risk_tolerance

        # Calculate bet size
        bet = self.bankroll * adjusted_kelly

        # Apply table limits
        bet = max(min_bet, min(bet, self.max_bet))

        # Round to nearest $5 or $10 increment
        bet = round(bet / 10) * 10

        return bet

    def simple_spread_bet(self, true_count: float, min_bet: float,
                         spread: int = 8) -> float:
        """
        Simple betting spread based on true count

        Args:
            true_count: Current true count
            min_bet: Minimum bet amount
            spread: Maximum bet spread (e.g., 1-8 = 8)
        """
        tc = int(true_count)

        if tc <= 0:
            bet_units = 1
        elif tc == 1:
            bet_units = 1
        elif tc == 2:
            bet_units = 2
        elif tc == 3:
            bet_units = 4
        elif tc == 4:
            bet_units = 6
        elif tc >= 5:
            bet_units = min(8, spread)
        else:
            bet_units = 1

        bet = min_bet * bet_units
        bet = max(self.min_bet, min(bet, self.max_bet))

        return bet

    def wong_halves_exit(self, true_count: float) -> bool:
        """
        Determine if player should exit table (Wong out)
        Exit when count is very negative
        """
        return true_count <= -2

    def update_bankroll(self, profit_loss: float):
        """Update bankroll after a session"""
        self.bankroll += profit_loss

    def get_risk_of_ruin(self, win_rate: float, avg_bet: float,
                        sessions: int = 100) -> float:
        """
        Estimate risk of ruin (losing entire bankroll)

        Simplified calculation using bankroll, average bet, and win rate
        """
        if avg_bet == 0:
            return 0.0

        # Calculate required bankroll units
        bankroll_units = self.bankroll / avg_bet

        # Risk of ruin approximation
        if win_rate <= 0:
            return 100.0

        # Using simplified formula
        ror = math.exp(-2 * win_rate * bankroll_units)
        return min(100.0, ror * 100)

    def optimal_bet_size(self, true_count: float, use_kelly: bool = True) -> float:
        """
        Get optimal bet size based on strategy

        Args:
            true_count: Current true count
            use_kelly: Use Kelly Criterion (True) or simple spread (False)
        """
        if use_kelly:
            return self.kelly_criterion_bet(true_count, self.min_bet)
        else:
            return self.simple_spread_bet(true_count, self.min_bet)
