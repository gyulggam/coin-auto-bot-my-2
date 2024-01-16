import pandas as pd

columns = ['market', 'candle_date_time_utc', 'candle_date_time_kst', \
      'opening_price', 'high_price', 'low_price', 'trade_price', \
      'timestamp', 'candle_acc_trade_price', 'candle_acc_trade_volume', 'unit'\
      ]
g_trading_coin_df = pd.DataFrame(columns=columns)

def get_trading_coin_df():
  return g_trading_coin_df

# coin: coin 이름       string
# add : 추가 삭제 구분    bool
def set_trading_coin_df(coin_df):
  new_row = pd.DataFrame([coin_df.loc[0]])
  print("coin_df",coin_df) 
  print("new_row",new_row) 
  global g_trading_coin_df
  g_trading_coin_df = pd.concat([g_trading_coin_df, new_row], ignore_index=True)
  g_trading_coin_df = g_trading_coin_df[g_trading_coin_df.duplicated(subset='market')]
  print(g_trading_coin_df)
