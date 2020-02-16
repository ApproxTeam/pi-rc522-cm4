#!/usr/bin/env python


import signal
import time
import sys

from pirc522 import RFID

run = True
rdr = RFID()
util = rdr.util()
util.debug = True

def end_read(signal,frame):
    global run
    print("\nCtrl+C captured, ending read.")
    run = False
    rdr.cleanup()
    sys.exit()

signal.signal(signal.SIGINT, end_read)

print("Starting")
while run:
    rdr.wait_for_tag()

    (error, data, back_data_request) = rdr.request()
    if not error:
        print("\nDetected: " + format(data, "02x"))

    (error, uid, back_data_anticoll) = rdr.anticoll()
    print("Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))
    if not error:
        if(back_data_request[0] == 68):
            # Mifare Ultralight, read without authentication
            # In case of ultralight anticoll uid can be bad
            util.set_tag(uid)
            dataReaded = rdr.read(0)
            print(dataReaded)
            dataReaded = rdr.read(1)
            print(dataReaded)
            dataReaded = rdr.read(2)
            print(dataReaded)
        elif(back_data_request[0] == 4):
            # Mifare 1K, normal auth procedure
            util.set_tag(uid)
            util.auth(rdr.auth_b, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
            util.read_out(4)
            util.deauth()
        time.sleep(1)
