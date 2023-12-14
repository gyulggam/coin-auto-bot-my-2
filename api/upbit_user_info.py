import uuid
import requests
import jwt
from config import config

access_key = config.get("access_key")
secret_key = config.get("secret_key")
server_url = config.get("server_url")

# 전체 잔고 확인
def get_balance():
    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.get(server_url + "/v1/accounts", headers=headers)

    return res.json()