from HQApi import HQApi, HQWebSocket

api = HQApi()
ws = HQWebSocket(api, demo=True)
ws.listen()


@ws.event("interaction")
def interaction(_):
    exit()
