import wifimgr
from time import sleep
import machine
import ure

try:
  import usocket as socket
except:
  import socket

led = machine.Pin(2, machine.Pin.OUT)

wlan = wifimgr.get_connection()
if wlan is None:
    print("Could not initialize the network connection.")
    while True:
        pass  # you shall not pass :D

# Main Code goes here, wlan is a working network.WLAN(STA_IF) instance.
print("ESP OK")


# This function contains of HTML files
def web_page(client):
  html = """\
        <html>
            <h1 style="color: #5e9ca0; text-align: center;">
                <span style="color: #ff0000;">
                    Nurse Watch
                </span>    
            </h1>
            <form action="entered" method="post">
                <table style="margin-left: auto; margin-right: auto;">
                    <tbody>
            <tr>
                            <td>Password:</td>
                            <td><input name="Password" type="text" /></td>
                        </tr>
                    </tbody>
                </table>
                <p style="text-align: center;">
                    <input type="submit" value="Submit" />
                </p>
            </form>
            
    """ 
  send_response(client,html)
  
# This function sends the response to the server  
def send_response(client, payload, status_code=200):
 client.sendall("HTTP/1.0 {} OK\r\n".format(status_code))
 client.sendall("Content-Type: text/html\r\n")
 client.sendall("Content-Length: {}\r\n".format(len(payload)))
 client.sendall("\r\n")
 if len(payload) > 0:
  client.sendall(payload)
  
# This function stores the value  
def handle_save_reco(client, request):
  match = ure.search("Password=([^&]*)",request)
  print(match.group(0).decode("utf-8"))
  
# This function sends invalid request to the server
def handle_not_found(client, url):
    send_response(client, "Path not found: {}".format(url), status_code=404)  
    
# Establish the bridge    
try:
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  s.bind(('', 80))
  s.listen(5)
except OSError as e:
  machine.reset()
  
while True:
  try:
    client, addr = s.accept()
    client.settimeout(5.0)
   
    request = b""
    try:
      while "\r\n\r\n" not in request:
            request += client.recv(512)
    except OSError:
      pass
   
    if "HTTP" not in request:  # skip invalid requests
                continue
                
    #Check URL inside request            
    try:
      url = ure.search("(?:GET|POST) /(.*?)(?:\\?.*?)? HTTP", request).group(1).decode("utf-8").rstrip("/")
    except :
      url = ure.search("(?:GET|POST) /(.*?)(?:\\?.*?)? HTTP", request).group(1).rstrip("/")
    
    # Categorize the request
    if url == "":
      web_page(client)
    elif url == "entered":
      handle_save_reco(client,request)
      web_page(client)
    else:
      handle_not_found(client,url)
    
    client.close()
  except OSError as e:
    client.close()
    print('Connection closed')


