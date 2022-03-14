from Functions import functions
from binance.spot import Spot
import os
from time import sleep


client = Spot(key=os.environ['KEY'], secret=os.environ['SECRET'], base_url='https://testnet.binance.vision')
# order_flag True = BTC already bought, False = waiting for circumstances to buy BTC
order_flag = True
while True:
    if client.get_open_orders() == []:
        print(client.time())
        my_BTC = functions.balance_BTC(client)
        my_USDT = functions.balance_USDT(client)
        data = functions.get_df()
        current_price = data.loc[5000,'price']
        # orders[0] = asks, orders[1] = bids
        orders = functions.logic1_sums(data, current_price)
        print(orders)
        # True = BTC already bought, False = BTC sold
        if orders[0] > 2 * orders[1] and order_flag:
            order_flag = functions.sell_BTC(my_BTC, current_price,client)
        elif orders[1] > 2 * orders[0] and order_flag is False:
            order_flag = functions.buy_BTC(my_USDT, current_price,client)

        print(client.get_open_orders())
    sleep(15)