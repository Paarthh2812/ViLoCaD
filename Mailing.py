import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import socket
import time

time.sleep(30)
ip_add = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] 
if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), 
s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, 
socket.SOCK_DGRAM)]][0][1]]) if l][0][0] # Retreiving IP Address of Machine

email_user = "-Send-EmailID-" # Email Id, configured for STMP Mailing Service
email_password = "--Your-Password--" # App Password, to be setup by STMP Service
email_send = "-Recieve-EmailID-" # Mail Id to Send the Mail

subject = "URL to Connect to ViLoCaD" # Mail Subject

msg = MIMEMultipart()
msg["From"] = email_user
msg["To"] = email_send
msg["Subject"] = subject

body = f"""Hi User, We are delighted to welcome you to our ViLoCaD 
- Video Lock Camera Door Utility \n Just Open any browser on the Network, 
your Raspberry is Connected and Type the below URL \n {ip_add}:8000 """
msg.attach(MIMEText(body,"plain"))

text = msg.as_string()
server = smtplib.SMTP("smtp.gmail.com",587)
server.starttls()
server.login(email_user,email_password)


server.sendmail(email_user,email_send,text)
server.quit()
