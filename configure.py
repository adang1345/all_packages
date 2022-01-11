"""Generate README.md."""

import urllib.request
import re
import datetime

html = urllib.request.urlopen('https://pypi.org/simple/').read().decode('utf-8')
num_packages = sum(1 for _ in re.finditer(r'>([^<]+)</a>', html))
now = datetime.datetime.utcnow()
with open('README.md', 'w') as file, open('README.md.txt') as file2:
    s = file2.read()
    file.write(s.format(num_packages, now.strftime('%d %b %Y')))
