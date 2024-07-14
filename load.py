import requests
import re
import json
import os
from os.path import dirname, abspath
d = dirname(abspath(__file__))

f = open("config.json")
j = json.load(f)

user = os.environ.get('USER')
os.system("crontab -r")
os.remove("crontab")
f = open("crontab", "w")
hosts = j['hosts'].keys()
for h in hosts:
    for o in j['hosts'][h]['outlets']:
        outlet = o['id']
        starttime = o['on_time']
        stoptime = o['off_time']

        f.write(f"{starttime % 100} {starttime // 100} * * * {user} ./etc/profile; python3 {d}/np-05b.py --host={h} --outlet={outlet} --onoff=1\n\n")
        f.write(f"{stoptime % 100} {stoptime // 100} * * * {user} ./etc/profile; python3 {d}/np-05b.py --host={h} --outlet={outlet} --onoff=0\n\n")

f.close()
os.system("crontab ./crontab")
os.system("crontab -l")
