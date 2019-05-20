from HQApi import HQApi

api = HQApi(proxy="https://207.154.197.214:8888")

print(api.get_show())
