import requests
import time 

def price(coin):
    while True:
        start = time.time()
        req = requests.get(f'https://api.kucoin.com/api/v1/prices?currencies={coin}')
        print(req.text)


