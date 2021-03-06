import struct
from .utility import sendRecieveMessage, makeMessage, decodeMessageString
from ..const import code

def request_gateway_version(gateway_socket):
    response = sendRecieveMessage(gateway_socket, code.VERSION_QUERY)
    return decodeMessageString(response)
