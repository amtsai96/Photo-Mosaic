#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sys import platform as sys_pf
if sys_pf == 'darwin':
    import matplotlib
    matplotlib.use("TkAgg")

from datalib import *
import os
from pylab import *
import pickle
from Tkinter import *
from PIL import ImageTk,Image
import tkMessageBox
import tkFileDialog
from ttk import Frame, Button, Label, Style
import csv
import colorsys
#from sklearn.metrics.pairwise import cosine_similarity
from scipy import spatial

global thumb
global thumb_mosaic

csvLoc = "./dataset/"
imgLoc = "./dataset/img/"
stretchHeight = False

class Window(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()
    
    def initUI(self):
        
        self.parent.title("HW4_made_by_103703010_103703015")
        self.pack(fill=BOTH, expand=1)
        
        # Open File
        self.fileName = StringVar(value = imgLoc + "ukbench00000.jpg")
        Button(self, text = "-- Select File --", command = openFile).grid(row=2, column=0, padx=570, pady=5, sticky=W+N+S)
        Label(self, textvariable = self.fileName).grid(row=3, column=0, columnspan=10, padx=670, pady=5, sticky=W+N+S)
        # Save File
        self.saveName = StringVar(value = "./mosaic.jpg")
        Button(self, text = "-- Save File To --", command = saveFile).grid(row=4, column=0, padx=570, pady=5, sticky=W+N+S)
        Label(self, textvariable = self.saveName).grid(row=5, column=0, columnspan=10, padx=670, pady=5, sticky=W+N+S)

        img = Image.open(self.fileName.get())
        tmpWidth = int(img.size[0]*480.0/img.size[1])
        if tmpWidth > 700:
            stretchHeight = True
            image = ImageTk.PhotoImage(img.resize((700, int(img.size[1]*700.0/img.size[0])),Image.ANTIALIAS))
        else:
            stretchHeight = False
            image = ImageTk.PhotoImage(img.resize((tmpWidth, 480),Image.ANTIALIAS))
        self.thumb = Label(self)
        self.thumb.grid(row=0, column=0, padx=15, pady=5, sticky=W)
        self.thumb.configure(image = image)
        self.thumb.image = image

        self.thumb_mosaic = Label(self)
        self.thumb_mosaic.grid(row=0, column=0, padx=735, pady=5, sticky=W)
        self.thumb_mosaic.configure(image = image)
        self.thumb_mosaic.image = image


        # Mode
        mode = StringVar(self)
        mode.set('-- Feature Mode --')
        menu = OptionMenu(self, mode, 'M1-Average_RGB','M2-Average_HSV','M3-Color_Histogram', 'M4-Color_Layout')
        menu.grid(row=6, column=0, padx=570, pady=5, sticky=W)
        
        countMode = StringVar(self)
        countMode.set('-- Distance Counting Mode --')
        countMenu = OptionMenu(self, countMode, 'C1-Euclidean','C2-Cosine Similarity')
        countMenu.grid(row=6, column=0, padx=770, pady=5, sticky=W)
        
        # Image Partition Size
        Label(self, text="Image Partition Size = ").grid(row=7, column=0,padx=600, sticky=W)
        self.column = StringVar(value="30")
        self.row = StringVar(value="30")
        
        #To check if the inputs are numbers
        vcmd = (self.register(self.isValidate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.columnEntry = Entry(self,textvariable = self.column, width = 4, validate = 'key', validatecommand = vcmd)
        self.columnEntry.grid(row=7, column=0, padx=750, pady=1 ,sticky=W)
        Label(self, text="x").grid(row=7, column=0, padx=800,sticky=W)
        self.rowEntry = Entry(self,textvariable = self.row, width = 4, validate = 'key', validatecommand = vcmd)
        self.rowEntry.grid(row=7, column=0,sticky=W, padx=820)
        
        # Start Processing Mosaic
        Button(self, text = "Start Processing Mosaic", command = lambda: startProcessing(mode.get(),countMode.get(),self.fileName.get(),self.saveName.get(),int(self.rowEntry.get()),int(self.columnEntry.get()))).grid(row=8, column=0, padx=630, pady=5, sticky=W)

    def isValidate(self, action, index, value_if_allowed,prior_value, text, validation_type, trigger_type, widget_name):
        return True if text in '0123456789' else False


def openFile():
    fileName = tkFileDialog.askopenfilename(initialdir = imgLoc)
    app.fileName.set(fileName)
    img = Image.open(app.fileName.get())
    tmpWidth = int(img.size[0]*480.0/img.size[1])
    if tmpWidth > 700:
        stretchHeight = True
        image = ImageTk.PhotoImage(img.resize((700, int(img.size[1]*700.0/img.size[0])),Image.ANTIALIAS))
    else:
        stretchHeight = False
        image = ImageTk.PhotoImage(img.resize((tmpWidth, 480),Image.ANTIALIAS))
    app.thumb.configure(image = image)
    app.thumb.image = image
    app.thumb_mosaic.configure(image = image)
    app.thumb_mosaic.image = image

#def showImg(img):
#    Image.open(img).show()

def saveFile():
    fileName = 'Mosaic.jpg'
    saveName = tkFileDialog.asksaveasfile(initialdir = "./",filetypes=[("Image","*.jpg")],initialfile=fileName)
    app.saveName.set(saveName.name)

##################   Calculate Formulas   ##################

def avgRGB_CountDistance(query,base):
    qData = convert(query,"Average_RGB")
    minValue = ['',float("inf")] #fileName,distance
    for row in xrange(0,len(base),4):
        distance = 0
        for i in xrange(1,4):
            distance += pow(abs(float(qData[i-1]) - float(base[row+i][1])) ,2)
        distance = sqrt(distance)
        if distance < minValue[1]:
            minValue = [base[row][0], distance]
    return minValue

def avgRGB_CountDistance_cos(query,base):
    qData = convert(query,"Average_RGB")
    minValue = ['',float("inf")] #fileName,distance
    for row in xrange(0,len(base),4):
        ql = []
        bl = []
        for i in xrange(1,4):
            ql.append(float(qData[i-1]))
            bl.append(float(base[row+i][1]))
        distance = spatial.distance.cosine(ql,bl)
        if distance < minValue[1]:
            minValue = [base[row][0], distance]
    return minValue

def avgHSV_CountDistance(query,base):
    qData = convert(query,"Average_HSV")
    minValue = ['',float("inf")] #fileName,distance
    for row in xrange(0,len(base),4):
        distance = 0
        for i in xrange(1,4):
            distance += pow(abs(float(qData[i-1]) - float(base[row+i][1])) ,2)
        distance = sqrt(distance)
        if distance < minValue[1]:
            minValue = [base[row][0], distance]
    return minValue

def avgHSV_CountDistance_cos(query,base):
    qData = convert(query,"Average_HSV")
    minValue = ['',float("inf")] #fileName,distance
    for row in xrange(0,len(base),4):
        ql = []
        bl = []
        for i in xrange(1,4):
            ql.append(float(qData[i-1]))
            bl.append(float(base[row+i][1]))
        distance = spatial.distance.cosine(ql,bl)
        if distance < minValue[1]:
            minValue = [base[row][0], distance]
    return minValue

def ColorHist_Distance(queryHist, baseHist):
    # 當作一般的histogram處理
    distance = [0, 0, 0]
    for i in range(len(queryHist)):
        sumQuery = sumBase = d = 0
        for j in range(len(queryHist[i])):
            if i == 1 and j > 101: # S and index > 100
                break;
            if i == 2 and j > 255: # V and index > 255
                break;
            d += min( float(queryHist[i][j]),float(baseHist[i][j]) )
            sumQuery += float(queryHist[i][j])
            sumBase += float(baseHist[i][j])
        distance[i] = d/min(sumQuery, sumBase)
    #    return distance[0]
    #    return (4*distance[0]+1*distance[1]+2*distance[2])/(4+1+2)
    return sqrt( pow(distance[0], 2) + pow(distance[1], 2) + pow(distance[2], 2) )

def ColorHist_Distance2(queryHSV_avg, baseHist):
    # 將每一個histogram依據加權平均轉換成一個代表性的hsv，再對兩個hsv tuple計算距離
    distance = [0, 0, 0] # H, S, V
    baseAvg = [0, 0, 0]
    for i in range(len(baseHist)):
        count = weighted_sum = 0
        for j in range(len(baseHist[i])):
            if i == 1 and j > 101: break
            if i == 2 and j > 255: break
            weighted_sum += j*float(baseHist[i][j])
            count += float(baseHist[i][j])
        baseAvg[i] = weighted_sum/count
        if i == 1:
            distance[i] = min(abs(queryHSV_avg[i]-baseAvg[i]),360-abs(queryHSV_avg[i]-baseAvg[i])) / 180.0
        elif i == 2:
            distance[i] = abs(queryHSV_avg[i]-baseAvg[i])
        else:
            distance[i] = abs(queryHSV_avg[i]-baseAvg[i])/255.0
    return sqrt(pow(distance[0],2)+pow(distance[1],2)+pow(distance[2],2))

def ColorHist_Distance2_cos(queryHSV_avg, baseHist):
    # 將每一個histogram依據加權平均轉換成一個代表性的hsv，再對兩個hsv tuple計算距離
#    distance = [0, 0, 0] # H, S, V
    ql = [0,0,0]
    bl = [0,0,0]
    baseAvg = [0, 0, 0]
    for i in range(len(baseHist)):
        count = weighted_sum = 0
        for j in range(len(baseHist[i])):
            if i == 1 and j > 101: break
            if i == 2 and j > 255: break
            weighted_sum += j*float(baseHist[i][j])
            count += float(baseHist[i][j])
        baseAvg[i] = weighted_sum/count
        if i == 1:
            sub = abs(queryHSV_avg[i]-baseAvg[i])
            ql[i] = queryHSV_avg[i]/360.0 if sub <= 180 else (360-queryHSV_avg[i])/360.0
            bl[i] = baseAvg[i]/360.0
        elif i == 2:
            ql[i] = queryHSV_avg[i]*1.0
            bl[i] = baseAvg[i]*1.0
        else:
            ql[i] = queryHSV_avg[i]/255.0
            bl[i] = baseAvg[i]/255.0
    return spatial.distance.cosine(ql,bl)

def colorHistogram_CountDistance(query, base):
    # H:[0,360] / S:[0,100] / V:[0,255]
    qData = convert(query,"Color_Histogram")
    queryHSV = [0, 0, 0]
    for i in range(len(qData)):
        count = weighted_sum = 0
        for j in range(len(qData[i])):
            if i == 1 and j > 100: break
            if i == 2 and j > 255: break
            weighted_sum += j*float(qData[i][j])
            count += float(qData[i][j])
        queryHSV[i] = (weighted_sum/count if not count == 0 else 0)
    
    minValue = ['',float("inf")] #fileName,distance
    for row in xrange(0,len(base),4):
#        distance = ColorHist_Distance(qData , [base[row+i] for i in range(1,4)] )
        distance = ColorHist_Distance2(queryHSV , [base[row+i] for i in range(1,4)] )
        if distance < minValue[1]:
            minValue = [base[row][0], distance]
    return minValue

def colorHistogram_CountDistance_cos(query, base):
    # H:[0,360] / S:[0,100] / V:[0,255]
    qData = convert(query,"Color_Histogram")
    queryHSV = [0, 0, 0]
    for i in range(len(qData)):
        count = weighted_sum = 0
        for j in range(len(qData[i])):
            if i == 1 and j > 100: break
            if i == 2 and j > 255: break
            weighted_sum += j*float(qData[i][j])
            count += float(qData[i][j])
        queryHSV[i] = (weighted_sum/count if not count == 0 else 0)

    minValue = ['',float("inf")] #fileName,distance
    for row in xrange(0,len(base),4):
        distance = ColorHist_Distance2_cos(queryHSV , [base[row+i] for i in range(1,4)] )
        if distance < minValue[1]:
            minValue = [base[row][0], distance]
    return minValue

def colorLayout_CountDistance(query, base):
    # 8*8 = 64 blocks
    qData = convert(query,"Color_Layout")
    minValue = ['',float("inf")] #fileName,distance
    for row in xrange(0,len(base),4):
        distance = 0
        for i in xrange(1,4):
            blockDistance = 0
            for j in xrange(1,65):
                blockDistance += pow(abs(float(qData[i-1][j-1]) - float(base[row+i][j])) ,2)
            distance += sqrt(blockDistance)
        if distance < minValue[1]:
            minValue = [base[row][0], distance]
    return minValue

def colorLayout_CountDistance_cos(query, base):
    # 8*8 = 64 blocks
    qData = convert(query,"Color_Layout")
    minValue = ['',float("inf")] #fileName,distance
    for row in xrange(0,len(base),4):
        bl=[]
        ql=[]
        for i in xrange(1,4):
            for j in xrange(1,65):
                ql.append(float(qData[i-1][j-1]))
                bl.append(float(base[row+i][j]))
        distance = spatial.distance.cosine(ql,bl)
        if distance < minValue[1]:
            minValue = [base[row][0], distance]
    return minValue

##################   Online Processing   ##################
def startProcessing(mode,countMode,fileName,saveName,row,column):
    query = Image.open(fileName)
    width, height = query.size
    csvName = ''
    formula = ''
    if mode[1] == "-":
        return -1
    elif mode[1] == "1":      #M1-Avg_RGB
        csvName = 'AverageRGB.csv'
        if countMode[1] == "1": #C1-Euclidean
            formula = avgRGB_CountDistance
        elif countMode[1] == "2": # C2-Cosine
            formula = avgRGB_CountDistance_cos

    elif mode[1] == "2":      #M2-Avg_HSV
        csvName = 'AverageHSV.csv'
        if countMode[1] == "1": #C1-Euclidean
            formula = avgHSV_CountDistance
        elif countMode[1] == "2": # C2-Cosine
            formula = avgHSV_CountDistance_cos

    elif mode[1] == "3":      #M3-Color_Histogram
        csvName = 'ColorHistogram.csv'
        if countMode[1] == "1": #C1-Euclidean
            formula = colorHistogram_CountDistance
        elif countMode[1] == "2": # C2-Cosine
            formula = colorHistogram_CountDistance_cos

    elif mode[1] == "4":    #M4-Color_Layout
        csvName = 'ColorLayout.csv'
        if countMode[1] == "1": #C1-Euclidean
            formula = colorLayout_CountDistance
        elif countMode[1] == "2": # C2-Cosine
            formula = colorLayout_CountDistance_cos

    print('Processing Photo Mosaic in ' + mode[3:] + ' / ' + countMode[3:] + ' mode.')
    with open(csvLoc + csvName, 'rb') as csvfile:
        Reader = csv.reader(csvfile)
        data = [row_ for row_ in Reader]
        
        blockW = width / column
        blockH = height / row
        output = Image.new('RGB', (blockW*column,blockH*row))
        for i in xrange(column):
            for j in xrange(row):
                # Update block boundary
                blockBoundary = (i*blockW, j*blockH, (i+1)*blockW, (j+1)*blockH)
#                print blockBoundary
                imgCrop = query.crop(blockBoundary)
                res = formula(imgCrop,data)
                print (' '*(3-len(str(i+1)))+str(i+1)+' x '+' '*(3-len(str(j+1)))+str(j+1)+' : '+res[0]+' , Distance = '+str(res[1]))
                imgNew = Image.open(imgLoc + res[0]).resize((blockW, blockH))
                output.paste(imgNew, blockBoundary)

    output.save(saveName, "JPEG", quality=85, optimize=True, progressive=True)

    # Show saved photo
    # showImg(saveName)
    img = Image.open(saveName)
    if stretchHeight:
        image = ImageTk.PhotoImage(img.resize((720, int(img.size[1]*720.0/img.size[0])),Image.ANTIALIAS))
    else:
        image = ImageTk.PhotoImage(img.resize((int(img.size[0]*480.0/img.size[1]), 480),Image.ANTIALIAS))
    app.thumb_mosaic.configure(image = image)
    app.thumb_mosaic.image = image

if __name__ == '__main__':
    root = Tk()
    app = Window(root)
    root.geometry("1440x780")
    root.mainloop()
