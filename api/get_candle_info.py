import requests
from urllib.parse import urlencode

def get_minute_candle(coin_name='XRP', payment_currency='KRW', count=200, date='', minute=5):
    query = {
        'market': f'{payment_currency}-{coin_name}',
        'count': str(count),
        'to': date,
    }
    query_string = urlencode(query)

    url = f"https://api.upbit.com/v1/candles/minutes/{minute}?{query_string}"
    headers = {"Accept": "application/json"}
    res = requests.get(url, headers=headers)
    
    if res.status_code == 200:
        return res.json()
    else:
        res.raise_for_status()