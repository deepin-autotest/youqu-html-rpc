import os
import random
import time
from xmlrpc.client import ServerProxy

from funnylog2 import logger

from youqu_html_rpc.config import config
from youqu_html_rpc.environment import environment as envir


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
    def server_user_password(cls):
        user, password = cls.server().server_user_password()
        return user, password

    @classmethod
    def gen(cls, data_path, gen_path, http_path):
        cls.server().gen_html(data_path, gen_path, http_path)

    @classmethod
    def environment(cls, data_path):
        envir(data_path)


    @classmethod
    def gen_rpc(cls, allure_data_path, allure_html_path, local_ip, report_base_path, dirname):
        log_server = servers = [i.strip() for i in config.SERVER_IP.split("/") if i]
        while servers:
            config.SERVER_IP = random.choice(servers)
            if YouQuHtmlRpc.check_connected() is False:
                servers.remove(config.SERVER_IP)
                config.SERVER_IP = None
            else:
                break
        if config.SERVER_IP is None:
            raise EnvironmentError(f"所有REPORT SERVER不可用: {log_server}")
        report_dirname = f'{time.strftime("%Y%m%d%H%M%S")}_{local_ip}_{dirname}'
        report_server_path = f"{report_base_path}/{report_dirname}"
        report_server_data_path = f"{report_server_path}/data"
        report_server_html_path = f"{report_server_path}/html"
        YouQuHtmlRpc.makedirs(report_server_data_path)
        rs_user, rs_password = YouQuHtmlRpc.server_user_password()
        logger.info(f"send data to report server: {config.SERVER_IP}")
        rsync = 'rsync -av -e "ssh -o StrictHostKeyChecking=no"'
        import pexpect
        stdout, return_code = pexpect.run(
            f"/bin/bash -c '{rsync} {str(allure_data_path)}/ {rs_user}@{config.SERVER_IP}:{report_server_data_path}/'",
            events={'password': f'{rs_password}\n'},
            withexitstatus=True,
            timeout=6000,
        )
        if return_code != 0:
            logger.error(f"failed to rsync to {config.SERVER_IP}")
            logger.error(stdout.decode("utf-8"))
        
        cls.gen(report_server_data_path, report_server_html_path, report_dirname)
        report_server_url = f"http://{config.SERVER_IP}/{report_dirname}"
        logger.info(f"html report url: {report_server_url}")
        with open(f"{allure_html_path}/{report_dirname}.txt", "w", encoding="utf-8") as f:
            f.write(report_server_url)
