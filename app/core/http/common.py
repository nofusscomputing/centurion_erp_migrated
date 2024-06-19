from enum import IntEnum



class Http():
    """Common HTTP Related objects"""


    class Status(IntEnum):
        """HTTP server status codes."""

        OK = 200

        CREATED = 201

        BAD_REQUEST = 400

        FORBIDDEN = 403

        SERVER_ERROR = 500
