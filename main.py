import socket
import network
from _thread import *
import _thread
import os
import machine
from settings import rtc

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect("Matthijs", "FrankIsGeweldig")

while not station.isconnected(): pass
station.ifconfig()

print(station.ifconfig())
print("Hello")

HEADERSIZE = 10
agendaEvent = [[],[],[],[],[],[],[],[],[],[],[],[]]

def loadAgenda():
    with open('eventStorage.txt', 'r') as file:
        for line in file:
            line = line.strip() #preprocess line
            month = int(line.split(',', 1)[0]) - 1 #-1 as array count starts at 0
            agendaEvent[month].append(line)

def saveAgenda():
    with open('eventStorage.txt', 'w') as file:
        for a in agendaEvent:
            for l in a:
                file.write(l + '\n')
    file.close()
    
def removeEvents(month,day):
    tempMonth = []
    for i in agendaEvent[month]:
        item = i.split(',')
        if day != int(item[1]):
            tempMonth.append(i)
    agendaEvent[month] = ''
    agendaEvent[month] = tempMonth
  
    
def rchop(string, ending):
    if string.endswith(ending):
        return string[:-len(ending)]
    return string

def processMessage(c,fullmsg):  
    msg = fullmsg.decode('utf-8')
    action = msg.split(',',1)[0]
    
    if action == 'Request':
        msgArray = msg.split(',')
        newMsg = ''
        month = int(msgArray[1])-1
        for i in agendaEvent[month]:
            temp = i.split(',')
            if int(temp[1]) == int(msgArray[2]):
                newMsg += i + '\n'
        newMsg = rchop(newMsg, '\n')
        fullMsg = bytes('{:<10}'.format(str(len(newMsg))), 'utf-8') + bytes(newMsg,'utf-8')
        c.send(fullMsg)
    elif action == 'Update': 
        temp = msg.split(',',3)
        month = int(temp[1]) - 1 #Array start at 0
        day = int(temp[2])
        msg = temp[3]
        
        removeEvents(month,day)
        
        if msg != '':
            linesplit = msg.split('\n')
            for i in linesplit:                                      
                agendaEvent[month].append(i)
        saveAgenda()        
 
def threaded(c):
    fullMsg = b''
    newMsg = True
    msglen = 0

    while True:
        print("Clock: ")
        print(rtc.datetime())
        buf = c.recv(1024)
        if newMsg:
            msglen = int(buf[:HEADERSIZE])
            newMsg = False
        fullMsg += buf

        if len(fullMsg) - HEADERSIZE == msglen:
            start_new_thread(processMessage, (c,fullMsg[10:],))
            newMsg = True
            msglen = 0
            fullMsg = b''

def Main():
    host = '192.168.1.100'
    port = 12345


    from getTime import settime
    settime()

    print("Clock: ")
    print(rtc.datetime())
    
    loadAgenda()
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to ip", host)
    print("socket binded to port", port)

    # put the socket into listening mode 
    s.listen(5)
    print("socket is listening")
    # a forever loop until client wants to exit
    while True:
        # establish connection with client
        c, addr = s.accept()

        # lock acquired by client 
        #print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])

        # Start a new thread and return its identifier

        start_new_thread(threaded, (c,))
    s.close()

Main()
