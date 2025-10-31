"""
Feature Engineering for Stock Market Prediction
Uses the custom TechnicalIndicators library
"""

import pandas as pd
import numpy as np
from indicators import TechnicalIndicators


class FeatureEngineer:
    """Create features for ML models"""
    
    def __init__(self, df):
        """
        Initialize with a dataframe containing: Open, High, Low, Close, Volume
        """
        self.df = df.copy()
        self.ti = TechnicalIndicators()
    
    def add_technical_indicators(self):
        """Add all technical indicators"""
        df = self.df
        
        print("Adding technical indicators...")
        
        # Moving Averages
        df['SMA_10'] = self.ti.sma(df['Close'], 10)
        df['SMA_20'] = self.ti.sma(df['Close'], 20)
        df['SMA_50'] = self.ti.sma(df['Close'], 50)
        df['SMA_200'] = self.ti.sma(df['Close'], 200)
        df['EMA_12'] = self.ti.ema(df['Close'], 12)
        df['EMA_26'] = self.ti.ema(df['Close'], 26)
        
        # RSI
        df['RSI_14'] = self.ti.rsi(df['Close'], 14)
        df['RSI_7'] = self.ti.rsi(df['Close'], 7)
        
        # MACD
        macd = self.ti.macd(df['Close'])
        df['MACD'] = macd['MACD']
        df['MACD_Signal'] = macd['MACD_Signal']
        df['MACD_Hist'] = macd['MACD_Hist']
        
        # Bollinger Bands
        bb = self.ti.bollinger_bands(df['Close'], window=20)
        df['BB_Upper'] = bb['BB_Upper']
        df['BB_Middle'] = bb['BB_Middle']
        df['BB_Lower'] = bb['BB_Lower']
        df['BB_Width'] = bb['BB_Width']
        df['BB_Position'] = (df['Close'] - bb['BB_Lower']) / (bb['BB_Upper'] - bb['BB_Lower'])
        
        # ATR (Volatility)
        df['ATR_14'] = self.ti.atr(df['High'], df['Low'], df['Close'], 14)
        
        # Stochastic
        stoch = self.ti.stochastic(df['High'], df['Low'], df['Close'])
        df['STOCH_K'] = stoch['STOCH_K']
        df['STOCH_D'] = stoch['STOCH_D']
        
        # OBV
        df['OBV'] = self.ti.obv(df['Close'], df['Volume'])
        
        # CCI
        df['CCI_20'] = self.ti.cci(df['High'], df['Low'], df['Close'], 20)
        
        # Williams %R
        df['Williams_R'] = self.ti.williams_r(df['High'], df['Low'], df['Close'], 14)
        
        # ADX
        adx = self.ti.adx(df['High'], df['Low'], df['Close'], 14)
        df['ADX'] = adx['ADX']
        df['Plus_DI'] = adx['Plus_DI']
        df['Minus_DI'] = adx['Minus_DI']
        
        self.df = df
        return self
    
    def add_price_features(self):
        """Add price-based features"""
        df = self.df
        
        print("Adding price features...")
        
        # Returns
        df['Returns'] = df['Close'].pct_change()
        df['Log_Returns'] = np.log(df['Close'] / df['Close'].shift(1))
        
        # Volatility (rolling std)
        df['Volatility_5'] = df['Returns'].rolling(window=5).std()
        df['Volatility_10'] = df['Returns'].rolling(window=10).std()
        df['Volatility_20'] = df['Returns'].rolling(window=20).std()
        df['Volatility_30'] = df['Returns'].rolling(window=30).std()
        
        # Price momentum
        df['Momentum_5'] = self.ti.momentum(df['Close'], 5)
        df['Momentum_10'] = self.ti.momentum(df['Close'], 10)
        df['Momentum_20'] = self.ti.momentum(df['Close'], 20)
        
        # Rate of change
        df['ROC_5'] = self.ti.roc(df['Close'], 5)
        df['ROC_10'] = self.ti.roc(df['Close'], 10)
        df['ROC_20'] = self.ti.roc(df['Close'], 20)
        
        # High-Low range
        df['HL_Range'] = df['High'] - df['Low']
        df['HL_Pct'] = (df['High'] - df['Low']) / df['Close']
        
        # Close position in daily range
        df['Close_Position'] = (df['Close'] - df['Low']) / (df['High'] - df['Low'])
        
        # Gap (Open vs previous Close)
        df['Gap'] = df['Open'] - df['Close'].shift(1)
        df['Gap_Pct'] = (df['Open'] - df['Close'].shift(1)) / df['Close'].shift(1)
        
        # Daily range vs average
        df['Range_vs_Avg'] = df['HL_Range'] / df['HL_Range'].rolling(20).mean()
        
        self.df = df
        return self
    
    def add_volume_features(self):
        """Add volume-based features"""
        df = self.df
        
        print("Adding volume features...")
        
        # Volume moving averages
        df['Volume_SMA_5'] = self.ti.sma(df['Volume'], 5)
        df['Volume_SMA_10'] = self.ti.sma(df['Volume'], 10)
        df['Volume_SMA_20'] = self.ti.sma(df['Volume'], 20)
        
        # Volume ratio
        df['Volume_Ratio_5'] = df['Volume'] / df['Volume_SMA_5']
        df['Volume_Ratio_20'] = df['Volume'] / df['Volume_SMA_20']
        
        # Volume rate of change
        df['Volume_ROC_5'] = self.ti.roc(df['Volume'], 5)
        
        # Price-Volume trend
        df['PV_Trend'] = df['Close'] * df['Volume']
        
        self.df = df
        return self
    
    def add_lagged_features(self, n_lags=5):
        """Add lagged features"""
        df = self.df
        
        print(f"Adding {n_lags} lagged features...")
        
        for i in range(1, n_lags + 1):
            df[f'Close_lag_{i}'] = df['Close'].shift(i)
            df[f'Returns_lag_{i}'] = df['Returns'].shift(i)
            df[f'Volume_lag_{i}'] = df['Volume'].shift(i)
        
        self.df = df
        return self
    
    def add_trend_features(self):
        """Add trend identification features"""
        df = self.df
        
        print("Adding trend features...")
        
        # MA crossovers
        df['SMA_Cross_20_50'] = (df['SMA_20'] > df['SMA_50']).astype(int)
        df['SMA_Cross_50_200'] = (df['SMA_50'] > df['SMA_200']).astype(int)
        
        # Price vs MA
        df['Price_vs_SMA20'] = (df['Close'] - df['SMA_20']) / df['SMA_20']
        df['Price_vs_SMA50'] = (df['Close'] - df['SMA_50']) / df['SMA_50']
        
        # Trend strength
        df['Trend_Strength'] = df['Close'].rolling(20).apply(
            lambda x: (x.iloc[-1] - x.iloc[0]) / x.iloc[0] if x.iloc[0] != 0 else 0
        )
        
        self.df = df
        return self
    
    def create_target(self, horizon=1, threshold=0.02, method='classification'):
        """
        Create target variable
        
        Parameters:
        -----------
        horizon : int
            How many days ahead to predict (1 = next day)
        threshold : float
            Minimum return for buy/sell classification (0.02 = 2%)
        method : str
            'classification' or 'regression'
        """
        df = self.df
        
        print(f"Creating target variable (horizon={horizon}, threshold={threshold*100}%)...")
        
        # Future returns
        df['Future_Returns'] = df['Close'].shift(-horizon) / df['Close'] - 1
        
        if method == 'classification':
            # Three classes: -1 (Sell), 0 (Hold), 1 (Buy)
            df['Target'] = 0  # Hold
            df.loc[df['Future_Returns'] > threshold, 'Target'] = 1  # Buy
            df.loc[df['Future_Returns'] < -threshold, 'Target'] = -1  # Sell
            
            # Count distribution
            target_counts = df['Target'].value_counts()
            print(f"\nTarget distribution:")
            print(f"  Buy (1):  {target_counts.get(1, 0)} ({target_counts.get(1, 0)/len(df)*100:.1f}%)")
            print(f"  Hold (0): {target_counts.get(0, 0)} ({target_counts.get(0, 0)/len(df)*100:.1f}%)")
            print(f"  Sell (-1): {target_counts.get(-1, 0)} ({target_counts.get(-1, 0)/len(df)*100:.1f}%)")
        
        elif method == 'regression':
            # Predict actual returns
            df['Target'] = df['Future_Returns']
        
        self.df = df
        return self
    
    def build_all_features(self, n_lags=5, target_horizon=1, target_threshold=0.02):
        """
        Build all features in one go
        """
        print("\n" + "="*60)
        print("BUILDING ALL FEATURES")
        print("="*60)
        
        self.add_technical_indicators()
        self.add_price_features()
        self.add_volume_features()
        self.add_lagged_features(n_lags)
        self.add_trend_features()
        self.create_target(target_horizon, target_threshold)
        
        print("\n All features built!")
        print(f"Total columns: {len(self.df.columns)}")
        print(f"Total rows: {len(self.df)}")
        
        return self
    
    def get_features(self, drop_na=True):
        """Return processed dataframe"""
        if drop_na:
            original_len = len(self.df)
            df_clean = self.df.dropna()
            dropped = original_len - len(df_clean)
            print(f"\nDropped {dropped} rows with NaN values")
            print(f"Remaining rows: {len(df_clean)}")
            return df_clean
        return self.df
    
    def get_feature_names(self, exclude=None):
        """Get list of feature column names"""
        if exclude is None:
            exclude = ['Open', 'High', 'Low', 'Close', 'Volume', 
                      'Target', 'Future_Returns', 'Ticker', 'Dividends', 
                      'Stock Splits']
        
        all_cols = self.df.columns.tolist()
        features = [col for col in all_cols if col not in exclude]
        
        print(f"\n Feature columns ({len(features)}):")
        for i, feat in enumerate(features, 1):
            print(f"  {i}. {feat}")
        
        return features
    
    def get_correlation_with_target(self, top_n=20):
        """Show correlation of features with target"""
        if 'Target' not in self.df.columns:
            print("  No target variable found. Run create_target() first.")
            return None
        
        feature_cols = self.get_feature_names()
        correlations = self.df[feature_cols + ['Target']].corr()['Target'].drop('Target')
        correlations = correlations.abs().sort_values(ascending=False)
        
        print(f"\n Top {top_n} features by correlation with target:")
        print("="*60)
        for i, (feat, corr) in enumerate(correlations.head(top_n).items(), 1):
            print(f"{i:2d}. {feat:30s} : {corr:.4f}")
        
        return correlations.head(top_n)