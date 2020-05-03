# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 19:44:35 2020

@author: Aya Samir Abohadima
"""
from pathlib import Path
import numpy as np
import cv2 as cv
codeFile= input("Please enter file of  codes in type .npy 1 d array  :\n")

deff=int(input("Please enter 1 if there are second file for colorCodes else enter  0  :\n"))
if(deff==1):codeSymbole=input("Please enter file of symbole codes if it defferent  in type .npy :\n")
fristDiminstion=int(input("Please enter frist dimension of image :\n"))
secondDiminstion=int(input("Please enter second dimension of image :\n"))
codeSymp=0
if(fristDiminstion>0 and secondDiminstion >0 and Path(codeFile).is_file() ):
    if( deff==1):
        if( Path(codeSymbole).is_file()): deff=1     
        codeSymp=np.load(codeSymbole)
    codes=np.load(codeFile)
    flattenArray1=[]
    index=0
    codenewindex=0
    for i in range(0,len(codes)):
        for k in range(0,codes[i][1]):
            flattenArray1.insert(index,flattenArray1[codenewindex-codes[i][0]+k])
            index+=1
        codenewindex=index
        if(deff==1):flattenArray1.insert(index,codeSymp[i])
        else: flattenArray1.insert(index,codes[i][2])
        index+=1
    imagFlatten=np.array(flattenArray1)
    image=imagFlatten.reshape(fristDiminstion, secondDiminstion).astype(np.uint8) 
    cv.imwrite('imageAfterDecoding.jpg', image) 
    
    
