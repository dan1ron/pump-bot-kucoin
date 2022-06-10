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
    

def keyboard_sell(coin_name, order_id, pairing_type, sell_target):
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

    keyboard_sell(coin_name, order_id, 'USDT')

    if sell_target:
        entry_price = kc_client.get_fiat_prices(symbol=coin_name)[coin_name]
        ord_bk_fa = kc_client.get_order_book(coin_name + '-USDT')['bids'][0]  # order book first order
        num_decimals_price = ord_bk_fa[0][::-1].find('.')
        num_decimals_amount = ord_bk_fa[1][::-1].find('.')
        deal_amount = f'%.{num_decimals_amount}f' % (float(kc_client.get_order(order_id['orderId'])['dealSize']) * 0.998)
        target_price = f'%.{num_decimals_price}f' % (float(entry_price) * ((TARGET_SELL_PERCENTAGE / 100) + 1))
            # the '%.2f' % is to limit decimals!
        sell_on_target(coin_name=coin_name, target_price=target_price, coin_amount=deal_amount, time_to_check=0.8, pairing_type='USDT')


def sell_on_target(coin_name, target_price, coin_amount, time_to_check, pairing_type):

    my_timer = threading.Timer(time_to_check, sell_on_target, args=[coin_name, target_price, coin_amount, time_to_check])
    my_timer.start()

    cur_price = kc_client.get_order_book(coin_name + f'-{pairing_type}')['asks'][0][0]
    if target_price < cur_price:
        order = kc_client.create_limit_order(coin_name + f'-{pairing_type}', Client.SIDE_SELL, price=target_price, size=coin_amount)
        print(f"{order} happened! selling on target price {str(target_price)}")
        my_timer.cancel()