from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from datetime import datetime,timedelta
from threading import Timer
import time
from random import randint
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

now = datetime.now()



options = Options()
options.headless = True
driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=options)
x=datetime.today()
y = x.replace(day=x.day, hour=6, minute=0, second=0, microsecond=0) + timedelta(days=1)
delta_t=y-x

secs=delta_t.seconds+1

def train_tracker():

    time_delay = randint(5,10)
    
    driver.get('https://www.rideuta.com/Rider-Tools/Schedules-and-Maps')
    route_button = driver.find_element_by_xpath('//*[@id="rail"]/ul/li[2]/a')
    route_button.click()

    time.sleep(time_delay)
    
    direction = driver.find_element_by_id('direction')
    direction.send_keys('To Medical')
    time.sleep(time_delay)
    
    stop = driver.find_element_by_name('stop[]')
    stop.send_keys('900 East Station')
    
    schedule_button = driver.find_element_by_id('routebutton')
    schedule_button.click()
    
    time.sleep(time_delay)
    
    train_times = driver.find_element_by_class_name('stop-times').text
    str(train_times)
    train_times=train_times.split('\n')
    
    content = []
    for i in train_times[:20]:
        content.append('There is a train at {}'.format(i))
    
    driver.quit()
    
    port = 465
    sender_email = ""
    receiver_email = ""
    password = ''
    
    message = MIMEMultipart()
    message["Subject"] = "Your Train Schedule"
    message["From"] = sender_email
    message["To"] = receiver_email
    
    message_title = 'The 900 East Station has the following times: \n'
    message_guts = " \n".join(content)
    
    guts1 = MIMEText(message_title, "text")
    guts2 = MIMEText(message_guts, "text")
    
    message.attach(guts1)
    message.attach(guts2)
    
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", port)
        server.ehlo()
        server.login(sender_email,password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.close()
    
        print('Email sent!')
    except:
        print('something went wrong')

t = Timer(secs, train_tracker)
t.start()