#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os

def printY(str):
    print("your input is: ", str)
    return
    

def userInput():
    str = raw_input("请输入：")
    printY(str)
    return str
    
def open_file():
    file = open("file_a.txt", "a")
    printY(file.name)
    strInput = userInput()
    printY("input " + strInput)
    file.write(strInput)
    file.close()
    return
    
def open_excel():
    file = os.open("Bank.xlsx", os.O_RDONLY)
    content = os.read(file, 100)
    printY(content)
    os.close(file)
    return

# open_file()
# userInput()