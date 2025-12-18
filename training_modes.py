"""
Interactive Training Modes
Speed counting, basic strategy drills, and full game simulation
"""

import time
import random
from typing import List, Tuple, Optional
from blackjack_engine import Card, Deck, Hand, BlackjackGame, GameRules, Suit
from counting_system import HiLoCounter, CountingTracker, BettingStrategy
from basic_strategy import BasicStrategy, Action
from session_tracker import SessionTracker


class SpeedCountTrainer:
    """Train card counting speed and accuracy"""

    def __init__(self, num_decks: int = 6):
        self.num_decks = num_decks
        self.deck = Deck(num_decks)
        self.counter = HiLoCounter()
        self.tracker = CountingTracker()

    def single_card_drill(self, num_cards: int = 52):
        """
        Practice counting single cards
        Shows one card at a time and tracks accuracy
        """
        print("\n" + "="*60)
        print("SINGLE CARD COUNTING DRILL")
        print("="*60)
        print(f"Count {num_cards} cards as fast as you can!")
        print("Press Enter after counting each card...")
        print()

        self.counter.reset(self.num_decks)
        self.deck.reset()
        start_time = time.time()

        for i in range(num_cards):
            card = self.deck.deal_card()
            actual_value = self.counter.count_card(card)

            print(f"Card {i+1}/{num_cards}: {card}")
            input("Press Enter to continue...")

        elapsed = time.time() - start_time

        print()
        print(f"Time: {elapsed:.2f} seconds")
        print(f"Running Count: {self.counter.get_running_count()}")
        print(f"Speed: {num_cards / elapsed:.1f} cards/second")
        print()

    def running_count_drill(self, num_rounds: int = 10):
        """
        Practice maintaining running count
        User must report running count after seeing multiple cards
        """
        print("\n" + "="*60)
        print("RUNNING COUNT DRILL")
        print("="*60)
        print("Keep a running count as cards are shown.")
        print("You'll be asked to report the count periodically.")
        print()

        self.counter.reset(self.num_decks)
        self.deck.reset()

        for round_num in range(num_rounds):
            # Show 3-7 random cards
            num_cards = random.randint(3, 7)
            cards = []

            print(f"\nRound {round_num + 1}/{num_rounds}")
            print("Cards: ", end="")

            for _ in range(num_cards):
                card = self.deck.deal_card()
                cards.append(card)
                self.counter.count_card(card)
                print(f"{card} ", end="", flush=True)
                time.sleep(0.3)  # Brief pause between cards

            print("\n")

            # Get user's count
            try:
                start = time.time()
                user_count = int(input("What's the running count? "))
                elapsed = time.time() - start

                actual_count = self.counter.get_running_count()
                self.tracker.record_count_attempt(actual_count, user_count, elapsed)

                if user_count == actual_count:
                    print(f"✓ Correct! Running count is {actual_count}")
                else:
                    print(f"✗ Incorrect. Running count is {actual_count} (you said {user_count})")

            except ValueError:
                print("Invalid input!")
                continue

        # Show results
        stats = self.tracker.get_stats()
        print("\n" + "="*60)
        print("DRILL RESULTS")
        print("="*60)
        print(f"Accuracy: {stats['accuracy']:.1f}%")
        print(f"Correct: {stats['correct']}/{stats['total_attempts']}")
        print(f"Average Error: {stats['average_error']:.2f}")
        print(f"Average Time: {stats['average_time']:.2f}s")
        print("="*60)

    def true_count_drill(self, num_rounds: int = 10):
        """
        Practice converting running count to true count
        """
        print("\n" + "="*60)
        print("TRUE COUNT CONVERSION DRILL")
        print("="*60)
        print("Convert running count to true count based on decks remaining.")
        print()

        for round_num in range(num_rounds):
            # Generate random scenario
            running_count = random.randint(-10, 10)
            decks_remaining = round(random.uniform(1.0, 6.0), 1)

            print(f"\nRound {round_num + 1}/{num_rounds}")
            print(f"Running Count: {running_count:+d}")
            print(f"Decks Remaining: {decks_remaining}")
            print()

            # Calculate actual true count
            actual_tc = running_count / decks_remaining

            # Get user's answer
            try:
                user_tc = float(input("True Count: "))

                self.tracker.record_true_count_attempt(actual_tc, user_tc)

                error = abs(actual_tc - user_tc)
                if error < 0.5:  # Allow 0.5 margin
                    print(f"✓ Correct! True count is {actual_tc:+.1f}")
                else:
                    print(f"✗ Incorrect. True count is {actual_tc:+.1f} (you said {user_tc:+.1f})")

            except ValueError:
                print("Invalid input!")
                continue

        # Show results
        stats = self.tracker.get_stats()
        print("\n" + "="*60)
        print("DRILL RESULTS")
        print("="*60)
        print(f"Average TC Error: {stats['average_tc_error']:.2f}")
        print("="*60)


class BasicStrategyTrainer:
    """Train perfect basic strategy"""

    def __init__(self, dealer_hits_soft_17: bool = False):
        self.strategy = BasicStrategy(dealer_hits_soft_17=dealer_hits_soft_17)
        self.correct = 0
        self.total = 0
        self.errors: List[dict] = []

    def generate_random_hand(self) -> Tuple[Hand, Card]:
        """Generate a random hand scenario"""
        deck = Deck(6)
        hand = Hand()

        # Generate player hand
        hand.add_card(deck.deal_card())
        hand.add_card(deck.deal_card())

        # Generate dealer upcard
        dealer_upcard = deck.deal_card()

        return hand, dealer_upcard

    def quiz_mode(self, num_questions: int = 20):
        """
        Quiz mode - test basic strategy knowledge
        """
        print("\n" + "="*60)
        print("BASIC STRATEGY QUIZ")
        print("="*60)
        print("Answer what you should do in each scenario.")
        print("Actions: H=Hit, S=Stand, D=Double, SP=Split, SR=Surrender")
        print()

        self.correct = 0
        self.total = 0
        self.errors = []

        for i in range(num_questions):
            hand, dealer_upcard = self.generate_random_hand()

            print(f"\nQuestion {i+1}/{num_questions}")
            print(f"Your hand: {hand}")
            print(f"Dealer shows: {dealer_upcard}")
            print()

            # Get correct action
            correct_action = self.strategy.get_action(hand, dealer_upcard)

            # Get user action
            user_input = input("Your action (H/S/D/SP/SR): ").strip().upper()

            # Map input to action
            action_map = {
                'H': Action.HIT,
                'S': Action.STAND,
                'D': Action.DOUBLE,
                'SP': Action.SPLIT,
                'SR': Action.SURRENDER
            }

            if user_input not in action_map:
                print("Invalid input!")
                continue

            user_action = action_map[user_input]
            self.total += 1

            # Check if correct
            if self.strategy.is_correct_action(hand, dealer_upcard, user_action):
                self.correct += 1
                print("✓ Correct!")
            else:
                print(f"✗ Incorrect. Should {self.strategy.get_action_string(correct_action)}")
                self.errors.append({
                    'hand': str(hand),
                    'dealer': str(dealer_upcard),
                    'correct': self.strategy.get_action_string(correct_action),
                    'yours': user_input
                })

        # Show results
        accuracy = (self.correct / self.total * 100) if self.total > 0 else 0
        print("\n" + "="*60)
        print("QUIZ RESULTS")
        print("="*60)
        print(f"Score: {self.correct}/{self.total} ({accuracy:.1f}%)")
        print()

        if self.errors:
            print("Mistakes to review:")
            for i, error in enumerate(self.errors, 1):
                print(f"{i}. Hand: {error['hand']}, Dealer: {error['dealer']}")
                print(f"   Correct: {error['correct']}, You chose: {error['yours']}")

        print("="*60)

    def practice_mode(self):
        """
        Practice mode - continuous practice with instant feedback
        """
        print("\n" + "="*60)
        print("BASIC STRATEGY PRACTICE")
        print("="*60)
        print("Practice basic strategy with instant feedback.")
        print("Type 'quit' to exit.")
        print()

        self.correct = 0
        self.total = 0

        while True:
            hand, dealer_upcard = self.generate_random_hand()

            print(f"\nYour hand: {hand}")
            print(f"Dealer shows: {dealer_upcard}")

            # Get correct action
            correct_action = self.strategy.get_action(hand, dealer_upcard)

            # Get user action
            user_input = input("Your action (H/S/D/SP/SR) or 'quit': ").strip().upper()

            if user_input == 'QUIT':
                break

            # Map input to action
            action_map = {
                'H': Action.HIT,
                'S': Action.STAND,
                'D': Action.DOUBLE,
                'SP': Action.SPLIT,
                'SR': Action.SURRENDER
            }

            if user_input not in action_map:
                print("Invalid input!")
                continue

            user_action = action_map[user_input]
            self.total += 1

            # Check if correct
            if self.strategy.is_correct_action(hand, dealer_upcard, user_action):
                self.correct += 1
                print("✓ Correct!")
            else:
                print(f"✗ Should {self.strategy.get_action_string(correct_action)}")

            # Show running accuracy
            accuracy = (self.correct / self.total * 100) if self.total > 0 else 0
            print(f"Accuracy: {self.correct}/{self.total} ({accuracy:.1f}%)")

        print("\nPractice complete!")


class FullGameSimulator:
    """
    Full blackjack game with counting and betting
    Realistic casino simulation for complete training
    """

    def __init__(self, rules: GameRules = GameRules(), starting_bankroll: float = 10000.0):
        self.rules = rules
        self.game = BlackjackGame(rules)
        self.counter = HiLoCounter()
        self.strategy = BasicStrategy(
            dealer_hits_soft_17=rules.dealer_hits_soft_17,
            can_surrender=rules.can_surrender,
            double_after_split=rules.can_double_after_split
        )
        self.betting_strategy = BettingStrategy(starting_bankroll)
        self.session = SessionTracker(starting_bankroll)
        self.show_count = True  # Show count for training

    def play_round(self, manual_bet: Optional[float] = None):
        """Play a single round"""
        self.game.new_round()

        # Get true count
        true_count = self.counter.get_true_count_from_deck(self.game.deck)

        # Determine bet
        if manual_bet:
            bet = manual_bet
        else:
            bet = self.betting_strategy.optimal_bet_size(true_count)

        # Place bet
        try:
            self.game.place_bet(bet)
        except ValueError as e:
            print(f"Error: {e}")
            return

        # Deal initial cards
        self.game.deal_initial_cards()

        # Count visible cards
        self.counter.count_card(self.game.player_hands[0].cards[0])
        self.counter.count_card(self.game.player_hands[0].cards[1])
        self.counter.count_card(self.game.dealer_hand.cards[0])  # Only first dealer card visible

        # Display
        print("\n" + "="*60)
        print(f"Bet: ${bet:.2f}")
        print(f"Dealer shows: {self.game.dealer_hand.cards[0]}")
        print(f"Your hand: {self.game.player_hands[0]}")

        if self.show_count:
            print(f"Running Count: {self.counter.get_running_count():+d}")
            print(f"True Count: {true_count:+.1f}")
            print(f"Decks Remaining: {self.game.deck.decks_remaining():.1f}")

        # Check for blackjacks
        if self.game.player_hands[0].is_blackjack():
            if self.game.dealer_hand.is_blackjack():
                print("Push - both blackjack!")
                profit = 0
            else:
                print("BLACKJACK! You win!")
                profit = bet * self.rules.blackjack_payout

            self.counter.count_card(self.game.dealer_hand.cards[1])  # Count hole card
            self.session.record_hand(bet, profit, 21, self.game.dealer_hand.value(),
                                    true_count, self.counter.get_running_count(),
                                    was_blackjack=True)
            return

        # Play player hands
        while not self.game.is_round_complete():
            hand = self.game.get_current_hand()

            if hand.is_bust():
                self.game.stand()
                continue

            # Get basic strategy recommendation
            dealer_upcard = self.game.dealer_hand.cards[0]
            recommended_action = self.strategy.get_action(
                hand, dealer_upcard,
                can_double=hand.can_double(),
                can_split=hand.can_split()
            )

            print(f"\nRecommended: {self.strategy.get_action_string(recommended_action)}")
            action_input = input("Action (H/S/D/SP/SR): ").strip().upper()

            if action_input == 'H':
                card = self.game.hit()
                self.counter.count_card(card)
                print(f"Drew: {card}")
                print(f"Hand: {hand}")

                if hand.is_bust():
                    print("BUST!")
                    self.game.stand()

            elif action_input == 'S':
                self.game.stand()

            elif action_input == 'D':
                try:
                    card = self.game.double_down()
                    self.counter.count_card(card)
                    print(f"Drew: {card}")
                    print(f"Hand: {hand}")
                    if hand.is_bust():
                        print("BUST!")
                except ValueError as e:
                    print(f"Error: {e}")

            elif action_input == 'SP':
                try:
                    hand1, hand2 = self.game.split()
                    print(f"Split into: {hand1} and {hand2}")
                except ValueError as e:
                    print(f"Error: {e}")

            elif action_input == 'SR':
                try:
                    self.game.surrender()
                    print("Surrendered")
                except ValueError as e:
                    print(f"Error: {e}")

        # Play dealer hand
        print(f"\nDealer's hole card: {self.game.dealer_hand.cards[1]}")
        self.counter.count_card(self.game.dealer_hand.cards[1])

        self.game.play_dealer_hand()
        print(f"Dealer hand: {self.game.dealer_hand}")

        # Count any additional dealer cards
        for card in self.game.dealer_hand.cards[2:]:
            self.counter.count_card(card)

        # Resolve hands
        total_profit = 0
        for hand in self.game.player_hands:
            profit = self.game.resolve_hand(hand)
            total_profit += profit

            if profit > 0:
                print(f"Hand {hand}: WIN +${profit:.2f}")
            elif profit < 0:
                print(f"Hand {hand}: LOSS ${profit:.2f}")
            else:
                print(f"Hand {hand}: PUSH")

        print(f"\nNet: ${total_profit:+.2f}")
        print(f"Bankroll: ${self.session.current_bankroll:,.2f} → ${self.session.current_bankroll + total_profit:,.2f}")

        # Record hand
        self.session.record_hand(
            bet, total_profit,
            self.game.player_hands[0].value(),
            self.game.dealer_hand.value(),
            true_count,
            self.counter.get_running_count()
        )

    def play_session(self):
        """Play a full session"""
        print("\n" + "="*60)
        print("FULL GAME SIMULATOR")
        print("="*60)
        print(f"Starting Bankroll: ${self.session.starting_bankroll:,.2f}")
        print(f"Rules: {self.rules.num_decks} decks, ", end="")
        print("H17" if self.rules.dealer_hits_soft_17 else "S17")
        print()

        self.counter.reset(self.rules.num_decks)

        while True:
            # Check for shuffle
            if self.game.deck.needs_shuffle():
                print("\n" + "~"*60)
                print("SHUFFLE!")
                print("~"*60)
                self.game.deck.reset()
                self.counter.reset(self.rules.num_decks)

            # Play round
            self.play_round()

            # Continue?
            continue_input = input("\nContinue? (y/n): ").strip().lower()
            if continue_input != 'y':
                break

        # Show session summary
        self.session.print_session_summary()
