import json
import threading

from lomond import WebSocket
from lomond.persist import persist

from HQApi import HQApi
from HQApi.exceptions import NotLive, WebSocketNotAvailable, ApiResponseError, BannedIPError


class HQWebSocket:
    def __init__(self, api: HQApi, demo: bool = False, custom_ws: str = None, show_debug: bool = True):
        self.api = api
        self.handlers = {}
        self.token = self.api.token
        self.headers = self.api.headers
        self.use_demo = False
        self.custom_ws = custom_ws
        try:
            self.headers["Authorization"]
        except:
            if demo:
                self.use_demo = True
            else:
                if not self.custom_ws:
                    raise WebSocketNotAvailable("You can't use websocket without token")
        try:
            self.show = HQApi.get_show(api)
            self.socket = self.show["broadcast"]["socketUrl"].replace("https", "wss")
            self.broadcast = self.show['broadcast']['broadcastId']
        except BannedIPError or ApiResponseError:
            if demo:
                self.use_demo = True
            else:
                if not self.custom_ws:
                    raise WebSocketNotAvailable("You can't use websocket with banned IP or invalid auth")
        except:
            if demo:
                self.use_demo = True
            else:
                if not self.custom_ws:
                    raise NotLive("Show isn't live and demo mode is disabled")
        if self.use_demo:
            if show_debug:
                print("[HQApi] Using demo websocket! Don't create issues with this websocket")
            self.socket = "wss://hqecho.herokuapp.com"  # Websocket with questions 24/7
            self.broadcast = 1
            self.ws = WebSocket(self.socket)
        elif self.custom_ws:
            if show_debug:
                print("[HQApi] Using custom websocket! Don't create issues with this websocket")
            self.socket = self.custom_ws
            self.broadcast = 1
            self.ws = WebSocket(self.socket)
        else:
            self.ws = WebSocket(self.socket)
            for header, value in self.headers.items():
                self.ws.add_header(str.encode(header), str.encode(value))

    def call(self, data):
        if data["type"] in self.handlers:
            for h in self.handlers[data["type"]]:
                h(data["data"])

    def event(self, type):
        def registerhandler(handler):
            if type in self.handlers:
                self.handlers[type].append(handler)
            else:
                self.handlers[type] = [handler]
            return handler

        return registerhandler

    def listen(self):
        thread = HQWebsocketListener(self)
        thread.start()

    def send_json(self, js=None):
        if js is None:
            js = {}
        self.ws.send_json(js)

    def send_life(self, questionId: int = 0, roundId: int = 0):
        if questionId != 0:
            self.send_json({"questionId": questionId, "authToken": self.token,
                            "broadcastId": self.broadcast,
                            "type": "useExtraLife"})
        elif roundId != 0:
            self.send_json({"roundId": questionId, "authToken": self.token,
                            "broadcastId": self.broadcast,
                            "type": "useExtraLife"})

    def send_answer(self, answerId: int, questionId: int):
        self.send_json({"answerId": answerId,
                        "questionId": questionId, "authToken": self.token,
                        "broadcastId": self.broadcast, "type": "answer"})

    def send_comment(self, avatarUrl: str, message: str, userId: int, username: str):
        self.send_json({"metadata": {"avatarUrl": avatarUrl,
                                     "interaction": "chat", "message": message, "userId": userId,
                                     "username": username}, "itemId": "chat",
                        "authToken": self.token,
                        "broadcastId": self.broadcast, "type": "interaction"})

    def send_wheel(self, showId: int, letter: str, item: str):
        self.send_json({"broadcastId": self.broadcast,
                        "authToken": self.token,
                        "type": "spin", "superWheelItem": item,
                        "letter": letter, "showId": showId})

    def send_letter(self, showId: int, letter: str, roundId: int):
        self.send_json({"type": "guess", "authToken": self.token, "showId": showId,
                        "broadcastId": self.broadcast, "letter": letter,
                        "roundId": roundId})

    def get_erasers(self, friendsIds: list):
        self.send_json({"authToken": self.token,
                        "friendsIds": friendsIds,
                        "broadcastId": self.broadcast,
                        "type": "erase1Earned"})

    def send_eraser(self, questionId: int):
        self.send_json({"type": "erase1",
                        "questionId": questionId,
                        "authToken": self.token,
                        "broadcastId": self.broadcast})

    def subscribe(self, type: str):
        self.send_json({"type": "subscribe",
                        "broadcastId": self.broadcast,
                        "authToken": self.token,
                        "gameType": type})

    def chat_visibility(self, enable: bool):
        self.send_json({"chatVisible": enable, "authToken": self.token,
                        "broadcastId": self.broadcast,
                        "type": "chatVisibilityToggled"})

    def checkpoint(self, winNow: bool, checkpointId: str):
        self.send_json({"broadcastId": self.broadcast,
                        "authToken": self.token,
                        "winNow": winNow,
                        "checkpointId": checkpointId,
                        "type": "checkpointResponse"})

    def send_wave(self, user: int, waveText: str):
        self.send_json({"broadcastId": self.broadcast,
                        "authToken": self.token,
                        "type": "sendWave",
                        "toUser": user,
                        "waveText": waveText})

    def send_survey_answer(self, answer: str, question: str):
        self.send_json({"broadcastId": self.broadcast,
                        "authToken": self.token,
                        "type": "surveyAnswer",
                        "surveyAnswerId": answer,
                        "surveyQuestionId": question})

    def toggle_sharing(self, enabled: bool):
        self.send_json({"broadcastId": self.broadcast,
                        "authToken": self.token,
                        "type": "toggleSharing",
                        "sharingEnabled": enabled})

    def viewer_snapshot(self, visible: bool, drawerOpen: bool, volumeLevel: int, gaid: str, request: int):
        self.send_json({"userBlob": {"chatVisible": visible,
                                     "drawerOpen": drawerOpen,
                                     "volumeLevel": volumeLevel,
                                     "gaid": gaid},
                        "broadcastId": self.broadcast,
                        "authToken": self.token,
                        "type": "viewerSnapshot",
                        "snapRequestId": request})

    def get(self):
        return self.ws

    def close(self):
        self.ws.close()

    def __str__(self):
        return "<HQWebsocket {} token={}>".format(self.api.version, self.token)


class HQWebsocketListener(threading.Thread):
    def __init__(self, new):
        threading.Thread.__init__(self)
        self.new = new

    def run(self):
        for msg in persist(self.new.ws):
            if msg.name == "text":
                data = json.loads(msg.text)
                self.new.call({"type": data["type"], "data": data})
