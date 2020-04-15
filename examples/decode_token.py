from HQApi import HQApi

token = "Token"
api = HQApi(token)

print(api.decode_jwt(api.token))
