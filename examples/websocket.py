from lomond.persist import persist
from HQApi import HQApi, HQWebSocket

token = "Token"
api = HQApi(token)
ws = HQWebSocket(api, demo=True)
websocket = ws.get()

for msg in persist(websocket):
    if msg.name == "text":
        print(msg.text)
