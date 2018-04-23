#!/usr/bin/env python3.6
from requests import get
from difflib import unified_diff as get_difference
from email.mime.text import MIMEText as MailMessage
from subprocess import run
from datetime import datetime
import os
from sys import argv

actual_hosts = """127.0.0.1	bonkomputilo\n\
45.79.149.122	mad-node\n\
168.235.103.80	production\n\
168.235.81.117	ramnode-dev\n\
104.131.66.158	deb9-NY-DigitalOcean"""

url = "http://someonewhocares.org/hosts/hosts"

response = get(url)
new_hosts = response.content.decode()

if "--apply" in argv:
    with open("/etc/hosts", 'w') as hf:
        hf.write(new_hosts)
        hf.write(actual_hosts)
    exit(0)

old_hostsfile = open("/etc/hosts")

diff = get_difference(
    str(old_hostsfile.read()).split('\n'),
    new_hosts.split('\n'),
    fromfile="/etc/hosts",
    tofile=url,
    fromfiledate=datetime.isoformat(datetime.fromtimestamp(os.stat('/etc/hosts').st_mtime)),
    tofiledate=response.headers['Date']
)
old_hostsfile.close()
diffstr = ''
for line in diff:
    diffstr += line + '\n'

if diff:
    print(diffstr)
