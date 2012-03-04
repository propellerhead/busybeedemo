import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template

import urllib2
from google.appengine.api import urlfetch

from django.utils import simplejson

import logging
    
class ApiHandler(webapp.RequestHandler):
  def get_page_name(self, path):
    pagename = None
    if len(path) > 2:
      pagename = path[2].lower()
    return pagename
    
  def get_action(self, path):
    action = None
    if len(path) > 3:
      action = path[3].lower()
    return action
    
  def get(self):
    path = self.request.path.split('/')
    page_name = self.get_page_name(path)
    action = self.get_action(path)
    result = False

    if page_name == 'checkname':
      name = self.request.get('url')
      
      try:
        validate = urllib2.urlopen('http://static.busybeehq.com/api/json?method=busybee.account.checkname&name=' + name)
        validate_json = validate.read()
      
        json = simplejson.loads(validate_json)
        if json['code'] == '200':
          result = True
      except urlfetch.Error, e:
        logging.error('Could not contact BusyBee HQ Server.')
        #TODO: Handle error.
    
    self.response.headers["Content-Type"] = "application/json"
    self.response.out.write(str(result).lower())

def main():
  application = webapp.WSGIApplication([('/api/.*', ApiHandler)], debug=True)
  util.run_wsgi_app(application)
    
if __name__ == '__main__':
  main()
