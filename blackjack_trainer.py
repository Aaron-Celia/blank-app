#!/usr/bin/env python3
"""
Blackjack Card Counting Training Suite
Complete training system for mastering card counting and basic strategy
"""

import sys
from blackjack_engine import GameRules
from training_modes import SpeedCountTrainer, BasicStrategyTrainer, FullGameSimulator
from session_tracker import BankrollManager


def print_banner():
    """Print application banner"""
    print("\n" + "="*70)
    print("  BLACKJACK CARD COUNTING TRAINING SUITE")
    print("  Master the Hi-Lo System & Perfect Basic Strategy")
    print("="*70)


def print_menu():
    """Print main menu"""
    print("\n" + "-"*70)
    print("MAIN MENU")
    print("-"*70)
    print("1. Card Counting Training")
    print("2. Basic Strategy Training")
    print("3. Full Game Simulator")
    print("4. Bankroll Management Tools")
    print("5. Game Rules Configuration")
    print("6. View Statistics")
    print("7. Help & Strategy Guide")
    print("0. Exit")
    print("-"*70)


def counting_menu():
    """Card counting training submenu"""
    print("\n" + "-"*70)
    print("CARD COUNTING TRAINING")
    print("-"*70)
    print("1. Single Card Drill - Practice counting individual cards")
    print("2. Running Count Drill - Maintain running count")
    print("3. True Count Conversion - Practice TC calculations")
    print("4. Speed Challenge - Count as fast as possible")
    print("0. Back to Main Menu")
    print("-"*70)

    choice = input("\nSelect option: ").strip()

    trainer = SpeedCountTrainer(num_decks=6)

    if choice == '1':
        num_cards = input("How many cards? (default 52): ").strip()
        num_cards = int(num_cards) if num_cards else 52
        trainer.single_card_drill(num_cards)

    elif choice == '2':
        num_rounds = input("How many rounds? (default 10): ").strip()
        num_rounds = int(num_rounds) if num_rounds else 10
        trainer.running_count_drill(num_rounds)

    elif choice == '3':
        num_rounds = input("How many rounds? (default 10): ").strip()
        num_rounds = int(num_rounds) if num_rounds else 10
        trainer.true_count_drill(num_rounds)

    elif choice == '4':
        print("\nSpeed Challenge: Count a full deck as fast as possible!")
        print("The final count should be 0 for a balanced count.")
        input("Press Enter to start...")
        trainer.single_card_drill(52)


def basic_strategy_menu(rules):
    """Basic strategy training submenu"""
    print("\n" + "-"*70)
    print("BASIC STRATEGY TRAINING")
    print("-"*70)
    print("1. Quiz Mode - Test your knowledge")
    print("2. Practice Mode - Continuous practice with feedback")
    print("3. View Strategy Charts")
    print("0. Back to Main Menu")
    print("-"*70)

    choice = input("\nSelect option: ").strip()

    trainer = BasicStrategyTrainer(dealer_hits_soft_17=rules.dealer_hits_soft_17)

    if choice == '1':
        num_questions = input("How many questions? (default 20): ").strip()
        num_questions = int(num_questions) if num_questions else 20
        trainer.quiz_mode(num_questions)

    elif choice == '2':
        trainer.practice_mode()

    elif choice == '3':
        print_strategy_charts(rules)


def print_strategy_charts(rules):
    """Print basic strategy charts"""
    print("\n" + "="*70)
    print(f"BASIC STRATEGY CHART ({'H17' if rules.dealer_hits_soft_17 else 'S17'})")
    print("="*70)
    print("\nHARD TOTALS:")
    print("-" * 70)
    print("Your Hand | 2  3  4  5  6  7  8  9  10  A")
    print("-" * 70)
    print("   8      | H  H  H  H  H  H  H  H   H  H")
    print("   9      | H  D  D  D  D  H  H  H   H  H")
    print("   10     | D  D  D  D  D  D  D  D   H  H")
    print("   11     | D  D  D  D  D  D  D  D   D  H  (H17: D vs A)")
    print("   12     | H  H  S  S  S  H  H  H   H  H")
    print("  13-16   | S  S  S  S  S  H  H  H   H  H")
    print("  17+     | S  S  S  S  S  S  S  S   S  S")
    print()
    print("SOFT TOTALS (with Ace):")
    print("-" * 70)
    print("Your Hand | 2  3  4  5  6  7  8  9  10  A")
    print("-" * 70)
    print("  A,2-A,3 | H  H  H  D  D  H  H  H   H  H")
    print("  A,4-A,5 | H  H  D  D  D  H  H  H   H  H")
    print("    A,6   | H  D  D  D  D  H  H  H   H  H")
    print("    A,7   | S  D  D  D  D  S  S  H   H  H")
    print("  A,8-A,9 | S  S  S  S  S  S  S  S   S  S")
    print()
    print("PAIRS:")
    print("-" * 70)
    print("Your Hand | 2  3  4  5  6  7  8  9  10  A")
    print("-" * 70)
    print("   2,2    | SP SP SP SP SP SP H  H   H  H  (with DAS)")
    print("   3,3    | SP SP SP SP SP SP H  H   H  H  (with DAS)")
    print("   4,4    | H  H  H  SP SP H  H  H   H  H  (with DAS)")
    print("   5,5    | D  D  D  D  D  D  D  D   H  H  (never split)")
    print("   6,6    | SP SP SP SP SP H  H  H   H  H  (with DAS)")
    print("   7,7    | SP SP SP SP SP SP H  H   H  H")
    print("   8,8    | SP SP SP SP SP SP SP SP  SP SP  (always split)")
    print("   9,9    | SP SP SP SP SP S  SP SP  S  S")
    print("  10,10   | S  S  S  S  S  S  S  S   S  S  (never split)")
    print("   A,A    | SP SP SP SP SP SP SP SP  SP SP  (always split)")
    print()
    print("SURRENDER (if allowed):")
    print("-" * 70)
    print("  15 vs 10")
    print("  16 vs 9, 10, A")
    print("="*70)


def full_game_menu(rules):
    """Full game simulator menu"""
    print("\n" + "-"*70)
    print("FULL GAME SIMULATOR")
    print("-"*70)
    print("Play realistic blackjack with counting and betting strategy.")
    print()

    bankroll = input("Starting bankroll (default $10,000): $").strip()
    bankroll = float(bankroll) if bankroll else 10000.0

    show_hints = input("Show count and recommendations? (y/n, default y): ").strip().lower()
    show_hints = show_hints != 'n'

    simulator = FullGameSimulator(rules, bankroll)
    simulator.show_count = show_hints

    simulator.play_session()


def bankroll_menu():
    """Bankroll management menu"""
    print("\n" + "-"*70)
    print("BANKROLL MANAGEMENT TOOLS")
    print("-"*70)
    print()

    bankroll = input("Total bankroll: $").strip()
    if not bankroll:
        return

    bankroll = float(bankroll)

    print("\nRisk Tolerance:")
    print("1. Conservative (safer, smaller bets)")
    print("2. Medium (balanced approach)")
    print("3. Aggressive (higher variance, bigger bets)")

    risk_choice = input("Select (1-3, default 2): ").strip()
    risk_map = {'1': 'conservative', '2': 'medium', '3': 'aggressive'}
    risk = risk_map.get(risk_choice, 'medium')

    manager = BankrollManager(bankroll, risk_tolerance=risk)
    manager.print_bankroll_status()

    print("\nRECOMMENDATIONS:")
    print("-" * 70)
    status = manager.get_bankroll_status()
    print(f"Recommended session bankroll: ${status['recommended_session_bankroll']:,.2f}")
    print(f"Maximum single bet: ${status['max_bet']:.2f}")
    print(f"Minimum bet (table minimum): $10-25")
    print()
    print("Betting Spread Guidelines:")
    print("  True Count <= 1: Min bet ($10-25)")
    print("  True Count = 2:  2-3 units")
    print("  True Count = 3:  4-5 units")
    print("  True Count = 4:  6-8 units")
    print("  True Count >= 5: 8-12 units (max)")
    print()
    print("Stop-Loss Thresholds:")
    print(f"  Exit if down: {manager.stop_loss_percentage * 100:.0f}%")
    print(f"  Exit if up: {manager.stop_win_percentage * 100:.0f}%")


def rules_configuration_menu():
    """Configure game rules"""
    print("\n" + "-"*70)
    print("GAME RULES CONFIGURATION")
    print("-"*70)
    print()

    num_decks = input("Number of decks (default 6): ").strip()
    num_decks = int(num_decks) if num_decks else 6

    print("\nDealer rule:")
    print("1. S17 (Dealer stands on soft 17) - Better for player")
    print("2. H17 (Dealer hits soft 17) - Worse for player")
    dealer_rule = input("Select (1-2, default 1): ").strip()
    dealer_hits_s17 = (dealer_rule == '2')

    print("\nBlackjack payout:")
    print("1. 3:2 (pays 1.5x) - Standard")
    print("2. 6:5 (pays 1.2x) - Avoid these tables!")
    payout_rule = input("Select (1-2, default 1): ").strip()
    bj_payout = 1.2 if payout_rule == '2' else 1.5

    surrender = input("Surrender allowed? (y/n, default y): ").strip().lower()
    surrender = surrender != 'n'

    das = input("Double after split allowed? (y/n, default y): ").strip().lower()
    das = das != 'n'

    rules = GameRules(
        num_decks=num_decks,
        dealer_hits_soft_17=dealer_hits_s17,
        blackjack_payout=bj_payout,
        can_surrender=surrender,
        can_double_after_split=das
    )

    print("\n" + "="*70)
    print("CONFIGURED RULES:")
    print("="*70)
    print(f"Decks: {rules.num_decks}")
    print(f"Dealer: {'H17' if rules.dealer_hits_soft_17 else 'S17'}")
    print(f"Blackjack payout: {rules.blackjack_payout}x")
    print(f"Surrender: {'Yes' if rules.can_surrender else 'No'}")
    print(f"Double after split: {'Yes' if rules.can_double_after_split else 'No'}")
    print("="*70)

    return rules


def help_menu():
    """Display help and strategy guide"""
    print("\n" + "="*70)
    print("HELP & STRATEGY GUIDE")
    print("="*70)
    print("""
THE HI-LO COUNTING SYSTEM:
--------------------------
Card Values:
  2, 3, 4, 5, 6  = +1  (Low cards favor dealer, good when removed)
  7, 8, 9        =  0  (Neutral cards)
  10, J, Q, K, A = -1  (High cards favor player, bad when removed)

Running Count: Keep a running total as cards are dealt

True Count: Running Count ÷ Decks Remaining
  - Adjusts for cards left in shoe
  - Used for betting and strategy decisions

BETTING STRATEGY:
-----------------
True Count  |  Bet Size
------------|------------
    <= 1    |  Minimum bet (1 unit)
     2      |  2-3 units
     3      |  4-5 units
     4      |  6-8 units
    >= 5    |  8-12 units (max)

BASIC STRATEGY:
---------------
Perfect basic strategy reduces house edge to ~0.5%
Combined with counting, you can gain 0.5-1.5% edge over casino

Key principles:
  - Always split 8s and Aces
  - Never split 10s or 5s
  - Double on 11 (except vs Ace in S17)
  - Stand on 17+
  - Hit 16 vs dealer 7+
  - Surrender 16 vs 9, 10, A (if allowed)

CASINO CONDITIONS:
------------------
Best conditions:
  ✓ 6-deck shoe (or fewer)
  ✓ S17 (dealer stands on soft 17)
  ✓ 3:2 blackjack payout
  ✓ Surrender allowed
  ✓ Double after split allowed
  ✓ 75%+ penetration

Avoid:
  ✗ 6:5 blackjack payout (terrible!)
  ✗ H17 (adds ~0.2% house edge)
  ✗ Continuous shuffle machines (can't count)
  ✗ Poor penetration (<70%)

BANKROLL MANAGEMENT:
--------------------
  - Total bankroll: 100-200 betting units minimum
  - Session bankroll: ~10% of total
  - Max bet: 1-2% of total bankroll
  - Use Kelly Criterion for optimal bet sizing
  - Set stop-loss limits (30-50% of session)
  - Set win goals (50-100% of session)

RISK OF RUIN:
-------------
With proper bankroll management:
  - 100 units: ~10% risk of ruin
  - 200 units: ~1% risk of ruin
  - 300+ units: <0.5% risk of ruin

CASINO HEAT:
------------
To avoid detection:
  - Don't make huge bet jumps
  - Vary bet sizes slightly at same count
  - Take breaks
  - Don't play too long at one table
  - Act casual, don't stare at cards
  - Tip dealers occasionally

PRACTICE RECOMMENDATIONS:
-------------------------
1. Master basic strategy first (95%+ accuracy)
2. Practice counting until you can count down a deck in <25 seconds
3. Practice true count conversions
4. Combine counting + basic strategy in full game mode
5. Start with conservative betting (half Kelly)
6. Track all sessions and analyze results

Remember: Card counting is LEGAL but casinos can ask you to leave!
""")
    print("="*70)


def main():
    """Main application loop"""
    print_banner()

    # Default rules (6-deck, S17)
    rules = GameRules()

    while True:
        print_menu()
        choice = input("\nSelect option: ").strip()

        if choice == '1':
            counting_menu()

        elif choice == '2':
            basic_strategy_menu(rules)

        elif choice == '3':
            full_game_menu(rules)

        elif choice == '4':
            bankroll_menu()

        elif choice == '5':
            new_rules = rules_configuration_menu()
            if new_rules:
                rules = new_rules

        elif choice == '6':
            print("\nStatistics feature - Session history would be loaded here")
            print("(Implement session history viewer)")

        elif choice == '7':
            help_menu()

        elif choice == '0':
            print("\nGood luck at the tables! Remember: count cards, not chips.")
            print("Play responsibly and within your limits.\n")
            sys.exit(0)

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting... Good luck!")
        sys.exit(0)
