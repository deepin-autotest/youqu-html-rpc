import os
from socketserver import ThreadingMixIn
from xmlrpc.server import SimpleXMLRPCServer
from youqu_html import YouQuHtml
from youqu_html.conf import setting
from youqu_html_rpc.config import config

class ThreadXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

def check_connected():
    return True

def server_user_password():
    return config.USERNAME, config.PASSWORD

def gen_html(data_path, gen_path, http_path):
    setting.html_title = "YouQu Report"
    setting.report_name = "YouQu Report"
    YouQuHtml.gen(data_path, gen_path)
    os.system(f"ln -s {gen_path} /var/www/html/{http_path}")


def makedirs(dirpath):
    os.makedirs(os.path.expanduser(dirpath), exist_ok=True)

def server():
    from youqu_html_rpc.config import config
    server = ThreadXMLRPCServer(("0.0.0.0", config.PORT), allow_none=True)
    server.register_function(gen_html, "gen_html")
    server.register_function(check_connected, "check_connected")
    server.register_function(makedirs, "makedirs")
    server.register_function(server_user_password, "server_user_password")
    print("Listen to client requests ...")
    server.serve_forever()


if __name__ == "__main__":
    server()