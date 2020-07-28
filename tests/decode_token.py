from HQApi import HQApi

api = HQApi(login_token='uQOOiASmugQh2F09qj39LO1DaWUf7bkSeUn4ofHQJl7dcgzNPzReI1aAHmm0Kgwc')

print(api.decode_jwt(api.token))
