#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sys import platform as sys_pf
if sys_pf == 'darwin':
    import matplotlib
    matplotlib.use("TkAgg")

import os
from pylab import *
import pickle
from Tkinter import *
from PIL import ImageTk,Image
import tkMessageBox
import tkFileDialog
from ttk import Frame, Button, Label, Style

global imgs
global thumb

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
        Button(self, text = "-- Select File --", command = openFile).grid(row=2, column=0, padx=650, pady=5, sticky=W)
        Label(self, textvariable = self.fileName).grid(row=3, column=0, columnspan=10, padx=600, pady=5, sticky=W+E+N+S)
        # Save File
        self.saveName = StringVar(value = "./example_Mosaic.jpg")
        Button(self, text = "-- Save File To --", command = saveFile).grid(row=4, column=0, padx=650, pady=5, sticky=W)
        Label(self, textvariable = self.saveName).grid(row=5, column=0, columnspan=10, padx=600, pady=5, sticky=W+E+N+S)

        img = Image.open(self.fileName.get())
        image = ImageTk.PhotoImage(img.resize((img.size[0]/2, img.size[1]/2),Image.ANTIALIAS))
        self.thumb = Label(self)
        self.thumb.grid(row=0, column=0, padx=720-img.size[0]/4, pady=5, sticky=W+E+N+S)
        self.thumb.configure(image = image)
        self.thumb.image = image

        
        # Mode
        mode = StringVar(self)
        mode.set('-- Select Mode --')
        menu = OptionMenu(self, mode, 'Q1-Average_RGB','Q2-Average_HSV','Q3-Color_Histogram', 'Q4-Color_Layout')
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
        Button(self, text = "Start Processing Mosaic", command = lambda: startSearching(mode.get(),self.fileName.get())).grid(row=8, column=0, padx=630, pady=5, sticky=W)

#        # Return Ranking List
#        self.imgs = []
#        for i in xrange(10):
#            self.imgs.append(Label(self))
#            self.imgs[i].grid(row = i / 5 + 4, column = i % 5 , padx=10, pady=20)

    def isValidate(self, action, index, value_if_allowed,prior_value, text, validation_type, trigger_type, widget_name):
        return True if text in '0123456789' else False


def openFile():
    fileName = tkFileDialog.askopenfilename(initialdir = "./dataset/img/")
    app.fileName.set(fileName)
    image = Image.open(app.fileName.get())
    image = ImageTk.PhotoImage(image.resize((image.size[0]/2, image.size[1]/2),Image.ANTIALIAS))
    app.thumb.configure(image = image)
    app.thumb.image = image

def saveFile():
    fileName = 'Mosaic.jpg'
    saveName = tkFileDialog.asksaveasfile(initialdir = "./",filetypes=[("Image","*.jpg")],initialfile=fileName)
    app.saveName.set(saveName.name)


#def Q1_CountDistance(query, base):
#    minTotal = 0
#    qTotal = 0
#    bTotal = 0
#    queryColor = query.histogram()
#    baseColor = base.histogram()
#    for i in xrange(0,len(baseColor)):
#        q = queryColor[i]
#        b = baseColor[i]
#        minTotal += min(q,b)
#        qTotal += q
#        bTotal += b
#    return 1 - float(minTotal / float(min(qTotal,bTotal)))

def colorLayout_CountDistance(query, base, weight):
    #Eular Distance
    dis = 0
    for i in xrange(1,len(query)):
        dis += weight[i-1] / 10 * pow(float(query[i]) - float(base[i]),2)
    return sqrt(dis)


def maxInList(list):
    max = [0,0.0] #[index,value]
    for l in list:
        if l[1] > max[1]:
            max = [list.index(l),l[1]]
    return max[0]

def minInList(list):
    min = [0,float("inf")] #[index,value]
    for l in list:
        if l[1] < min[1]:
            min = [list.index(l),l[1]]
    return min[0]

def startSearching(mode,fileName):
    query = Image.open(fileName)
    path,dirs,dataset = os.walk(fileName[:-16]).next()
    fileName = fileName[-16:]
    #print fileName
    res = []
    if mode[1] == "-":
        return -1
    
    if mode[1] == "1":      #Q1-Avg_RGB
        print('1')

    elif mode[1] == "2":      #Q2-Avg_HSV
        print('2')

    
    elif mode[1] == "3":      #Q3-Color_Histogram
        print('3')
#        res = [["",float("inf")] for i in xrange(10)] #[fileName,distance]
#        for imgName in dataset:
#            img = Image.open(path+'/'+imgName)
#            distance = Q1_CountDistance(query,img)
#            #print distance
#            index = maxInList(res)
#            if distance < res[index][1]:
#                res[index] = [imgName,distance]
#        res = sorted(res,key = lambda x: x[1])

    elif mode[1] == "4":    #Q4-Color_Layout
        print('4')
#        res = [["",float("inf")] for i in xrange(10)] #[fileName,distance]
#        qIndex = int(fileName[7:-4]) * 4 #Query index
#        with open('./dataset/Q2.csv', 'rb') as csvfile:
#            Reader = csv.reader(csvfile)
#            data = [row for row in Reader]
#            for row in xrange(0,len(data),4):
#                distance = 0
#                for i in xrange(0,4):
#                    distance += colorLayout_CountDistance(data[qIndex+i], data[row+i], [j for j in xrange(len(data[0])-1,0,-1)])
#                index = maxInList(res)
#                #print res[index][1]
#                if distance < res[index][1]:
#                    res[index] = [data[row][0],distance]
#        res = sorted(res,key = lambda x: x[1])


    print "#  Query: " + fileName + " / " + mode
#    print res

#    for i in xrange(10):
#        imgName = path + res[i][0]
#        image = Image.open(imgName)
#        image = ImageTk.PhotoImage(image.resize((int(image.size[0]*0.85), int(image.size[1]*0.85)),Image.ANTIALIAS))
#        app.imgs[i].configure(image = image)
#        app.imgs[i].image = image

if __name__ == '__main__':
    root = Tk()
    app = Window(root)
    root.geometry("1920x1080")
    root.mainloop()

  
