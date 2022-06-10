from pynput.keyboard import Listener, KeyCode
import threading
from kucoin.client import Client

api_key = 'Your Kucoin API key'
api_secret = 'Your Kucoin API secret'
api_passphrase = 'Your Kucoin API passphrase'
kc_client = Client(api_key, api_secret, api_passphrase)

USDT = 1000
TARGET_SELL_PERCENTAGE = 100



def buy_coin(coin_name):
    order = kc_client.create_market_order(coin_name + '-USDT', Client.SIDE_BUY, size=USDT)
    keyboard_sell(coin_name=coin_name, order_id=order['orderId'], pairing_type='USDT')
    print(f"market buy order {order} happened!")
    keyboard_sell(coin_name, order, 'USDT', )
    

def keyboard_sell(coin_name, order_id, pairing_type):
    ord_bk_fa = kc_client.get_order_book(f"{coin_name}-{pairing_type}")['bids'][0]  # order book first order
    num_decimals_amount = ord_bk_fa[1][::-1].find('.')

    deal_amount = f'%.{num_decimals_amount}f' % (float(kc_client.get_order(order_id)['dealSize']) * 0.998)

    def sell_keypress(*key):
        try:
            if key[0] == KeyCode.from_char('l'):
                print('\nlimit sell!')
                cur_price = kc_client.get_order_book(coin_name + f'-{pairing_type}')['asks'][0][0]
                order = kc_client.create_limit_order(coin_name + f'-{pairing_type}', Client.SIDE_SELL, price=cur_price, size=deal_amount)
                print(f"limit sell order {order} happened!")

            if key[0] == KeyCode.from_char('m'):
                print('\nmarket sell!')
                order = kc_client.create_market_order(coin_name + f'-{pairing_type}', Client.SIDE_SELL, size=deal_amount)
                print(f"market sell order {order} happened!")

        except Exception as err:
            print("ORDER SELL FAILED")
            print(f"{err.__class__} -- {err}")

    def key():  # starts listener module
        with Listener(on_press=sell_keypress) as listener:
            listener.join()

    threading.Thread(target=key).start()
