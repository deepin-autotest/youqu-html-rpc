import os
from xmlrpc.client import ServerProxy

from youqu_html_rpc.config import config


class YouQuHtmlRpc:

    @classmethod
    def server_url(cls):
        return f"http://{config.SERVER_IP}:{config.PORT}"

    @classmethod
    def server(cls):
        return ServerProxy(cls.server_url(), allow_none=True)

    @classmethod
    def check_connected(cls):
        try:
            return cls.server().check_connected()
        except OSError:
            return False

    @classmethod
    def makedirs(cls, dirpath):
        cls.server().makedirs(dirpath)

    @classmethod
    def gen(cls, data_path, gen_path, http_path):
        cls.server().gen_html(data_path, gen_path, http_path)
