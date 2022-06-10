from pyrogram import Client, filters
import price
from pump_bot import buy_coin


api_id = 000
api_hash = ''
TARGET = -1001219293084

app = Client("bot")

@app.on_message(filters.chat(TARGET))
async def welcome(client, message):
    txt = message.text
    coin = txt.partition('Coin is: ')[2]
    if coin.isupper():
        buy_coin(coin)
        price.price(coin)
        

if __name__ == "__main__":
    app.run()
