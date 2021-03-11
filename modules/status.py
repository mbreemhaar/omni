import re
import socket
import ipaddress

# This field will contain an OmniInterface object when init() is called
omni = None


def init():
    """
    init is used to initialize the commands specified in this module, using the
    interface that was placed in the omni variable before init() is called
    """
    omni.add_command(get_server_status, 'status', 'Ping a server ip:port to see if it is online')


def ping_to_ip(ip, port):
    """
    Function that pings to an ip:port combo and returns true if a response from the remote is given
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.settimeout(2)
        s.connect((ip, port))
        s.shutdown(2)
        return True
    except (ConnectionRefusedError, socket.timeout):
        return False


async def get_server_status(args, message):
    """
    Command that returns the status of a specific ip:port combination

    Works with ip:port or url:port depending on the address a user is checking
    """
    if not args:
        return "Please give me an ip:port to ping to"

    pattern = r'(?:(?P<ip>(?:\d{1,3}.){3}\d{1,3})|(?P<url>(?:\w+.)+\w{2,})):(?P<port>\d+)'
    regex = re.compile(pattern, re.I)
    match = regex.match(str(args[0]))

    if not match:
        return "Please specify a valid ip:port combination"

    if current_ip := re.search(pattern, args[0]).group('ip'):
        if ipaddress.ip_address(current_ip).is_private:
            return "Unable to check private ip address"
    else:
        current_ip = re.search(pattern, args[0]).group('url')

    current_port = int(re.search(pattern, args[0]).group('port'))

    if ping_to_ip(current_ip, current_port):
        return args[0] + " is online"
    else:
        return args[0] + " is offline"
