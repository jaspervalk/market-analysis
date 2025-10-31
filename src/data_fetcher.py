"""Stock Data Fetcher"""
import yfinance as yf
import pandas as pd

class StockDataFetcher:
    """Fetch and manage stock data"""
    
    def __init__(self):
        self.data = {}
    
    def fetch(self, ticker, period='3y'):
        """Fetch stock data"""
        print(f"Fetching {ticker} data...")
        stock = yf.Ticker(ticker)
        df = stock.history(period=period)
        
        if len(df) == 0:
            print(f"No data found for {ticker}")
            return None
        
        self.data[ticker] = df
        print(f"Got {len(df)} days of data")
        return df
    
    def get_info(self, ticker):
        """Get fundamental info"""
        stock = yf.Ticker(ticker)
        return stock.info
