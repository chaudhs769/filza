#!/usr/bin/python3
import os
import json
import base64
import requests
import configparser


class Filza:
    def __init__(self, ip, port):
        self.ios_ip = ip
        self.ios_server_port = port
        self.session = requests.session()

    def go(self, server_username, server_password, path='/'):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        }

        if server_username and server_password:
            headers['Authorization'] = f'Basic {base64.b64encode(f"{server_username}:{server_password}".encode()).decode()}'
        
        response = self.session.get(f'http://{self.ios_ip}:{self.ios_server_port}', headers=headers)
        response.raise_for_status()

        query_string_params = {
            'path': path,
            'mode': 'getfolder',
            'showThumbs': True,
            'time': 415
        }
        response = self.session.get(f'http://{self.ios_ip}:{self.ios_server_port}/connectors/html/filemanager.html', params=query_string_params, headers=headers)
        response.raise_for_status()
        return response.json()


root_directory = os.getcwd()
cfg = configparser.ConfigParser()
configFilePath = os.path.join(root_directory, 'config.cfg')
cfg.read(configFilePath)

username = cfg.get('authentication', 'username')
password = cfg.get('authentication', 'password')

idevice_ip = cfg.get('webdav', 'idevice_ip')
port = cfg.get('webdav', 'port')

f = Filza(idevice_ip, port)
print(json.dumps(f.go(username, password), indent=4))
