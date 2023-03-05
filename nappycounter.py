import RPi.GPIO as GPIO
import time
import tm1637 # LCD Screen
from datetime import datetime
import datetime
import os
import epd2in9bc # For the epaper
from PIL import Image,ImageDraw,ImageFont
import textwrap

brightness_value = 1 # 1 bis 7
tm = tm1637.TM1637(clk=21, dio=20, brightness=brightness_value) # Where LCD is connected.

epd = epd2in9bc.EPD()

font22 = ImageFont.truetype("Font.ttc", 22)
font20 = ImageFont.truetype("Font.ttc", 20)
font18 = ImageFont.truetype("Font.ttc", 18)
font16 = ImageFont.truetype("Font.ttc", 16)

width = 296
height = 128

# Set up buttons
button_black = 5
button_dual = (6, 13)

GPIO.setup(button_black, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_dual, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    
# Define button callback functions
def button_black_callback(channel):
    today = day_and_time() # Get today's date.
    today = '{:%A, %Y-%m-%d}'.format(today) + ' (' + '{:%H:%M}'.format(today) + ')' # Make the format nicer.
    message = "(Black) There were a pee and poo on " + str(today)
    print(message)
    writetofile(message) # Note it down in a file.
    print_to_LCD(3) # Show on LCD display "Poo" so I know the correct button was pressed.
    printEverything() # Refresh my epaper with the data.

def button_dual_callback(channel):
    today = day_and_time()
    today = '{:%A, %Y-%m-%d}'.format(today) + ' (' + '{:%H:%M}'.format(today) + ')'
    if channel == button_dual[0]:
        message = "(Blue) There was a poo on " + str(today)
        print(message)
        writetofile(message)
        print_to_LCD(2)
        printEverything()
    elif channel == button_dual[1]:
        message = "(Yellow) There was a pee on " + str(today)
        print(message)
        writetofile(message)
        print_to_LCD(1)
        printEverything()
    else:
        pass

def day_and_time():
    today = datetime.datetime.today()
    return today
# pee = 1, poo = 2, both = 3


def print_to_LCD(value):
    if value == 2:
        tm.show('Poo')
    elif value == 1:
        tm.show('Pee')
    elif value == 3:
        tm.show('Both')
    time.sleep(2)
    tm.write([0, 0, 0, 0]) 

def getNappiesToday(today):
    today = '{:%Y-%m-%d}'.format(today)
    # Create the file if it doesn't exist
    filename = "nappies.txt" # Our file for the nappy info.
    if not os.path.exists(filename):
        open(filename, 'w').close()
    with open(filename, 'r') as f:
        # Count the number of nappies changed today by counting how often today's date appears in all lines.
        num_nappies_today = sum(1 for line in f if str(today) in line)
        # Reset file pointer to beginning
        f.seek(0)
        num_both_today = sum(1 for line in f if str(today) in line and "Black" in line)
        f.seek(0)
        num_poos_today = sum(1 for line in f if str(today) in line and "Blue" in line) + num_both_today
        f.seek(0)
        num_pees_today = sum(1 for line in f if str(today) in line and "Yellow" in line) + num_both_today
        f.seek(0)
        total_nappies_to_date = sum(1 for line in f)
        numbers = [num_nappies_today, num_poos_today, num_pees_today, total_nappies_to_date]
        return numbers

def givestats():
    today = day_and_time()
    numbers = getNappiesToday(today)
    nappiestoday = numbers[0]
    poostoday = numbers[1]
    peestoday = numbers[2]
    totalnappies_to_date = numbers[3]
    today = '{:%A, %Y-%m-%d}'.format(today) + ' (' + '{:%H:%M}'.format(today) + ')'
    statsmsg = str(today) + "\nNappies changed today: " + str(nappiestoday) + "\nPoos today: " + str(poostoday) + "\nPees today: " + str(peestoday) + "\nNappies changed to date: " + str(totalnappies_to_date)
    return statsmsg
    
def writetofile(message):
    filename = "nappies.txt" # Our file for the nappy info.
    with open(filename, 'a') as file:
        file.write(message  + ".\n")
    
def print18(x,y,drawblack, message):
    drawblack.text((x,y), message, font = font18, fill = 0)
    
def printEverything():
    statsmsg = givestats()
    epd.init() # Initializing the epaper
    image = Image.new('1', (height, width), 255)  # 255: clear the frame
    ryimage = Image.new('1', (height, width), 255) 
    HBlackimage = Image.new('1', (width, height), 255)  # 298*126
    HRYimage = Image.new('1', (width, height), 255)
    drawblack = ImageDraw.Draw(HBlackimage)
    drawry = ImageDraw.Draw(HRYimage)
    draw = ImageDraw.Draw(image)
    
    print18(4,4, drawblack, statsmsg) # This prints the message to the epaper.
    
    epd.display(epd.getbuffer(HBlackimage), epd.getbuffer(HRYimage))
    epd.sleep()
    
# Add button event detection
GPIO.add_event_detect(button_black, GPIO.FALLING, callback=button_black_callback, bouncetime=2000)
GPIO.add_event_detect(button_dual[0], GPIO.FALLING, callback=button_dual_callback, bouncetime=2000)
GPIO.add_event_detect(button_dual[1], GPIO.FALLING, callback=button_dual_callback, bouncetime=2000)



# Wait for events
try:
    while True:
        time.sleep(2)
except KeyboardInterrupt:
    GPIO.cleanup()
