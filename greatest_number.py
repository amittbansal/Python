# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import math
import numpy

x = int(input("Enter the number : "))
y1=[]                   # list with number break i.e contain each digit of nuber
y2=[]                   # list with average of consecutive number
y3=[]                   # list for storing number after replacing the number
y = map(int,str(x))
print (y)
z = len(y)

for i in range(0,z):
    if (i<(4)):
        a = [y[i],y[i+1]]    
        y1.append(int(math.ceil(numpy.mean(a))))
print (y1)      

sum0 = 0
sum1 = 0
sum2 = 0
b = 3

for k in range (2,z):
    sum0 = (sum0*10)+y[k]
num = str(int(y1[0])) + str(sum0)
y3.append(num)

for i in range(1,z-1):    
    for j in range (0,i): 
       sum1 = (sum1*10)+y[j]
    
    for k in range (b,z):
        sum2 = (sum2*10)+y[k]
    b=b+1
    
    if (sum2<=0):
        sum2 = ""
        
    total = str(sum1)+str(y1[i])+str(sum2)
    y3.append(total)
    sum1 = 0
    sum2 = 0

print (y3[:])    
print ("Greatest number is : {}".format(int(max(y3))))