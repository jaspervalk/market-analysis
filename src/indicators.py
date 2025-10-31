"""Technical Indicators Library - Extended"""
import pandas as pd
import numpy as np

# Existing functions (keep these)
def sma(data, window):
    return data.rolling(window=window).mean()

def ema(data, window):
    return data.ewm(span=window, adjust=False).mean()

def rsi(data, window=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def macd(data, fast=12, slow=26, signal=9):
    ema_fast = ema(data, fast)
    ema_slow = ema(data, slow)
    macd_line = ema_fast - ema_slow
    signal_line = ema(macd_line, signal)
    histogram = macd_line - signal_line
    return pd.DataFrame({
        'MACD': macd_line,
        'Signal': signal_line,
        'Histogram': histogram
    })

def bollinger_bands(data, window=20, num_std=2):
    middle = sma(data, window)
    std = data.rolling(window=window).std()
    upper = middle + (std * num_std)
    lower = middle - (std * num_std)
    return pd.DataFrame({
        'Upper': upper,
        'Middle': middle,
        'Lower': lower
    })

def adx(high, low, close, window=14):
    """Average Directional Index - Trend Strength"""
    plus_dm = high.diff()
    minus_dm = -low.diff()
    
    plus_dm[plus_dm < 0] = 0
    minus_dm[minus_dm < 0] = 0
    
    tr1 = high - low
    tr2 = abs(high - close.shift())
    tr3 = abs(low - close.shift())
    tr = pd.DataFrame({'tr1': tr1, 'tr2': tr2, 'tr3': tr3}).max(axis=1)
    
    atr = tr.rolling(window=window).mean()
    plus_di = 100 * (plus_dm.rolling(window=window).mean() / atr)
    minus_di = 100 * (minus_dm.rolling(window=window).mean() / atr)
    
    dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
    adx_value = dx.rolling(window=window).mean()
    
    return pd.DataFrame({
        'ADX': adx_value,
        'Plus_DI': plus_di,
        'Minus_DI': minus_di
    })

def atr(high, low, close, window=14):
    """Average True Range - Volatility"""
    tr1 = high - low
    tr2 = abs(high - close.shift())
    tr3 = abs(low - close.shift())
    tr = pd.DataFrame({'tr1': tr1, 'tr2': tr2, 'tr3': tr3}).max(axis=1)
    return tr.rolling(window=window).mean()

def stochastic(high, low, close, k_window=14, d_window=3):
    """Stochastic Oscillator"""
    lowest_low = low.rolling(window=k_window).min()
    highest_high = high.rolling(window=k_window).max()
    
    k_percent = 100 * ((close - lowest_low) / (highest_high - lowest_low))
    d_percent = k_percent.rolling(window=d_window).mean()
    
    return pd.DataFrame({
        'K': k_percent,
        'D': d_percent
    })

def cci(high, low, close, window=20):
    """Commodity Channel Index"""
    typical_price = (high + low + close) / 3
    sma_tp = typical_price.rolling(window=window).mean()
    mean_deviation = typical_price.rolling(window=window).apply(
        lambda x: np.abs(x - x.mean()).mean()
    )
    cci_value = (typical_price - sma_tp) / (0.015 * mean_deviation)
    return cci_value

def williams_r(high, low, close, window=14):
    """Williams %R"""
    highest_high = high.rolling(window=window).max()
    lowest_low = low.rolling(window=window).min()
    
    wr = -100 * ((highest_high - close) / (highest_high - lowest_low))
    return wr

def roc(data, window=10):
    """Rate of Change"""
    return ((data - data.shift(window)) / data.shift(window)) * 100

def obv(close, volume):
    """On Balance Volume"""
    return (np.sign(close.diff()) * volume).fillna(0).cumsum()

def mfi(high, low, close, volume, window=14):
    """Money Flow Index - RSI with Volume"""
    typical_price = (high + low + close) / 3
    money_flow = typical_price * volume
    
    positive_flow = money_flow.where(typical_price > typical_price.shift(1), 0)
    negative_flow = money_flow.where(typical_price < typical_price.shift(1), 0)
    
    positive_mf = positive_flow.rolling(window=window).sum()
    negative_mf = negative_flow.rolling(window=window).sum()
    
    mfr = positive_mf / negative_mf
    mfi_value = 100 - (100 / (1 + mfr))
    
    return mfi_value

def cmf(high, low, close, volume, window=20):
    """Chaikin Money Flow"""
    mfv = ((close - low) - (high - close)) / (high - low) * volume
    mfv = mfv.fillna(0)
    cmf_value = mfv.rolling(window=window).sum() / volume.rolling(window=window).sum()
    return cmf_value

def supertrend(high, low, close, atr_period=10, multiplier=3):
    """SuperTrend Indicator - Fixed Version"""
    atr_values = atr(high, low, close, atr_period)
    
    hl_avg = (high + low) / 2
    upper_band = hl_avg + (multiplier * atr_values)
    lower_band = hl_avg - (multiplier * atr_values)
    
    supertrend = pd.Series(index=close.index, dtype=float)
    direction = pd.Series(index=close.index, dtype=int)
    
    # Initialize first valid values (skip NaN from ATR calculation)
    first_valid = atr_period
    supertrend.iloc[first_valid] = lower_band.iloc[first_valid]
    direction.iloc[first_valid] = 1
    
    for i in range(first_valid + 1, len(close)):
        # Bullish trend (direction = 1)
        if direction.iloc[i-1] == 1:
            if close.iloc[i] > lower_band.iloc[i]:
                supertrend.iloc[i] = lower_band.iloc[i]
                direction.iloc[i] = 1
            else:
                supertrend.iloc[i] = upper_band.iloc[i]
                direction.iloc[i] = -1
        # Bearish trend (direction = -1)
        else:
            if close.iloc[i] < upper_band.iloc[i]:
                supertrend.iloc[i] = upper_band.iloc[i]
                direction.iloc[i] = -1
            else:
                supertrend.iloc[i] = lower_band.iloc[i]
                direction.iloc[i] = 1
    
    return pd.DataFrame({
        'SuperTrend': supertrend,
        'Direction': direction
    })

def keltner_channels(high, low, close, window=20, atr_period=10, multiplier=2):
    """Keltner Channels"""
    middle = ema(close, window)
    atr_values = atr(high, low, close, atr_period)
    
    upper = middle + (multiplier * atr_values)
    lower = middle - (multiplier * atr_values)
    
    return pd.DataFrame({
        'Upper': upper,
        'Middle': middle,
        'Lower': lower
    })

def donchian_channels(high, low, window=20):
    """Donchian Channels"""
    upper = high.rolling(window=window).max()
    lower = low.rolling(window=window).min()
    middle = (upper + lower) / 2
    
    return pd.DataFrame({
        'Upper': upper,
        'Middle': middle,
        'Lower': lower
    })

def ichimoku_cloud(high, low, close):
    """Ichimoku Cloud - multi-timeframe support/resistance"""
    conversion = (high.rolling(9).max() + low.rolling(9).min()) / 2
    base = (high.rolling(26).max() + low.rolling(26).min()) / 2
    span_a = ((conversion + base) / 2).shift(26)
    span_b = ((high.rolling(52).max() + low.rolling(52).min()) / 2).shift(26)
    
    return pd.DataFrame({
        'Conversion': conversion,
        'Base': base,
        'Span_A': span_a,
        'Span_B': span_b
    })

def squeeze_momentum(high, low, close, bb_length=20, kc_length=20):
    """
    Squeeze Momentum - detects consolidation before breakouts
    
    Returns DataFrame with:
    - Squeeze_On: Boolean indicating if squeeze is active (BB inside KC)
    - Momentum: Price momentum value
    """
    # Calculate Bollinger Bands and Keltner Channels
    bb = bollinger_bands(close, bb_length)
    kc = keltner_channels(high, low, close, kc_length)
    
    # Squeeze detection: BB inside KC means consolidation
    squeeze_on = (bb['Lower'] > kc['Lower']) & (bb['Upper'] < kc['Upper'])
    
    # Calculate momentum (simplified version)
    # Momentum = Close - SMA of close over bb_length
    momentum = close - sma(close, bb_length)
    
    return pd.DataFrame({
        'Squeeze_On': squeeze_on,
        'Momentum': momentum
    })

def vwap(high, low, close, volume):
    """Volume Weighted Average Price"""
    typical_price = (high + low + close) / 3
    return (typical_price * volume).cumsum() / volume.cumsum()

print('Extended indicators module loaded')