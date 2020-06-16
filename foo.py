# I ran this in Pycharm to create a
# client socket that is connected to
# a server running on ESP32.
#
# This client send message to the
# server.
#
import socket



soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.connect(('192.168.1.18', 8765))
msg = '1,1,Test,14:00,Here\n5,4,Test2,14:00,There'
msg = str.encode(msg, 'utf-8')
soc.send(msg)
soc.close()
