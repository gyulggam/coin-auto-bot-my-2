import uuid
import requests
import jwt
from urllib.parse import urlencode
import hashlib
from config import config

access_key = config.get("access_key")
secret_key = config.get("secret_key")
server_url = config.get("server_url")

# 시장가 매수 주문
def buy_market_order(market_buy_amt, coin_name='XRP', payment_currency='KRW'):
    query = {
        'market': f'{payment_currency}-{coin_name}',
        'side': 'bid',
        'price': str(market_buy_amt),
        'ord_type': 'price'
    }
    query_string = urlencode(query).encode()

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.post(server_url + "/v1/orders", params=query, headers=headers)

    return res.json()

# 시장가 매도 주문
def sell_market_order(market_sell_amt, coin_name='XRP', payment_currency='KRW'):
    query = {
        'market': f'{payment_currency}-{coin_name}',
        'side': 'ask',
        'volume': str(market_sell_amt),
        'ord_type': 'market'
    }
    query_string = urlencode(query).encode()

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.post(server_url + "/v1/orders", params=query, headers=headers)

    return res.json()

# 지정가 매도 주문
def sell_limit_order(price, amt, coin_name='XRP', payment_currency='KRW'):
    query = {
        'market': f'{payment_currency}-{coin_name}',
        'side': 'ask',
        'volume': str(amt),
        'price': str(price),
        'ord_type': 'limit',
    }
    query_string = urlencode(query).encode()

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, config.get("secret_key"))
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.post(server_url + "/v1/orders", params=query, headers=headers)

    return res.json()
