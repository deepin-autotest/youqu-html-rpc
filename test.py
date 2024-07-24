from youqu_html_rpc import YouQuHtmlRpc

from youqu_html_rpc.config import config

config.SERVER_IP = "10.8.12.47"

a =YouQuHtmlRpc.check_connected()
print(a)