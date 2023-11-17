json_data = {
    "hosts": [
        {
            "id": "00:00:00:00:00:02/None",
            "mac": "00:00:00:00:00:02",
            "vlan": "None",
            "innerVlan": "None",
            "outerTpid": "unknown",
            "configured": False,
            "ipAddresses": ["10.0.0.2"],
            "locations": [{"elementId": "of:0000000000000001", "port": "2"}],
        },
        {
            "id": "00:00:00:00:00:03/None",
            "mac": "00:00:00:00:00:03",
            "vlan": "None",
            "innerVlan": "None",
            "outerTpid": "unknown",
            "configured": False,
            "ipAddresses": ["10.0.0.3"],
            "locations": [{"elementId": "of:0000000000000003", "port": "1"}],
        },
        {
            "id": "00:00:00:00:00:01/None",
            "mac": "00:00:00:00:00:01",
            "vlan": "None",
            "innerVlan": "None",
            "outerTpid": "unknown",
            "configured": False,
            "ipAddresses": ["10.0.0.1"],
            "locations": [{"elementId": "of:0000000000000001", "port": "1"}],
        },
        {
            "id": "00:00:00:00:00:04/None",
            "mac": "00:00:00:00:00:04",
            "vlan": "None",
            "innerVlan": "None",
            "outerTpid": "unknown",
            "configured": False,
            "ipAddresses": ["10.0.0.4"],
            "locations": [{"elementId": "of:0000000000000004", "port": "1"}],
        },
    ]
}

hosts_lists = {}

for host in json_data["hosts"]:
    ip_address = host["ipAddresses"][0]
    element_id = host["locations"][0]["elementId"]
    port = host["locations"][0]["port"]

    hosts_lists[ip_address] = {
        "flag": "0",
        "elementId": element_id,
        "port": port,
    }

for ip_address, host_info in hosts_lists.items():
    element_id = host_info["elementId"]
    print(ip_address)
    print(element_id)
