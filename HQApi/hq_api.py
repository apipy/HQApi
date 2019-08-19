import json

import jwt
import requests
from HQApi.exceptions import ApiResponseError, BannedIPError


class BaseHQApi:
    def __init__(self, token: str = None, logintoken: str = None):
        self.token = token
        self.logintoken = logintoken

    def api(self):
        return self

    def get_users_me(self):
        return self.fetch("GET", "users/me")

    def get_user(self, id: str):
        return self.fetch("GET", "users/{}".format(id))

    def search(self, name):
        return self.fetch("GET", 'users?q={}'.format(name))

    def get_payouts_me(self):
        return self.fetch("GET", "users/me/payouts")

    def get_show(self):
        return self.fetch("GET", "shows/now")

    def get_schedule(self):
        return self.fetch("GET", 'shows/schedule')

    def easter_egg(self, type: str = "makeItRain"):
        return self.fetch("POST", "easter-eggs/{}".format(type))

    def make_payout(self, email: str):
        return self.fetch("POST", "users/me/payouts", {"email": email})

    def send_code(self, phone: str, method: str = "sms"):
        return self.fetch("POST", "verifications", {"phone": phone, "method": method})

    def confirm_code(self, verificationid: str, code: int):
        return self.fetch("POST", "verifications/{}".format(verificationid), {"code": code})

    def register(self, verificationid: str, name: str, referral: str = None):
        return self.fetch("POST", "users", {
            "country": "MQ==", "language": "eu",
            "referringUsername": referral,
            "username": name,
            "verificationId": verificationid})

    def delete_avatar(self):
        return self.fetch("DELETE", "users/me/avatarUrl")

    def add_referral(self, referral: str):
        return self.fetch("PATCH", "users/me", {"referringUsername": referral})

    def add_friend(self, id: str):
        return self.fetch("POST", "friends/{}/requests".format(id))

    def friend_status(self, id: str):
        return self.fetch("GET", "friends/{}/status".format(id))

    def remove_friend(self, id: str):
        return self.fetch("DELETE", "friends/{}".format(id))

    def accept_friend(self, id: str):
        return self.fetch("PUT", "friends/{}/status".format(id), {"status": "ACCEPTED"})

    def check_username(self, name: str):
        return self.fetch("POST", "usernames/available", {"username": name})

    def get_tokens(self, login_token: str):
        return self.fetch("POST", "tokens", {'token': login_token})

    def edit_username(self, username: str):
        return self.fetch("PATCH", "users/me", {"username": username})

    def get_logintoken(self):
        return self.fetch("GET", "users/me/token")

    def send_documents(self, id, email, paypal_email, country):
        return self.fetch("POST", "users/{}/payouts/documents".format(id),
                          {"email": email, "country": country, "payout": paypal_email})

    def register_device_token(self, token):
        return self.fetch("POST", "users/me/devices", {"token": token})

    def config(self):
        return self.fetch("GET", "config")

    def get_optins(self):
        return self.fetch("GET", "opt-in")

    def set_optin(self, name: str, value: bool):
        return self.fetch("POST", "opt-in", {"value": value, "opt": name})

    def season_xp(self):
        return self.fetch("GET", "seasonXp/settings")

    def referrals(self):
        return self.fetch("GET", "show-referrals")

    def leaderboard(self, mode: str):
        return self.fetch("GET", "users/leaderboard?mode={}".format(mode))

    def set_avatar(self, file: str):
        return self.fetch("POST", "users/me/avatar", files={"file": ("file", open(file, 'rb').read(), 'image/jpeg')})

    def store(self):
        return self.fetch("GET", "store/products")

    def start_offair(self):
        return self.fetch('POST', "offair-trivia/start-game")

    def offair_trivia(self, id: str):
        return self.fetch('GET', 'offair-trivia/{}'.format(id))

    def send_offair_answer(self, id: str, answer_id: str):
        return self.fetch('POST', 'offair-trivia/{}/answers'.format(id), {"offairAnswerId": answer_id})

    def custom(self, method, func, data):
        return self.fetch(method, func, data)


class HQApi(BaseHQApi):
    def __init__(self, token: str = None, logintoken: str = None,
                 version: str = "1.39.0", host: str = "https://api-quiz.hype.space/",
                 proxy: str = None, verify: bool = True):
        super().__init__(token, logintoken)
        self.version = "2.4.3"
        self.session = requests.Session()
        self.token = token
        self.logintoken = logintoken
        self.hq_version = version
        self.host = host
        self.v = verify
        self.p = dict(http=proxy, https=proxy)
        self.headers = {
            "x-hq-client": "Android/" + self.hq_version}
        if logintoken:
            self.token = self.get_tokens(logintoken)["accessToken"]
        if self.token:
            self.headers["Authorization"] = "Bearer " + self.token

    def fetch(self, method="GET", func="", data=None, files=None):
        if data is None:
            data = {}
        try:
            if method == "GET":
                content = self.session.get(self.host + "{}".format(func), data=data,
                                           headers=self.headers, proxies=self.p, verify=self.v).json()
            elif method == "POST":
                content = self.session.post(self.host + "{}".format(func), data=data,
                                            headers=self.headers, proxies=self.p, files=files, verify=self.v).json()
            elif method == "PATCH":
                content = self.session.patch(self.host + "{}".format(func), data=data,
                                             headers=self.headers, proxies=self.p, verify=self.v).json()
            elif method == "DELETE":
                content = self.session.delete(self.host + "{}".format(func), data=data,
                                              headers=self.headers, proxies=self.p, verify=self.v).json()
            elif method == "PUT":
                content = self.session.put(self.host + "{}".format(func), data=data,
                                           headers=self.headers, proxies=self.p, verify=self.v).json()
            else:
                content = self.session.get(self.host + "{}".format(func), data=data,
                                           headers=self.headers, proxies=self.p, verify=self.v).json()
            error = content.get("error")
            if error:
                raise ApiResponseError(json.dumps(content))
            return content
        except json.decoder.JSONDecodeError:
            raise BannedIPError("Your IP is banned")

    def decode_jwt(self, jwt_text: str):
        return jwt.decode(jwt_text.encode(), verify=False)

    def set_token(self, token):
        self.token = token
        if self.token:
            self.headers["Authorization"] = "Bearer " + self.token

    def __str__(self):
        return "<HQApi {} token={}>".format(self.version, self.token)
