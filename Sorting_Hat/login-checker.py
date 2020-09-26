#!/usr/bin/python
# coding=utf-8
'''
Created on Sep 7, 2016

@author: spark343
'''
import csv, glob, os, datetime, subprocess, imacros

def login(login, password,class_num):
    lines=[]

    lines.append("SET !REPLAYSPEED MEDIUM\n" +
                #"SET !TIMEOUT_STEP 0\n" +
                #"SET !ERRORIGNORE YES\n" +
                #"TAB T=1\n" +
                "URL GOTO=https://www.classdojo.com/\n" +
                "TAG POS=1 TYPE=A ATTR=ID:page-header-login-button\n" +
                "TAG POS=2 TYPE=INPUT:TEXT ATTR=* CONTENT=" + login + "\n" +
                "SET !ENCRYPTION NO\n" +
                "TAG POS=1 TYPE=INPUT:PASSWORD ATTR=* CONTENT=" + password + "\n" +
                "TAG POS=1 TYPE=BUTTON ATTR=TXT:Log<SP>in\n")# +
                #"TAG POS=1 TYPE=IMG ATTR=SRC:https://teach-static.classdojo.com/2961a6408144bfc97987a05f60a6ce9d.png\n")

    with open("/home/spark343/iMacros/Macros/#Classdojo.iim", 'w') as outfile:
    	for line in lines:
    		outfile.write(line)
def logins():
    ifile= open("Teachers.csv", 'rb')
    logins = list(csv.reader(ifile))


    for user in logins:
    	login(user[0],user[1],user[2])
    	subprocess.call("firefox imacros://run/?m=#Classdojo.iim", shell=True)
    	#subprocess.call("sleep 1", shell=True)

def main():
    #students=addZeros(cummulativeListSorted())
    #tallies=tallyList(students)
    logins()

if __name__ == "__main__":
    main()
