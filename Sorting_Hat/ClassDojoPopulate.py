#!/usr/bin/python
# coding=utf-8
'''
Created on Sep 7, 2016

@author: spark343
'''
import csv, glob, os, datetime, subprocess

def main():
    ifile= open("final.csv", 'rb')
    Courses = list(csv.reader(ifile))
    lines=[]
    for course in Courses:
        lines.append("VERSION BUILD=9030808 RECORDER=FX\n" +
            "SET !REPLAYSPEED SLOW\n" +
            "SET !TIMEOUT_STEP 0\n" +
            "SET !ERRORIGNORE YES\n" +
            #"TAB T=1\n" +
            "URL GOTO=https://www.classdojo.com/\n" +
            "TAG POS=1 TYPE=A ATTR=ID:page-header-login-button\n" +
            "TAG POS=2 TYPE=INPUT:TEXT ATTR=* CONTENT=" + course[0] + "\n" +
            "SET !ENCRYPTION NO\n" +
            "TAG POS=1 TYPE=INPUT:PASSWORD ATTR=* CONTENT=" + course[1] + "\n" +
            "TAG POS=1 TYPE=BUTTON ATTR=TXT:Log<SP>in\n")
        lines.append(
            #"URL GOTO=https://teach.classdojo.com/#/launchpad\n" +
            "TAG POS=1 TYPE=DIV ATTR=TXT:" + course[2].replace(" ","<SP>") + "\n" +
            "TAG POS=1 TYPE=IMG ATTR=SRC:https://teach-static.classdojo.com/c7368053a3cc09b15dd6497f5fbfe0fe.png\n" +
            "TAG POS=1 TYPE=SPAN ATTR=TXT:Edit<SP>class\n" +
            "SET !REPLAYSPEED FAST\n")

        for x in xrange(1,50):
            lines.append(
                "EVENT TYPE=CLICK SELECTOR=\"HTML>BODY>DIV:nth-of-type(4)>DIV>DIV>DIV:nth-of-type(2)>DIV>DIV>DIV>DIV>DIV>DIV>DIV>DIV:nth-of-type(2)\" BUTTON=0\n" +
                "EVENT TYPE=CLICK SELECTOR=\"HTML>BODY>DIV:nth-of-type(5)>DIV>DIV>DIV:nth-of-type(3)>DIV>DIV>A>DIV>DIV>SPAN\" BUTTON=0\n" +
                "EVENT TYPE=CLICK SELECTOR=\"HTML>BODY>DIV:nth-of-type(6)>DIV>DIV>DIV:nth-of-type(3)>DIV>DIV:nth-of-type(3)>BUTTON\" BUTTON=0\n")

        lines.append(
            #"TAG POS=1 TYPE=IMG ATTR=SRC:https://teach-static.classdojo.com/f3bc748410ad4803c928f1153e789c9f.png\n" +
            #"EVENT TYPE=CLICK SELECTOR=\"HTML>BODY>DIV>DIV>DIV>DIV>DIV:nth-of-type(2)>DIV>DIV>DIV>DIV>DIV:nth-of-type(2)>DIV>DIV:nth-of-type(2)>INPUT\" BUTTON=0\n" +
            #"EVENTS TYPE=KEYPRESS SELECTOR=\"HTML>BODY>DIV>DIV>DIV>DIV>DIV:nth-of-type(2)>DIV>DIV>DIV>DIV>DIV:nth-of-type(2)>DIV>DIV:nth-of-type(2)>INPUT\" CHARS=\"" + course[2] + "\"\n" +
            #"EVENT TYPE=CLICK SELECTOR=\"HTML>BODY>DIV>DIV>DIV>DIV>DIV:nth-of-type(2)>DIV>DIV>DIV>DIV>DIV:nth-of-type(3)>DIV>DIV:nth-of-type(2)>DIV>DIV>DIV\" BUTTON=0\n" +
            #"EVENT TYPE=MOUSEDOWN SELECTOR=\"HTML>BODY>DIV>DIV>DIV>DIV>DIV:nth-of-type(2)>DIV>DIV>DIV>DIV>DIV:nth-of-type(3)>DIV>DIV:nth-of-type(2)>DIV>DIV:nth-of-type(2)>DIV>DIV:nth-of-type(15)\" BUTTON=0\n"
            #"TAG POS=1 TYPE=BUTTON ATTR=TXT:Add<SP>class\n" +
            "SET !REPLAYSPEED MEDIUM\n" +
            "TAG POS=1 TYPE=SPAN ATTR=TXT:Import<SP>student<SP>list\n" +
            "EVENT TYPE=CLICK SELECTOR=\"HTML>BODY>DIV:nth-of-type(4)>DIV>DIV>DIV:nth-of-type(2)>DIV>DIV>DIV>DIV:nth-of-type(4)>TEXTAREA\" BUTTON=0\n" +
            "EVENTS TYPE=KEYPRESS SELECTOR=\"HTML>BODY>DIV:nth-of-type(4)>DIV>DIV>DIV:nth-of-type(2)>DIV>DIV>DIV>DIV:nth-of-type(4)>TEXTAREA\" CHARS=\"" + ','.join(course[3:len(course)]) + "\"\n" +
            "TAG POS=1 TYPE=BUTTON ATTR=TXT:Import<SP>list\n" +
            "TAG POS=1 TYPE=BUTTON ATTR=TXT:Continue\n" +
            "TAG POS=1 TYPE=BUTTON ATTR=TXT:Done<SP>adding<SP>students\n")
            #"TAG POS=1 TYPE=IMG ATTR=SRC:https://teach-static.classdojo.com/fa5a8149fa7d0cd6effa7271ef78cea7.png\n")
    with open("/home/spark343/iMacros/Macros/#ClassDojoPopulate.iim", 'w') as outfile:
        for line in lines:
            outfile.write(line)


if __name__ == "__main__":
    main()
