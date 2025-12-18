import os, re


class EmailData:
    def __init__(self, sender_name, sender_email, date, subject, body):
        self.sender_name = sender_name
        self.sender_email = sender_email
        self.date = date
        self.subject = subject
        self.body = body
        self.rep = 0

    def __str__(self):
        return f"{self.sender_name}\n{self.sender_email}\n{self.date}\n{self.subject}\n{self.body}\n\n"
    


path = os.path.dirname(os.path.abspath(__file__))
print(path)


emails = os.listdir(path + "\\Emails\\")
print(emails)

emailData = []

#collect data
for file in emails:
    eml = open(path + "\\Emails\\" + file)

    aggregate = eml.read()
    eml.seek(0)

    curLine = eml.readline()

    while curLine.split(":")[0] != "Date":
        curLine = eml.readline()
    
    date = curLine.split(": ")[1]



    # date and from are ordered differently sometimes, return to start
    eml.seek(0)

    while curLine.split(":")[0] != "Subject":
        curLine = eml.readline()
    
    subject = curLine[curLine.index(":")+2:]



    eml.seek(0)

    while curLine.split(":")[0] != "From":
        curLine = eml.readline()

    idx = curLine.index("<")
    name = curLine[6:idx-1]

    sender = curLine[idx+1:len(curLine)-2]

    #inconsistent position again
    eml.seek(0)
    while curLine.split(":")[0] != "Content-Type":
        curLine = eml.readline()

    body = ""
    bodytype = curLine.split(": ")[1]

    if "multipart" in bodytype:
        if "boundary" in bodytype:
            boundary = curLine[curLine.index("=")+2:len(curLine)-2]
        else:
            #some boundaries are on the next line
            curLine = eml.readline()
            boundary = curLine[curLine.index("=")+2:len(curLine)-2]
        
        print(eml.readline())
        eml.readline()
        while boundary not in curLine:
            curLine = eml.readline()
            print(curLine)
            body+=curLine
            #ABOVE DOES NOT WORK YET

        print(boundary)
    elif "text" in bodytype:
        body = "htmlfiller"
    else:
        body = "not found"


    #put data in object
    emailData.append(EmailData(name, sender, date, subject, body))

    eml.close()

#print emldata
for eml in emailData:
    print(eml)

