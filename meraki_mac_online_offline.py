import requests
import json
from prettytable import PrettyTable
import urllib3
from json import dumps
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import time

# Set api key. The below api key is for the Meraki Sandbox
# Replace it with your API key
api_key = 'type_api_key'

# Set header parameters
headers = {
   "X-Cisco-Meraki-API-Key" : api_key
}

url = "https://dashboard.meraki.com/api/v0/organizations" 

# Send request and get response
response = requests.request(
   "GET", 
   url,
   headers=headers
)
org_id = requests.get('https://dashboard.meraki.com/api/v0/organizations',verify = False, headers={'X-Cisco-Meraki-API-Key': api_key})
print(org_id.content)

table = PrettyTable(['Mac-address','Status'])
macaddress= open("macaddress.txt", "r")
for macs in macaddress:
    time.sleep(2)
    macs=str(macs).replace("\n","")
    url ='https://api.meraki.com/api/v1/organizations/type_org_id/clients/search?mac='+str(macs)
    devices = requests.get('https://api.meraki.com/api/v1/organizations/type_org_id/clients/search?mac='+str(macs), headers={'X-Cisco-Meraki-API-Key': api_key})
    code = str(devices.status_code)
    print(code)
    if code == "200":
     device_response = devices.json()
     converted = dumps(device_response)
     devices = device_response.get('Online')
     status_device = str(devices)

     if "Online" in converted:
        table.add_row([macs,"Online"])
     if "ffline" in converted:
        table.add_row([macs,"0ffline-But-seen-On-Meraki"])
    if code == "204":
     table.add_row([macs,"Offline-No-Ever-Seen-In-Meraki"])
print(table)    
with open('meraki_phone_status_seen_no_seen.csv', 'a', newline='') as f_output:
 f_output.write(table.get_csv_string())