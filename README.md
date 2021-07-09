Varta battery info to influx
============================

Replace this config in `__main__.py` with the correct values.

```
BATTERY = {
    "url": "http://hostname/cgi/ems_data.xml",
    "name": "TheBattery"
}

INFLUX = {
    "url": "https://hostname:8086/write?db=databasename", 
    "username":"leuser", 
    "password":"lepassword"
}
```

Parsing state of charge as percentage and state of the battery and post it to influx.
See [docs]( https://www.loxwiki.eu/pages/viewpage.action?pageId=39354750 ).
