#!/usr/bin/env python
#-*- coding: utf-8 -*-

from PIL import ImageTk, Image
import os
import numpy as np
import pandas
from scipy.fftpack import dct
from scipy.misc import toimage
import colorsys

def zigZagIndex(n):
    def move(i, j):
        if j < (n - 1):
            return max(0, i - 1), j + 1
        else:
            return i + 1, j

    #Create an n*n array
    a = [[0] * n for i in xrange(n)]
    x, y = 0, 0
    for v in xrange(n * n):
        a[y][x] = v
        if (x + y) & 1:
            x, y = move(x, y)
        else:
            y, x = move(y, x)
    return a

def zigZag(list):
    back = [[ 0 for _ in xrange(8 * 8)]for _ in xrange(3)]
    for x in xrange(3):
        index = zigZagIndex(8)
        for i in xrange(8):
            for j in xrange(8):
                back[x][index[i][j]] = list[x][i][j]
    return back

def convert(query, mode):
    if(query.mode!="RGB"):
        query = query.convert("RGB")

    # mode
    if mode == "Average_RGB":
        width,height = query.size
        pixel = query.load()
        Avg = [0,0,0]
            
        for i in xrange(width):
            for j in xrange(height):
                r,g,b = pixel[i,j]
                Avg[0] += r
                Avg[1] += g
                Avg[2] += b

        pixelNum = width * height
        for x in xrange(len(Avg)):
            Avg[x]/= pixelNum

        return Avg
    
    elif mode == "Average_HSV":
        width,height = query.size
        pixel = query.load()
        Avg = [0,0,0]
        
        for i in xrange(width):
            for j in xrange(height):
                r,g,b = pixel[i,j]
                h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
                Avg[0] += h
                Avg[1] += s
                Avg[2] += v
    
        pixelNum = width * height
        for x in xrange(len(Avg)):
            Avg[x]/= pixelNum
                
        return Avg

    elif mode == "Color_Histogram":
        width,height = query.size
        # RGB to HSV
        imgHSV = [[[0 for k in xrange(3)] for j in xrange(height)]for i in xrange(width)]
        hsvHistogram = [[0 for k in xrange(360)] for j in xrange(3)]
        pixel = query.load()
        for i in xrange(width):
            for j in xrange(height):
                r, g, b = pixel[i,j]
                h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
                h, s, v = int(h*360), int(s*100), int(round(v*255))
                imgHSV[i][j][0],imgHSV[i][j][1],imgHSV[i][j][2] = h,s,v
                hsvHistogram[0][h] += 1
                hsvHistogram[1][s] += 1
                hsvHistogram[2][v] += 1
        return hsvHistogram

    elif mode == "Color_Layout":
        width,height = query.size
        
        # Image Partition
        ImgPartitionWidth = max(width / 8, 1)
        ImgPartitionHeight = max(height / 8, 1)
        ImgPartitionRGB = [[[0 for j in xrange(8)] for i in xrange(8)]for k in xrange(3)]
        pixel = query.load()
        for i in xrange(width):
            for j in xrange(height):
                for k in xrange(3):
                    xIndex = i/ImgPartitionWidth
                    yIndex = j/ImgPartitionHeight
                    if(xIndex < 8 and yIndex < 8):
                        ImgPartitionRGB[k][xIndex][yIndex] += pixel[i,j][k]

        ImgPartitionBase = ImgPartitionWidth*ImgPartitionHeight
        for i in xrange(8):
            for j in xrange(8):
                for k in xrange(3):
                    ImgPartitionRGB[k][i][j] /= ImgPartitionBase
                    #print ImgPartitionRGB[k][i][j]

        #RGB to YCbCr
        #Y = 16 + 65.738*R/256 + 129.057*G/256 + 25.064*B/256
        #Cb = 128 - 37.945*R/256 - 74.494*G/256 + 112.439*B/256
        #Cr = 128 + 112.439*R/256 - 94.154*G/256 - 18.285*B/256
        ImgPartitionYCbCr = [[[0 for j in xrange(8)] for i in xrange(8)]for k in xrange(3)]
        for i in xrange(8):
            for j in xrange(8):
                ImgPartitionYCbCr[0][i][j] = 16 + ImgPartitionRGB[0][i][j]*65.738/256 + ImgPartitionRGB[1][i][j]*129.057/256 + ImgPartitionRGB[2][i][j]*25.064/256
                ImgPartitionYCbCr[1][i][j] = 128 - ImgPartitionRGB[0][i][j]*37.945/256 - ImgPartitionRGB[1][i][j]*74.494/256 + ImgPartitionRGB[2][i][j]*112.439/256
                ImgPartitionYCbCr[2][i][j] = 128 + ImgPartitionRGB[0][i][j]*112.439/256 - ImgPartitionRGB[1][i][j]*94.154/256 - ImgPartitionRGB[2][i][j]*18.285/256

        # DCT Transform
        ImgDCT = [0 for x in xrange(3)]
        for k in xrange(3):
            ImgDCT[k] = dct(ImgPartitionYCbCr[k])
    
        # Zig-Zag Scan
        finalList = zigZag(ImgDCT)

        return finalList
