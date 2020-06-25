from settings import rtc, servoOpen,servoClosed
import machine
from servo import Servo
from time import sleep

medicineSchedule = []
alarmId = []
turnTableServo = Servo(machine.Pin(4))
lidServo = Servo(machine.Pin(5))

def setTimeToSec(medicineAlarm):
    med = medicineAlarm.split(',')
    return (int(med[2])*3600+int(med[3])*60)

def setAlarms():
    medicineSchedule.sort(key=setTimeToSec)
    date = rtc.datetime()
    currentDate = date[3]
    for m in medicineSchedule:
        med = m.split(',')
        if int(med[0]) == currentDate:
            alarmId.append((date[0], date[1], date[2], int(med[2]),int(med[3]),0))
    print(alarmId)

def checkAlarm(i):
    if rtc.datetime()[0] == int(i[0]) and rtc.datetime()[1] == int(i[1]) and rtc.datetime()[2] == int(i[2]) and rtc.datetime()[4] >= int(i[3]) and rtc.datetime()[5] >= int(i[4]):
        return True
    else:
        return False
    
def openMedDraw(number):
    lidServo.write_angle(servoClosed)   
    servoAngle = -90 + (number*25)
    turnTableServo.write_angle(servoAngle)
    time.sleep(2)
    lidServo.write_angle(servoOpen)
    
def waitForAlarms():
    print("Wait")
    newDay = False
    while True:
        for i in alarmId:
            if checkAlarm(i):
                print("AlarmDone")
                med = medicineSchedule.pop()
                med = med.split(',')
                alarmId.pop()
                openMedDraw(int(med[4]))
                if not alarmId:
                    newDay = True
        if rtc.datetime()[4] == 0 and newDay:
            setAlarms()