import base64
import aiohttp


class Connector:
    def __init__(self, authtoken, region):
        self.session = None
        self.authToken = authtoken
        self.region = region

    async def __aenter__(self):
        headers = {"x-hq-stk": base64.b64encode(str(self.region).encode()).decode(),
                   "x-hq-client": "Android/1.20.1",
                   "Authorization": "Bearer " + self.authToken}
        self.session = aiohttp.ClientSession(headers=headers)

    async def __aexit__(self, type, value, traceback):
        await self.session.close()
