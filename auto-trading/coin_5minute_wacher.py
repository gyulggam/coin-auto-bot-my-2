import uuid
import requests
import jwt
import ta
# from concurrent.futures import ThreadPoolExecutor
import concurrent.futures 
from datetime import datetime
import time
from urllib.parse import urlencode
import hashlib
import pandas as pd
from config import config
from global_variable import set_trading_coin_df
from get_candle_info import get_minute_candle
from get_coin_symbol import get_all_symbol
from bollinger_bands import set_bollinger_bands
from rsi import set_rsi

access_key = config.get("access_key") # upbit access_key
secret_key = config.get("secret_key") # upbit secret_key
server_url = config.get("server_url") # upbit api server_url

all_coin_list = get_all_symbol()    # 업비트 모든 코인 리스트
except_coin_list = [                # 거래 제외 코인 리스트
  'BTC',
  'ETH',
  'DOGE',
  'XRP',
  'BTG',
  'ANKR',
  'EOS',
  'QTUM',
  'XLM',
  'FLOW',
  'TON',
  'USDT',
  'TRX',
  'NEO',
  'ORBS',
  'HBAR',
  'VET',
  'BCH',
  'MTL',
  'CTC',
  'SEI',
  'DOT',
  'EGLD',
  'AXS',
  'XEC',
  'GRT',
  'TT',
  'META',
  'STPT',
  'ZRX',
  'PUNDIX',
  'UPP',
  'MVL'
]
filter_coin_list = list(filter(lambda x: x not in except_coin_list, all_coin_list)) # 거래 제외 코인 목록 제거한 코인 리스트
# filter_coin_list = ['XTZ', 'BLUR', 'SUI'] # 모든 코인을 돌 수 없어서 내가 선별함
columns = ['market', 'candle_date_time_utc', 'candle_date_time_kst', \
      'opening_price', 'high_price', 'low_price', 'trade_price', \
      'timestamp', 'candle_acc_trade_price', 'candle_acc_trade_volume', 'unit'\
      ]
today_date_str = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
candle_minute = 30 # 분봉 단위
lower_range_value = 0.99 # 볼린저 밴드 하단 값 깊이 캐치 볼밴 하단보다 1%밑일때 잡는다.

def process_coin(coin):
  while True:
    print(f"{coin}-{datetime.now()}: 코인 탐색 시작")
    # today_date_str = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    candle_info = get_minute_candle(coin_name=coin, count=200, minute=candle_minute) # 5분봉 데이터 200개
    coin_catch = pd.DataFrame(columns=columns)
    df = pd.DataFrame(candle_info, columns=columns)
    df = df.sort_values(by='candle_date_time_kst', ascending=True)
    
    coin_df = set_bollinger_bands(df, 30, 2) # 데이터 프레임에 볼린저 밴드 값 셋팅
    coin_df = set_rsi(coin_df, 13) # 데이터 프레임에 rsi 값 셋팅
    
    # today_data = coin_df[coin_df['candle_date_time_kst'].str.startswith(today_date_str)] # 일별 서칭을 할땐 사용함 오늘 날짜의 데이터만 선택
    today_data = coin_df.iloc[-1] # 분봉에서 최근데이터만 선택
    
    # 볼린저밴드의 하단 3% 보다 가격이 더떨어지고 rsi가 30이하일때 캐치
    # coin_catch = today_data[(today_data["bol_lower_band"] * lower_range_value + today_data["bol_lower_band"] > today_data["trade_price"]) & (today_data['rsi'] < 30)] # 일별에서만 씀
    if (today_data["bol_lower_band"] * lower_range_value > today_data["trade_price"]) & (today_data['rsi'] < 30):
      print(f"{coin}이 검색되었습니다.")
      coin_catch = today_data
    
    if not coin_catch.empty:
      set_trading_coin_df(coin_catch)

    time.sleep(3)

def coin_watcher():
  # process coin에서 while 돌게 아니고 여기서 돌아서 스텝을 넘어가게끔 해야할것같아.
  for step in range(0, len(filter_coin_list), 10):
    current_coins = filter_coin_list[step:step + 10]
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
      
      futures = [executor.submit(process_coin, coin) for coin in current_coins]
      print(current_coins)

      # 각 future의 결과를 얻음
      for future in concurrent.futures.as_completed(futures):
        try:
          result = future.result()
          print(result)
          # 여기서 결과를 처리하거나 필요에 따라 저장
          pass
        except Exception as e:
          print("코인 탐색 멈춤")
          print(f"Error: {e}")
        except KeyboardInterrupt:
          print("프로그램이 사용자에 의해 중단되었습니다.")
          executor.shutdown(wait=False)
        finally:
          # 프로그램 종료 전에 정리 작업 수행
          print("프로그램을 종료합니다.")
# def coin_watcher():
#   with ThreadPoolExecutor() as executor:
#     results = []
#     for coin in filter_coin_list:
#       # 동적으로 쿼리 수를 조절
#       start_time = time.time()
#       while True:
#         result = executor.submit(process_coin, coin)

#         # 요청 간격이 너무 짧으면 대기
#         elapsed_time = time.time() - start_time
#         if elapsed_time < 1 / 2:
#           time.sleep(1 / 2 - elapsed_time)
#         else:
#           break

#   # 결과를 딕셔너리로 변환
#   try:
#     for result in results:
#       print(result)
#       pass
#   except Exception as e:
#     print("코인 탐색 멈춤")
#     print(f"Error: {e}")
#   except KeyboardInterrupt:
#     print("프로그램이 사용자에 의해 중단되었습니다.")
#     executor.shutdown(wait=False)
#   finally:
#     # 프로그램 종료 전에 정리 작업 수행
#     print("프로그램을 종료합니다.")

