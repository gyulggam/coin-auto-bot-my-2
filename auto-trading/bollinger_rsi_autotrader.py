# 승률 100% AIS1 Upbit 봇 구현
import sys
import os
import platform
if platform.system() == 'Windows':
    # Windows 경로
    sys.path.append('D:\\개발\\coin-auto-bot-my\\api')
    sys.path.append('D:\\개발\\coin-auto-bot-my\\config')
    sys.path.append('D:\\개발\\coin-auto-bot-my\\transaction_technique')
else:
    # macOS 경로
    sys.path.append('/Users/kjs/Desktop/Traning/coin-auto-bot-my-2/api')
    sys.path.append('/Users/kjs/Desktop/Traning/coin-auto-bot-my-2/config')
    sys.path.append('/Users/kjs/Desktop/Traning/coin-auto-bot-my-2/transaction_technique')

from datetime import datetime
import uuid
import requests
import time
import pandas
# from telegram import Bot
from urllib.parse import urlencode
from config import config
from get_coin_symbol import get_all_symbol
from global_variable import get_trading_coin_df
from coin_5minute_wacher import coin_watcher

current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)
root_dir = os.path.dirname(current_dir)


# TELEGRAM_BOT_TOKEN_FOR_AIS1 = config.get("TELEGRAM_BOT_TOKEN_FOR_AIS1")   # 내 telegram bot token 입력
# TELEGRAM_CHAT_ID_FOR_AIS1 = config.get("TELEGRAM_CHAT_ID_FOR_AIS1")       # 내 telegram chat id 입력

# 전역변수
all_coin_list = get_all_symbol()   # 업비트 모든 코인 리스트
except_coin_list = ['DOGE', 'XRP', 'BTG', 'ANKR', 'EOS', 'QTUM', 'XLM', 'FLOW', 'TON', 'USDT', 'TRX', 'NEO', 'ORBS', 'HBAR', 'VET', 'BCH', 'MTL'] # 거래 제외 코인 리스트
filter_coin_list = list(filter(lambda x: x not in except_coin_list, all_coin_list)) # 거래 제외 코인 목록 제거한 코인 리스트
file_path =  os.path.join(root_dir, 'catch_coin.csv') # 임시로 검색기에 잡힌 코인을 저장해둘 파일
# telegram_bot = telegram.Bot(TELEGRAM_BOT_TOKEN_FOR_AIS1) # set telegram bot

# 설정값변수 설정
target_sell_price_ratio = 1.02          # 매수후 매수평단가 대비 +2% 상승에 매도
has_position = {}                       # 포지션 보유유무
buy_amount_capital = 1_000_000          # 구매할 금액
sell_order_amount = {}                  # 매도할 수량
target_sell_price = {}                  # 매도할 금액
each_average_buy_price = {}             # 매수 평단가
yesterday_change_rate_threshold = 0.10  # 전날 상승률 threshold

def upbit_price_tick_revision(price):
    price = float(price)

    if price < 0.1:
        price = "{:0.0{}f}".format(price, 4) #소수점 넷째자리
    elif price < 1:
        price = "{:0.0{}f}".format(price, 3) #소수점 셋째자리
    elif price < 10:
        price = "{:0.0{}f}".format(price, 2) #소수점 둘째자리
    elif price < 100:
        price = "{:0.0{}f}".format(price, 1) #소수점 첫째자리
    elif price < 1000:
        price = "{:0.0{}f}".format(price, 0) #1원 단위
    elif price < 10_000:
        price = round(float("{:0.0{}f}".format(price, 0)) / 5)*5 # 5원 단위
    elif price < 100_000:
        price = round(float("{:0.0{}f}".format(price, 0)) / 10)*10 # 10원 단위
    elif price < 500_000:
        price = round(float("{:0.0{}f}".format(price, 0)) / 50)*50 # 50원 단위
    elif price < 1_000_000:
        price = round(float("{:0.0{}f}".format(price, 0)) / 100)*100 # 100원 단위
    elif price < 2_000_000:
        price = round(float("{:0.0{}f}".format(price, 0)) / 500)*500 # 500원 단위
    elif price >= 2_000_000:
        price = round(float("{:0.0{}f}".format(price, 0)) / 1000)*1000 # 1000원 단위

    price = float(price)

    return price

if __name__ == "__main__":
  coin_watcher() # 코인 검색하는 watcher
  
  while True:
    watch_coin_df = get_trading_coin_df()
    
    if len(watch_coin_df) > 0:
      watch_coin_df.to_csv(file_path, index=False)
      print(f'검색된코인: {watch_coin_df}')
      
    # telegram_message_list = [str(datetime.datetime.now()), '자동 거래 스타트']
    # telegram_bot.sendMessage(chat_id=TELEGRAM_CHAT_ID_FOR_AIS1, text=' '.join(telegram_message_list))

    # 목표로하는 코인의 ticker들
    # total_ticker_list = filter_coin_list
    # print(total_ticker_list)
    # print('Upbit AIS1 코인 개수 :', len(total_ticker_list))

    # for ticker in total_ticker_list:
    #     # 변수 초기화
    #     has_position[ticker] = False

    #     get_day_candle_result = get_minute_candle(coin_name=ticker, count=200, minute=5)

    #     telegram_message_list = [str(datetime.datetime.now()), f'@@@@@@@ canlde update {ticker} yesterday_change_rate: {(yesterday_change_rate)} @@@@@@@@@@@@@']
    #     telegram_bot.sendMessage(chat_id=TELEGRAM_CHAT_ID_FOR_AIS1, text=' '.join(telegram_message_list))

    #     # 전체 코인 보유 잔량이 있는지 확인
    #     balance_result = get_balance()
    #     #print(balance_result)
    #     for each_asset in balance_result:
    #         each_ticker = each_asset['currency']
    #         if each_ticker in total_ticker_list:
    #             hold_amount = float(each_asset['balance'])
    #             avg_buy_price = float(each_asset['avg_buy_price'])            
    #             print(f"{each_ticker} 보유 개수 :", hold_amount)
    #             print(f"{each_ticker} 평균 매수 가격 :", avg_buy_price)

    #             # 5000원 이상 해당 코인을 보유중일 경우 보유중으로 판단
    #             if (hold_amount * avg_buy_price) > 5000.0:
    #                 has_position[each_ticker] = True
    #     time.sleep(0.1)

    #     # 코인을 보유중이지 않고 전일 시가대비 종가 상승률이 +10%이상이면 해당 코인을 매수
    #     if has_position[ticker] == False and yesterday_change_rate > yesterday_change_rate_threshold:
    #         order_amount = buy_amount_capital
    #         print(f'{ticker} 목표 매수 금액 :', order_amount)

    #         buy_market_order_result = buy_market_order(coin_name=ticker, market_buy_amt=order_amount)
    #         print(f'{ticker} 시장가 매수 주문! order_id : {buy_market_order_result["uuid"]}')                        
    #         has_position[ticker] = True
    #         time.sleep(0.3)

    #         telegram_message_list = [ticker, '------------- buy order occured ----------']
    #         telegram_bot.sendMessage(chat_id=TELEGRAM_CHAT_ID_FOR_AIS1, text=' '.join(telegram_message_list))

    #         # 잔고확인 API를 통한 보유 개수 확인 & 구매 금액 확인
    #         get_balance_result = get_balance()
    #         for each_asset in get_balance_result:
    #             if each_asset['currency'] == ticker:
    #                 sell_order_amount[ticker] = float(each_asset['balance'])
    #                 each_average_buy_price[ticker] = float(each_asset['avg_buy_price'])

    #                 each_target_sell_price = each_average_buy_price[ticker] * target_sell_price_ratio
    #                 target_sell_price[ticker] = upbit_price_tick_revision(each_target_sell_price) # 호가단위 보정

    #                 # 구매 가격의 +0.02%에 지정가 매도 주문 실행
    #                 result = sell_limit_order(target_sell_price[ticker], sell_order_amount[ticker], coin_name=ticker)
    #                 print(result)

    #                 telegram_message_list = [ticker, '------------- limit sell order occured ----------', 'target_price :', str(target_sell_price[ticker])]
    #                 telegram_bot.sendMessage(chat_id=TELEGRAM_CHAT_ID_FOR_AIS1, text=' '.join(telegram_message_list))

    #         time.sleep(0.1)