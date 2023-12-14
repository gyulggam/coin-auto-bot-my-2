import uuid
import requests
import jwt
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
# filter_coin_list = list(filter(lambda x: x not in except_coin_list, all_coin_list)) # 거래 제외 코인 목록 제거한 코인 리스트
filter_coin_list = ['ARK', 'SC', 'IOST','IQ', 'IOTA', 'ELF', 'THETA', 'ZRX'] # 모든 코인을 돌 수 없어서 내가 선별함
columns = ['market', 'candle_date_time_utc', 'candle_date_time_kst', \
      'opening_price', 'high_price', 'low_price', 'trade_price', \
      'timestamp', 'candle_acc_trade_price', 'candle_acc_trade_volume', 'unit'\
      ]
today_date_str = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

def process_coin(coin):
  time.sleep(0.08)
  while True:
    print(f"{coin}-{datetime.now()}: 코인 탐색 시작")
    try:
      today_date_str = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
      candle_info = get_minute_candle(coin_name=coin, count=200, minute=5) # 5분봉 데이터 200개
      df = pd.DataFrame(candle_info, columns=columns)
      df = df.sort_values(by='candle_date_time_kst', ascending=True)
      
      coin_df = set_bollinger_bands(df, 30, 2) # 데이터 프레임에 볼린저 밴드 값 셋팅
      coin_df = set_rsi(coin_df, 13) # 데이터 프레임에 rsi 값 셋팅
      today_data = coin_df[coin_df['candle_date_time_kst'].str.startswith(today_date_str)] # 오늘 날짜의 데이터만 선택
      
      # 볼린저밴드의 하단 3% 보다 가격이 더떨어지고 rsi가 30이하일때 캐치
      coin_catch = today_data[(today_data["bol_lower_band"] * 0.03 + today_data["bol_lower_band"] > today_data["low_price"]) & (today_data['rsi'] < 30)]

      if not coin_catch.empty and 'market' in coin_catch.columns:
        set_trading_coin_df(coin_catch)

      
    except ZeroDivisionError as e:
      print("코인 탐색 멈춤")
      print(f"coinname:{coin} Error: {e}")

    time.sleep(3)

def coin_watcher():
  # ThreadPoolExecutor를 사용하여 병렬 처리
  with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
    # process_coin 함수를 각 코인에 대해 병렬로 실행
    # 결과는 futures 리스트에 저장
    print(filter_coin_list)
    futures = [executor.submit(process_coin, coin) for coin in filter_coin_list]

    # 각 future의 결과를 얻음
    for future in concurrent.futures.as_completed(futures):
        try:
            result = future.result()
            print(result)
            # 여기서 결과를 처리하거나 필요에 따라 저장
        except Exception as e:
            print(f"Error: {e}")
