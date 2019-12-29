#-*- coding: utf-8 -*-

import sys
import os
import shutil
import getopt
from random import randint, random


__author__ = """ 
    
    * by: c0der @kard3ti_Ca*
    
    Bsecdat is a tool for erase secure files for os GNU/Linux, the first version in perl by *blackngel*
    in set saqueadores the ezine number 30 security of data, this tool is modified
    for me, written in python. """


__licence__ = """

	BSecdat is a tool for erase secure files.
	
	This program is free software; you can redistribute it and/or
	modify it under the terms of the GNU General Public License
	as published by the Free Software Foundation; either version 2
	of the License, or (at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program; if not, write to the Free Software
	Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

	The authors disclaims all responsibility in the use of this tool. """


class Color(object):
      """ Color for text inputs """
      OKGREEN = '\033[92m'
      OKRED = '\033[91m'
      FAIL = chr(27)+"[0;31"
      ENDC = '\033[0m'
      YELLOW = '\033[33m'


class BsecDat(object):
      """ BsecDat is a Tool for secure erase. """
      
      def __init__(self, file=None, rewrite=None):
	  """ Initialize or not the file and number of rewrite """
	  self._file = file
	  self._rewrite = rewrite
	  self.files_delete = 0
      
      def set_file(self, file):
	  """ Establish the file. @params file type(file) """
	  self._file = file
	  
      def set_rewrite(self, rewrite):
	  """ Establish the number of rewrite. @params rewrite type(int) """
	  self._rewrite = rewrite
	
      def get_file_size(self):
	  """ Return the size of file """
	  size = os.path.getsize(self._file)
	  return size
	
      def rewrite_file(self):
	  """ Rewrite the content file and truncate 0 the file size """
	  if not os.path.isfile(self._file):
	      raise ValueError('A file was expected !') 
	  if self._rewrite <= 0:
	      raise ValueError('The number must be > 0')
	  
	  try:
	      with open(self._file, 'w') as f:
		    for i in xrange(self._rewrite):
			f.seek(0, 0)
			for j in xrange(self.get_file_size()):
			    c = randint(0, 255)
			    f.write(chr(c))
		    # truncate 0 the file size
		    f.truncate(0)
	  except IOError:
		 os.chmod(self._file, 700) # Setting permission
		 self.rewrite_file()       # call method again
	       
      def change_properties(self):
	  """ Change properties the file, Change access date and modify date."""
	  os.utime(self._file, (0, 0))
	    
      def get_rename_file(self):
	  """ Rename the file and return name """
	  name = str(random() * 255)
	  os.rename(self._file, name)
	  return name

      def delete_file(self):
	  """ Remove file. """
	  os.unlink(self.get_rename_file())
	  path = os.path.dirname(self._file)
	  print Color.OKRED+'[*] %s'%path+Color.ENDC
	  print Color.OKGREEN+'[+] Remove file /%s ....'%os.path.basename(self._file)+Color.ENDC
      
      def delete_directory(self, directory):
	  shutil.rmtree(directory)
	  print Color.OKRED+'[+] delete directory %s..'%directory+Color.ENDC
      
      def recycling(self, file):
	  """ Recycling in folder the files remove. """
	  if not os.path.exists('recycling'):
	      os.mkdir('recycling')
	  shutil.move(file, 'recycling')
      
      def info(self):
	  print Color.OKGREEN+'[+] INFO: %d deleted files..'%self.files_delete+Color.ENDC
      
      def run(self):
	  """ Initialize of program... """
	  self.rewrite_file()
	  self.change_properties()
	  self.delete_file()
	  self.files_delete += 1


def logo():
    hello = """
    
	*********************************************************
	*    _____                      __          _           *
	*   |   _ \____  ____  ____    |  | ____ _ | |_ 	*
	*   |  __ /  __|/  _ \/  _ | __|  |/  _ ' |   _|	*	
	*   |   _ \___ \   __/| |_  / __  |  (_|  |  |_		*
	*   |_____/___ /\____|\____|\_____|\____,_|\___|	*
	*	       Secure erase files.			*
	*		    V. 1.1				*
	*	  ** By: c0der - 07/05/15 **			*
	*    The first version in perl by blackngel in 		*
	*    set saqueadores, This version is modified for me.	*
	*********************************************************
	  
	  """
    print Color.YELLOW+hello+Color.ENDC

def usage():
    print 'BSecdat Tool'
    print 
    print 'Usage: Bsecdat.py -f myfile r -2'
    print '-d --directory		-directory [dir] delete a dir or tree of dirs with files'
    print '-f --file		-file [file] delete a file'
    print '-r --rewrite		-rewrite [number] number of rewrite'
    print '-h --help		-help'
    print
    print 'Example: '
    print 'Bsecdat.py -d mydirectory -r 3'
    print 'Bsecdat.py -f myfile -r 4'
    print
    

def delete_files_folder(directory, rewrite):
    """ Delete a tree of directory with files. """
    if not os.path.isdir(directory):
	raise ValueError('A directory was expected !')
    
    tree = os.walk(directory)   	# Tree of directories
    bsec = BsecDat() 		# Create instace 
    bsec.set_rewrite(rewrite) 	# Establish number of rewrite
    
    errors = 0
    for tupla in tree:
	path, dirs, files = tupla
	absolute_path = os.path.abspath(path)
	if files:
	   for file in files:
		try:
		    bsec.set_file(absolute_path+'/'+file) # Establish file
		    bsec.run()	# Run ..delete file
		except:
		    errors += 1
		    print Color.OKRED+'[!] Error file not valid %s'%file+Color.ENDC
		    
    # if all files are deleted, deleted directory
    if not errors:
	bsec.delete_directory(directory)
    
    print '[+] Errors: %d errors'%errors
    bsec.info() # Info: number of deleted files
    
    
def test():
    """ Test de prueba. """
    text = """ KWrite is a simple text editor, with syntax highlighting, 
	       codefolding, dynamic word wrap and more,
	       it's the lightweight version of Kate, providing more speed for minor 
	       tasks. It ships per default with KDEBASE package. """
    
    if not os.path.exists('test'):
	os.mkdir('test')
    
    for j in xrange(10):
	os.mkdir('test/test_'+str(j))
	for i in xrange(10):
	    with open('test/test_'+str(j)+'/test_'+str(i)+'.txt', 'a+') as f:
		f.write(text)
	    
    print 'Test ...create dir'
    

def main():
    """ Initialize program. Principal function. """
    
    directory = ''	# Directory
    file = ''		# File
    rewrite = 1 	# Establish rewrite 1 by default
    
    if not len(sys.argv[1:]):
	usage()
	sys.exit(1)

    # Arguments by line commands
    try:
	opts, args = getopt.getopt(sys.argv[1:], 'f:d:r:h', ['file', 'directory', 'rewrite', 'help'])
	
    except getopt.GetoptError as err:
	usage()
	print err
	sys.exit(1)  
  
    for opt, arg in opts:
	if opt in ('-h', '--help'):
	    usage()
	    sys.exit(1)
	elif opt in ('-d', '--directory'):
	     directory = arg
	elif opt in ('-f', '--file'):
	     file = arg
	elif opt in ('-r', '--rewrite'):
	     rewrite = int(arg)
	     
    # Validate Arguments
    if file and rewrite and not directory:
	bsec = BsecDat(file, rewrite)
	bsec.run()
	bsec.info()
    elif directory and rewrite and not file:
	delete_files_folder(directory, rewrite)
    else:
	usage()
 

if __name__ == '__main__':
    logo()
    main()












