try:
    import usocket as socket
except:
    import socket
try:
    import ustruct as struct
except:
    import struct


# (date(2000, 1, 1) - date(1900, 1, 1)).days * 24*60*60
NTP_DELTA = 3155673600

# The NTP host can be configured at runtime by doing: ntptime.host = 'myhost.org'
host = "pool.ntp.org"


def time():
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1B
    addr = socket.getaddrinfo(host, 123)[0][-1]
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        sock.settimeout(1)
        res = sock.sendto(NTP_QUERY, addr)
        msg = sock.recv(48)
    finally:
        sock.close()
    val = struct.unpack("!I", msg[40:44])[0]
    return val - NTP_DELTA 


# There's currently no timezone support in MicroPython, so
# utime.localtime() will return UTC time (as if it was .gmtime())
def settime():
    print("Here")
    t = time()
    t1 = t + 120*60
    from settings import rtc
    import utime
    tm = utime.localtime(t1)
    rtc.datetime((tm[0], tm[1], tm[2], tm[6], tm[3], tm[4], tm[5], 0))