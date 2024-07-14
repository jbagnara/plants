import requests
import re
import argparse
import json

from requests.auth import HTTPBasicAuth
from os.path import dirname, abspath
d = dirname(abspath(__file__))

parser = argparse.ArgumentParser()
parser.add_argument('--host')
parser.add_argument('--outlet')
parser.add_argument('--onoff')
args = parser.parse_args()

host = args.host
outlet = args.outlet
onoff = args.onoff

f = open(f"{d}/config.json")
j = json.load(f)

user = j['hosts'][host]['user']
passwd = j['hosts'][host]['passwd']

with requests.sessions.Session() as session:
    session.auth = (user, passwd)
    
    r = session.get(f"http://{host}")
    r.raise_for_status()

    r = session.get(f"http://{host}/status.xml")
    r.raise_for_status()
    pattern = re.compile(r'<rly%s>(1|0)</rly%s>'%(outlet,outlet))
    status = pattern.search(r.text).group()[6:7]

    if onoff != status:
        r = session.get(f"http://{host}/cmd.cgi?rly={outlet}")
        r.raise_for_status()

    f.close()
    print("Success!")
