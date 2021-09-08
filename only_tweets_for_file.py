#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 16 14:16:58 2017

@author: amitbansal
"""
import os
import re
directory='/Users/amitbansal/Desktop/testfileforexractingtweets/everydaysexism2017-05-14.json'  # file path
destination='/Users/amitbansal/Desktop/'					# path where you want to create only tweets file
with open(directory,'r') as f: 
    for line in f:
        line1 = line.split(',')
        line2 = line1[0].split()
        fi=str(destination)+str(line2[1])+str('.txt')
        f1=re.search('text=\'(.+?)\',',line)
        if os.path.exists(fi):
            f=open(fi,'a')
            f.write(f1.group(1))
            f.write("\n")
            f.close()
        else:
            f=open(fi,'w')
            f.write(f1.group(1))
            f.write("\n")
            f.close()
        
            
        
         
            
            
         