#App Name Smart Vehicle Anti-theft system
#Version 0.0.1
#Project started at March 1/23
#Author Mohammed Kedir

from datetime import date
from flask import Flask, request
from twilio import twiml
import os
from twilio.rest import Client

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

security_enabled = True
vehicle_owner_phone_no = "+2519XXXXXXXXXX"
vehicle_alert_enabled = False
vehicle_movement_detected = False
latitude = 0
longitude = 0

app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    number = request.form['From']
    message_body = request.form['Body']

    if message_body == "E" and number == vehicle_owner_phone_no and security_enabled == False:
        security_enabled = True
        resp = twiml.Response()
        resp.message('Vehicle Security Enabled!'.format(number, message_body))
        resp.message('Hello {}, you said: {}'.format(number, message_body))
        return str(resp)
    
    elif message_body == "D" and number == vehicle_owner_phone_no and security_enabled == True:
        security_enabled = False
        resp = twiml.Response()
        resp.message('Vehicle Security Disabled!'.format(number, message_body))
        resp.message('Hello {}, you said: {}'.format(number, message_body))
        return str(resp)
    
    elif message_body == "S" and number == vehicle_owner_phone_no and security_enabled == True and vehicle_alert_enabled == True:
        # set vehicle alert state
        vehicle_alert_enabled = False

        # set vehicle movement detection status
        vehicle_movement_detected = False

        # get vehicle gps location
        latitude = get_vehicle_gps_location()[0]
        longitude = get_vehicle_gps_location()[1]

        # enable vehicle alert sound
        enable_vehicle_alert_sound()

        # send sms
        resp = twiml.Response()
        resp.message('Vehicle Stopped!!!\n Alert Sound Activated\n Vehicle GPS Location:-\n Latitude: {}\n Longitude {}'.format(latitude, longitude))
        return str(resp)
    


if __name__ == "__main__":
    app.run(debug=True)

def check_vehicle_movement():
    #detect vehicle movement using raspberry pi motion detecter module
    return True

def get_vehicle_gps_location():
    #get vehicle gps location using raspberry pi GPS module
    return [2.709658418882217, 54.336351294797055]

def enable_vehicle_alert_sound():
    #this function will enable vehicle alert sound
    return

def enable_vehicle_alert_sound():
    #this function will disable vehicle alert sound
    return

while True:
    vehicle_movement_detected = check_vehicle_movement()
    if vehicle_movement_detected == True and security_enabled == True:
        # set vehicle alert state
        vehicle_alert_enabled = True

        # get vehicle gps location
        latitude = get_vehicle_gps_location()[0]
        longitude = get_vehicle_gps_location()[1]

        # get current date
        today = date.today()

        # send alert SMS
        message = client.messages.create(
            body='Alert!!!\n Your vehicle is moving\n Date: {}\n Vehicle GPS Location:-\n Latitude: {}\n Longitude {}'.format(today, latitude, longitude),
            from_='+15017122661',
            to=vehicle_owner_phone_no
        )

        print(message.sid)
