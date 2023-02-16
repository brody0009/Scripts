import requests
import json
from prettytable import PrettyTable

phone_counter = 0
# Set api key. The below api key is for the Meraki Sandbox
# Replace it with your API key
api_key = 'type_api_here_key'

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
r = requests.get('https://n17.meraki.com/api/v1/organizations/708753991357431888/networks',verify = False, headers={'X-Cisco-Meraki-API-Key': api_key})

networks= json.loads(r.text)
table = PrettyTable(['Mac-address','IP','Manufacture','Switch','Port','Vlan','Status' ])
#table.padding_width = 1()
for network in networks:
    devices = requests.get('https://n259.meraki.com/api/v1/networks/'+network["id"]+'/clients', headers={'X-Cisco-Meraki-API-Key': api_key})
    device_response = json.loads(devices.text)
    #print(device_response)
    for endpoint in device_response:
        if "48:9e:bd" in endpoint['mac']:
            #print(endpoint['mac'],endpoint['manufacturer'], endpoint['recentDeviceName'],endpoint['switchport'])
            table.add_row([endpoint['mac'],endpoint['ip'],endpoint['manufacturer'], endpoint['recentDeviceName'],endpoint['switchport'],endpoint['vlan'],endpoint['status']])
            phone_counter = phone_counter +1
print(table)    
with open('meraki_report_device.csv', 'a', newline='') as f_output:
 f_output.write(table.get_csv_string())
print("Number of IP phones found : "+ str(phone_counter))


    ##https://developer.cisco.com/codeexchange/github/repo/meraki/automation-scripts/
    #deploydevices.py
    #deploydevices.py: This script claims multiple devices and licenses into an organization, 
    #creates a new network for them and binds that network to an existing template. Initial config, 
    #including hostnames and street address/map markers are set for the devices. 
    #Will set network timezone to match street address if provided with a Google Maps API key.