class ApiResponseError(Exception):
    pass


class BannedIPError(Exception):
    pass


class NotLive(Exception):
    pass


class WebSocketNotAvailable(Exception):
    pass