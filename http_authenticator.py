#!/usr/bin/env python
import httplib
import re
import urllib,sys,getpass

if len(sys.argv) == 1:
    print 'program name [login/logout/keepalive] [username] (if login)'
    sys.exit()

if sys.argv[1] == 'keepalive':
    req = httplib.HTTPConnection('172.16.1.1', 1000)
    req.request('GET', '/keepalive?0000000000000000000')
    data = req.getresponse().read()
    if len(re.findall(r'logout', data)):
        print 'Timer restarted '
    else:
        print 'Error restarting timer'
    sys.exit()

if sys.argv[1] == 'logout':
    req = httplib.HTTPConnection('172.16.1.1', 1000)
    req.request('GET', '/logout?')
    data = req.getresponse().read()
    if len(re.findall(r'successfully',data)):
        print 'Logged out successfully'
    else :
        print 'Error logging out'
    sys.exit()

if sys.argv[1] == 'login' and len(sys.argv) == 4 :
    req = httplib.HTTPConnection('172.16.1.1', 1000)
    req.request('GET', '/login?')
    data = req.getresponse()
    real = data.read()
    magic = re.findall(r'magic" value="(\w+)"', real)[0]

    user = sys.argv[2]
    password = sys.argv[3]
    #password = getpass.getpass()

    params = urllib.urlencode(
        {'4Tredir': 'http%3A%2F%2Fnitdelhi.ac.in%2F', 'magic': magic, 'username': user, 'password': password})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    req.request("POST", "/", params, headers)
    data = req.getresponse().read()
    if len(re.findall(r'logout',data)):
        print 'Logged IN succesfully'
    else :
        print 'Error logging IN'
    sys.exit()

else:
    print 'program name [login/logout/keepalive] [username] (if login)'
    sys.exit()

