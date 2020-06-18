# Pint
For this Pint project, Nurse Watch is built of ESP32-WROOM which has the internal built Wi-Fi and Bluetooth. The language used for this microcontroller is Arduino, it can be considered more efficient in this situation because of the support of E-ink Display.

To implement the Nurse Watch, user has to follow the given step: 
 1. Download one of those recommended application: Arduino IDE
 2. Fill in the SSID and PASSWORD for the WiFi connection:
    `const char* ssid = " ";`
    `const char* password =  " ";`
 3. You can find the port with unique type unit16_t, for this case, I recommended the value should be 8888.
 4. GxEPDMaster is a zip file which contains the library supporting deriving the Pin and manipulating the data to trasnfer to E-INK             display. If the given zip is not responding, please follow the link below:  https://github.com/ZinggJM/GxEPD. Then, choose option:         `ADD.zip library` inside Arduino.
 
Importantly, user has to pay fully attention to the IP address of your connection in the serrial command so user can access to the socket:
`WiFi connected with IP: xxx.xxx.xxx.xxx` . By noticing the IP, many users connecting to the same WiFi as the Nurse Watch's can easily      establish the socket connection to send/receive data.

