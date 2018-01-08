#!/usr/bin/env python
#-*- coding: utf-8 -*-

from datalib import *
import os
import numpy as np
import pandas

path = "./dataset/img/"
#path,dirs,dataset = os.walk(path).next()
fileNum = 1000
fileNamePrefix = 'ukbench'
csvLocation = "./dataset/"

# Average_RGB
if not os.path.exists(csvLocation + "AverageRGB.csv"):
    for i in xrange(fileNum):
        fileName = fileNamePrefix + '0'*(5-len(str(i))) + str(i) + '.jpg'
        data = pandas.DataFrame(convert(fileName, "Average_RGB"))
        with open(csvLocation + "AverageRGB.csv", 'a') as save:
            data.to_csv(save, header=True, index_label=fileName)

else:
    while os.path.exists(csvLocation + "AverageRGB.csv"):
        option = raw_input("AverageRGB.csv has existed, would you like to override it ? (Y/N)")
        print option
        if (option == "y" or option == "Y" ):
            os.remove(csvLocation + "AverageRGB.csv")
            for i in xrange(fileNum):
                fileName = fileNamePrefix + '0'*(5-len(str(i))) + str(i) + '.jpg'
                data = pandas.DataFrame(convert(fileName, "Average_RGB"))
                with open(csvLocation + "AverageRGB.csv", 'a') as save:
                    data.to_csv(save, header=True, index_label=fileName)
            break
        elif (option == "n" or option == "N" ):
            break

# Average_HSV
if not os.path.exists(csvLocation + "AverageHSV.csv"):
    for i in xrange(fileNum):
        fileName = fileNamePrefix + '0'*(5-len(str(i))) + str(i) + '.jpg'
        data = pandas.DataFrame(convert(fileName, "Average_HSV"))
        with open(csvLocation + "AverageHSV.csv", 'a') as save:
            data.to_csv(save, header=True, index_label=fileName)

else:
    while os.path.exists(csvLocation + "AverageHSV.csv"):
        option = raw_input("AverageHSV.csv has existed, would you like to override it ? (Y/N)")
        print option
        if (option == "y" or option == "Y" ):
            os.remove(csvLocation + "AverageHSV.csv")
            for i in xrange(fileNum):
                fileName = fileNamePrefix + '0'*(5-len(str(i))) + str(i) + '.jpg'
                data = pandas.DataFrame(convert(fileName, "Average_HSV"))
                with open(csvLocation + "AverageHSV.csv", 'a') as save:
                    data.to_csv(save, header=True, index_label=fileName)
            break
        elif (option == "n" or option == "N" ):
            break

# Color_Histogram
if not os.path.exists(csvLocation + "ColorHistogram.csv"):
    for i in xrange(fileNum):
        fileName = fileNamePrefix + '0'*(5-len(str(i))) + str(i) + '.jpg'
        data = pandas.DataFrame(convert(fileName, "Color_Histogram"))
        with open(csvLocation + "ColorHistogram.csv", 'a') as save:
            data.to_csv(save, header=True, index_label=fileName)

else:
    while os.path.exists(csvLocation + "ColorHistogram.csv"):
        option = raw_input("ColorHistogram.csv has existed, would you like to override it ? (Y/N)")
        print option
        if (option == "y" or option == "Y" ):
            os.remove(csvLocation + "ColorHistogram.csv")
            for i in xrange(fileNum):
                fileName = fileNamePrefix + '0'*(5-len(str(i))) + str(i) + '.jpg'
                data = pandas.DataFrame(convert(fileName, "Color_Histogram"))
                with open(csvLocation + "ColorHistogram.csv", 'a') as save:
                    data.to_csv(save, header=True, index_label=fileName)
            break
        elif (option == "n" or option == "N" ):
            break


# Color_Layout
if not os.path.exists(csvLocation + "ColorLayout.csv"):
    for i in xrange(fileNum):
        fileName = fileNamePrefix + '0'*(5-len(str(i))) + str(i) + '.jpg'
        data = pandas.DataFrame(convert(fileName, "Color_Layout"))
        with open(csvLocation + "ColorLayout.csv",'a') as save:
            data.to_csv(save,header=True,index_label = fileName)
else:
    while os.path.exists(csvLocation + "ColorLayout.csv"):
        option = raw_input("ColorLayout.csv has existed, would you like to override it ? (Y/N)")
        print option
        if (option == "y" or option == "Y" ):
            os.remove(csvLocation + "ColorLayout.csv")
            for i in xrange(fileNum):
                fileName = fileNamePrefix + '0'*(5-len(str(i))) + str(i) + '.jpg'
                data = pandas.DataFrame(convert(fileName, "Color_Layout"))
                with open(csvLocation + "ColorLayout.csv",'a') as save:
                    data.to_csv(save,header=True,index_label = fileName)
            break
        elif (option == "n" or option == "N" ):
            break
