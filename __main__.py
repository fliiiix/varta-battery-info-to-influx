import requests
import xml.etree.ElementTree as ET

BATTERY = {
    "url": "http://hostname/cgi/ems_data.xml",
    "name": "TheBattery"
}

INFLUX = {
    "url": "https://hostname:8086/write?db=databasename",
    "username":"leuser",
    "password":"lepassword"
}

response = requests.get(BATTERY['url'])
root = ET.fromstring(response.text)
print(f"response: {response.text}")

# State of Charge
battery_percent_full = root.find(".//var[@name='SOC']").attrib["value"]
print(f"procent full: {battery_percent_full}")

# State
battery_state = root.find(".//var[@name='State']").attrib["value"]
print(f"State: {battery_state}")


data = "battery,name={} percentfull={}i,state={}i".format(
    BATTERY['name'],
    battery_percent_full,
    battery_state
)

r = requests.post(INFLUX["url"], data=data, auth=(INFLUX["username"], INFLUX["password"]))

print(data)
print(r.text)
