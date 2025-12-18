# 🎰 Blackjack Card Counting Training Suite

A comprehensive, professional-grade training system to master card counting and blackjack basic strategy. This suite uses the **Hi-Lo counting system** and includes mathematical optimizations, betting strategies, bankroll management, and complete game simulations to prepare you for live casino play.

## 🎯 Features

### Card Counting Training
- **Hi-Lo System Implementation** - Industry-standard balanced counting system
- **Running Count Practice** - Track counts across multiple cards
- **True Count Conversion** - Master the critical skill of adjusting for deck penetration
- **Speed Drills** - Improve counting speed to casino-level performance
- **Accuracy Tracking** - Monitor your progress with detailed statistics

### Basic Strategy Training
- **Perfect Basic Strategy** - Mathematically optimal play for every situation
- **S17/H17 Variations** - Support for different dealer rules
- **Quiz Mode** - Test your knowledge with randomized scenarios
- **Practice Mode** - Continuous training with instant feedback
- **Strategy Charts** - Complete reference charts for hard, soft, and pair hands

### Full Game Simulation
- **Realistic Casino Gameplay** - Complete blackjack implementation
- **6-Deck Shoe Simulation** - Industry-standard shoe with cut card
- **All Major Rule Variations**:
  - S17 vs H17 (dealer stands/hits on soft 17)
  - 3:2 vs 6:5 blackjack payouts
  - Surrender options
  - Double after split
  - Insurance
- **Live Count Display** - See running count and true count in real-time
- **Strategy Hints** - Optional recommendations for learning

### Betting Strategy & Bankroll Management
- **Kelly Criterion Betting** - Mathematically optimal bet sizing
- **Risk Management** - Conservative, medium, and aggressive profiles
- **Bankroll Tracking** - Monitor your bankroll across sessions
- **Stop-Loss/Stop-Win Limits** - Automatic threshold warnings
- **Risk of Ruin Calculations** - Understand your long-term risk
- **Bet Spread Recommendations** - Optimal betting based on true count

### Performance Analytics
- **Session Tracking** - Comprehensive statistics for every session
- **Win Rate Analysis** - Track wins, losses, and pushes
- **Hourly Rate Calculation** - Measure your expected earnings
- **Basic Strategy Accuracy** - Monitor correct play percentage
- **Count Correlation** - Analyze betting and counting performance
- **Session History** - Review past sessions and improve

## 📋 Requirements

- Python 3.7 or higher
- No external dependencies required (uses Python standard library only)

## 🚀 Installation

1. Clone or download this repository:
```bash
git clone <repository-url>
cd blackjack-training-suite
```

2. Make the main script executable (optional):
```bash
chmod +x blackjack_trainer.py
```

3. Run the trainer:
```bash
python blackjack_trainer.py
```

## 💡 Quick Start Guide

### 1. Master Basic Strategy First
Before counting cards, you must know perfect basic strategy:

```bash
python blackjack_trainer.py
# Select: 2 (Basic Strategy Training)
# Select: 1 (Quiz Mode)
```

**Goal:** Achieve 95%+ accuracy before moving to counting

### 2. Learn Card Counting
Start with single card drills, then progress to running counts:

```bash
# Select: 1 (Card Counting Training)
# Select: 1 (Single Card Drill)
```

**Goal:** Count down a full deck in under 25 seconds with no errors

### 3. Practice True Count Conversion
Master converting running count to true count:

```bash
# Select: 1 (Card Counting Training)
# Select: 3 (True Count Conversion)
```

**Goal:** Calculate true count accurately within 1-2 seconds

### 4. Full Game Practice
Combine everything in realistic gameplay:

```bash
# Select: 3 (Full Game Simulator)
```

**Goal:** Maintain accurate count while playing perfect basic strategy

## 📊 The Hi-Lo Counting System

### Card Values
| Cards | Value |
|-------|-------|
| 2, 3, 4, 5, 6 | +1 |
| 7, 8, 9 | 0 |
| 10, J, Q, K, A | -1 |

### Running Count
Keep a running total as each card is dealt:
- Start at 0 when shoe is shuffled
- Add/subtract based on card values
- Running count alone is not enough!

### True Count
Adjust running count for cards remaining:

```
True Count = Running Count ÷ Decks Remaining
```

**Example:**
- Running Count: +6
- Decks Remaining: 3
- True Count: +6 ÷ 3 = +2

## 💰 Betting Strategy

### Recommended Bet Spread (1-12 units)

| True Count | Bet Size | Units | Example ($10 min) |
|------------|----------|-------|-------------------|
| +1 or less | Minimum | 1 | $10 |
| +2 | Small | 2-3 | $20-30 |
| +3 | Medium | 4-5 | $40-50 |
| +4 | Large | 6-8 | $60-80 |
| +5 or more | Maximum | 8-12 | $80-120 |

### Kelly Criterion
The app includes Kelly Criterion betting for optimal bet sizing:

```
Kelly % = Edge / Variance
Edge ≈ True Count × 0.5%
```

**Recommendation:** Use **Half Kelly** (50%) for reduced variance

## 🎓 Strategy Deviations (Indices)

When count is favorable, deviate from basic strategy:

| Play | Basic Strategy | Index | True Count |
|------|----------------|-------|------------|
| Insurance | Never | Take | +3 or higher |
| 16 vs 10 | Hit | Stand | 0 or higher |
| 15 vs 10 | Hit | Stand | +4 or higher |
| 12 vs 3 | Hit | Stand | +2 or higher |
| 12 vs 2 | Hit | Stand | +3 or higher |
| 10,10 vs 5 | Stand | Split | +5 or higher |
| 10,10 vs 6 | Stand | Split | +4 or higher |

## 💵 Bankroll Management

### Minimum Bankroll
- **Conservative:** 200 betting units (ROR < 1%)
- **Medium:** 150 betting units (ROR ~ 2%)
- **Aggressive:** 100 betting units (ROR ~ 10%)

### Example
If your max bet is $100:
- Conservative: $20,000 bankroll
- Medium: $15,000 bankroll
- Aggressive: $10,000 bankroll

### Session Bankroll
Use **10%** of total bankroll per session

### Stop-Loss & Stop-Win
- **Stop-Loss:** Quit if down 30-50% of session bankroll
- **Stop-Win:** Quit if up 50-100% of session bankroll

## 📈 Expected Results

With perfect play and good conditions:

| True Count | Player Edge |
|------------|-------------|
| -2 or less | -1.0% to -2.0% (Don't play!) |
| -1 | -0.5% |
| 0 | ~0% (House edge with basic strategy) |
| +1 | +0.5% |
| +2 | +1.0% |
| +3 | +1.5% |
| +4 | +2.0% |
| +5 | +2.5% |

**With 1-12 spread:** ~0.5-1.5% overall edge

**Expected Hourly Rate:**
```
Hourly = (Average Bet) × (Hands/Hour) × (Edge)
Example: $50 avg × 60 hands × 1% = $30/hour
```

## 🎲 Casino Conditions

### Best Conditions
✅ 6-deck shoe (or fewer decks)
✅ S17 (dealer stands on soft 17)
✅ 3:2 blackjack payout
✅ Surrender allowed
✅ Double after split allowed
✅ 75%+ penetration (deal deep into shoe)
✅ Uncrowded table (more hands per hour)

### Avoid These Conditions
❌ 6:5 blackjack (adds 1.4% house edge!)
❌ H17 (adds 0.2% house edge)
❌ Continuous shuffle machines (counting impossible)
❌ Poor penetration (<70%)
❌ No surrender
❌ No double after split

## 🕵️ Avoiding Detection

Card counting is **legal** but casinos can ask you to leave:

1. **Don't make obvious bet jumps** - Vary bets smoothly
2. **Act casual** - Don't stare intensely at cards
3. **Take breaks** - Don't play marathon sessions
4. **Move tables** - Don't stay at one table too long
5. **Tip dealers** - Builds goodwill
6. **Avoid table max bets** - Stay under the radar
7. **Play with others** - Solo players get more attention
8. **Don't show frustration** - Stay emotionally neutral

## 📝 Training Schedule

### Week 1-2: Basic Strategy
- Goal: 95%+ accuracy on quiz mode
- Practice: 30-60 minutes daily
- Test yourself on all hand types

### Week 3-4: Card Counting
- Goal: Count deck in <25 seconds
- Practice: Single card drills daily
- Progress to running count drills

### Week 5-6: True Count
- Goal: Accurate conversion in 1-2 seconds
- Practice: True count drills
- Combine with running count

### Week 7-8: Full Game
- Goal: Maintain count during gameplay
- Practice: Full game simulator
- Track session statistics

### Week 9+: Advanced Practice
- Goal: Casino-ready speed and accuracy
- Practice: Full sessions with betting
- Review and analyze performance

## 🎮 File Structure

```
blackjack-training-suite/
├── blackjack_trainer.py      # Main application entry point
├── blackjack_engine.py        # Core game engine (deck, hands, rules)
├── counting_system.py         # Hi-Lo counting and betting strategy
├── basic_strategy.py          # Perfect basic strategy engine
├── training_modes.py          # Training drills and simulators
├── session_tracker.py         # Bankroll and session management
├── README.md                  # This file
└── sessions.json              # Session history (created on first use)
```

## 🧮 Mathematical Foundation

### House Edge Reduction
- **No Strategy:** ~2% house edge
- **Basic Strategy:** ~0.5% house edge
- **Card Counting:** 0.5-1.5% player edge

### Expected Value (EV)
```
EV = (Win Probability × Win Amount) - (Loss Probability × Loss Amount)
```

### Kelly Criterion
```
Kelly % = (Edge / Variance)
Recommended: Use 25-50% of Kelly for lower risk
```

### Risk of Ruin (ROR)
```
ROR ≈ ((1 - Edge) / (1 + Edge)) ^ Bankroll_Units
```

## ⚠️ Legal Disclaimer

This software is for **educational and entertainment purposes only**.

- Card counting is legal in most jurisdictions
- Casinos are private property and can refuse service
- Gambling involves risk - never bet more than you can afford to lose
- This software does not guarantee profits
- Always gamble responsibly and within your means
- Check local gambling laws before playing

## 🎯 Tips for Success

1. **Master basic strategy FIRST** - You can't count if you can't play
2. **Practice at home extensively** - Casino environment is distracting
3. **Start with minimum bets** - Build confidence before raising stakes
4. **Keep accurate count** - One mistake can ruin your edge
5. **Manage bankroll strictly** - Variance can be brutal
6. **Stay disciplined** - Don't chase losses or play drunk
7. **Know when to quit** - Set limits and stick to them
8. **Play optimal conditions** - Table selection matters
9. **Track all sessions** - Analyze your results
10. **Stay humble** - Edge is small, variance is large

## 🤝 Contributing

Improvements and suggestions welcome! This is an educational tool designed to teach proper blackjack strategy and card counting techniques.

## 📚 Additional Resources

- **Books:**
  - "Beat the Dealer" by Edward Thorp
  - "Blackjack Attack" by Don Schlesinger
  - "Professional Blackjack" by Stanford Wong
  - "Burning the Tables in Las Vegas" by Ian Andersen

- **Websites:**
  - Wizard of Odds (www.wizardofodds.com)
  - BlackjackApprenticeship.com
  - Blackjack Forum (www.blackjackforumonline.com)

## 📜 License

This project is provided as-is for educational purposes.

---

**Remember:** The house always has an edge in the long run unless you use proper strategy and counting. This trainer gives you the skills - discipline and bankroll management do the rest.

**Good luck, and may the count be with you! 🎴**
