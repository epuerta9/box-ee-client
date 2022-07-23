from machine import Pin, reset
import time
import socket
from wireless.html import home_html, submitted_html
from lib.repo import Repo

def save_api_key(key):
  repo = Repo()
  repo.add

def web_page():
  try:
    import usocket as socket
  except:
    import socket

  import network

  import esp
  esp.osdebug(None)

  import gc
  gc.collect()

  ssid = 'MicroPython-AP'
  password = '123456789'

  ap = network.WLAN(network.AP_IF)
  ap.active(True)
  ap.config(essid=ssid, password=password)

  while ap.active() == False:
    pass

  print('Connection successful')
  print(ap.ifconfig())

  led = Pin(14, Pin.OUT)
  if led.value() == 1:
    gpio_state="ON"
  else:
    gpio_state="OFF"

  html = """<html><head> <title>ESP Web Server</title> <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,"> <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
  h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #e7bd3b; border: none; 
  border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
  .button2{background-color: #4286f4;}</style></head><body> <h1>ESP Web Server</h1> 
  <p>GPIO state: <strong>""" + gpio_state + """</strong></p><p><a href="/?led=on"><button class="button">ON</button></a></p>
  <p><a href="/?led=off"><button class="button button2">OFF</button></a></p></body></html>"""
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  s.bind(('', 80))
  s.listen(5)

  while True:
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    request = request.decode()
    print('Content = %s' % request)
    #checking for length of request.
    #sometimes browsers fire off multiple requests and index out of range becomes an issue with the following line
    if not request:
      conn.close()
      break
    else:
      fields = request.split("\r\n")
      fields = fields[1:] #ignore the GET / HTTP/1.1
      output = {}
      if "ssid" in fields[-1]:
        print(fields[-1].split("&"))
        field_list = fields[-1].split('&')
        for field in field_list:
          key,value = field.split("=")
          output[key] = value 
    
        print(output)
        

        response = submitted_html
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()
        gc.collect()

        if len(list(output.keys())) >= 1:
          print('LED ON')
          led.value(1)
          time.sleep(3)
          led.value(0)       
        break
    
    response = home_html

    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()
    gc.collect()

  reset()

