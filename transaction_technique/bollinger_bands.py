import pandas as pd

def set_bollinger_bands(coin_df_origin, ma = 20, std = 2):
  result = coin_df_origin.copy(deep=True)
  # 계산에 필요한 값 추가

  # 볼린저 밴드 계산을 위한 상수
  bol_ma = ma # 20일 이동 평균
  bol_std_multiplier = std # 표준편차에(bol_ma) 곱함

  bol_middle_band = result['trade_price'].rolling(window=bol_ma).mean()
  
  bol_upper_band = bol_middle_band + (result['trade_price'].rolling(window=bol_ma).std() * bol_std_multiplier)
  bol_lower_band = bol_middle_band - (result['trade_price'].rolling(window=bol_ma).std() * bol_std_multiplier)

  result['bol_middle_band'] = bol_middle_band # 볼린저밴드 중앙
  result['bol_upper_band'] = bol_upper_band # 볼린저밴드 상단
  result['bol_lower_band'] = bol_lower_band # 볼린저밴드 하단
  
  return result