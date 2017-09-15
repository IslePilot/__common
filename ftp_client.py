#!/usr/bin/python

"""
Copyright (C) 2015 AeroSys Engineering, Inc.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Revision History:
  2015-01-10`, ksb, created
"""

import sys
sys.path.append("..")

import os
import os.path

import signal

import socket
from ftplib import FTP

# define a version for this file
VERSION = "1.0.20150110a"

def signal_handler(signal, frame):
  print "You pressed Control-c.  Exiting."
  sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

class FTP_Client(object):

  def __init__(self, hostname, user, passwd):
    # start out not ready
    self.ready = False

    # convert the hostname to an IP number
    host = socket.gethostbyname(hostname)

    # attempt to connect
    connect_attempts = 0
    while connect_attempts < 10:
      try:
        self.ftp = FTP(host, timeout=20)
      except:
        connect_attempts+=1
        print "unable to connect to %s.  Attempt %d"%connect_attempts
        if connect_attempts == 10:
          print "Giving up connecting to %s as %s"%(host, exc)
          return
        pass

    print "Connected to {:s}".format(host)

    # attempt to login
    try:
      self.ftp.login(user, passwd)
    except:
      print "Unable to login as {:s}".format(user)
      return
    print "Logged in as {:s}".format(user)

    # print the welcome message
    #print self.ftp.getwelcome()

    self.ready = True

    return


  def disconnect(self):
    if self.ready:
      # disconnect
      self.ftp.close()
      self.ready = False
    return

  def binary_put(self, filename):
    # if we aren't connected just return
    if self.ready == False:
      print "Not connected...unable to upload."
      return

    # open the file
    f = open(filename, "rb")

    # get the basename
    base = os.path.basename(filename)

    # upload the file
    print "uploading binary file {:s}".format(filename)
    try:
      self.ftp.storbinary("STOR {:s}".format(base), f)
    except:
      print "unable to upload {:s}".format(filename)
      f.close()
      return
    print "done."

    f.close()
    return

  def binary_get(self, filename):
    # if we aren't connected just return
    if self.ready == False:
      print "Not connected...unable to download."
      return

    # open a file for writing
    f = open(filename, "wb")

    # download the file
    print "downloading binary file {:s}".format(filename)
    try:
      self.ftp.retrbinary("RETR {:s}".format(filename), f.write)
    except:
      print "unable to download {:s}".format(filename)
      f.close()
      return
    print "done."

    f.close()
    return

def main():
  print("Copyright (C) 2015 AeroSys Engineering, Inc.")
  print("This program comes with ABSOLUTELY NO WARRANTY;")
  print("This is free software, and you are welcome to redistribute it")
  print("under certain conditions.  See GNU Public License.")
  print("")

  print("Press Control-c to exit.")
  # the file contains one line with the username and password separated by a space
  login = open('/home/pi/py_scripts/picam/.wunderground.txt', 'r')
  contents = login.read()
  login.close
  data = contents.split()
  username = data[0]
  password = data[1]

  server = 'webcam.wunderground.com'
  filename = '/mnt/keith-pc/timelapse/image.jpg'

  ftp = FTP_Client(server, username, password)
  ftp.binary_put(filename)
  ftp.disconnect()

  
  

# only run main if this is called directly
if __name__ == '__main__':
  main()

