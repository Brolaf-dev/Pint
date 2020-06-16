import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
sock.bind(('127.0.0.1', 8765)) 
sock.listen(5) 
print("Server listening")
while True:  
    connection,address = sock.accept()  
    buf = connection.recv(1024)     		
    connection.close()
