from config import config
import uuid
import requests
import jwt

access_key = config.get("access_key") # upbit access_key
secret_key = config.get("secret_key") # upbit secret_key
server_url = config.get("server_url") # upbit api server_url

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