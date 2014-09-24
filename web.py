#!/usr/bin/env python
import SocketServer
import SimpleHTTPServer
import os
import time
import urllib2
import json
import wink

w = wink.init()


def send_html(self,content):
  self.send_response(200)
  self.send_header('Content-type','text/html')
  self.end_headers()
  self.wfile.write(content)
def send_json(self, content):
  self.send_response(200)
  self.send_header('Content-type','text/json')
  self.end_headers()
  self.wfile.write(json.dumps(content))
def send_all(self, content):
  self.send_response(200)
  self.send_header('Content-type','text/jsonp')
  self.end_headers()
  self.wfile.write(content)


class CustomHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        pass_server=str(self.headers.get('Host').partition(":")[0])
        if self.path=='/robots.json':
            #send_html(self,str(w.get_robots()).replace('"','""').replace("'",'"').replace('u":','u::').replace('u"','"').replace("u::",'u":').replace(": True,",":true,").replace(": False,",":false,").replace(': None',':""'))
            send_json(self, w.get_robots())
        elif self.path=='/scenes.json':
            send_json(self,w.get_scenes())
        elif self.path=='/profile.json':
            send_json(self,w.get_profile())
        elif self.path=='/devices.json':
            send_json(self,w.get_devices())
        elif self.path=='/services.json':
            send_json(self,w.get_services())
        elif self.path=='/icons.json':
            send_json(self,w.get_icons())
        elif self.path=='/channels.json':
            send_json(self,w.get_channels())
        elif self.path.startswith('/all.json'):
            send_all(self,"var smarts=[]; smarts['channels']="+str(json.dumps(w.get_channels()))+"; smarts['icons']="+str(json.dumps(w.get_icons()))+"; smarts['robots']="+str(json.dumps(w.get_robots()))+"; smarts['profile']="+str(json.dumps(w.get_profile()))+"; smarts['devices']="+str(json.dumps(w.get_devices()))+"; smarts['services']="+str(json.dumps(w.get_services()))+"; smarts['scenes']="+str(json.dumps(w.get_scenes()))+";")
        else:
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

PORT = 1024

SocketServer.ThreadingTCPServer.allow_reuse_address = True
httpd = SocketServer.ThreadingTCPServer(('0.0.0.0', PORT),CustomHandler)

print "serving at port", PORT
httpd.serve_forever()
#httpd.handle_request()
    

