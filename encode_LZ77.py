# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 08:47:50 2020
encode LZ77
@author: Aya Samir Abohadima
"""
def checkEqual (flattenArray,searchindex,lockindex,send,slinderlen):
    if(lockindex>=slinderlen or lockindex>=len(flattenArray)-1) :
        return
    if(flattenArray[searchindex]==flattenArray[lockindex]):
        if(send[0]==0 and send[1]==0): send[0]=lockindex-searchindex
        send[1]+=1
        send[2]=flattenArray[lockindex+1]
        checkEqual(flattenArray,searchindex+1,lockindex+1,send,slinderlen)
    else :
        send[2]=flattenArray[lockindex]

def findMaxEqual(flattenArray,searchF,lockaheadIndex,slinderlen):
    searchE=lockaheadIndex-1
    lastSend=[0,0,flattenArray[lockaheadIndex]]
    for i in range(searchE,searchF-1,-1):
        send=[0,0,flattenArray[lockaheadIndex]]
        checkEqual(flattenArray,i,lockaheadIndex,send,slinderlen)
        if(send[0]>lastSend[0] and send[1]>lastSend[1]):
            lastSend=send
    return lastSend

def LZ77Encode(flattenArray,slinderLen,checkaheadLen,numcode):
   
    lockIndex=1
    searchF=lockIndex-1-(slinderLen-checkaheadLen)
    index=1
    ifDeferent=0;
    if(slinderLen>=256):
         ifDeferent=1;
         arrayCodes=[[0,0]]
         numcode.insert(0,flattenArray[0])
    else: arrayCodes=[[0,0,flattenArray[0]]]
    while(lockIndex<len(flattenArray)):
        toSearch=0
        if(searchF>0): toSearch=searchF
        code1=findMaxEqual(flattenArray,toSearch,lockIndex,lockIndex+checkaheadLen)
        if(ifDeferent==1):
            last=[]
            last.insert(0,code1[0])
            last.insert(1,code1[1])
            numcode.insert(len(numcode),code1[2])
            arrayCodes.insert(index,last)
        else:
            arrayCodes.insert(index,code1)
        searchF+=arrayCodes[index][1]+1
        lockIndex+=arrayCodes[index][1]+1
        index+=1
        #print(arrayCodes)
    return arrayCodes
        

## imports
from pathlib import Path
import numpy as np
import cv2 as cv
image = input("Please enter a image file name + type example 'image1.JPG' :\n")
lock_aheadLen =int(input("Please enter a lock_ahead length :\n"))
windowLength=int(input("Please enter a window length :\n"))
#read image and flatten it  
if(Path(image).is_file() and lock_aheadLen>0 and windowLength > lock_aheadLen):   
    img=cv.imread(image)
    grayImage=cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    print (grayImage.shape)
    flattenArray=grayImage.flatten()
    numcodes=[]
    if(windowLength>=256):
        codes=np.array(LZ77Encode(flattenArray,windowLength,lock_aheadLen,numcodes)).astype(np.uint16)
        np.save("codes",codes)
        colorcodes=np.array(numcodes).astype(np.uint8)
        np.save("colorCode",colorcodes)
        print('codes  <back,len> in codes.npy  <code> in colorCode.npy ')
    else:
       # print(LZ77Encode(flattenArray,windowLength,lock_aheadLen,numcodes))
        codes=np.array(LZ77Encode(flattenArray,windowLength,lock_aheadLen,numcodes)).astype(np.uint8)
        np.save("codes",codes)
        print('codes  <back,len,code> in codes.npy ')
else:
    print('invalid inputs' )

