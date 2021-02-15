#Note: Make sure all the installations are properly done, also don't name this python file by the name of 'email.py'!
#Use a different name for file else it will lead to an error.
#Check the python documentation: https://docs.python.org/3/library/email.html for an email and MIME handling package.

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from_addr = '####@gmail.com'    #sender's email address
to_addr = '***@gmail.com'       #receiver's email address
text = '''Body of the Email goes here...'''

username = 'Sender\'s Username'
password = 'password for the user id'

msg = MIMEMultipart()               #Creating an object for MIMEMultipart

msg['From'] = from_addr
msg['To'] = to_addr
msg['Subject'] = 'Subject of Email goes here...'
msg.attach(MIMEText(text))


server = smtplib.SMTP('smtp.gmail.com:587')       # sending request to server
server.ehlo()           #server object
server.starttls()              # used to send data between server and client
server.ehlo()
server.login(username,password)      # login id and password of gmail
server.sendmail(from_addr,to_addr,msg.as_string())            # Sending email
print('Done')        #Get the confirmation on command line
server.quit()
