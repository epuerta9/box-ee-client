from machine import Pin, reset
import time
from wireless.html import home_html, submitted_html
from lib.repo import Repo

def save_credentials(ssid, password, key):
  repo = Repo()
  repo.add(ssid=ssid, password=password, device_api_key=key)
  repo.flush()
  repo.close()


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
          print("saving credentials...")
          save_credentials(output['ssid'], output['password'], output['device-key'])
        break
    
    response = home_html

    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()
    gc.collect()

  reset()

