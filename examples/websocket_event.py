from HQApi import HQApi, HQWebSocket

token = "Token"
api = HQApi(token)
ws = HQWebSocket(api, demo=True)
ws.listen()


@ws.event("interaction")
def interaction(data):
    print("Interaction: " + str(data))
