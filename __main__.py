import requests
import js2py

BATTERY = {
    "url": "http://hostname/cgi/ems_data.js",
    "name": "TheBattery"
}

INFLUX = {
    "url": "https://hostname:8086/write?db=databasename",
    "username":"leuser",
    "password":"lepassword"
}

response = requests.get(BATTERY['url'])

# State of Charge
soc = """
var sum = 0;
var chargerCount = 2;

for (var i = 0; i < chargerCount; i++) {
    if (typeof Charger_Data[i] == "undefined") {
      continue;
    }

    sum += Charger_Data[i][2]; 
}
Math.round(sum/chargerCount);
"""

ems_data = response.text
battery_percent_full = js2py.eval_js(ems_data + soc)
print(f"procent full: {battery_percent_full}")

gridpower = """
WR_U_VERBUND_L1_INDEX = 5;
WR_U_VERBUND_L2_INDEX = 6;
WR_U_VERBUND_L3_INDEX = 7;
WR_I_VERBUND_L1_INDEX = 8;
WR_I_VERBUND_L2_INDEX = 9;
WR_I_VERBUND_L3_INDEX = 10;
Math.round((
        WR_Data[WR_U_VERBUND_L1_INDEX] * WR_Data[WR_I_VERBUND_L1_INDEX]
      + WR_Data[WR_U_VERBUND_L2_INDEX] * WR_Data[WR_I_VERBUND_L2_INDEX]
      + WR_Data[WR_U_VERBUND_L3_INDEX] * WR_Data[WR_I_VERBUND_L3_INDEX]
      ) / 100);
"""

power_grid = js2py.eval_js(ems_data + gridpower)
print(f"watts from/to grid: {power_grid}")

batteriepower = """
WR_U_INSEL_L1_INDEX = 11;
WR_U_INSEL_L2_INDEX = 12;
WR_U_INSEL_L3_INDEX = 13;
WR_I_INSEL_L1_INDEX = 14;
WR_I_INSEL_L2_INDEX = 15;
WR_I_INSEL_L3_INDEX = 16;
Math.round((
        WR_Data[WR_U_INSEL_L1_INDEX] * WR_Data[WR_I_INSEL_L1_INDEX]
      + WR_Data[WR_U_INSEL_L2_INDEX] * WR_Data[WR_I_INSEL_L2_INDEX]
      + WR_Data[WR_U_INSEL_L3_INDEX] * WR_Data[WR_I_INSEL_L3_INDEX]
      ) / 100);
"""

power_batterie = js2py.eval_js(ems_data + batteriepower)
print(f"watts from/to battrie: {power_batterie}")

productionpower = """
WR_PMB_INDEX = 39;
Math.round(WR_Data[WR_PMB_INDEX])
"""

power_production = js2py.eval_js(ems_data + productionpower)
print(f"watts production: {power_production}")

def calulate_power_usage():
    if power_production <= 0:
        if power_grid <= 0 and power_batterie <= 0:
            return abs(power_grid + power_batterie)
        else:
            return 0
    else:
        if grid > 0:
            return power_production - power_grid - power_batterie
        else:
            return power_production - power_batterie + abs(power_grid)

# calculate power usage
power_usage = calulate_power_usage()
print(f"watts usage: {power_usage}")

data = "battery,name={} percentfull={}i,grid={}i,battery={}i,production={}i,usage={}i".format(
    BATTERY['name'],
    battery_percent_full,
    power_grid,
    power_batterie,
    power_production,
    power_usage
)

r = requests.post(INFLUX["url"], data=data, auth=(INFLUX["username"], INFLUX["password"])

print(data)
print(r.text)
