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

global thumb
global thumb_mosaic

csvLoc = "./dataset/"
imgLoc = "./dataset/img/"

class Window(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()
    
    def initUI(self):
        
        self.parent.title("HW4_made_by_103703010_103703015")
        self.pack(fill=BOTH, expand=1)
        
        # Open File
        self.fileName = StringVar(value = "./example.jpg")
        Button(self, text = "-- Select File --", command = openFile).grid(row=2, column=0, padx=600, pady=5, sticky=W+N+S)
        Label(self, textvariable = self.fileName).grid(row=3, column=0, columnspan=10, padx=700, pady=5, sticky=W+N+S)
        # Save File
        self.saveName = StringVar(value = "./example_Mosaic.jpg")
        Button(self, text = "-- Save File To --", command = saveFile).grid(row=4, column=0,columnspan=10, padx=600, pady=5, sticky=W+N+S)
        Label(self, textvariable = self.saveName).grid(row=5, column=0, columnspan=10, padx=700, pady=5, sticky=W+N+S)

        img = Image.open(self.fileName.get())
        image = ImageTk.PhotoImage(img.resize((int(img.size[0]*500.0/img.size[1]), 500),Image.ANTIALIAS))
        self.thumb = Label(self)
        self.thumb.grid(row=0, column=0, padx=20, pady=5, sticky=W)
        self.thumb.configure(image = image)
        self.thumb.image = image

        img = Image.open(self.fileName.get())
        image = ImageTk.PhotoImage(img.resize((int(img.size[0]*500.0/img.size[1]), 500),Image.ANTIALIAS))
        self.thumb_mosaic = Label(self)
        self.thumb_mosaic.grid(row=0, column=0, padx=740, pady=5, sticky=W)
        self.thumb_mosaic.configure(image = image)
        self.thumb_mosaic.image = image


        # Mode
        mode = StringVar(self)
        mode.set('-- Select Mode --')
        menu = OptionMenu(self, mode, 'M1-Average_RGB','M2-Average_HSV','M3-Color_Histogram', 'M4-Color_Layout')
        menu.grid(row=6, column=0, padx=640, pady=5, sticky=W)
        
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
        Button(self, text = "Start Processing Mosaic", command = lambda: startProcessing(mode.get(),self.fileName.get(),self.saveName.get(),int(self.rowEntry.get()),int(self.columnEntry.get()))).grid(row=8, column=0, padx=630, pady=5, sticky=W)

    def isValidate(self, action, index, value_if_allowed,prior_value, text, validation_type, trigger_type, widget_name):
        return True if text in '0123456789' else False


def openFile():
    fileName = tkFileDialog.askopenfilename(initialdir = imgLoc)
    app.fileName.set(fileName)
    img = Image.open(app.fileName.get())
    image = ImageTk.PhotoImage(img.resize((int(img.size[0]*500.0/img.size[1]), 500),Image.ANTIALIAS))
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

def colorHistogram_CountDistance(query, base):
    # H:[0,360] / S:[0,100] / V:[0,255]
    qData = convert(query,"Color_Histogram")
    minValue = ['',float("inf")] #fileName,distance
    for row in xrange(0,len(base),4):
        distance = 0
        for i in xrange(1,4):
            for j in xrange(1,len(base[0])):
                sub = abs(float(qData[i-1][j-1]) - float(base[row+i][j]))
                if i == 1: # H
                    distance += pow( min(sub,360-sub) / 180.0 ,2)
                elif i == 2: # S
                    if j > 100: break
                    distance += pow( sub / 100.0 ,2)
                elif i == 3: # V
                    if j > 255: break
                    distance += pow( sub / 255.0 ,2)
        distance = sqrt(distance)
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

def startProcessing(mode,fileName,saveName,row,column):
    query = Image.open(fileName)
    width, height = query.size
    csvName = ''
    formula = ''
    if mode[1] == "-":
        return -1
    elif mode[1] == "1":      #M1-Avg_RGB
        csvName = 'AverageRGB.csv'
        formula = avgRGB_CountDistance
    elif mode[1] == "2":      #M2-Avg_HSV
        csvName = 'AverageHSV.csv'
        formula = avgHSV_CountDistance
    elif mode[1] == "3":      #M3-Color_Histogram
        csvName = 'ColorHistogram.csv'
        formula = colorHistogram_CountDistance
    elif mode[1] == "4":    #M4-Color_Layout
        csvName = 'ColorLayout.csv'
        formula = colorLayout_CountDistance

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
                print blockBoundary
                imgCrop = query.crop(blockBoundary)
                res = formula(imgCrop,data)
                print (str(i+1)+' x '+str(j+1)+' : '+res[0]+' , Distance = '+str(res[1]))
                imgNew = Image.open(imgLoc + res[0]).resize((blockW, blockH))
                output.paste(imgNew, blockBoundary)

    output.save(saveName, "JPEG", quality=85, optimize=True, progressive=True)

    # Show saved photo
    # showImg(saveName)
    img = Image.open(saveName)
    image = ImageTk.PhotoImage(img.resize((int(img.size[0]*500.0/img.size[1]), 500),Image.ANTIALIAS))
    app.thumb_mosaic.configure(image = image)
    app.thumb_mosaic.image = image

if __name__ == '__main__':
    root = Tk()
    app = Window(root)
    root.geometry("1440x780")
    root.mainloop()
