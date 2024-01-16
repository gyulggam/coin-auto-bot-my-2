import json
import os

current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)
path = os.path.join(current_dir, 'common.json')

def load_config():
    with open(path, 'r') as file:
        config = json.load(file)
    return config

# 모듈에서 직접 import 하기 위한 코드
config = load_config()