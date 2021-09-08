# -*- coding: utf-8 -*-

"""
Created on Sun Mar 05 12:29:08 2017
@author: SLIS IT
"""

import time
import os
import re

start_time = time.clock()

i = 1

path_source = '/Users/amitbansal/Desktop/November'
path_destination = '/Users/amitbansal/Desktop/ Trump'

file_name = str(os.path.basename(path_source)) + ".txt"

for filename in os.listdir(path_source):
    a = open(os.path.join(path_source,filename),'r')
    b = a.readlines()
    for line in b:

        for result in re.findall(' text=\'(.*?)\',', line, re.S):
            
            if(os.path.isfile(os.path.join(path_destination,file_name))):
                file_open=open(os.path.join(path_destination,file_name),'a')
                file_open.write(result)
                file_open.write('\n')

            else :
                file_open=open(os.path.join(path_destination,file_name),'w')
                file_open.write(result)
                file_open.write('\n')

    print "\n"
    print "%s" %filename
    print "%d" %i
    print time.clock() - start_time, "seconds program took to finish its job \n"
    i = i+1
    start_time = time.clock()
