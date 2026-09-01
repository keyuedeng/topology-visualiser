import getpass

from netmiko import ConnectHandler


def get_credentials():
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    secret = getpass.getpass("Enable secret (press Enter to reuse password): ") or password
    return username, password, secret


def connect(host: str, username: str, password: str, secret: str):
    device_params = {
        "device_type": "cisco_ios",
        "host": host,
        "username": username,
        "password": password,
        "secret": secret,
    }
    connection = ConnectHandler(**device_params)
    connection.enable()
    return connection
