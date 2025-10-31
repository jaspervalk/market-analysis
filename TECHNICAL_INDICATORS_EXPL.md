# Technical Indicators Reference Guide
**For Swing Trading System**

Last Updated: October 22, 2025

---

## Table of Contents
1. [Trend Indicators](#trend-indicators)
2. [Momentum Indicators](#momentum-indicators)
3. [Volume Indicators](#volume-indicators)
4. [Volatility Indicators](#volatility-indicators)
5. [Scoring System Logic](#scoring-system-logic)
6. [Real-World Examples](#real-world-examples)
7. [Common Patterns](#common-patterns)

---

## Trend Indicators

### ADX (Average Directional Index)
**Purpose:** Measures trend strength (not direction)

**Scale:** 0-100
- **0-20:** No trend (ranging/choppy market)
- **20-25:** Weak trend forming
- **25-50:** Strong trend (tradeable)
- **50+:** Very strong trend (rare)

**How to Read:**
```
ADX = 15 → Market is choppy, avoid trend-following strategies
ADX = 30 → Strong trend exists, safe to follow the trend
ADX = 45 → Very strong trend, ride it until ADX starts declining
```

**Real Example (AMZN):**
```
ADX: 29.6 = Strong trend in progress
This means: There IS a clear trend happening (not random noise)
```

**Why It Matters:**
- You make money in trends, lose money in chop
- ADX tells you if a real move is happening
- High ADX = Trust other trend signals
- Low ADX = Use mean reversion instead

**Analogy:** ADX is wind speed. High wind (ADX > 25) means sailboats can move. No wind (ADX < 20) means you're stuck.

---

### Plus_DI / Minus_DI (Directional Indicators)
**Purpose:** Determines trend direction (works with ADX)

**How to Read:**
- **Plus_DI > Minus_DI:** Buyers winning (uptrend)
- **Minus_DI > Plus_DI:** Sellers winning (downtrend)
- **Gap between them:** Shows trend strength

**Combined Reading:**
```
Scenario 1: ADX = 30, Plus_DI = 35, Minus_DI = 15
→ Strong uptrend (high ADX + buyers dominating)

Scenario 2: ADX = 30, Plus_DI = 15, Minus_DI = 35
→ Strong downtrend (high ADX + sellers dominating)

Scenario 3: ADX = 15, Plus_DI = 20, Minus_DI = 18
→ No trend (low ADX + close battle = chop)
```

**System Usage:**
```python
if ADX > 25:
    if Plus_DI > Minus_DI:
        trend = "UPTREND"  # +5 points
    else:
        trend = "DOWNTREND"  # -5 points
```

**Analogy:** Two teams in tug-of-war. Plus_DI (blue team) vs Minus_DI (red team). ADX tells you how hard they're pulling.

---

### SuperTrend
**Purpose:** Visual trend indicator (like a trailing stop)

**Values:**
- **Direction = 1:** Bullish (price above SuperTrend line)
- **Direction = -1:** Bearish (price below SuperTrend line)

**How It Works:**
- Uses ATR (volatility) to set distance from price
- Flips when price crosses the line
- Acts as dynamic support/resistance

**Visual:**
```
Price above SuperTrend → Green line → Uptrend
Price below SuperTrend → Red line → Downtrend
```

**Why It's Useful:**
- Clear visual trend confirmation
- Reduces whipsaws (false signals)
- Works as trailing stop loss level

**System Usage:**
- Combined with ADX to confirm trend direction
- Only used when ADX confirms strong trend exists

---

### Moving Averages (SMA)
**Purpose:** Shows average price over time (smooths out noise)

**Types:**
- **SMA_20:** Short-term (1 month)
- **SMA_50:** Medium-term (2.5 months)
- **SMA_200:** Long-term (1 year)

**Price Structure Analysis:**

**Perfect Bullish Alignment (+3 points):**
```
Close > SMA_20 > SMA_50 > SMA_200
$217  > $210   > $200   > $190

Visual: Stairs going up
Meaning: All timeframes agree = strong uptrend
```

**Bullish Short-Term (+2 points):**
```
Close > SMA_20 > SMA_50 (but SMA_200 anywhere)
$217  > $210   > $200

Meaning: Short-term strength, long-term uncertain
```

**Bearish Short-Term (-2 points):**
```
Close < SMA_20 < SMA_50
$195  < $200   < $210

Meaning: Recent weakness appearing
```

**Perfect Bearish Alignment (-3 points):**
```
Close < SMA_20 < SMA_50 < SMA_200
$190  < $195   < $200   < $210

Visual: Stairs going down
Meaning: All timeframes bearish = strong downtrend
```

**Real Example:**
```
AMZN: Close < SMA_20 < SMA_50
→ "Bearish short-term structure" (-2 points)
→ Price recently broke below 20-day average (warning sign)
```

**Analogy:** MAs are layers of support/resistance. Perfect bullish = climbing stairs. Breaking below = stairs collapsing.

---

## Momentum Indicators

### RSI (Relative Strength Index)
**Purpose:** Measures if stock is overbought or oversold

**Scale:** 0-100
- **70-100:** Overbought (too much buying)
- **30-70:** Neutral zone
- **0-30:** Oversold (too much selling)

**Trading Rules:**
```
In UPTREND:
- RSI dips to 30-40 → Buy the pullback
- RSI > 70 → Take profits or wait

In DOWNTREND:
- RSI rallies to 60-70 → Fade the bounce
- RSI < 30 → Don't catch falling knife
```

**System Scoring:**
```
RSI < 30 → Oversold (counts toward +3 to +6 points if 2-3 indicators agree)
RSI > 70 → Overbought (counts toward -3 to -6 points if 2-3 indicators agree)
```

**Why Confluence Matters:**
- 1 oversold indicator = Weak signal
- 2 oversold indicators = +5 points (good signal)
- 3 oversold indicators = +6 points (very strong signal)

**Example:**
```
RSI = 28 (oversold)
Stochastic = 18 (oversold)
MFI = 22 (oversold)

→ 3 indicators agree → +6 points → Strong buy signal
```

**Analogy:** RSI is a speedometer for buying pressure. Over 70 = driving too fast (crash coming). Under 30 = too slow (can accelerate).

---

### Stochastic Oscillator
**Purpose:** Where is price in its recent high-low range?

**Components:**
- **%K:** Fast line (current reading)
- **%D:** Slow line (3-day average)

**Scale:** 0-100
- **80-100:** Overbought (price near recent high)
- **20-80:** Neutral
- **0-20:** Oversold (price near recent low)

**How to Read:**
```
Both %K and %D < 20 → Strong oversold
Both %K and %D > 80 → Strong overbought
%K crosses above %D in oversold → Buy signal
%K crosses below %D in overbought → Sell signal
```

**System Usage:**
- Requires BOTH %K AND %D in extreme zones
- Adds to momentum confluence count

**Example:**
```
Stoch_K = 18, Stoch_D = 15 → Both below 20
→ Counts as oversold signal
→ Combines with RSI and MFI for +5 or +6 points
```

**Analogy:** "On a scale of 0-100, where is price in its recent range?" If at 90, it's near the top and might reverse.

---

### MFI (Money Flow Index)
**Purpose:** RSI but with volume (shows "smart money")

**Scale:** 0-100
- **80-100:** Overbought with volume confirmation
- **20-80:** Neutral
- **0-20:** Oversold with volume confirmation

**Why It's Better Than RSI:**
```
RSI = Price momentum only
MFI = Price momentum + Volume

Example:
RSI shows oversold (30) but MFI doesn't (45)
→ Weak signal (retail selling, no institutional buying)

RSI shows oversold (30) AND MFI shows oversold (18)
→ Strong signal (institutions accumulating)
```

**System Usage:**
```
MFI < 20 → Oversold (adds to confluence)
MFI > 80 → Overbought (adds to confluence)
```

**Analogy:** RSI counts how many people are buying. MFI counts how much money they're spending. Big difference!

---

### MACD (Moving Average Convergence Divergence)
**Purpose:** Trend momentum and reversals

**Components:**
- **MACD Line:** Fast EMA - Slow EMA
- **Signal Line:** 9-day average of MACD
- **Histogram:** MACD - Signal (distance between them)

**Signals:**
```
MACD > Signal + Histogram positive → Bullish (+1 point)
MACD < Signal + Histogram negative → Bearish (-1 point)
MACD crossing above Signal → Buy signal
MACD crossing below Signal → Sell signal
```

**Why Only 1 Point in System:**
- MACD is **lagging** (tells you what happened, not what's coming)
- Good for confirmation, not primary signal
- Trend strength (ADX) matters more

**Visual Example:**
```
Histogram rising from negative to positive:
   ||||
  |||||
 ||||||
|||||||  ← MACD crossing above Signal (buy signal)
-------
  |||||
   ||||
    |||
```

**Analogy:** MACD is the rearview mirror. Tells you what just happened, not what's ahead.

---

## Volume Indicators

### VWAP (Volume Weighted Average Price)
**Purpose:** The "fair value" price where most volume traded

**Calculation:**
```
VWAP = Σ(Price × Volume) / Σ(Volume)
```

**Think of It As:**
- Average price weighted by volume
- Where institutions filled their orders
- Intraday "fair value" benchmark

### Why VWAP Matters (CRITICAL)

**The Farmer's Market Analogy:**
```
Most people bought apples at $2.00 (VWAP)
Late buyer pays $2.30 (current price)

Question: Is $2.30 a good price?
Answer: NO! You're overpaying by 15%
```

**Real Trading:**
```
Current Price: $217.35
VWAP: $190.41
Deviation: +14.1%

Translation: You're paying $27 more per share than average
```

### VWAP Deviation Rules

**System Thresholds:**
```
Within ±3% of VWAP → Neutral (no score adjustment)
±3-5% from VWAP → Caution zone
>±5% from VWAP → Adjustment triggered

Above VWAP >3% → -2 points (overextended)
Below VWAP >3% → +2 points (undervalued)
```

**Why These Rules:**

**Mean Reversion (The Rubber Band Effect):**
```
Price stretches away from VWAP → Eventually snaps back
Like a rubber band → The further you pull, the stronger the snap

VWAP = $100
Price = $114 (+14%)
→ VERY stretched rubber band
→ High probability of snapback to $100-105
```

**Real Examples:**

**Good Entry (Price Below VWAP):**
```
Price: $187
VWAP: $195
Deviation: -4.1%

System: +2 points for "undervalued vs VWAP"
Meaning: Buying below where institutions bought = good value
```

**Bad Entry (Price Above VWAP):**
```
Price: $217
VWAP: $190
Deviation: +14.1%

System: -2 points for "overextended vs VWAP"
Meaning: Paying 14% premium = poor value, likely to fall
```

**When to Ignore VWAP:**
- Strong breakouts (price running away from VWAP is normal)
- End of day (VWAP resets daily)
- Low volume stocks (VWAP less reliable)

**Best Practice:**
```
Uptrend Strategy:
- Wait for pullback toward VWAP
- Buy when price within 2-3% of VWAP
- Target: Previous swing high

Example:
Stock rallies from $100 → $120 (VWAP at $110)
Wait for pullback to $112-115 (near VWAP)
Then enter long with VWAP as support
```

**Analogy:** VWAP is sea level. Price is a boat. When boat is 14% above sea level, gravity (mean reversion) will pull it back down.

---

### CMF (Chaikin Money Flow)
**Purpose:** Is money flowing in or out of the stock?

**Scale:** -1.0 to +1.0
- **>+0.1:** Accumulation (buying pressure)
- **-0.1 to +0.1:** Neutral
- **<-0.1:** Distribution (selling pressure)

**How It Works:**
```
Close near HIGH of day + High volume = Buying pressure
Close near LOW of day + High volume = Selling pressure
```

**System Usage (Volume Confirmation):**
```
Volume > 1.5x average + CMF > 0.1 → +2 points
Volume > 1.5x average + CMF < -0.1 → -2 points
```

**Why This Matters:**
- High volume alone means nothing (could be buyers OR sellers)
- CMF tells you WHO won (buyers or sellers)

**Example:**
```
Volume Ratio: 2.3x (high volume day)
CMF: +0.25 (strong buying)

→ +2 points for "High volume with buying pressure"
→ Institutions are accumulating
```

**Analogy:** CMF watches a crowded store. Are people walking in with empty bags (buying) or out with full bags (selling)?

---

### Volume Ratio
**Purpose:** Is today's volume normal or unusual?

**Calculation:**
```
Volume_Ratio = Current Volume / 20-day Average Volume
```

**Interpretation:**
```
< 0.5 → Very low volume (half normal)
0.5-1.5 → Normal volume range
> 1.5 → High volume (1.5x+ normal)
> 2.0 → Very high volume (2x+ normal)
```

**Why It Matters:**
- Price moves on low volume don't last
- High volume confirms the move is real
- Breakouts need volume confirmation

**System Requirements:**
```
Volume must be >1.5x average for volume confirmation scoring
Then combine with CMF to determine if bullish or bearish
```

---

## Volatility Indicators

### ATR (Average True Range)
**Purpose:** Measures how much a stock typically moves per day

**Usage:**
- **Stop Loss Placement:** Entry - (2 × ATR)
- **Position Sizing:** Adjust shares based on ATR
- **Target Setting:** Entry + (3 × ATR) for profit target

**Example:**
```
AMZN ATR: $5.71 (2.6% of price)

Stop Loss: $217.35 - (2 × $5.71) = $205.93
Risk per share: $11.42

Translation: Stock typically moves $5.71/day
Using 2× ATR gives room for normal volatility
```

**Why 2× ATR for Stops:**
- 1× ATR = Too tight (normal noise stops you out)
- 2× ATR = Balanced (allows breathing room)
- 3× ATR = Too wide (risk too much)

**Position Sizing with ATR:**
```
High ATR stock: $15 ATR → 2× = $30 risk → Buy fewer shares
Low ATR stock: $2 ATR → 2× = $4 risk → Buy more shares

This normalizes risk across different volatility stocks
```

---

### Squeeze Indicator (Bollinger Bands vs Keltner Channels)
**Purpose:** Detects low volatility before big moves

**How It Works:**
```
Normal Market:
Keltner Channels:  |------[    ]------|
Bollinger Bands:      |---[  ]---|

Squeeze (Compression):
Keltner Channels:  |------[    ]------|
Bollinger Bands:         |-[]--|
                            ↑
                   Bands squeezed inside channels
```

**What It Means:**
- Volatility contracting
- Market "coiling" like a spring
- Big move coming (but direction unknown)

**Why System Penalizes It:**
```
Squeeze_On = True → -2 points

Reason: "Avoid breakout traps"
Problem: You don't know which way it will break
Risk: Buy thinking it'll go up, but it breaks down instead
```

**Better Strategy During Squeeze:**
```
Wait for squeeze to release → Bands expand again
Then trade in direction of breakout
```

**Visual Timeline:**
```
Day 1-5: Squeeze_On = True (bands compressing)
Day 6: Breakout occurs (bands start expanding)
Day 7+: Squeeze_On = False → Safe to trade breakout direction
```

**Real Example:**
```
AMZN: Squeeze_On = True
System: -2 points
Translation: Market compressing, wait for release before entering
```

**Analogy:** Compressed spring. You don't want to guess which direction it'll fly. Wait for release, then trade that direction.

---

### Historical Volatility Percentile
**Purpose:** Is current volatility high, normal, or low?

**Scale:** 0.0 to 1.0 (percentile rank)
- **>0.7:** High volatility (top 30% of range)
- **0.3-0.7:** Normal volatility
- **<0.3:** Low volatility (bottom 30% of range)

**System Usage:**
```
Vol_Percentile > 0.8 → Score × 0.7 (reduce conviction by 30%)

Reason: High volatility = unpredictable
Action: Be more cautious, reduce position size
```

**Position Sizing Adjustment:**
```
HIGH_VOL regime detected:
- Reduce shares by 50%
- Wider stops required
- Less predictable price action
```

---

## Scoring System Logic

### Score Range: -15 to +15

### Component Breakdown

**1. TREND (Highest Weight): ±5 points**
```
Strong uptrend (ADX >25, SuperTrend bullish): +5
Moderate uptrend (ADX 20-25, SuperTrend bullish): +3
Neutral/Ranging (ADX <20): 0
Moderate downtrend (ADX 20-25, SuperTrend bearish): -3
Strong downtrend (ADX >25, SuperTrend bearish): -5
```

**Why Highest Weight:**
- Trend is king in trading
- Strong trends persist longer than expected
- Catching trends = 80% of profits

---

**2. MOMENTUM CONFLUENCE: ±3 to ±6 points**
```
1 oversold indicator: 0 points (not enough)
2 oversold indicators: +5 points (good confluence)
3 oversold indicators: +6 points (very strong confluence)

Same for overbought (negative points)
```

**Why Non-Linear:**
- 1 indicator = Could be noise
- 2 indicators = Probably real
- 3 indicators = Definitely real (bonus point)

**Indicators Checked:**
- RSI < 30 or > 70
- Stochastic K&D < 20 or > 80
- MFI < 20 or > 80

---

**3. VOLUME CONFIRMATION: ±2 points**
```
Volume > 1.5x + CMF > 0.1: +2 (high volume buying)
Volume > 1.5x + CMF < -0.1: -2 (high volume selling)
Otherwise: 0
```

**Why Required:**
- Price moves without volume don't last
- Volume shows institutional participation
- CMF shows who won (buyers or sellers)

---

**4. PRICE STRUCTURE: ±2 to ±3 points**
```
Perfect bullish (Close > SMA_20 > SMA_50 > SMA_200): +3
Bullish short-term (Close > SMA_20 > SMA_50): +2
Neutral: 0
Bearish short-term (Close < SMA_20 < SMA_50): -2
Perfect bearish (Close < SMA_20 < SMA_50 < SMA_200): -3
```

**Why It Matters:**
- Multiple timeframe confirmation
- Shows if trend is intact or breaking

---

**5. VWAP DEVIATION: ±2 points**
```
>3% above VWAP: -2 (overextended)
Within ±3% of VWAP: 0 (fair value)
>3% below VWAP: +2 (undervalued)
```

**Why Critical:**
- Mean reversion to VWAP is real
- Buying far from VWAP = poor entry
- Professional traders use VWAP extensively

---

**6. SQUEEZE DETECTION: -2 points**
```
Squeeze_On = True: -2 (avoid breakout traps)
Squeeze_On = False: 0
```

**Why Penalize:**
- Direction unknown during compression
- False breakouts common
- Better to wait for confirmation

---

**7. MACD: ±1 point**
```
MACD > Signal + Histogram positive: +1
MACD < Signal + Histogram negative: -1
Otherwise: 0
```

**Why Only 1 Point:**
- Lagging indicator
- Confirmation only, not primary signal
- Less reliable than trend/momentum

---

**8. VOLATILITY ADJUSTMENT: ×0.7 multiplier**
```
If Vol_Percentile > 0.8:
    Score = Score × 0.7

Example: Score was +10 → Becomes +7
```

**Why Reduce Conviction:**
- High volatility = unpredictable
- Stops hit more often
- Lower win rate in chaos

---

### Signal Thresholds (STRICT)

```
STRONG BUY: Score ≥8 AND R:R ≥2.5:1
BUY: Score ≥6 AND R:R ≥2.0:1
STRONG SELL: Score ≤-8 AND R:R ≥2.5:1
SELL: Score ≤-6 AND R:R ≥2.0:1
NO TRADE: Everything else
```

**Why Both Conditions Required:**
- Good score + bad R:R = Bad trade (too much risk)
- Good R:R + low score = Weak trade (might not work)
- Both must be satisfied = High probability + good risk/reward

---

## Real-World Examples

### Example 1: AMZN - NO TRADE (Current)

**Raw Data:**
```
Price: $217.35
VWAP: $190.41 (+14.1% deviation)
ADX: 29.6
SuperTrend_Direction: 1 (bullish)
Plus_DI: 28, Minus_DI: 12
Close < SMA_20 < SMA_50
Squeeze_On: True
MACD: Bullish
```

**Scoring Breakdown:**
```
1. Strong uptrend (ADX 29.6): +5
2. Bearish short-term structure: -2
3. Overextended vs VWAP (+14.1%): -2
4. Squeeze active: -2
5. MACD bullish: +1
───────────────────────────────────
Total Score: 0 / 15
R:R Ratio: 0.95:1
Signal: NO TRADE
```

**Why NO TRADE:**
- Score is 0 (need ≥6 for BUY)
- R:R is 0.95 (need ≥2.0 for BUY)
- Both conditions fail

**Translation:**
"Yes, there's a strong uptrend, BUT you'd be buying 14% overextended in a compression zone with poor risk/reward. Wait for better entry."

**Better Strategy:**
- Wait for pullback to $200-205 (near VWAP)
- OR wait for squeeze to release with upward breakout
- OR pass and look for cleaner setups

---

### Example 2: Hypothetical BUY Signal

**Raw Data:**
```
Price: $198
VWAP: $195 (-1.5% deviation)
ADX: 28
SuperTrend_Direction: 1 (bullish)
Plus_DI: 32, Minus_DI: 15
Close > SMA_20 > SMA_50 > SMA_200
RSI: 35 (oversold)
Stochastic: 22 (oversold)
MFI: 28 (not oversold, but low)
Volume_Ratio: 1.8x
CMF: +0.15
Squeeze_On: False
MACD: Bullish
```

**Scoring Breakdown:**
```
1. Strong uptrend (ADX 28): +5
2. Multiple oversold (RSI + Stoch = 2): +5
3. High volume with buying (1.8x + CMF): +2
4. Perfect bullish MA alignment: +3
5. Near VWAP (within 2%): 0
6. No squeeze: 0
7. MACD bullish: +1
───────────────────────────────────
Total Score: 16 / 15 (caps at 15)
R:R Ratio: 3.2:1
Signal: STRONG BUY
```

**Why STRONG BUY:**
- Score ≥8 ✓ (has 15)
- R:R ≥2.5:1 ✓ (has 3.2:1)
- Both conditions met

**Translation:**
"Strong uptrend pullback to oversold levels with multiple confirmations, high volume buying, perfect structure, and excellent risk/reward. High-probability trade."

---

### Example 3: Hypothetical NO TRADE (Good Score, Bad R:R)

**Raw Data:**
```
Price: $215
VWAP: $210 (+2.4% deviation)
ADX: 32
SuperTrend_Direction: 1
Close > SMA_20 > SMA_50
RSI: 38 (oversold)
Stochastic: 25 (oversold)
Volume_Ratio: 1.7x
CMF: +0.12
Recent_High: $218 (target only $3 away)
ATR: $6
Stop: $203 (2×ATR)
```

**Scoring Breakdown:**
```
1. Strong uptrend: +5
2. Oversold confluence (2 indicators): +5
3. Volume confirmation: +2
4. Bullish short-term structure: +2
5. Near VWAP: 0
───────────────────────────────────
Total Score: 14 / 15
R:R Ratio: 0.25:1 (Risk $12, Reward $3)
Signal: NO TRADE
```

**Why NO TRADE:**
- Score ≥8 ✓ (has 14, excellent!)
- R:R ≥2.0:1 ✗ (has 0.25:1, terrible!)
- Only one condition met = NO TRADE

**Translation:**
"Great technical setup, but target is too close. You'd risk $12 to make $3. Wait for bigger move or adjust target."

---

### Example 4: Ranging Market

**Raw Data:**
```
Price: $105
VWAP: $105 (0% deviation)
ADX: 18 (no trend)
Plus_DI: 21, Minus_DI: 20 (close battle)
RSI: 32 (oversold)
Stochastic: 18 (oversold)
MFI: 24 (oversold)
Volume_Ratio: 2.1x
CMF: +0.18
```

**Scoring Breakdown:**
```
1. No trend (ADX 18): 0
2. Multiple oversold (3 indicators): +6
3. High volume buying: +2
4. At VWAP: 0
───────────────────────────────────
Total Score: 8 / 15
R:R Ratio: 2.8:1
Signal: STRONG BUY
```

**Why This Works:**
- Score ≥8 ✓ (has 8)
- R:R ≥2.5:1 ✓ (has 2.8:1)
- Both conditions met

**Strategy Type:** Mean Reversion
- No trend, so use oversold bounce
- Multiple indicators confirm oversold
- High volume accumulation
- At fair value (VWAP)
- Good R:R to recent resistance

**Translation:**
"In ranging market, heavily oversold with volume support. Mean reversion play to resistance."

---

## Common Patterns

### Pattern 1: Trend Pullback (Best Setup)
```
Strong uptrend (ADX >25)
Price pulls back to VWAP or SMA_50
Multiple oversold signals
Volume dries up on pullback
Then volume picks up with bounce

Score: 10-15
Signal: STRONG BUY
Strategy: Buy the dip in uptrend
```

---

### Pattern 2: Overextended Trend (Avoid)
```
Strong uptrend (ADX >25)
Price far above VWAP (>10%)
No oversold readings (RSI >60)
Squeeze forming

Score: 0-4
Signal: NO TRADE
Strategy: Wait for pullback
```

---

### Pattern 3: Mean Reversion (Ranging)
```
Low ADX (<20, no trend)
Multiple oversold signals
Price below VWAP
High volume buying (CMF positive)

Score: 6-10
Signal: BUY (if R:R good)
Strategy: Fade to resistance
```

---

### Pattern 4: False Breakout (Trap)
```
Moderate trend (ADX 20-25)
Price overextended vs VWAP
Squeeze active
Volume not confirming

Score: -2 to +2
Signal: NO TRADE
Strategy: Wait for confirmation
```

---

### Pattern 5: Confirmed Breakout (Rare)
```
ADX rising from <20 to >25
Price breaking above resistance
Volume 2x+ normal
CMF strongly positive
No squeeze (or just released)

Score: 8-12
Signal: BUY
Strategy: Momentum breakout
```

---

## Risk Management Rules

### Position Sizing
```
Account Risk: 1% per trade
Risk Per Share: Entry - Stop_Loss

Shares = (Account × 1%) / Risk_Per_Share

Example:
Account: $100,000
Risk: 1% = $1,000
Stop: $11.42 risk per share

Shares = $1,000 / $11.42 = 87 shares
```

### Stop Loss Placement
```
Always: Entry - (2 × ATR)

Why 2× ATR:
- 1× = Too tight (noise stops you out)
- 2× = Balanced (normal volatility room)
- 3× = Too wide (risk too much)
```

### Volatility Adjustment
```
If HIGH_VOL regime (Vol_Percentile >0.7):
- Reduce position size by 50%
- Accept wider stops
- Lower win rate expected
```

### Risk/Reward Minimums
```
BUY: Minimum 2.0:1 R:R
STRONG BUY: Minimum 2.5:1 R:R

Never enter if R:R <2:1
Even if score is perfect
```

---

## Quick Reference Table

| Indicator | Bullish | Neutral | Bearish | Points |
|-----------|---------|---------|---------|--------|
| ADX + Direction | >25, Plus_DI wins | 20-25 or <20 | >25, Minus_DI wins | ±5 or ±3 |
| Momentum (2-3) | RSI/Stoch/MFI <30 | Mixed | RSI/Stoch/MFI >70 | ±5 to ±6 |
| Volume | High vol + CMF >0.1 | Normal or mixed | High vol + CMF <-0.1 | ±2 |
| MA Structure | Perfect alignment | Partial | Inverse alignment | ±2 to ±3 |
| VWAP | <-3% deviation | ±3% | >+3% deviation | ±2 |
| Squeeze | Released/Off | - | Active/On | -2 |
| MACD | Bullish cross | - | Bearish cross | ±1 |
| Volatility | - | Normal (<0.8) | High (>0.8) | ×0.7 |

---

## Conclusion

**Core Principles:**

1. **Trend First:** ADX + Direction = Highest weight (±5)
2. **Confluence Matters:** Multiple indicators > single indicator
3. **Volume Confirms:** No signal valid without volume
4. **Value Conscious:** Price vs VWAP matters (mean reversion)
5. **Risk First:** R:R must meet minimum thresholds
6. **Volatility Aware:** Reduce conviction in chaos

**Signal Quality Hierarchy:**

```
STRONG BUY/SELL: Score ≥8, R:R ≥2.5 → Take these
BUY/SELL: Score ≥6, R:R ≥2.0 → Consider these
NO TRADE: Everything else → Pass and wait
```

**Remember:**
- Not every day has a trade
- "NO TRADE" is a position
- Patience beats forcing bad setups
- System protects you from yourself

---

**Next Steps:**
1. Backtest these rules on historical data
2. Validate weights empirically
3. Adjust thresholds based on results
4. Add to watchlist when signals approach trigger levels

---

*This is an educational tool. Always validate signals with additional analysis. Past performance does not guarantee future results. Not financial advice.*