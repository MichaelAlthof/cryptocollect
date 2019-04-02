import json
from pymongo import MongoClient
import websocket
import datetime

mongo_client = MongoClient('mongodb://dataadmin:daPknihTi7@localhost/cryptocurrency')
db = mongo_client['cryptocurrency']
bitfinex_coll = db['bitfinex']

def on_message(mes):
    print(datetime.datetime.now())
    print("Bitfinex - 10 - XMR-USD:" + " " + mes)
    message = json.loads(mes)
    if message[1] in ('tu'):
        result = {'_id': message[2][0], 't': message[2][1], 'v': message[2][2], 'p': message[2][3],
                  'c': 'XMR-USD'}
        res = bitfinex_coll.insert_one(result)


ws = websocket.WebSocketApp('wss://api-pub.bitfinex.com/ws/2')

ws.on_open = lambda self: self.send('{ "event": "subscribe", "channel": "trades", "symbol": "tXMRUSD"}')

ws.on_message = lambda self, evt: on_message(evt)

ws.run_forever(ping_interval=10, ping_timeout=5)