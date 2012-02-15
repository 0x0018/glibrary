#!/usr/bin/env python
from phpserialize import *
from random import Random

import hashlib
import re
import requests
import time

class GLibrary():
  """Generic library for Gaia Online"""
  def __init__(self):
    self.avasrv = 'http://a2.gaiaonline.com'
    self.imgsrv = 'http://s2.cdn.gaiaonline.com'
    self.mainsrv = 'http://www.gaiaonline.com'

    self.agent = ('Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0.1)' + 
                    ' Gecko/20100101 Firefox/7.0.12011-10-16 20:23:00')

    self.session = requests.session(headers={'User-Agent': self.agent})
  
  def refresh(self):
    self.session = requests.session(headers={'User-Agent': self.agent})
 
  def md5(self, string):
    return hashlib.md5(string).hexdigest()
  
  def generate(self, mode):
    """Generate a Username, Password, or (Fake) Email Address based on mode"""
    chars = '789yuiophjknmYUIPHJKLNM'
    length = 8 if mode.lower() == 'password' else 16

    ret = ''
    for i in range(length):
      ret = ret + Random().choice(chars)
    
    if mode.lower() != 'password': ret = ret.lower()
    return ret.lower() + '@mail.com' if mode.lower() == "email" else ret
  
  def create(self, email=None, username=None, password=None):
    """
    Create an account on Gaia Online
    If a parameter isn't specified, generate one.
    A generated email will not be functional (the account cannot be verified).

    """
    email_, username_, password_ = email, username, password  # Avoid conflict
    if email_ == None: email_ = self.generate('email')  # Make one up
    if username_ == None: username_ = self.generate('username')
    if password_ == None: password_ = self.generate('password')

    registration = self.mainsrv + '/gapi/rest/registration'
    ref = self.imgsrv + '/images/Gaia_Flash/registration/guestRegistration.swf'
    headers = {'Referrer': ref + '?gver=46'}

    self.session.get(self.mainsrv + '/register/flash/?v=c&_gaia_t_=4950')

    qstring = '?t=602'
    url = registration + '/initialize'
    obj = loads(self.session.get(url).content)
    nonce = obj['n']

    qstring = '?username=%s&count=4&suggestion=1&n=%s' % (username_, nonce)
    url = registration + '/checkusernameavailability' + qstring
    r = loads(self.session.get(url, headers=headers).content)

    if r == False:
      if username == None:
        return self.create(email_, self.generate('username'), password_)
      else:
        return "Error. Supplied username is not available."

    pdict = dict(mouth=10000, outfit=21065, hair=7067, n=nonce,
              gender='m', eyes=894, base=34)
    url = registration + '/setavatar?'
    r = loads(self.session.post(url, headers=headers, data=pdict).content)
    if r != True: return r
    
    pdict = dict(password=password_, fb_sessionkey='', fb_uid='',
                  recaptcha_response_field='bypass', accept_tos=1,
                  dob='4/1/1995', password_confirm=password_, email=email_,
                  email_alert=0, n=nonce, username=username_,
                  hash=self.md5(nonce + '8elly8eansvryhngry'))
    url = registration + '/setuserinfo?'
    r = loads(self.session.post(url, headers=headers, data=pdict).content)

    if r != True:
      messages = []
      for key,val in enumerate(r):
        messages.append(r[key]['message'])
      return messages

    qstring = '?fb_sessionkey=&fb_uid=&n=' + nonce
    url = registration + '/createaccount' + qstring
    r = loads(self.session.get(url, headers=headers).content)
    if r != True: return r

    qstring = '?v=phpobject&m=' + dumps([[107]])
    r = loads(self.session.get(self.mainsrv + '/chat/gsi/' + qstring).content)

    return [str(r[0][2]['gaia_id']), password_]

if __name__ == "__main__":
  glib = GLibrary()
  glib.create()
