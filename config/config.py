import json

def load_config():
    with open('D:\개발\coin-auto-bot-my\config\common.json', 'r') as file:
        config = json.load(file)
    return config

# 모듈에서 직접 import 하기 위한 코드
config = load_config()