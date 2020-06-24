import socket
import network
from _thread import *
import _thread
import os
import random
from settings import rtc
from Medicine import medicineSchedule,setAlarms,waitForAlarms

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
    
def removeAgendaEvents(month,day):
    tempMonth = []
    for i in agendaEvent[month]:
        item = i.split(',')
        if day != int(item[1]):
            tempMonth.append(i)
    agendaEvent[month] = ''
    agendaEvent[month] = tempMonth

def loadMedicineSchedule():
    with open('medicineStorage.txt', 'r') as file:
        for line in file:
            line = line.strip() #preprocess line
            medicineSchedule.append(line)

def saveMedicineSchedule():
    with open('medicineStorage.txt', 'w') as file:
        for a in medicineSchedule:               
            file.write(a + '\n')    
    file.close()

def removeMedicineScheduleEvents(day):
    templist = []
    global medicineSchedule
    for med in medicineSchedule:
        medicineDay = int(med.split(',',1)[0])
        if day == medicineDay:
            templist.append(med)
    medicineSchedule = templist
            
def rchop(string, ending):
    if string.endswith(ending):
        return string[:-len(ending)]
    return string

def processMessage(c,fullmsg):  
    msg = fullmsg.decode('utf-8')
    action = msg.split(',',1)[0]
    
    if action == 'Request agenda':
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
    elif action == 'Update agenda': 
        temp = msg.split(',',3)
        month = int(temp[1]) - 1 #Array start at 0
        day = int(temp[2])
        msg = temp[3]
        
        removeAgendaEvents(month,day)
        
        if msg != '':
            linesplit = msg.split('\n')
            for i in linesplit:                                      
                agendaEvent[month].append(i)
                
        saveAgenda()
    #MedicineSchedule    
    elif action == 'Request med':
        msgArray = msg.split(',')
        newMsg = ''
        day = int(msgArray[1])
        for i in medicineSchedule:
            temp = i.split(',')
            if int(temp[0]) == int(msgArray[1]):
                newMsg += i + '\n'
        newMsg = rchop(newMsg, '\n')
        fullMsg = bytes('{:<10}'.format(str(len(newMsg))), 'utf-8') + bytes(newMsg,'utf-8')
        c.send(fullMsg)

    elif action == 'Update med':
        temp = msg.split(',',2)
        day = int(temp[1])
        msg = temp[2]
        
        removeMedicineScheduleEvents(day)
        
        if msg != '':
            linesplit = msg.split('\n')
            for i in linesplit:
                medicineSchedule.append(i)
        saveMedicineSchedule()  
    elif action == 'EmergencyCall':

        char = ["0644626244","0626142741","0611554488"]
        index = len(char)
        randomNumber = random.randint(0,index-1)
        randomStatus = random.randint(0, 1)

        print('Choose to connect number: '+ char[randomNumber])
        if(randomStatus == 0):
            print('Unsuccessfully connected to ' + char[randomNumber])
        else:
            print('Successfully connected to ' + char[randomNumber])

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
    s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    host = '192.168.1.100'
    port = 54321


    from getTime import settime
    settime()

    print("Clock: ")
    print(rtc.datetime())
    
    loadAgenda()
    loadMedicineSchedule()
    setAlarms()
    s.bind((host, port))
    start_new_thread(waitForAlarms,())

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
