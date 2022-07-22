# WiiM-Remote-Pi-Pico-W
Simple hack to test IR remote control with WiiM Mini on Pi Pico W

Uses a cheap remote and sensor from Amazon:  https://www.amazon.com/gp/product/B07DJ58XGC/
and a Pi Pico W.  

Thanks to Peter Hinch for his great MicroPython libraries.  This uses his micropython_ir: https://github.com/peterhinch/micropython_ir

The code expects the sensor on GP28, but any other GPIO can be used.

Remote control keys:

Keys 1-9 will play the corresponding Queue item.

Left Arrow = Previous

Right Arrow = Next

OK = Play/Pause


Edit secrets.py with your WiFi info, and the WiiM Mini's IP address.  Use Thonny to push the files to your Pi Pico W and test.  When working, simply power the Pi Pico W from a wall wart.
