import os 
import requests
import json
from requests.auth import HTTPBasicAuth
import random

class ONOS:
    username = "onos"
    password = "rocks"
    onos_url = "http://localhost:8181/onos/v1/"
    
    def getmethod(self, key):
        getpath = os.path.join(self.onos_url, key)
        response = requests.get(getpath, auth=(self.username, self.password))
        json_data = response.json()
        list = {}
        if(key=="hosts"):
            for host in json_data["hosts"]:
                ip_address = host["ipAddresses"][0]
                element_id = host["locations"][0]["elementId"]
                port = host["locations"][0]["port"]
                list[ip_address] = {
                "flag": "0",
                "elementId":element_id,
                "port":port,}
        if(key=="devices"):
            # Extract the "id" value for each device
            device_ids = [device["id"] for device in json_data.get("devices", [])]

            # Print the resulting array
            print(device_ids)

            #json request for devices. 
            return 0

        return list

    def postmethod(self,deviceID,data):

        headers = {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
        }
        appnum = random.randint(1,1000)
        #used to manage JSON Files 
        appID = "?appID=00"+str(appnum)
        setting = "flows/"
        getpath = os.path.join(self.onos_url,setting,deviceID,appID)
        response = requests.post(getpath, json=data, headers=headers, auth=(self.username, self.password))
        return response




"""In summary, this JSON structure defines a flow entry with a specific priority, timeout, and match criteria. 
It directs packets with an Ethernet type of "0x88cc" arriving at the device with ID "of:0000000000000001" to be sent out to the controller port ("CONTROLLER").
 This rule remains active indefinitely (isPermanent is true) until explicitly removed."""