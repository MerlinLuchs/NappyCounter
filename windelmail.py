import requests
from time import sleep
import smtplib
import os
from epaper_windel import getNappiesToday, day_and_time


SMTP_SERVER = 'smtp.gmail.com' #Email Server (don't change!)
SMTP_PORT = 587 #Server Port (don't change!)
GMAIL_USERNAME = 'xxxxxx@gmail.com' #change this to match your gmail account
GMAIL_PASSWORD = 'xxxxxx' #change this to match your gmail app-password
sendTo = ['mom@xxx.xx', 'dad@xxx.xx']
emailSubject = "Nappies"

script_dir = os.path.dirname(os.path.abspath(__file__)) # Directory for crontab
filename_nappiestxt = os.path.join(script_dir, "nappies.txt") # when running via crontab
filename_greetingtxt = os.path.join(script_dir, "mail-greeting.txt") # when running via crontab
filename_goodbyetxt = os.path.join(script_dir, "mail-goodbye.txt") # when running via crontab
filename_finalmessage = os.path.join(script_dir, "finalmessage.txt") # when running via crontab
class Emailer:
    def sendmail(self, recipient, subject, content):
        #Create Headers
        headers = ["From: " + GMAIL_USERNAME, "Subject: " + subject, "To: " + recipient,
            "MIME-Version: 1.0", "Content-Type: text/plain"]
        headers = "\r\n".join(headers)

        #Connect to Gmail Server
        session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        session.ehlo()
        session.starttls()
        session.ehlo()

        #Login to Gmail
        session.login(GMAIL_USERNAME, GMAIL_PASSWORD)

        #Send Email & Exit
        session.sendmail(GMAIL_USERNAME, recipient, headers + "\r\n\r\n" + content)
        session.quit

sender = Emailer()

# with open("nappies.txt", "r") as filestream:
with open(filename_nappiestxt, "r") as filestream:
        with open(filename_greetingtxt, "r") as file:
            greeting = file.read()
        with open(filename_goodbyetxt, "r") as file:
            goodbye = file.read()
        f = open(filename_finalmessage, "w")
        f.write(greeting)
        f.close()
        today = day_and_time()
        numbers = getNappiesToday(today)
        nappiestoday = numbers[0]
        poostoday = numbers[1]
        peestoday = numbers[2]
        totalnappies_to_date = numbers[3]
        # with open('finalmessage.txt', 'a') as f:
        with open(filename_finalmessage, 'a') as f:
                f.write('{:%A, %Y-%m-%d}'.format(today) + ' (' + '{:%H:%M}'.format(today) + ')' + "\n\nPoos: " + str(poostoday) + "\nPees: " + str(peestoday) + "\nNappies changed today: " + str(nappiestoday) + "\n\nNappies changed since birth: " + str(totalnappies_to_date))
                f.write(goodbye)
        # with open('finalmessage.txt', 'r') as file:
        with open(filename_finalmessage, 'r') as file:
            emailContent = file.read()
        for recipient in sendTo:
            sender.sendmail(recipient, emailSubject, emailContent)
        # print(emailContent)
