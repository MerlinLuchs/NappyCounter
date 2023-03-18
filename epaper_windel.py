import epd2in9bc # For the epaper
from PIL import Image,ImageDraw,ImageFont
import textwrap
from datetime import datetime
import datetime
import time 
import os

epd = epd2in9bc.EPD()
font_path = os.path.join(os.path.dirname(__file__), 'Font.ttc')
font22 = ImageFont.truetype(font_path, 22)
font20 = ImageFont.truetype(font_path, 20)
font18 = ImageFont.truetype(font_path, 18)
font16 = ImageFont.truetype(font_path, 16)
script_dir = os.path.dirname(os.path.abspath(__file__)) # To create nappies.txt in script directory when running via crontab
filename = os.path.join(script_dir, "nappies.txt")

width = 296
height = 128


printed = False

def print18(x,y,drawblack, message):
    drawblack.text((x,y), message, font = font18, fill = 0)
    drawblack.line((0, 24, width, 24), fill=0)
    
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

def getNappiesToday(today):
    today = '{:%Y-%m-%d}'.format(today)
    # Create the file if it doesn't exist
    # filename = "nappies.txt" # Our file for the nappy info.
    # filename = os.path.join(script_dir, "nappies.txt") # Filepath for crontab
    # if not os.path.exists(filename):
        # open(filename, 'w').close()
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
    
def day_and_time():
    today = datetime.datetime.today()
    return today
    
# if printed == False:
    # printEverything()
    # printed = True
