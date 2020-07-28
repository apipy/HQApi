import json
import threading
from lomond import WebSocket
from lomond.persist import persist
from HQApi import HQApi
from HQApi.exceptions import NotLive, WebSocketNotAvailable, ApiResponseError, BannedIPError


class HQWebSocket:
    def __init__(self, api: HQApi, demo: bool = False, custom_ws: str = None, show_debug: bool = True):
        # TODO: Rewrite this again
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

    def send_life(self, question_id: int = 0, round_id: int = 0):
        if question_id != 0:
            self.send_json({"questionId": question_id,
                            "type": "useExtraLife"})
        elif round_id != 0:
            self.send_json({"roundId": question_id,
                            "type": "useExtraLife"})

    def send_answer(self, answer_id: int, question_id: int):
        self.send_json({"answerId": answer_id,
                        "questionId": question_id,
                        "type": "answer"})

    def send_comment(self, avatar_url: str, message: str, user_id: int, username: str):
        self.send_json({"metadata": {"avatarUrl": avatar_url,
                                     "interaction": "chat", "message": message, "userId": user_id,
                                     "username": username}, "itemId": "chat",
                        "type": "interaction"})

    def send_wheel(self, show_id: int, letter: str, item: str):
        self.send_json({
            "type": "spin", "superWheelItem": item,
            "letter": letter, "showId": show_id})

    def send_letter(self, show_id: int, letter: str, round_id: int):
        self.send_json({"type": "guess", "showId": show_id,
                        "letter": letter,
                        "roundId": round_id})

    def get_erasers(self, friends_ids: list):
        self.send_json({"authToken": self.token,
                        "friends_ids": friends_ids,
                        "type": "erase1Earned"})

    def send_eraser(self, question_id: int):
        self.send_json({"type": "erase1",
                        "questionId": question_id})

    def subscribe(self, game_type: str):
        self.send_json({"type": "subscribe",
                        "gameType": game_type})

    def chat_visibility(self, enable: bool):
        self.send_json({"chatVisible": enable,
                        "type": "chatVisibilityToggled"})

    def checkpoint(self, win_now: bool, checkpoint_id: str):
        self.send_json({
            "winNow": win_now,
            "checkpointId": checkpoint_id,
            "type": "checkpointResponse"})

    def send_wave(self, user: int, wave_text: str):
        self.send_json({
            "type": "sendWave",
            "toUser": user,
            "waveText": wave_text})

    def send_survey_answer(self, answer_id: str, question_id: str):
        self.send_json({
            "type": "surveyAnswer",
            "surveyAnswerId": answer_id,
            "surveyQuestionId": question_id})

    def toggle_sharing(self, enabled: bool):
        self.send_json({
            "type": "toggleSharing",
            "sharingEnabled": enabled})

    def viewer_snapshot(self, visible: bool, drawer_open: bool, volume_level: int, gaid: str, request: int):
        self.send_json({"userBlob": {"chatVisible": visible,
                                     "drawerOpen": drawer_open,
                                     "volumeLevel": volume_level,
                                     "gaid": gaid},
                        "type": "viewerSnapshot",
                        "snapRequestId": request})

    def answer_multi(self, answer_ids: list, question_id: int):
        self.send_json({"type": "answerMulti",
                        "answerIds": answer_ids,
                        "questionId": question_id})

    def joke_vote(self, session_id: str, vote: str):
        self.send_json({"type": "jokeVote",
                        "jokeSessionId": session_id,
                        "vote": vote})

    def outgoing_chat(self, msg: str):
        self.send_json({"type": "chat",
                        "message": msg})

    def product_purchase_cancelled(self, idempotency_key: str, scene_id: str, sku: str, time: str):
        self.send_json({"type": "productPurchaseCancelled",
                        "idempotencyKey": idempotency_key,
                        "sceneId": scene_id,
                        "sku": sku,
                        "time": time})

    def product_purchase_started(self, idempotency_key: str, scene_id: str, sku: str, time: str):
        self.send_json({"type": "productPurchaseStarted",
                        "idempotencyKey": idempotency_key,
                        "sceneId": scene_id,
                        "sku": sku,
                        "time": time})

    def swiped(self, action: str, survey_key: str):
        self.send_json({"type": "swiped",
                        "action": action,
                        "surveyKey": survey_key})

    def purple_jupiter(self, attestation_timing_ms: str, token: str):
        self.send_json({"type": "purpleJupiter",
                        "body": {"attestationTimingMs": attestation_timing_ms, "success": True, "token": token}})

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
