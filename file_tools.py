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
  2015-01-17, ksb, created
"""

import sys
sys.path.append("..")

import shutil
import errno
import sys

# define a version for this file
VERSION = "1.0.20150117a"

def version():
  """Return the file tools version.

  returns: version string"""
  return "File Tools Version: {:s}".format(VERSION)

def copy_file(src, dest):
  """Copy a file from src to dest):

  src:  full pathname of file to copy
  dest:  full pathname of new copy

  returns: True: copy succeeded
           False: copy failed"""
  try:
    shutil.copy(src, dest)
  except OSError as exc:
    # Getting strange error claiming unable when
    # copying to windows mounted drive.  The call
    # succeeds but fails the try
    # print "OSError ", errno.errorcode[exc.errno]
    pass
  except Exception as exc:
    print "file_tools.copy_file():  Unable to copy file {:s} to {:s}".format(src, dest)
    print sys.exc_info()[0]
    print sys.exc_info()[1]
    print "Error: ", errno.errorcode[exc.errno]
    return False

  return True


def main():
  print("Copyright (C) 2015 AeroSys Engineering, Inc.")
  print("This program comes with ABSOLUTELY NO WARRANTY;")
  print("This is free software, and you are welcome to redistribute it")
  print("under certain conditions.  See GNU Public License.")
  print("")

  # tests
  print version()

  copy_file('/home/pi/temp/this.txt', '/home/pi/temp/that.txt')

  


# only run main if this is called directly
if __name__ == '__main__':
  main()

