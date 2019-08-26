import paho.mqtt.client as mqttClient
import time
import base64
import python_cayennelpp.decoder
import json


def on_connect(client, userdata, flags, rc):
	if rc == 0:
		print("Connected to broker")
		global Connected #Use global variable
		Connected = True #Signal connection
	else:
		print("Connection failed")
 
def on_message(client, userdata, message):
	print "Message received: "  + message.payload
	message = str(message.payload.decode('utf-8'))[1:-1]
	try:
		message = json.loads(message)
		payload = message["payload"]
		deveui = message["deveui"]
		dev_payload_decoded_base64 = base64.b64decode(payload).encode('hex')
		dev_payload_decoded_lpp = python_cayennelpp.decoder.decode(dev_payload_decoded_base64)
		print "dev_payload_decoded_lpp: " + str(dev_payload_decoded_lpp)
		value = dev_payload_decoded_lpp[0]["value"]
		url = "machineq/" + str(deveui)
		ret = client.publish(url, value)

		#check for temperature reading
		try:
			value = dev_payload_decoded_lpp[1]["value"]
			url += "/temperature"
			ret = client.publish(url, value)
		except KeyError:
			pass

	except Exception as e:
		print "error: " + str(e)
 
Connected = False #global variable for the state of the connection
 
broker_address= "localhost" #Broker address
port = 1883 #Broker port
 
client = mqttClient.Client("Python")	   #create new instance
client.on_connect= on_connect #attach function to callback
client.on_message= on_message #attach function to callback
 
client.connect(broker_address, port=port) #connect to broker
 
client.loop_start()	#start the loop
 
while Connected != True: #Wait for connection
	time.sleep(0.1)
 
client.subscribe("machineq/payload")
 
try:
	while True:
		time.sleep(1)

except KeyboardInterrupt:
	print "exiting"
	client.disconnect()
	client.loop_stop()
