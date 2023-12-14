import pandas

def set_rsi(coin_df_origin, rsi_period = 13):
  result = coin_df_origin.copy(deep=True)

  # 가격 변화율 계산
  delta = result['trade_price'].diff(1)
  
  # 상승한 가격 변화만 가져오기 (음수는 0으로 대체)
  gain = delta.where(delta > 0, 0)

  # 하락한 가격 변화만 가져오기 (양수는 0으로 대체)
  loss = -delta.where(delta < 0, 0)
  
  # 이동평균 계산
  avg_gain = gain.rolling(window=rsi_period, min_periods=1).mean()
  avg_loss = loss.rolling(window=rsi_period, min_periods=1).mean()

  # 상대적 강도 계산
  rs = avg_gain / avg_loss

  # RSI 계산
  rsi = 100 - (100 / (1 + rs))
  
  result['rsi'] = rsi

  return result