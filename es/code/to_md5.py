#!/usr/bin/env python3

import hashlib
import subprocess
import re

'''
rename files in a folder to their respective md5 values. preserve types. 
'''

endpat = re.compile('.*(\\..*)')
filelist = subprocess.check_output(['find', './', '-type', 'f']).decode().split('\n')[:-1]

for myf in filelist:
    m = endpat.match(myf)
    ending = m.group(1)
    m = hashlib.md5()
    infile = open(myf, 'rb')
    m.update(infile.read())
    infile.close()
    subprocess.check_output(['mv', myf, m.hexdigest() + ending])
