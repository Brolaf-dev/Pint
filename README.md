# Pint
For this Pint project, Nurse Watch is built of ESP32-WROOM which has the internal built Wi-Fi and Bluetooth. The language used for this microcontroller is Micropython, it is a lean and efficient implementation of Python 3 that contains a small batch of the Python library.

To implement the Nurse Watch, user has to follow the given step: 
 1. Download one of those recommended application: UPycraft or Thonny.
 2. WifiMgr.py is an extended library which was invented and developed by `randomnertutorials`. This supports your ESP32 by displaying the     options of available Wi-Fi nearby, moreover, it stores the joint Wi-Fi ssids and passwords inside file .dat in order to speed up for       the next time.
 3. Main.py contains various functions for the ESP32-WROOM. More details, dig in the comments inside the code.
 
 Importantly, user has to pay fully attention to the IP address of your connection so user can access to the web server:
 `Connected. Network config:  ('xxx.xxx.xxx.xx', '255.255.255.0', '192.168.137.1', '192.168.137.1')`
 You can find that after colon, the first address after the brackets. 
