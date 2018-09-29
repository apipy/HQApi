from HQApi import HQApi

bearer = "Bearer"
api = HQApi(bearer)

print(str(api.get_show()))
