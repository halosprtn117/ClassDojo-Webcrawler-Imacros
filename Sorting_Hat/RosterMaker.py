#!/usr/bin/python
# coding=utf-8
'''
Created on Sep 7, 2016

@author: spark343
'''
import csv, glob, os, datetime, subprocess

def main():
	ifile=open("Original.csv", 'rb')
	lines=csv.reader(ifile)
	

	temp1=[]
	for line in lines:
		temp1.append(line[4].split(",")[0] + "-Period " + line[5][0] + "," + line[1].split(",")[1].split(" ")[1] + " " + line[1].split(",")[0])

	temp1.sort()

	courses=[]
	entry=""
	temp=list("Classname")

	for line in temp1:

		if line.split(",")[0]!=temp:
			if len(entry) != 0:
				courses.append(entry +"\n")
			temp=line.split(",")[0]
			entry=line.split(",")[0] + "," + line.split(",")[1]
		else:
			entry+= "," + line.split(",")[1]
	courses.append(entry +"\n")

	final=[]
	for course in courses:
		ifile.close()
		ifile=open("Teachers.csv", 'rb')
		teachers=csv.reader(ifile)
		for teacher in teachers:
			if course.split("-")[0] == teacher[3]:
				final.append(teacher[0] + "," + teacher[1] + "," + course)











	with open("final.csv", 'w') as outfile:
		for x in final:
			outfile.write(x)

if __name__ == "__main__":
    main()

#lastname=line[1].split(",")[0]
#firstname=line[1].split(",")[1].split(" ")[1]
#teacher=line[4].split(",")[0]
#period=line[5][0]

