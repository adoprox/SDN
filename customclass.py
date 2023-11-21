import os
import requests
import json
from requests.auth import HTTPBasicAuth
import random


class ONOS:
    username = "onos"
    password = "rocks"
    onos_url = "http://localhost:8181/onos/v1/"

    # Fetches data using GET request based on provided key
    def getmethod(self, key):
        getpath = os.path.join(self.onos_url, key)
        response = requests.get(getpath, auth=(self.username, self.password))
        json_data = response.json()
        result = {}

        if key == "hosts":
            # Extracts host information and stores it in a dictionary
            for host in json_data["hosts"]:
                ip_address = host["ipAddresses"][0]
                element_id = host["locations"][0]["elementId"]
                port = host["locations"][0]["port"]
                result[ip_address] = {
                    "flag": "0",
                    "elementId": element_id,
                    "port": port,
                }
        if key == "devices":
            # Extracts device IDs and stores them in a list
            result = [device["id"] for device in json_data.get("devices", [])]

        return result

    # Sends POST request to add flow rules
    def postmethod(self, deviceID, postdata):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        appnum = random.randint(1, 1000)
        appID = "?appID=00" + str(appnum)
        setting = "flows/"
        flows_id = deviceID + appID
        getpath = os.path.join(self.onos_url, setting, flows_id)
        response = requests.post(getpath, data=json.dumps(postdata), headers=headers, auth=(self.username, self.password))
        return response

    # Deletes specific flows based on device ID and login ID
    def autodeletmethod(self, key, device_ID, loginID):
        device_ID = device_ID.replace('of:', 'of%3A')
        getpath = os.path.join(self.onos_url, key, device_ID)
        response = requests.get(getpath, auth=(self.username, self.password))

        loginID = loginID + "/32"
        json_data = response.json()

        # Filters flow IDs based on specific criteria
        filtered_flow_ids = [
            entry['id'] for entry in json_data.get("flows", [])
            if entry.get("appId") == "org.onosproject.rest"
            and any(
                criterion.get("type") == "IPV4_SRC" and criterion.get("ip") == loginID
                for criterion in entry.get("selector", {}).get("criteria", [])
            )
            and any(
                instruction.get("type") == "NOACTION"
                for instruction in entry.get("treatment", {}).get("instructions", [])
            )
        ]

        headers = {
            'Accept': 'application/json'
        }
        
        # Deletes flows with specified flow IDs
        for flow_id in filtered_flow_ids:
            url = os.path.join(getpath, flow_id)
            response = requests.delete(url, headers=headers, auth=("onos", "rocks"))
        
        return response
