import requests

def get_all_symbol():
    krw_coin_list = []
    url =  "https://api.upbit.com/v1/market/all?isDetails=false"
    headers = {"Accept": "application/json"}
    res = requests.get(url, headers=headers)
    
    coin_list = res.json()
    
    for coin in coin_list:
        ticker = coin['market']
        
        if ticker.startswith('KRW'):
            krw_coin_list.append(ticker.split('-')[1])

    return krw_coin_list