"""
Session Tracking and Bankroll Management
Track performance, statistics, and bankroll across sessions
"""

import json
import time
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class HandResult:
    """Result of a single hand"""
    timestamp: float
    bet_amount: float
    profit_loss: float
    player_total: int
    dealer_total: int
    true_count: float
    running_count: int
    action_taken: str
    was_correct_bs: bool  # Was basic strategy followed?
    was_blackjack: bool
    was_bust: bool
    was_surrendered: bool


@dataclass
class SessionStats:
    """Statistics for a playing session"""
    session_id: str
    start_time: float
    end_time: Optional[float]
    starting_bankroll: float
    ending_bankroll: float
    total_hands: int
    hands_won: int
    hands_lost: int
    hands_pushed: int
    blackjacks: int
    busts: int
    surrenders: int
    total_wagered: float
    net_profit_loss: float
    win_rate: float
    hourly_rate: float
    basic_strategy_accuracy: float
    max_bet: float
    min_bet: float
    average_bet: float
    average_true_count: float
    max_true_count: float
    min_true_count: float
    hands_results: List[HandResult]


class SessionTracker:
    """Track blackjack playing sessions and statistics"""

    def __init__(self, starting_bankroll: float = 10000.0):
        self.starting_bankroll = starting_bankroll
        self.current_bankroll = starting_bankroll
        self.session_id = f"session_{int(time.time())}"
        self.start_time = time.time()
        self.end_time: Optional[float] = None

        # Session tracking
        self.hands_results: List[HandResult] = []
        self.total_hands = 0
        self.hands_won = 0
        self.hands_lost = 0
        self.hands_pushed = 0
        self.blackjacks = 0
        self.busts = 0
        self.surrenders = 0
        self.total_wagered = 0.0

        # Basic strategy tracking
        self.basic_strategy_correct = 0
        self.basic_strategy_total = 0

        # Betting tracking
        self.bets: List[float] = []
        self.true_counts: List[float] = []

    def record_hand(self, bet_amount: float, profit_loss: float,
                   player_total: int, dealer_total: int,
                   true_count: float, running_count: int,
                   action_taken: str = "",
                   was_correct_bs: bool = True,
                   was_blackjack: bool = False,
                   was_bust: bool = False,
                   was_surrendered: bool = False):
        """Record the result of a hand"""

        # Update bankroll
        self.current_bankroll += profit_loss

        # Create hand result
        hand_result = HandResult(
            timestamp=time.time(),
            bet_amount=bet_amount,
            profit_loss=profit_loss,
            player_total=player_total,
            dealer_total=dealer_total,
            true_count=true_count,
            running_count=running_count,
            action_taken=action_taken,
            was_correct_bs=was_correct_bs,
            was_blackjack=was_blackjack,
            was_bust=was_bust,
            was_surrendered=was_surrendered
        )

        self.hands_results.append(hand_result)

        # Update statistics
        self.total_hands += 1
        self.total_wagered += bet_amount
        self.bets.append(bet_amount)
        self.true_counts.append(true_count)

        if profit_loss > 0:
            self.hands_won += 1
        elif profit_loss < 0:
            self.hands_lost += 1
        else:
            self.hands_pushed += 1

        if was_blackjack:
            self.blackjacks += 1

        if was_bust:
            self.busts += 1

        if was_surrendered:
            self.surrenders += 1

        # Basic strategy tracking
        self.basic_strategy_total += 1
        if was_correct_bs:
            self.basic_strategy_correct += 1

    def get_win_rate(self) -> float:
        """Calculate win rate percentage"""
        if self.total_hands == 0:
            return 0.0
        return (self.hands_won / self.total_hands) * 100

    def get_net_profit_loss(self) -> float:
        """Get net profit/loss for session"""
        return self.current_bankroll - self.starting_bankroll

    def get_hourly_rate(self) -> float:
        """Calculate hourly win/loss rate"""
        elapsed = time.time() - self.start_time
        hours = elapsed / 3600.0

        if hours == 0:
            return 0.0

        return self.get_net_profit_loss() / hours

    def get_basic_strategy_accuracy(self) -> float:
        """Get basic strategy accuracy percentage"""
        if self.basic_strategy_total == 0:
            return 100.0
        return (self.basic_strategy_correct / self.basic_strategy_total) * 100

    def get_average_bet(self) -> float:
        """Get average bet size"""
        if len(self.bets) == 0:
            return 0.0
        return sum(self.bets) / len(self.bets)

    def get_average_true_count(self) -> float:
        """Get average true count during session"""
        if len(self.true_counts) == 0:
            return 0.0
        return sum(self.true_counts) / len(self.true_counts)

    def get_roi(self) -> float:
        """Calculate return on investment percentage"""
        if self.total_wagered == 0:
            return 0.0
        return (self.get_net_profit_loss() / self.total_wagered) * 100

    def get_hands_per_hour(self) -> float:
        """Calculate hands played per hour"""
        elapsed = time.time() - self.start_time
        hours = elapsed / 3600.0

        if hours == 0:
            return 0.0

        return self.total_hands / hours

    def get_session_stats(self) -> SessionStats:
        """Get comprehensive session statistics"""
        self.end_time = time.time()

        return SessionStats(
            session_id=self.session_id,
            start_time=self.start_time,
            end_time=self.end_time,
            starting_bankroll=self.starting_bankroll,
            ending_bankroll=self.current_bankroll,
            total_hands=self.total_hands,
            hands_won=self.hands_won,
            hands_lost=self.hands_lost,
            hands_pushed=self.hands_pushed,
            blackjacks=self.blackjacks,
            busts=self.busts,
            surrenders=self.surrenders,
            total_wagered=self.total_wagered,
            net_profit_loss=self.get_net_profit_loss(),
            win_rate=self.get_win_rate(),
            hourly_rate=self.get_hourly_rate(),
            basic_strategy_accuracy=self.get_basic_strategy_accuracy(),
            max_bet=max(self.bets) if self.bets else 0.0,
            min_bet=min(self.bets) if self.bets else 0.0,
            average_bet=self.get_average_bet(),
            average_true_count=self.get_average_true_count(),
            max_true_count=max(self.true_counts) if self.true_counts else 0.0,
            min_true_count=min(self.true_counts) if self.true_counts else 0.0,
            hands_results=self.hands_results
        )

    def save_session(self, filepath: str = "sessions.json"):
        """Save session data to file"""
        stats = self.get_session_stats()

        # Convert to dict
        stats_dict = asdict(stats)

        # Load existing sessions
        sessions = []
        if Path(filepath).exists():
            with open(filepath, 'r') as f:
                sessions = json.load(f)

        # Add this session
        sessions.append(stats_dict)

        # Save
        with open(filepath, 'w') as f:
            json.dump(sessions, f, indent=2)

    def print_session_summary(self):
        """Print a formatted session summary"""
        stats = self.get_session_stats()
        elapsed = stats.end_time - stats.start_time if stats.end_time else 0
        hours = elapsed / 3600.0
        minutes = (elapsed % 3600) / 60.0

        print("\n" + "="*60)
        print("SESSION SUMMARY")
        print("="*60)
        print(f"Session ID: {stats.session_id}")
        print(f"Duration: {int(hours)}h {int(minutes)}m")
        print()
        print(f"Starting Bankroll: ${stats.starting_bankroll:,.2f}")
        print(f"Ending Bankroll:   ${stats.ending_bankroll:,.2f}")
        print(f"Net Profit/Loss:   ${stats.net_profit_loss:+,.2f}")
        print(f"ROI:               {self.get_roi():+.2f}%")
        print()
        print(f"Hands Played:      {stats.total_hands}")
        print(f"Hands Won:         {stats.hands_won} ({stats.win_rate:.1f}%)")
        print(f"Hands Lost:        {stats.hands_lost}")
        print(f"Hands Pushed:      {stats.hands_pushed}")
        print(f"Blackjacks:        {stats.blackjacks}")
        print()
        print(f"Total Wagered:     ${stats.total_wagered:,.2f}")
        print(f"Average Bet:       ${stats.average_bet:.2f}")
        print(f"Min Bet:           ${stats.min_bet:.2f}")
        print(f"Max Bet:           ${stats.max_bet:.2f}")
        print()
        print(f"Average True Count: {stats.average_true_count:+.2f}")
        print(f"Max True Count:     {stats.max_true_count:+.2f}")
        print(f"Min True Count:     {stats.min_true_count:+.2f}")
        print()
        print(f"Basic Strategy Accuracy: {stats.basic_strategy_accuracy:.1f}%")
        print(f"Hourly Rate:            ${stats.hourly_rate:+,.2f}/hr")
        print(f"Hands Per Hour:         {self.get_hands_per_hour():.1f}")
        print("="*60)


class BankrollManager:
    """Manage bankroll with risk management rules"""

    def __init__(self, total_bankroll: float, risk_tolerance: str = "medium"):
        """
        Args:
            total_bankroll: Total available bankroll
            risk_tolerance: "conservative", "medium", or "aggressive"
        """
        self.total_bankroll = total_bankroll
        self.current_bankroll = total_bankroll
        self.risk_tolerance = risk_tolerance

        # Set risk parameters based on tolerance
        self._set_risk_parameters()

    def _set_risk_parameters(self):
        """Set parameters based on risk tolerance"""
        if self.risk_tolerance == "conservative":
            self.kelly_fraction = 0.25  # Quarter Kelly
            self.max_bet_percentage = 0.01  # 1% of bankroll
            self.stop_loss_percentage = 0.30  # Stop at 30% loss
            self.stop_win_percentage = 0.50  # Stop at 50% win

        elif self.risk_tolerance == "medium":
            self.kelly_fraction = 0.50  # Half Kelly
            self.max_bet_percentage = 0.02  # 2% of bankroll
            self.stop_loss_percentage = 0.40  # Stop at 40% loss
            self.stop_win_percentage = 0.75  # Stop at 75% win

        else:  # aggressive
            self.kelly_fraction = 0.75  # Three-quarter Kelly
            self.max_bet_percentage = 0.03  # 3% of bankroll
            self.stop_loss_percentage = 0.50  # Stop at 50% loss
            self.stop_win_percentage = 1.00  # Stop at 100% win

    def get_recommended_session_bankroll(self) -> float:
        """Get recommended bankroll for a single session"""
        # Typically 10% of total bankroll per session
        return self.current_bankroll * 0.10

    def get_max_bet(self) -> float:
        """Get maximum bet based on bankroll"""
        return self.current_bankroll * self.max_bet_percentage

    def should_stop_loss(self) -> bool:
        """Check if stop-loss threshold reached"""
        loss = (self.total_bankroll - self.current_bankroll) / self.total_bankroll
        return loss >= self.stop_loss_percentage

    def should_stop_win(self) -> bool:
        """Check if stop-win threshold reached"""
        profit = (self.current_bankroll - self.total_bankroll) / self.total_bankroll
        return profit >= self.stop_win_percentage

    def update_bankroll(self, profit_loss: float):
        """Update current bankroll"""
        self.current_bankroll += profit_loss

    def get_bankroll_status(self) -> dict:
        """Get current bankroll status"""
        profit_loss = self.current_bankroll - self.total_bankroll
        profit_loss_pct = (profit_loss / self.total_bankroll) * 100

        return {
            'total_bankroll': self.total_bankroll,
            'current_bankroll': self.current_bankroll,
            'profit_loss': profit_loss,
            'profit_loss_pct': profit_loss_pct,
            'max_bet': self.get_max_bet(),
            'recommended_session_bankroll': self.get_recommended_session_bankroll(),
            'should_stop_loss': self.should_stop_loss(),
            'should_stop_win': self.should_stop_win(),
        }

    def print_bankroll_status(self):
        """Print formatted bankroll status"""
        status = self.get_bankroll_status()

        print("\n" + "="*50)
        print("BANKROLL STATUS")
        print("="*50)
        print(f"Total Bankroll:     ${status['total_bankroll']:,.2f}")
        print(f"Current Bankroll:   ${status['current_bankroll']:,.2f}")
        print(f"Profit/Loss:        ${status['profit_loss']:+,.2f} ({status['profit_loss_pct']:+.2f}%)")
        print(f"Max Bet Allowed:    ${status['max_bet']:.2f}")
        print(f"Recommended Session: ${status['recommended_session_bankroll']:,.2f}")
        print()

        if status['should_stop_loss']:
            print("⚠️  STOP LOSS THRESHOLD REACHED!")
        if status['should_stop_win']:
            print("✓ STOP WIN TARGET REACHED!")

        print("="*50)
