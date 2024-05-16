# SPDX-FileCopyrightText: 2020 Brent Rubell for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import ipaddress
import ssl
import wifi
import socketpool
import adafruit_requests

# URLs to fetch from
POACHOMETER_URL = "https://nerdymark.com/poachometer.json"

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

wifi.radio.connect(secrets["ssid"], secrets["password"])
pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())

response = requests.get(POACHOMETER_URL)

# Parse JSON
# [{"benefits":"executive package (full plus equity and bonus)","location":"Downtown San Jose","name":"Mark","salary":"$500,000 USD per year","term":"2 year minimum","title":"Universal Solvent (Software Engineer)"}]
poachometer = response.json()

# Print the poachometer - Screen is only 40 characters wide
print("Poachometer:")
for poach in poachometer:
    print("Name:", poach["name"])
    print("Title:", poach["title"])
    print("Location:", poach["location"])
    print("Salary:", poach["salary"])
    print("Benefits:", poach["benefits"][:36] + "...")  # Truncate benefits
