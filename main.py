import rp2
import network
import ubinascii

import time
from machine import Pin
from ir_rx.nec import NEC_16  # NEC remote, 8 bit addresses

import wiimclient as wc
from secrets import secrets

# Set country to avoid possible errors
rp2.country('US')

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
# If you need to disable powersaving mode
# wlan.config(pm = 0xa11140)

# See the MAC address in the wireless chip OTP
mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
print('mac = ' + mac)

# Load login data from different file for safety reasons
ssid = secrets['ssid']
pw = secrets['pw']
wiimip = secrets['wiimip']

wlan.connect(ssid, pw)

# Wait for connection with 10 second timeout
timeout = 10
while timeout > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    timeout -= 1
    print('Waiting for connection...')
    time.sleep(1)

# Handle connection error
# Error meanings
# 0  Link Down
# 1  Link Join
# 2  Link NoIp
# 3  Link Up
# -1 Link Fail
# -2 Link NoNet
# -3 Link BadAuth

wlan_status = wlan.status()

if wlan_status != 3:
    raise RuntimeError('Wi-Fi connection failed')
else:
    print('Connected')
    status = wlan.ifconfig()
    print('ip = ' + status[0])

keymap = {69:1,70:2,71:3,68:4,64:5,67:6,7:7,21:8,9:9}
          
def callback(keycode, addr, ctrl):
    if keycode < 0:  # NEC protocol sends repeat codes.
        #print('Repeat code.')
        pass
    else:
        print(keycode)
        if keycode == 28:
        # Play / Pause
            dict = wc.invokeWiimAction(wiimip,'AVTransport','GetTransportInfo')
            if dict['CurrentTransportState'] == 'PLAYING':
                wc.invokeWiimAction(wiimip,'AVTransport','Pause')
            else:
                wc.invokeWiimAction(wiimip,'AVTransport','Play',{'Speed': '1'})
                
        elif keycode == 90:
        # Next
            wc.invokeWiimAction(wiimip,'AVTransport','Next')
        elif keycode == 8:
        # Prev
            wc.invokeWiimAction(wiimip,'AVTransport','Previous')
        elif keycode == 24:
        # Volume Up
            dict = wc.invokeWiimAction(wiimip,'RenderingControl','GetVolume',{'Channel':'Master'})
            print(dict['CurrentVolume'])
            ## TODO: SetVolume
        elif keycode == 82:
        # Volume Down
            dict = wc.invokeWiimAction(wiimip,'RenderingControl','GetVolume',{'Channel':'Master'})
            print(dict['CurrentVolume'])
            ## TODO: SetVolume
        elif keycode in keymap:
        # 1-9: Play Queue index 1-9
            index = keymap[keycode]
            dict = wc.invokeWiimAction(wiimip,'PlayQueue','PlayQueueWithIndex',{'QueueName':'CurrentQueue','Index':f'{index}'})
            
        
ir = NEC_16(Pin(28, Pin.IN), callback)
while True:
    time.sleep_ms(500)