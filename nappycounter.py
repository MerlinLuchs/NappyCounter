import RPi.GPIO as GPIO
import time
import tm1637 # LCD Screen
from datetime import datetime
import datetime
import os
from epaper_windel import *

brightness_value = 1 # 1 bis 7
tm = tm1637.TM1637(clk=21, dio=20, brightness=brightness_value) # Where LCD is connected.


# Set up buttons
button_black = 5
button_dual = (6, 13)

GPIO.setup(button_black, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_dual, GPIO.IN, pull_up_down=GPIO.PUD_UP)

script_dir = os.path.dirname(os.path.abspath(__file__)) # Directory for crontab
filename = os.path.join(script_dir, "nappies.txt") # when running via crontab

    
# Define button callback functions
def button_black_callback(channel):
    today = day_and_time() # Get today's date.
    today = '{:%A, %Y-%m-%d}'.format(today) + ' (' + '{:%H:%M}'.format(today) + ')' # Make the format nicer.
    message = "(Black) There were a pee and poo on " + str(today)
    print(message)
    writetofile(message) # Note it down in a file.
    print_to_LCD(3) # Show on LCD display "Poo" so I know the correct button was pressed.
    # printEverything()

def button_dual_callback(channel):
    today = day_and_time()
    today = '{:%A, %Y-%m-%d}'.format(today) + ' (' + '{:%H:%M}'.format(today) + ')'
    if channel == button_dual[0]:
        message = "(Blue) There was a poo on " + str(today)
        print(message)
        writetofile(message)
        print_to_LCD(2)
        # printEverything()
    elif channel == button_dual[1]:
        message = "(Yellow) There was a pee on " + str(today)
        print(message)
        writetofile(message)
        print_to_LCD(1)
        # printEverything()
    else:
        pass

def day_and_time():
    today = datetime.datetime.today()
    return today
# pee = 1, poo = 2, both = 3


def print_to_LCD(value):
    today = day_and_time()
    numbers = getNappiesToday(today)
    nappiestoday = numbers[0]
    poostoday = numbers[1]
    peestoday = numbers[2]
    totalnappies_to_date = numbers[3]
    if value == 2:
        tm.show('Poo')
        time.sleep(2)
        tm.write([0, 0, 0, 0])
        tm.show(str(poostoday))
        # time.sleep(2)
        # tm.write([0, 0, 0, 0])
        # tm.show(str(totalnappies_to_date))
    elif value == 1:
        tm.show('Pee')
        time.sleep(2)
        tm.write([0, 0, 0, 0])
        tm.show(str(peestoday))
        # time.sleep(2)
        # tm.write([0, 0, 0, 0])
        # tm.show(str(totalnappies_to_date))
    elif value == 3:
        tm.show('Both')
        time.sleep(2)
        tm.write([0, 0, 0, 0])
        tm.show(str(nappiestoday))
        # time.sleep(2)
        # tm.write([0, 0, 0, 0])
        # tm.show(str(totalnappies_to_date))
    time.sleep(2)
    tm.write([0, 0, 0, 0])
    printEverything()

    
def writetofile(message):
    # filename = "nappies.txt" # Our file for the nappy info.
    with open(filename, 'a') as file:
        file.write(message  + ".\n")    



    
# Add button event detection
# The bouncetime is so high because I was getting double button-presses whenever the LED or the ePaper
# was still busy when the bouncetime was over. Now the bouncetime lasts longer than it takes the epaper
# to refresh and that seems to have fixed the issue.
GPIO.add_event_detect(button_black, GPIO.FALLING, callback=button_black_callback, bouncetime=30000)
GPIO.add_event_detect(button_dual[0], GPIO.FALLING, callback=button_dual_callback, bouncetime=30000)
GPIO.add_event_detect(button_dual[1], GPIO.FALLING, callback=button_dual_callback, bouncetime=30000)



# Wait for events
try:
    while True:
        time.sleep(200)
except KeyboardInterrupt:
    print("INTERRUPT - There was an interrupt and we're cleaning the GPIOs.")
    GPIO.cleanup()
    print("INTERRUPT - Cleanup done.")
