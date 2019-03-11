from HQApi import HQApi

api = HQApi(proxy="https://163.172.220.221:8888")

print(api.get_show())
