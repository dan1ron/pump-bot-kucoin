from pynput.keyboard import Listener, KeyCode
from kucoin.client import Client
import threading
from config import kc_client, SIZE, PAIRING_TYPE




def buy_coin(coin_name):
    order = kc_client.create_market_order(coin_name + f'-{PAIRING_TYPE}', Client.SIDE_BUY, size=SIZE)
    entry_price = kc_client.get_fiat_prices(symbol=coin_name)[coin_name]  # or take from bid?
    keyboard_sell(coin_name=coin_name, order_id=order['orderId'], pairing_type=PAIRING_TYPE)
    print(f"market buy order {order} happened!")
    profit_tracker(coin_name, entry_price)

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

def profit_tracker(coin_name, entry_price):
    while True:
        profit = round(((float(kc_client.get_fiat_prices(symbol=coin_name)[coin_name]) - entry_price) / entry_price) * 100)
        print(f'~{profit} %')
