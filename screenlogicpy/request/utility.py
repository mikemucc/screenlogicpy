import socket
import struct
from ..const import ScreenLogicError, header, code

def sendRecieveMessage(gateway_socket, code, message=b''):
    gateway_socket.sendall(makeMessage(code, message))
    data = gateway_socket.recv(1024)
    if not data:
        raise ScreenLogicError("No data recieved from the gateway. Request code: {}".format(code))
    rcvCode, buff = takeMessage(data)
    if (rcvCode != (code + 1)):
        raise ScreenLogicError("Unexpected response recieved from the gateway. Expected: {}. Recieved: {}.".format(code + 1, rcvCode))
    return buff


def encodeMessageString(string):
    data = string.encode()
    length = len(data)
    pad = 4 - (length % 4)  # pad 'x' to multiple of 4
    fmt = "<I" + str(length) + "s" + str(pad) + "x"
    return struct.pack(fmt, length, data)

def decodeMessageString(data):
    #length = len(data)
    size = struct.unpack_from("<I", data, 0)[0]
    return struct.unpack_from("<" + str(size) + "s", 
                              data, 
                              struct.calcsize("<I"))[0].decode("utf-8")

# Protocol header for every (non-datagram) message sent to/from
# the gateway. 
# This header describes the first 8 bytes:
# 0          2          4           8                              N
# | MSG CD 1 | MSG CD 2 | Data Size | Message Data (parameters) -> |
 
# appends a header to an optional already formatted message.
def makeMessage(msgCode2, messageData=b''):
    return struct.pack(header.fmt + str(len(messageData)) + "s", 
                       code.MSG_CODE_1, 
                       msgCode2, 
                       len(messageData), 
                       messageData)

# takes the header off of the pool message and returns just the message part
def takeMessage(message):
    messageBytes = len(message) - header.length
    #pylint: disable=unused-variable
    rcvCode1, rcvCode2,\
        rcvLen, data = struct.unpack(header.fmt + str(messageBytes) + "s",
                                     message)
    if(rcvLen != messageBytes):
        raise ScreenLogicError("Invalid response recieved from host.")
    if(rcvCode2 == code.UNKNOWN_ANSWER):
        raise ScreenLogicError("Unexpected response recieved from the gateway. Recieved code_unknown.")
    return rcvCode2, data # return raw data
