import base64

from lomond import WebSocket

from HQApi import HQApi


class HQWebSocket:
    def __init__(self, api: HQApi):
        self.api = api
        self.authtoken = HQApi.api(api).authtoken
        self.region = HQApi.api(api).region
        self.headers = {
            "x-hq-stk": base64.b64encode(str(self.region).encode()).decode(),
            "x-hq-client": "Android/1.26.2",
            "Authorization": "Bearer " + self.authtoken}
        if HQApi.get_show(api)["active"]:
            self.socket = HQApi.get_show(api)["broadcast"]["socketUrl"].replace("https", "wss")
            self.broadcast = HQApi.get_show(api)['broadcast']['broadcastId']
        else:
            print("Using demo websocket!")
            self.socket = "ws://hqecho.herokuapp.com"  # Websocket with questions 24/7
            self.broadcast = 1
        self.ws = WebSocket(self.socket)
        for header, value in self.headers.items():
            self.ws.add_header(str.encode(header), str.encode(value))
        for _ in self.ws.connect():
            self.success = 1

    def send_json(self, json=None):
        if json is None:
            json = {}
        self.ws.send_json(json)

    def send_life(self, questionid):
        self.send_json({"questionId": str(questionid), "authToken": self.authtoken,
                        "broadcastId": str(self.broadcast),
                        "type": "useExtraLife"})

    def send_answer(self, answerid, questionid):
        self.send_json({"answerId": str(answerid),
                        "questionId": str(questionid), "authToken": self.authtoken,
                        "broadcastId": str(str(self.broadcast)), "type": "answer"})

    def send_comment(self, avatarUrl, message, userId, username):
        self.send_json({"metadata": {"avatarUrl": avatarUrl,
                                     "interaction": "chat", "message": message, "userId": str(userId),
                                     "username": username}, "itemId": "chat",
                        "authToken": self.authtoken,
                        "broadcastId": str(self.broadcast), "type": "interaction"})

    def send_wheel(self, showId, letter):
        self.send_json({"type": "spin", "authToken": self.authtoken,
                        "showId": str(showId), "broadcastId": self.broadcast,
                        "letter": letter})

    def send_letter(self, showId, letter, roundId):
        self.send_json({"type": "guess", "authToken": self.authtoken, "showId": str(showId),
                        "broadcastId": self.broadcast, "letter": letter,
                        "roundId": str(roundId)})

    def get(self):
        return self.ws

    def close(self):
        self.ws.close()
