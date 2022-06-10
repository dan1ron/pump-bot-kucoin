import threading
from pyrogram import Client, filters
import price, pump_bot


api_id = 000
api_hash = ''
TARGET = -1001219293084

app = Client("bot2")

@app.on_message()
async def welcome(client, message):
    txt = message.text
    coin = txt.partition('Coin is: ')[2]
    if coin.isupper():
        pump_bot.buy_coin(coin)
        
        price.price(coin)
        

if __name__ == "__main__":
    app.run()
