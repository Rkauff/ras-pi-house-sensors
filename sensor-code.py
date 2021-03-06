import RPi.GPIO as GPIO
import dht11
import time
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# initialize GPIO
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)

# read data using pin 17
instance = dht11.DHT11(pin=17)
            
# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('//home//pi//House Sensor Data-c84f0eea71d2.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
sheet = client.open("House Sensor Data").sheet1

try:
    while True:
        
        if creds.access_token_expired:
            client.login()  # refreshes the token, because Google expires the token after 1 hour.
        result = instance.read()
        temp_in_f = str((result.temperature * 9/5) + 32)
        humidity = str(result.humidity)
        date_and_time = str(datetime.datetime.now())
        
        if result.is_valid():
            print("Last valid input: " + str(datetime.datetime.now()))
            print("Temperature (F): " + temp_in_f)
            print("Humidity: " + humidity)

            row_count = sheet.get_all_values()
            last_row = len(row_count)
        
            sheet.update_cell(last_row + 1, 1, date_and_time)
            sheet.update_cell(last_row + 1 ,2, temp_in_f)
            sheet.update_cell(last_row + 1 ,3, humidity)
            sheet.update_cell(last_row + 1 ,4, "Basement")
        
        time.sleep(60)

except KeyboardInterrupt:
    print("Cleanup")
    GPIO.cleanup()
