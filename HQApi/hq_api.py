import base64
import json
import requests
from HQApi.exceptions import ApiResponseError


class BaseHQApi:
    def __init__(self, authtoken, region="1"):
        self.authtoken = authtoken
        self.region = region

    def fetch(self, method="GET", func="", data=[]):
        return method, func, data

    def get_users_me(self):
        return self.fetch("GET", "users/me")

    def get_payouts_me(self):
        return self.fetch("GET", "users/me/payouts")

    def get_show(self):
        return self.fetch("GET", "shows/now")

    def easter_egg(self):
        return self.fetch("POST", "easter-eggs/makeItRain")

    def make_payout(self, email):
        return self.fetch("POST", "users/me/payouts", {"email": email})


class HQApi(BaseHQApi):
    def __init__(self, authtoken, region="1"):
        super().__init__(authtoken, region=region)
        self.authToken = authtoken
        self.region = region
        self.session = requests.Session()
        self.session.headers.update({
            "x-hq-stk": base64.b64encode(str(self.region).encode()).decode(),
            "x-hq-client": "Android/1.19.1",
            "Authorization": "Bearer " + self.authToken})

    def fetch(self, method="GET", func="", data={}):
        if method == "GET":
            content = self.session.get("https://api-quiz.hype.space/{}".format(func), data=data).json()
        elif method == "POST":
            content = self.session.post("https://api-quiz.hype.space/{}".format(func), data=data).json()
        elif method == "PATCH":
            content = self.session.patch("https://api-quiz.hype.space/{}".format(func), data=data).json()
        else:
            content = self.session.get("https://api-quiz.hype.space/{}".format(func), data=data).json()
        error = content.get("error")
        if error:
            raise ApiResponseError(json.dumps(content))
        return content


class AsyncHQApi(BaseHQApi):
    def __init__(self, authtoken, connector, region="1"):
        super().__init__(authtoken, region=region)
        self.authtoken = authtoken
        self.region = region
        self.connector = connector

    async def fetch(self, method="GET", func="", data={}):
        if method == "GET":
            async with self.connector.session.get("https://api-quiz.hype.space/{}".format(func),
                                                  data=data) as response:
                content = await response.json()
                error = content.get("error")
                if error:
                    raise ApiResponseError(json.dumps(content))
                return content
        elif method == "POST":
            async with self.connector.session.post("https://api-quiz.hype.space/{}".format(func),
                                                   data=data) as response:
                content = await response.json()
                error = content.get("error")
                if error:
                    raise ApiResponseError(json.dumps(content))
                return content
        elif method == "PATCH":
            async with self.connector.session.patch("https://api-quiz.hype.space/{}".format(func),
                                                    data=data) as response:
                content = await response.json()
                error = content.get("error")
                if error:
                    raise ApiResponseError(json.dumps(content))
                return content
        else:
            async with self.connector.session.get("https://api-quiz.hype.space/{}".format(func),
                                                  data=data) as response:
                content = await response.json()
                error = content.get("error")
                if error:
                    raise ApiResponseError(json.dumps(content))
                return content
