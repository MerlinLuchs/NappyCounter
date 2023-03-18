# NappyCounter

This nappy counter counts nappies via three buttons. One is a seeed Grove button (https://www.berrybase.de/en/seeed-grove-dual-taster) that was adjusted to have three cable endings rather than the seeed plug. The other is a random other button from Aliexpress (https://de.aliexpress.com/item/1005002951123869.html). Also attached is a 2.9 inch epaper display (https://www.berrybase.de/en/2.9-296-128-epaper-display-modul-mit-spi-interface-dreifarbig-rot-schwarz-weiss) and a LED display (https://www.berrybase.de/en/7-segment-led-display-modul-i2c-schnittstelle-tm1637-14mm-rot).

IMPORTANT! The epaper config files (in my case epd2in9bc.py and epdconfig.py) also need to be in the directory.

The nappy counter reacts to a button press. Blue button, LED display shows "Poo" and then the number of poo nappies that day.The epaper then updates with the statistics. Yellow button is for pee, black button is for both in one nappy. 

The windelmail.py is running on a cronjob to send an email every night with today's stats. 
