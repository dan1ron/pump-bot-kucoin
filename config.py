import kucoin.client 
from pyrogram import Client

# Telegram Information!
api_id = 000
api_hash = ''
app = Client('bot', api_id, api_hash)

# KuCoin Information!
api_key = 'Your Kucoin API key'
api_secret = 'Your Kucoin API secret'
api_passphrase = 'Your Kucoin API passphrase'
kc_client = kucoin.client.Client(api_key, api_secret, api_passphrase)

Pump_Channel = -1001219293084 #id tg channel
SIZE = 1000 #purchase size
PAIRING_TYPE = 'USDT'