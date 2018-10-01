import base64
from lomond import WebSocket
from HQApi import HQApi


class HQWebSocket:
    def __init__(self, api: HQApi):
        self.api = api
        self.authtoken = HQApi.bearer(api)
        self.region = HQApi.country(api)
        self.headers = {
            "x-hq-stk": base64.b64encode(str(self.region).encode()).decode(),
            "x-hq-client": "Android/1.20.1",
            "Authorization": "Bearer " + self.authtoken}
        if HQApi.get_show(api)["active"]:
            self.socket = HQApi.get_show(api)["broadcast"]["socketUrl"].replace("https", "wss")
            self.broadcastid = HQApi.get_show(api)['broadcast']['broadcastId']
        else:
            print("Using demo websocket!")
            self.socket = "ws://hqecho.herokuapp.com"  # Websocket with questions 24/7
            self.broadcastid = 1
        self.ws = WebSocket(self.socket)
        for header, value in self.headers.items():
            self.ws.add_header(str.encode(header), str.encode(value))
        for msg in self.ws.connect():
            self.success = 1

    def send_json(self, json={}):
        for msg in self.ws.connect():
            if msg.name == "text":
                self.ws.send_json(json)
                self.ws.close()

    def send_life(self, questionid):
        for msg in self.ws.connect():
            if msg.name == "text":
                self.ws.send_json({"questionId": str(questionid), "authToken": str(self.authtoken),
                              "broadcastId": str(self.broadcastid),
                              "type": "useExtraLife"})
                self.ws.close()

    def send_answer(self, answerid, questionid):
        for msg in self.ws.connect():
            if msg.name == "text":
                self.ws.send_json({"answerId": str(answerid),
                              "questionId": str(questionid), "authToken": str(self.authtoken),
                              "broadcastId": str(str(self.broadcastid)), "type": "answer"})
                self.ws.close()

    def join(self):
        return self.ws
