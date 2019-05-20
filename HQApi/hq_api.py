import json
import requests
from aws_requests_auth.aws_auth import AWSRequestsAuth
import jwt
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

    def change_avatar(self, url):
        return self.fetch("PUT", "users/me/avatarUrl", {"avatarUrl": url})

    def upload_avatar(self, file):
        aws = self.aws_credentials()
        requests.put("https://hypespace-quiz.s3.amazonaws.com/avatars/{}".format(file),
                     data=open(file, 'rb').read(), auth=AWSRequestsAuth(aws_access_key=aws["accessKeyId"],
                                                                        aws_secret_access_key=aws["secretKey"],
                                                                        aws_token=aws["sessionToken"],
                                                                        aws_host='hypespace-quiz.s3.amazonaws.com',
                                                                        aws_region='us-east-1',
                                                                        aws_service='s3'), headers={"Content-Type": "text/html"})

    def custom(self, method, func, data):
        return self.fetch(method, func, data)


class HQApi(BaseHQApi):
    def __init__(self, token: str = None, logintoken: str = None,
                 version: str = "1.33.0", host: str = "https://api-quiz.hype.space/",
                 proxy: str = None):
        super().__init__(token, logintoken)
        self.token = token
        self.logintoken = logintoken
        self.version = version
        self.host = host
        self.p = dict(http=proxy, https=proxy)
        self.headers = {
            "x-hq-client": "Android/" + self.version}
        if logintoken:
            self.token = self.get_tokens(logintoken)["accessToken"]
        if self.token:
            self.headers = {
                "Authorization": "Bearer " + self.token,
                "x-hq-client": "Android/" + self.version}

    def fetch(self, method="GET", func="", data=None):
        if data is None:
            data = {}
        try:
            if method == "GET":
                content = requests.get(self.host + "{}".format(func), data=data,
                                       headers=self.headers, proxies=self.p).json()
            elif method == "POST":
                content = requests.post(self.host + "{}".format(func), data=data,
                                        headers=self.headers, proxies=self.p).json()
            elif method == "PATCH":
                content = requests.patch(self.host + "{}".format(func), data=data,
                                         headers=self.headers, proxies=self.p).json()
            elif method == "DELETE":
                content = requests.delete(self.host + "{}".format(func), data=data,
                                          headers=self.headers, proxies=self.p).json()
            elif method == "PUT":
                content = requests.put(self.host + "{}".format(func), data=data,
                                       headers=self.headers, proxies=self.p).json()
            else:
                content = requests.get(self.host + "{}".format(func), data=data,
                                       headers=self.headers, proxies=self.p).json()
            error = content.get("error")
            if error:
                raise ApiResponseError(json.dumps(content))
            return content
        except json.decoder.JSONDecodeError:
            raise BannedIPError("Your IP is banned")

    def decode_token(self, token: str = None):
        if token:
            self.token = token
        return jwt.decode(self.token.encode(), verify=False)
