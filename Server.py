import RPi.GPIO as GPIO
import os
import time
from time import sleep
from http.server import BaseHTTPRequestHandler, HTTPServer
import socket

ip_add = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] 
if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), 
s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, 
socket.SOCK_DGRAM)]][0][1]]) if l][0][0]

host_name = ip_add
host_port = 8000

class MyServer(BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _redirect(self, path):
        self.send_response(303)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', path)
        self.end_headers()

    def do_GET(self):
        html = '''
           <html>
           <body style="width:960px; margin: 20px auto;background-color:powderblue;">>
           <img style="display: block;-webkit-user-select: none;margin: auto;background-color: hsl(0, 0%, 25%);" src="http://{}:8081/0/stream" alt="Camera Footage">
           <h1>ViLoCaD</h1>
           <p>Welcome to Door Lock Setup :</p>
           <form action="/" method="POST">
               Door :
               <input type="submit" name="submit" value="Lock">
               <input type="submit" name="submit" value="Unlock">
           </form>
           <p>(C) Home Automation Team : Minor Project Under Guidance of Dr. Arun Parakh
           </p>
           </body>
           </html>
        '''
        f = open("Pressed.txt", "r")
        temp = f.read()
        self.do_HEAD()
        self.wfile.write(html.format(ip_add).encode("utf-8"))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) 
        post_data = self.rfile.read(content_length).decode("utf-8") 
        post_data = post_data.split("=")[1] 

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(18, GPIO.OUT)

        if post_data == 'Lock':
            GPIO.output(18, GPIO.HIGH)
        else:
            GPIO.output(18, GPIO.LOW)
        print("Door is {}".format(post_data))
        self._redirect('/') 


if __name__ == '__main__':
    http_server = HTTPServer((host_name, host_port), MyServer)
    print("Server Starts - %s:%s" % (host_name, host_port))
    
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()