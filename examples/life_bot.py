import json
import re

from lomond.persist import persist

from HQApi import HQApi, HQWebSocket

bearers = ["Bearer 1", "Bearer 2"]
for bearer in bearers:
    api = HQApi(bearer)
    ws = HQWebSocket(api)
    websocket = ws.get()
    for msg in persist(websocket):
        if msg.name == "text":
            data = json.loads(re.sub(r"[\x00-\x1f\x7f-\x9f]", "", msg.text))
            if data["type"] != "interaction":
                ws.close()
