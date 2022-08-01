import re

from yaml import parse
result = {}
shared = {}
teststring= '''-
port xdsl-line:1/1/2/1
  admin-up
  link-updown-trap
  user kuehnemund
  no severity # value=default
  no port-type # value=uni
exit
port xdsl-line:1/1/2/2
  no admin-up
  no link-updown-trap
  no user # value=available
  no severity # value=default
  no port-type # value=uni
'''

for line in teststring.splitlines():
    cap = re.match(re.compile(r'''\s+(?P<negate> no)?\s+(user\s(?P<user>[a-zA-Z0-9_]*))''', re.VERBOSE,), line)
    if cap:
        capdict = cap.groupdict()
        capdict = dict(
            (k, v) for k, v in capdict.items() if v is not None
        )