from lomond.persist import persist
from HQApi import HQApi, HQWebSocket

api = HQApi()
ws = HQWebSocket(api, demo=True)
websocket = ws.get()

for msg in persist(websocket):
    if msg.name == "text":
        exit()