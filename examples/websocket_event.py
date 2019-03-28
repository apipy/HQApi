from HQApi import HQApi, HQWebSocket

bearer = "Bearer"
api = HQApi(bearer)
ws = HQWebSocket(api, demo=True, log_new_methods=True)
ws.listen()


@ws.event("interaction")
def interaction(data):
    print("Interaction: " + str(data))
