run_access_point()


#ssid = "Forrest"
#password = "00golenRetriever09"
#print("Connecting to wifi...")
#counter=0
## Activate the station interface
#sta_if = network.WLAN(network.STA_IF)
#sta_if.active(True)
## Connect to your wifi network
#sta_if.connect(ssid, password)
#if counter > 15:
#    sys.exit(1) 
#while not sta_if.isconnected():
#    counter += 1
## Print out the network configuration received from DHCP
#
#print('network config:', sta_if.ifconfig())