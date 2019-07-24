#!/usr/bin/env python
# coding: utf-8

# In[2]:
##################################################################################
#				Author : Mehdi Zare				 #
#				Date   : 7/24/2019				 #
#				University of South Carolina			 #
#	Purpose: Divide HISTORY file, the teajectory file of MD from DL_POLY     #
##################################################################################			
import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import matplotlib.pyplot as plt


# # Collect the information of HISTORY file

# In[3]:


def Info(filename):
    try:
        fhand=open(filename)
    except:
        print('file', filename, 'cannot be opened')
        return
    
    # Get info of trajectory and metalID, read only the first 8 lines
    countline=0
    for line in fhand:
        countline += 1
        
         # trajectory
        if (countline == 2):
            info= line.strip().split()
            for index, item in enumerate(info):
                info[index]=int(item)
            totatoms, totconf, totlines= info[2:5]
            OneConfLine=int((totlines-2)/totconf)
        
        #Get Metal ID
        if (countline == 7):
            metalID=line.strip().split()[0]
            
        #break reading after line 8
        if (countline == 8):
            break
      
    print('TotAtoms',totatoms,'totconf ',totconf,'totlines',totlines, 'OneConfLine is', OneConfLine,'\n')
    
    #close the file and open it again and then divide HISTORY
    fhand.close()
    
 
    return int(totlines), int(totconf), int(OneConfLine)

# # Show information to the user and ask for the mode

# In[4]:


def mode():
    info=Info('HISTORY')
    print(info)
    print("\n Please enter what mode you want to run the program:'\n         cont: contious divide with no skip \n         espa: Evenly spaced conformations \n         skip: countious divide with skip \n ")

    mode=input('mode:')
    if (mode == 'cont' or mode == 'espa' or mode == 'skip') :
        print( ' Thanks! lets continue')
    else:
        print (' Your answer should be one of options above, please try later')
        return

    # mode cont
    if (mode == 'cont'):
        files=int(input('How many files do you need: '))
        each=int(input('How many conformations do you need in each file: '))
        return mode, files, each, info
    
    # mode espa
    elif (mode == 'espa'):
        needconf=int(input(' \n How many conformations do you need: '))
        return mode, needconf, info
    
    elif (mode == 'skip'):
        files=int(input('How many files do you need: '))
        each=int(input('How many conformations do you need in each file: '))
        skip=int(input('How many conformations do you want to be skipped: '))
        return mode, files, each, skip, info


# # Continouos divide

# In[5]:


def cont():
    each=int(final[2])
    totconf=int(final[3][1])
    totlines=int(final[3][0])
    OneConfLine=int(final[3][2])
    files=int(final[1])
    
    # read and store all HISTORY lines in data
    fread=open('HISTORY')
    data=fread.readlines()
    fread.close()
    newline=str((OneConfLine*each)+2)
    oldline=str(totlines)
    
    for fnum in range(1,files+1):
        fwrite=open('HISTORY.' + str(fnum),'a')
        # modify & add header
        fwrite.write(data[0])
        sec=data[1].replace(str(totconf),str(each))
        fwrite.write(sec.replace(oldline,newline))
        # write the file
        eachline= OneConfLine * each
        UB = (fnum * eachline) + 2
        LB = UB - eachline
        for k in range(LB,UB,1):
             fwrite.write(data[k])
        fwrite.close()


# # Evenly spaced divide

# In[6]:


def espa():
    needconf=int(final[1])
    totconf=int(final[2][1])
    totlines=int(final[2][0])
    OneConfLine=int(final[2][2])
    even=int(totconf / needconf)
    print('\n You will have a spaced HISTORY with',needconf,'conformation, the gap between each conf. is', even, '\n')
    
    # read and store all HISTORY lines in data
    fread=open('HISTORY')
    data=fread.readlines()
    fread.close()
    newline=str((OneConfLine*needconf)+2)
    oldline=str(totlines)
    
    fwrite=open('HISTORY.' + str(needconf),'a')
    # modify & add header
    fwrite.write(data[0])
    sec=data[1].replace(str(totconf),str(needconf))
    fwrite.write(sec.replace(oldline,newline))
    
    i=1
    j=1
    while (i <= needconf):
        UB= (j*OneConfLine) + 2
        LB= UB - OneConfLine
        for k in range(LB,UB,1):
             fwrite.write(data[k])
        i += 1
        j += even
    
    
    fwrite.close()


# # skip divide

# In[7]:


def skip():
    each=int(final[2])
    totconf=int(final[4][1])
    totlines=int(final[4][0])
    OneConfLine=int(final[4][2])
    files=int(final[1])
    skip=int(final[3])
    print('\n You will have',files,' HISTORY with',each,'conformations, skipped conformatinos is', skip, '\n')
    
    # read and store all HISTORY lines in data
    fread=open('HISTORY')
    data=fread.readlines()
    fread.close()
    newline=str((OneConfLine*each)+2)
    oldline=str(totlines)
    
    ii=0  # variable for skip
    for fnum in range(1,files+1):
        fwrite=open('HISTORY.' + str(fnum),'a')
        # modify & add header
        fwrite.write(data[0])
        sec=data[1].replace(str(totconf),str(each))
        fwrite.write(sec.replace(oldline,newline))
    
        # write the file
        eachline= OneConfLine * each
        skipline= OneConfLine * skip
        UB = (fnum * eachline) + 2 + (ii * skipline)
        LB = UB - eachline
        for k in range(LB,UB,1):
             fwrite.write(data[k])
        fwrite.close()
        ii += 1


# In[9]:


final=(mode())

if (final[0] == 'cont'):
    # warining
    if int(final[3][1]) % int(final[1] * final[2]) != 0:
        print(' \n Be aware that you do not want the remainder of conformations \n                 you want', final[1], 'files each has ', final[2],'conformation \n                 while the total conformation in HISTORY is ', final[3][1],)
    # Error
    if int(final[3][1]) < int(final[1] * final[2]):
        print('\n your total conformations in HISTORY file is less than what you asked for')
    # fine
    else:    
        cont()
        
elif (final[0] == 'espa'):
    # Error
    if int(final[2][1]) < int(final[1]) :
        print('\n your total conformations in HISTORY file is less than what you asked for')
    # fine
    else:    
        espa()
        
elif (final[0] == 'skip'):
    #warnning
    if int(final[4][1]) != int( final[1] * final[2] + ((final[1] - 1) * final[3]) ):
        print(' \n Be aware that you do not want the remainder of conformations \n')
    # Error
    if int(final[4][1]) < int( final[1] * final[2] + ((final[1] - 1) * final[3]) ):
        print('\n your total conformations in HISTORY file is less than what you asked for')
    # fine
    else:
        skip()


# In[ ]:




