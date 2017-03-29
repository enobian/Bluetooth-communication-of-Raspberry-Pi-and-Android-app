import os
import glob
import time
import RPi.GPIO as GPIO
from bluetooth import *

#SETUP GPIO LAYOUT
GPIO.setmode(GPIO.BOARD)

#SETUP PINS
GPIO.setup(11, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(13, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(15, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(16, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(18, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(22, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(29, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(31, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

b1=b2=b3=b4=b5=b6=b7=b8=0
x=1
wait = 0.001

connection = False
server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service( server_sock, "VoltMeterPiServer",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ] 
#                   protocols = [ OBEX_UUID ] 
                    )
while True:           
	if(connection == False):
		print("Waiting for connection on RFCOMM channel %d" % port)
		client_sock, client_info = server_sock.accept()
		connection = True
		print("Accepted connection from ", client_info)
	try:
        	data = client_sock.recv(1024)
       		if (data == "disconnect"):
			print("Client wanted to disconnect")
			client_sock.close()
			connection = False
		elif (data == "voltage"):
			if (GPIO.input(11) == True):
				time.sleep(wait)
				if (GPIO.input(11) == True):
					b1 = 1
			else:
				b1 = 0
			if (GPIO.input(13) == True):
				time.sleep(wait)
				if (GPIO.input(13) == True):
					b2 = 1
			else:
				b2 = 0
			if (GPIO.input(15) == True):
				time.sleep(wait)
				if (GPIO.input(15) == True):
					b3 = 1
			else:
				b3 = 0
			if (GPIO.input(16) == True):
				time.sleep(wait)
				if (GPIO.input(16) == True):
					b4 = 1
			else:
				b4 = 0
			if (GPIO.input(18) == True):
				time.sleep(wait)
				if (GPIO.input(18) == True):
					b5 = 1
			else:
				b5 = 0
			if (GPIO.input(22) == True):
				time.sleep(wait)
				if (GPIO.input(22) == True):
					b6 = 1
			else:
				b6 = 0
			if (GPIO.input(29) == True):
				time.sleep(wait)
				if (GPIO.input(29) == True):
					b7 = 1
			else:
				b7 = 0
			if (GPIO.input(31) == True):
				time.sleep(wait)
				if (GPIO.input(31) == True):
					b8 = 1
			else:
				b8 = 0
			val = (1*b1)+(2*b2)
			val = val+(4*b3)+(8*b4)
			val = val+(16*b5)+(32*b6)
			val = val+(64*b7)+(128*b8)
			vol = float(val)/255 * 5
			print "ADC value (8bit): " + str(val)
			print "Voltage: " + str(round(vol,2))
			client_sock.send("%s" % round(vol,2))
			print ("SENT: %s" % round(vol,2))
        	else:
			print("RECEIVED: %s" % data)
			client_sock.send("%s" % data)
			print("SENT: %s" % data) 
	except IOError:
    		print("Connection disconnected!")
		client_sock.close()
		connection = False
		pass
	except BluetoothError:
		print("Something wrong with bluetooth")
	except KeyboardInterrupt:
		print("\nDisconnected")
		client_sock.close()
		server_sock.close()
		break

