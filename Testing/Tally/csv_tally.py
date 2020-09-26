#!/usr/bin/python
'''
Created on Sep 7, 2016

@author: spark343
'''
import csv, glob, os


def cummulativeListSorted():
    entries = []
    for files in glob.glob("*.csv"):
        ifile= open(files, 'rb')
        reader = csv.DictReader(ifile)
        for row in reader:
#            if not ('Student' in reader.fieldnames and
#                'Dignitas Gold (3)' in reader.fieldnames and
#                'Dignitas Silver (1)' in reader.fieldnames and
#                'Gravitas Gold (3)' in reader.fieldnames and
#                'Gravitas Silver (1)' in reader.fieldnames and
#                'Pietas Gold (3)' in reader.fieldnames and
#                'Pietas Silver (1)' in reader.fieldnames):
#                break
            entries.append(row['Student'] + "," +
            row['Positive'])
#            row['Dignitas Silver (1)'] + "," +
#            row['Gravitas Gold (3)'] + "," +
#            row['Gravitas Silver (1)'] + "," +
#            row['Pietas Gold (3)'] + "," +
#            row['Pietas Silver (1)'])
    entries.sort()
    return entries
    
def addZeros(entries):
    output=[]
    for x in entries:
        temp=""
        for y in x.split(','):
            if y is None:
                temp+= "0,"
            elif len(y)>0:
                temp+= y +","
            else:
                temp+= "0,"
                
        output.append(temp[0:len(temp)-1])
    return output


def tallyList(entries):
    output=["Student," +
            "Positive,"]
#            "Dignitas Silver (1)," +
#            "Gravitas Gold (3)," +
#            "Gravitas Silver (1)," +
#            "Pietas Gold (3)," +
#            "Pietas Silver (1),"]
    i=0
    for x in entries:
        print type(x)
        if (x.split(',')[0]==output[i].split(',')[0]):
            output[i]=output[i].split(',')[0] + ',' + \
            str(int(output[i].split(',')[1]) + int(x.split(',')[1]))
            #str(int(output[i].split(',')[2]) + int(x.split(',')[2])) + ',' + \
            #str(int(output[i].split(',')[3]) + int(x.split(',')[3])) + ',' + \
            #str(int(output[i].split(',')[4]) + int(x.split(',')[4])) + ',' + \
            #str(int(output[i].split(',')[5]) + int(x.split(',')[5])) + ',' + \
            #str(int(output[i].split(',')[6]) + int(x.split(',')[6]))
        else:
            output.append(x)
            i+=1

    I=open('StudentTotal.csv', 'w')
    for i in output:
        I.write(i + "\n")
    return output

def main():
    students=tallyList(cummulativeListSorted())
#    tallies=tallyList(students)    

if __name__ == "__main__":
    main()
