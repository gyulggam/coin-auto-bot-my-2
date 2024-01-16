import pandas as pd

columns = ['market', 'candle_date_time_utc', 'candle_date_time_kst', \
      'opening_price', 'high_price', 'low_price', 'trade_price', \
      'timestamp', 'candle_acc_trade_price', 'candle_acc_trade_volume', 'unit', \
      'bol_lower_band', 'bol_middle_band', 'bol_upper_band', 'rsi'
      ]
g_trading_coin_df = pd.DataFrame(columns=columns)

def get_trading_coin_df():
  return g_trading_coin_df

# coin: coin 이름       string
# add : 추가 삭제 구분    bool
def set_trading_coin_df(coin_df):
  new_raw = pd.DataFrame([coin_df])
  global g_trading_coin_df
  # 빈 열이나 모든 값이 NA인 열 제거
  g_trading_coin_df = g_trading_coin_df.dropna(axis=1, how='all')
  g_trading_coin_df = pd.concat([g_trading_coin_df, new_raw], ignore_index=True)
  g_trading_coin_df = g_trading_coin_df = g_trading_coin_df.drop_duplicates(subset='market', keep='last')
