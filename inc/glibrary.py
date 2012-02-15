#!/usr/bin/env python
import hashlib
import re
import requests

class GLibrary():
  """Generic library for Gaia Online"""
  def __init__(self):
    self.ava_srv = 'http://a2.gaiaonline.com'
    self.img_srv = 'http://s2.cdn.gaiaonline.com'
    self.main_srv = 'http://www.gaiaonline.com'

    self.agent = 'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) ' +
                  'AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 ' +
                  'Mobile/7B334b Safari/531.21.102011-10-16 20:23:50'

    self.session = requests.session(headers={'User-Agent': self.agent})
  
  def refresh(self):
    self.session = requests.session(headers={'User-Agent': self.agent})
 
  def md5(self, string):
    return hashlib.md5(string).hexdigest()