from pyrogram import filters
from config import app, Pump_Channel
import pump_func

@app.on_message(filters.chat(Pump_Channel))
async def welcome(client, message):
    txt = message.text
    coin = txt.partition('Coin is: ')[2]
    if coin.isupper():
        pump_func.buy_coin(coin)        

if __name__ == "__main__":
    app.run()
