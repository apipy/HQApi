from HQApi import HQApi

bearer = "Bearer"
api = HQApi(bearer, 1)

print(str(api.get_show()))
