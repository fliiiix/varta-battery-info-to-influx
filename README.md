Varta battery info to influx
============================

Replace this config in `__main__.py` with the correct values.

```
BATTERY = {
    "url": "http://hostname/cgi/ems_data.js",
    "name": "TheBattery"
}

INFLUX = {
    "url": "https://hostname:8086/write?db=databasename", 
    "username":"leuser", 
    "password":"lepassword"
}
```
