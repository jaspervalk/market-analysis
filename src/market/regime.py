"""
Market Regime Detection

Identifies overall market health to prevent buying during corrections/bear markets.
Checks:
- Major indices trend (SPY, QQQ)
- VIX (fear gauge)
- Market breadth (% stocks above 200-day MA)
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


class MarketRegime:
    """Detects market regime (bull, neutral, bear)"""

    def __init__(self):
        self.cache = {}
        self.cache_time = None
        self.cache_duration = timedelta(hours=1)

    def _fetch_cached(self, ticker, period='6mo'):
        """Fetch data with 1-hour cache"""
        cache_key = f"{ticker}_{period}"
        now = datetime.now()

        if (self.cache_time and
            cache_key in self.cache and
            (now - self.cache_time) < self.cache_duration):
            return self.cache[cache_key]

        try:
            data = yf.download(ticker, period=period, progress=False)
            if not data.empty:
                # Flatten multi-level columns if present
                if isinstance(data.columns, pd.MultiIndex):
                    data.columns = data.columns.get_level_values(0)
                self.cache[cache_key] = data
                self.cache_time = now
                return data
        except:
            pass

        return None

    def check_index_health(self, ticker='SPY'):
        """
        Check if major index is healthy

        Returns:
            dict with:
                - healthy: bool
                - trend: 'bullish' | 'bearish' | 'neutral'
                - price: float
                - sma_50: float
                - sma_200: float
                - reason: str
        """
        df = self._fetch_cached(ticker, period='1y')
        if df is None or len(df) < 200:
            return {
                'healthy': None,
                'trend': 'unknown',
                'reason': 'Could not fetch index data'
            }

        # Convert to scalar values to avoid Series ambiguity
        current_price = float(df['Close'].iloc[-1])
        sma_50 = float(df['Close'].rolling(50).mean().iloc[-1])
        sma_200 = float(df['Close'].rolling(200).mean().iloc[-1])

        # Check trend
        above_50 = current_price > sma_50
        above_200 = current_price > sma_200
        ma_aligned = sma_50 > sma_200  # 50 above 200 = uptrend

        if above_50 and above_200 and ma_aligned:
            trend = 'bullish'
            healthy = True
            reason = f'{ticker} above 50 & 200 MA (uptrend)'
        elif not above_200:
            trend = 'bearish'
            healthy = False
            reason = f'{ticker} below 200 MA (downtrend)'
        else:
            trend = 'neutral'
            healthy = True
            reason = f'{ticker} mixed signals'

        return {
            'healthy': healthy,
            'trend': trend,
            'price': current_price,
            'sma_50': sma_50,
            'sma_200': sma_200,
            'reason': reason
        }

    def check_vix(self):
        """
        Check VIX (fear gauge)

        Returns:
            dict with:
                - level: float
                - status: 'low' | 'elevated' | 'high' | 'extreme'
                - healthy: bool
                - reason: str
        """
        df = self._fetch_cached('^VIX', period='1mo')
        if df is None or df.empty:
            return {
                'level': None,
                'status': 'unknown',
                'healthy': None,
                'reason': 'Could not fetch VIX data'
            }

        vix = float(df['Close'].iloc[-1])

        if vix < 15:
            status = 'low'
            healthy = True
            reason = f'VIX {vix:.1f} (low fear - healthy)'
        elif vix < 20:
            status = 'normal'
            healthy = True
            reason = f'VIX {vix:.1f} (normal - healthy)'
        elif vix < 30:
            status = 'elevated'
            healthy = False
            reason = f'VIX {vix:.1f} (elevated fear - caution)'
        else:
            status = 'extreme'
            healthy = False
            reason = f'VIX {vix:.1f} (extreme fear - danger)'

        return {
            'level': vix,
            'status': status,
            'healthy': healthy,
            'reason': reason
        }

    def check_market_breadth(self, tickers=None):
        """
        Check what % of stocks are above their 200-day MA

        Args:
            tickers: List of tickers to check (default: common large caps)

        Returns:
            dict with:
                - pct_above_200ma: float (0-100)
                - healthy: bool
                - reason: str
        """
        if tickers is None:
            # Sample of major stocks across sectors
            tickers = [
                'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA',
                'JPM', 'V', 'JNJ', 'WMT', 'PG', 'UNH', 'MA', 'HD',
                'BAC', 'XOM', 'DIS', 'NFLX', 'ADBE', 'CRM', 'COST'
            ]

        above_200 = 0
        total = 0

        for ticker in tickers:
            df = self._fetch_cached(ticker, period='1y')
            if df is not None and len(df) >= 200:
                price = df['Close'].iloc[-1]
                sma_200 = df['Close'].rolling(200).mean().iloc[-1]
                if price > sma_200:
                    above_200 += 1
                total += 1

        if total == 0:
            return {
                'pct_above_200ma': None,
                'healthy': None,
                'reason': 'Could not calculate breadth'
            }

        pct = (above_200 / total) * 100

        if pct > 60:
            healthy = True
            reason = f'{pct:.0f}% stocks above 200 MA (strong breadth)'
        elif pct > 40:
            healthy = True
            reason = f'{pct:.0f}% stocks above 200 MA (neutral)'
        else:
            healthy = False
            reason = f'{pct:.0f}% stocks above 200 MA (weak breadth)'

        return {
            'pct_above_200ma': pct,
            'healthy': healthy,
            'reason': reason
        }

    def get_regime(self, check_breadth=False):
        """
        Comprehensive market regime check

        Args:
            check_breadth: bool - Include breadth check (slower but more accurate)

        Returns:
            dict with:
                - regime: 'bull' | 'bear' | 'correction' | 'neutral'
                - healthy: bool
                - confidence: float (0-100)
                - checks: dict of individual check results
                - recommendation: str
        """
        checks = {}

        # Check SPY
        checks['spy'] = self.check_index_health('SPY')

        # Check QQQ (tech-heavy)
        checks['qqq'] = self.check_index_health('QQQ')

        # Check VIX
        checks['vix'] = self.check_vix()

        # Optional breadth check
        if check_breadth:
            checks['breadth'] = self.check_market_breadth()

        # Determine overall regime
        healthy_count = 0
        total_checks = 0

        for key in ['spy', 'qqq', 'vix']:
            if checks[key]['healthy'] is not None:
                total_checks += 1
                if checks[key]['healthy']:
                    healthy_count += 1

        if check_breadth and checks.get('breadth', {}).get('healthy') is not None:
            total_checks += 1
            if checks['breadth']['healthy']:
                healthy_count += 1

        confidence = (healthy_count / total_checks * 100) if total_checks > 0 else 0

        # Determine regime
        if confidence >= 75:
            regime = 'bull'
            healthy = True
            recommendation = 'BUY signals are valid'
        elif confidence >= 50:
            regime = 'neutral'
            healthy = True
            recommendation = 'BUY signals valid with caution'
        elif confidence >= 25:
            regime = 'correction'
            healthy = False
            recommendation = 'WAIT - Market correction in progress'
        else:
            regime = 'bear'
            healthy = False
            recommendation = 'WAIT - Bear market conditions'

        return {
            'regime': regime,
            'healthy': healthy,
            'confidence': confidence,
            'checks': checks,
            'recommendation': recommendation
        }


def check_market_health(verbose=True, check_breadth=False):
    """
    Quick function to check market health

    Args:
        verbose: bool - Print details
        check_breadth: bool - Include breadth check (slower)

    Returns:
        dict - Market regime data
    """
    regime = MarketRegime()
    result = regime.get_regime(check_breadth=check_breadth)

    if verbose:
        print("="*60)
        print("MARKET REGIME ANALYSIS")
        print("="*60)
        print(f"\nRegime: {result['regime'].upper()}")
        print(f"Confidence: {result['confidence']:.0f}%")
        print(f"Recommendation: {result['recommendation']}")
        print(f"\nDetails:")

        for key, check in result['checks'].items():
            status = 'HEALTHY' if check.get('healthy') else 'UNHEALTHY'
            if check.get('healthy') is None:
                status = 'UNKNOWN'
            print(f"  [{status}] {check.get('reason', 'N/A')}")

        print("="*60)

    return result
