__author__ = 'Vadim Melnyk'
import urllib
import json
from pprint import pprint
import random
import string

def random_name(y):
    return ''.join(random.choice(string.ascii_lowercase) for x in range(y))


class Yourls():
    hostname = ''
    signature = ''
    def __init__(self, hostname, signature):
        if hostname[7::] != 'http://':
            self.hostname = 'http://' + hostname
            # print self.hostname
        else:
            self.hostname = hostname
        self.signature = signature

    def shorten_link(self, link, name):
        url_request = self.hostname + '/yourls-api.php?signature='+self.signature+'&action=shorturl&url=' + link
        url_request += '&keyword=' + random_name(5) + '&title=' + name + '&format=json'
        json_request = urllib.urlopen(url_request)
        print url_request
        data = json.loads(json_request.read())
        # pprint(data)
        # print data['shorturl']
        # print data['status']
        if data['status'] == 'success':
            return data['shorturl']
        else:
            return data['status']
