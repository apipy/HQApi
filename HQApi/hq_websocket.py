from lomond import WebSocket

from HQApi import HQApi
from HQApi.exceptions import NotLive, WebSocketNotAvailable


class HQWebSocket:
    def __init__(self, api: HQApi, demo: bool = False):
        self.api = api
        self.authtoken = self.api.authtoken
        self.version = self.api.version
        if self.authtoken != "":
            self.headers = {
                "x-hq-client": "Android/" + self.api.version,
                "Authorization": "Bearer " + self.authtoken}
            if HQApi.get_show(api)["active"]:
                self.socket = HQApi.get_show(api)["broadcast"]["socketUrl"].replace("https", "wss")
                self.broadcast = HQApi.get_show(api)['broadcast']['broadcastId']
            elif demo:
                print("Using demo websocket!")
                self.socket = "ws://hqecho.herokuapp.com"  # Websocket with questions 24/7
                self.broadcast = 1
            else:
                raise NotLive("Show isn't live and demo mode is disabled")
            self.ws = WebSocket(self.socket)
            for header, value in self.headers.items():
                self.ws.add_header(str.encode(header), str.encode(value))
            for _ in self.ws.connect():
                self.success = 1
        else:
            raise WebSocketNotAvailable("You can't use websocket without bearer")

    def send_json(self, json=None):
        if json is None:
            json = {}
        self.ws.send_json(json)

    def send_life(self, questionId):
        self.send_json({"questionId": questionId, "authToken": self.authtoken,
                        "broadcastId": self.broadcast,
                        "type": "useExtraLife"})

    def send_answer(self, answerId, questionId):
        self.send_json({"answerId": answerId,
                        "questionId": questionId, "authToken": self.authtoken,
                        "broadcastId": self.broadcast, "type": "answer"})

    def send_comment(self, avatarUrl, message, userId, username):
        self.send_json({"metadata": {"avatarUrl": avatarUrl,
                                     "interaction": "chat", "message": message, "userId": userId,
                                     "username": username}, "itemId": "chat",
                        "authToken": self.authtoken,
                        "broadcastId": self.broadcast, "type": "interaction"})

    def send_wheel(self, showId, letter):
        self.send_json({"type": "spin", "authToken": self.authtoken,
                        "showId": showId, "broadcastId": self.broadcast,
                        "letter": letter})

    def send_letter(self, showId, letter, roundId):
        self.send_json({"type": "guess", "authToken": self.authtoken, "showId": showId,
                        "broadcastId": self.broadcast, "letter": letter,
                        "roundId": roundId})

    def get_erasers(self, friendsIds):
        self.send_json({"authToken": self.authtoken,
                        "friendsIds": friendsIds,
                        "broadcastId": self.broadcast,
                        "type": "erase1Earned"})

    def send_eraser(self, questionId):
        self.send_json({"type": "erase1",
                        "questionId": questionId,
                        "authToken": self.authtoken,
                        "broadcastId": self.broadcast})

    def get(self):
        return self.ws

    def close(self):
        self.ws.close()
