import httplib
import urllib
from json import dumps

class Importer:

    def __init__(self):
        self.conn = httplib.HTTPConnection('localhost', 9200)
        self.conn.connect()

    def commit(self, commit):
        json = dumps(commit, indent=2)
        headers = {
            "Content-type": "application/json"
        }
        path = 'git/commits/' + commit['hash']
        self.conn.request("PUT", path, json, headers)
        resp = self.conn.getresponse()
        resp.read()
