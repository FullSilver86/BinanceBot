from binance.spot import Spot
import pandas as pd
import requests


def balance_BTC(client):
    my_balance = client.account()["balances"]
    my_BTC = next((item for item in my_balance if item['asset'] == "BTC"), None)
    print(f"My BTC balance is {my_BTC}")
    return my_BTC['free']

def balance_USDT(client):
    my_balance = client.account()["balances"]
    my_USDT = next((item for item in my_balance if item['asset'] == "USDT"), None)
    print(f"My USDT balance is {my_USDT}")
    return my_USDT['free']

def get_df():
    r = requests.get("https://api.binance.com/api/v3/depth",
                     params=dict(symbol="BTCUSDT", limit=5000))
    results = r.json()

    frames = {side: pd.DataFrame(data=results[side], columns=["price", "quantity"],dtype=float)
               for side in ["bids", "asks"]}
    frames_list = [frames[side].assign(side=side) for side in frames]
    data = pd.concat(frames_list, axis="index",
                      ignore_index=True, sort=True)
    return data

def logic1_sums(data, current_price):
    filt_close = (data.price < (current_price+1000)) & (data.price > current_price-1000)
    data_close = data.loc[filt_close]
    asks = data_close['side'] == 'asks'
    bids = data_close['side'] == 'bids'
    asks_sum = data_close[asks].sum()["quantity"]
    bids_sum = data_close[bids].sum()["quantity"]
    return [asks_sum,bids_sum]

def sell_BTC(my_BTC, current_price,client):
    params = {
        'symbol': 'BTCUSDT',
        'side': 'SELL',
        'type': 'LIMIT',
        'timeInForce': 'GTC',
        'quantity': my_BTC,
        'price': current_price
    }

    response = client.new_order(**params)
    print(response)
    return False


def buy_BTC(my_USDT, current_price,client):
    params = {
        'symbol': 'BTCUSDT',
        'side': 'BUY',
        'type': 'LIMIT',
        'timeInForce': 'GTC',
        'quantity': round(float(my_USDT)/current_price,6),
        'price': current_price
    }

    response = client.new_order(**params)
    print(response)
    return True