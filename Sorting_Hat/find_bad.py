import csv, glob, os, datetime, subprocess

def cummulativeListSorted():
    os.chdir("Classdojo_CSV")
    entries = []
    for files in glob.glob("*.csv"):
        ifile= open(files, 'rb')
        reader = csv.DictReader(ifile)
        for row in reader:
            if not ('Student' in reader.fieldnames and
                'Dignitas Gold (3)' in reader.fieldnames and
                'Dignitas Silver (1)' in reader.fieldnames and
                'Gravitas Gold (3)' in reader.fieldnames and
                'Gravitas Silver (1)' in reader.fieldnames and
                'Pietas Gold (3)' in reader.fieldnames and
                'Pietas Silver (1)' in reader.fieldnames):
                print ifile
#                print row
                break
            entries.append(row['Student'] + "," +
            row['Dignitas Gold (3)'] + "," +
            row['Dignitas Silver (1)'] + "," +
            row['Gravitas Gold (3)'] + "," +
            row['Gravitas Silver (1)'] + "," +
            row['Pietas Gold (3)'] + "," +
            row['Pietas Silver (1)'])
    entries.sort()
    return entries




def main():
    students=cummulativeListSorted()
    #tallies=tallyList(students)

if __name__ == "__main__":
    main()
