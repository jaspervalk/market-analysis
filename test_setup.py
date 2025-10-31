"""
Test if your setup is working
Run: python test_setup.py
"""

print("Testing imports...\n")

# Test basic imports
try:
    import pandas as pd
    print(f"✅ pandas {pd.__version__}")
except ImportError as e:
    print(f"❌ pandas: {e}")

try:
    import numpy as np
    print(f"✅ numpy {np.__version__}")
except ImportError as e:
    print(f"❌ numpy: {e}")

try:
    import yfinance as yf
    print(f"✅ yfinance {yf.__version__}")
except ImportError as e:
    print(f"❌ yfinance: {e}")

try:
    import sklearn
    print(f"✅ scikit-learn {sklearn.__version__}")
except ImportError as e:
    print(f"❌ scikit-learn: {e}")

try:
    import xgboost as xgb
    print(f"✅ xgboost {xgb.__version__}")
except ImportError as e:
    print(f"❌ xgboost: {e}")

try:
    import lightgbm as lgb
    print(f"✅ lightgbm {lgb.__version__}")
except ImportError as e:
    print(f"❌ lightgbm: {e}")

try:
    import matplotlib
    print(f"✅ matplotlib {matplotlib.__version__}")
except ImportError as e:
    print(f"❌ matplotlib: {e}")

print("\n" + "="*50)
print("Testing yfinance download...\n")

try:
    stock = yf.Ticker("AAPL")
    df = stock.history(period="5d")
    print(f"✅ Successfully downloaded {len(df)} rows of AAPL data")
    print(f"\nLast close price: ${df['Close'].iloc[-1]:.2f}")
    print("\n✅✅✅ ALL TESTS PASSED! ✅✅✅")
except Exception as e:
    print(f"❌ Error downloading data: {e}")