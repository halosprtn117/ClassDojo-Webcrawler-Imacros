#!/usr/bin/python
# coding=utf-8
'''
Created on Sep 7, 2016

@author: spark343
'''
import csv, glob, os, datetime, subprocess

def cummulativeListSorted():
    os.chdir("Classdojo_CSV")
    entries = []
    teachers = []
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
            teachers.append(files.split('-')[2] + "," +
                row['Positive'])
            entries.append(row['Student'] + "," +
                row['Positive'])
#            row['Dignitas Gold (3)'] + "," +
#            row['Dignitas Silver (1)'] + "," +
#            row['Gravitas Gold (3)'] + "," +
#            row['Gravitas Silver (1)'] + "," +
#            row['Pietas Gold (3)'] + "," +
#            row['Pietas Silver (1)'])
    entries.sort()
    teachers.sort()

    output=["Teacher," + "Positive,"]
    i=0
    for x in teachers:
        if (x.split(',')[0]==output[i].split(',')[0]):
            output[i]=output[i].split(',')[0] + ',' + \
            str(int(output[i].split(',')[1]) + int(x.split(',')[1]))
        else:
            output.append(x)
            i+=1    
    
    I=open('TeacherTotal.csv', 'w')
    for i in output:
        I.write(i + "\n")

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

#            "Dignitas Gold (3)," +
#            "Dignitas Silver (1)," +
#            "Gravitas Gold (3)," +
#            "Gravitas Silver (1)," +
#            "Pietas Gold (3)," +
#            "Pietas Silver (1),"]
    i=0
    for x in entries:
        if (x.split(',')[0]==output[i].split(',')[0]):
            output[i]=output[i].split(',')[0] + ',' + \
            str(int(output[i].split(',')[1]) + int(x.split(',')[1]))
#            str(int(output[i].split(',')[1]) + int(x.split(',')[1])) + ',' + \
#            str(int(output[i].split(',')[2]) + int(x.split(',')[2])) + ',' + \
#            str(int(output[i].split(',')[3]) + int(x.split(',')[3])) + ',' + \
#            str(int(output[i].split(',')[4]) + int(x.split(',')[4])) + ',' + \
#            str(int(output[i].split(',')[5]) + int(x.split(',')[5])) + ',' + \
#            str(int(output[i].split(',')[6]) + int(x.split(',')[6]))
        else:
            output.append(x)
            i+=1

    I=open('StudentTotal.csv', 'w')
    for i in output:
        I.write(i + "\n")
    return output

def findStudent():
    studenttotal=[]
    with open("StudentTotal.csv", 'rb') as ifile:
    	for line in csv.reader(ifile):
        	studenttotal.append(line)

    students=[]
    with open("../Students.csv", 'rb') as ifile:
    	for line in csv.reader(ifile):
        	students.append(line) 

    final=["Student," +
            "Grade," +
            "Positive,"]
#            "Dignitas Gold (3)," +
#            "Dignitas Silver (1)," +
#            "Gravitas Gold (3)," +
#            "Gravitas Silver (1)," +
#            "Pietas Gold (3)," +
#            "Pietas Silver (1),"]

    for lines in studenttotal:
        for student in students:
			if lines[0] ==student[0]:
				final.append(student + lines[1:])

    with open("StudentTotal.csv", 'w') as outfile:
        writer=csv.writer(outfile,delimiter=',')
        outfile.write("Student," +
            "Grade," +
            "Positive," + "\n")
#            "Dignitas Gold (3)," +
#            "Dignitas Silver (1)," +
#            "Gravitas Gold (3)," +
#            "Gravitas Silver (1)," +
#            "Pietas Gold (3)," +
#            "Pietas Silver (1)," + "\n")
        writer.writerows(final[1:])


def login(login, password,class_num):
    lines=[]
    today = datetime.date.today()
    first = today.replace(day=1)
    lastmonth = (first - datetime.timedelta(days=1)).strftime("%B")
    #lastmonth = "January"

    lines.append("VERSION BUILD=9030808 RECORDER=FX\n" +
    			"SET !TIMEOUT_PAGE 10\n" +
                "SET !TIMEOUT_STEP 100\n" +
                "SET !REPLAYSPEED FAST\n" +
                "SET !ERRORIGNORE NO\n" +
                "TAB T=1\n" +
                "URL GOTO=https://www.classdojo.com/\n" +
                "TAG POS=1 TYPE=A ATTR=ID:page-header-login-button\n" +
                "TAG POS=2 TYPE=INPUT:TEXT ATTR=* CONTENT=" + login + "\n" +
                "SET !ENCRYPTION NO\n" +
                "TAG POS=1 TYPE=INPUT:PASSWORD ATTR=* CONTENT=" + password + "\n" +
                "TAG POS=1 TYPE=BUTTON ATTR=TXT:Log<SP>in\n")
    i=1
    while i <= int(class_num):
        lines.append("TAG POS=" + str(i) + " TYPE=IMG ATTR=SRC:https://teach-static.classdojo.com/a9f65cb8abb215a590f49ccd73f6a5aa.png\n" +
            "TAG POS=1 TYPE=SPAN ATTR=TXT:View<SP>reports\n" +
            "SET !ERRORIGNORE YES\n" +
            "SET !TIMEOUT_STEP 0\n" +
            "TAG POS=2 TYPE=SPAN ATTR=TXT:This<SP>week\n" +
            "TAG POS=1 TYPE=SPAN ATTR=TXT:Last<SP>month<SP>(" + lastmonth +")\n" +
            "SET !ERRORIGNORE NO\n" +
            "SET !TIMEOUT_STEP 100\n" +
            "TAG POS=1 TYPE=SPAN ATTR=TXT:View<SP>spreadsheet\n" +
            "TAG POS=1 TYPE=BUTTON ATTR=TXT:×\n" +
            "TAG POS=1 TYPE=SPAN ATTR=TXT:Your<SP>classes\n")
        i+=1
    lines.append("TAB CLOSE\n"+
            "WAIT SECONDS=10\n")
    with open("/home/spark343/iMacros/Macros/#Classdojo.iim", 'w') as outfile:
    	for line in lines:
    		outfile.write(line)





def logins():
    subprocess.call("mv ~/Downloads/*.csv ~/Downloads/temp", shell=True)
    subprocess.call("rm ~/Desktop/Sorting_Hat/Classdojo_CSV/*.csv", shell=True)
    ifile= open("Teachers.csv", 'rb')
    logins = list(csv.reader(ifile))


    for user in logins:
    	login(user[0],user[1],user[2])
    	subprocess.call("firefox imacros://run/?m=#Classdojo.iim", shell=True)
    	subprocess.call("sleep 1", shell=True)


    subprocess.call("mv ~/Downloads/*.csv /home/spark343/Desktop/Sorting_Hat/Classdojo_CSV/", shell=True)

    #findStudent(tallyList(addZeros(cummulativeListSorted())))
    tallyList(addZeros(cummulativeListSorted()))
    findStudent()

def main():
    #students=addZeros(cummulativeListSorted())
    #tallies=tallyList(students)
    logins()

if __name__ == "__main__":
    main()
