import json
import requests
from HQApi.exceptions import ApiResponseError, BannedIPError


class BaseHQApi:
    def __init__(self, authtoken):
        self.authtoken = authtoken

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

    def aws_credentials(self):
        return self.fetch("GET", "credentials/s3")

    def delete_avatar(self):
        return self.fetch("DELETE", "users/me/avatarUrl")

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

    def custom(self, method, func, data):
        return self.fetch(method, func, data)


class HQApi(BaseHQApi):
    def __init__(self, authtoken: str = "", version: str = "1.30.0", proxy: str = None):
        super().__init__(authtoken)
        self.authToken = authtoken
        self.version = version
        if authtoken == "":
            self.headers = {
                "x-hq-client": "Android/" + self.version}
        else:
            self.headers = {
                "Authorization": "Bearer " + self.authtoken,
                "x-hq-client": "Android/" + self.version}
        self.p = dict(http=proxy, https=proxy)

    def fetch(self, method="GET", func="", data=None):
        if data is None:
            data = {}
        try:
            if method == "GET":
                content = requests.get("https://api-quiz.hype.space/{}".format(func), data=data,
                                       headers=self.headers, proxies=self.p).json()
            elif method == "POST":
                content = requests.post("https://api-quiz.hype.space/{}".format(func), data=data,
                                        headers=self.headers, proxies=self.p).json()
            elif method == "PATCH":
                content = requests.patch("https://api-quiz.hype.space/{}".format(func), data=data,
                                         headers=self.headers, proxies=self.p).json()
            elif method == "DELETE":
                content = requests.delete("https://api-quiz.hype.space/{}".format(func), data=data,
                                          headers=self.headers, proxies=self.p).json()
            elif method == "PUT":
                content = requests.put("https://api-quiz.hype.space/{}".format(func), data=data,
                                       headers=self.headers, proxies=self.p).json()
            else:
                content = requests.get("https://api-quiz.hype.space/{}".format(func), data=data,
                                       headers=self.headers, proxies=self.p).json()
            error = content.get("error")
            if error:
                raise ApiResponseError(json.dumps(content))
            return content
        except json.decoder.JSONDecodeError:
            raise BannedIPError("Your IP is banned")
