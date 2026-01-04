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
        return f"Sender: {self.sender_name}\nEmail: {self.sender_email}\nDate: {self.date}\nSubject: {self.subject}\n{self.body}\n\n"
    


path = os.path.dirname(os.path.abspath(__file__))
print(path)


emails = os.listdir(path + "\\Emails2\\")
print(emails)

emailData = []

#collect data
for file in emails:
    eml = open(path + "\\Emails2\\" + file)

    print("opened")
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
        
        #skip past some stuff (skip to open boundary, skip to new line/contents)
        curLine = eml.readline()
        while boundary not in curLine:
            curLine = eml.readline()
        while curLine != "\n":
            curLine = eml.readline()

        curLine = eml.readline()

        while boundary not in curLine:
            body+=curLine
            curLine = eml.readline()
            

    elif "text" in bodytype:
        while curLine != "\n":
            curLine = eml.readline()

        for line in eml:
            body+=line
    else:
        body = "not found"


    #put data in object
    emailData.append(EmailData(name, sender, date, subject, body))

    print("closed")
    eml.close()



#print emldata
for eml in emailData:
    print(eml)


    

file = open(path + "\\spamkeywords.txt")
contents = file.read()
file.close()
spamwords = contents.split("\n")

for eml in emailData:
    sc = 0
    for word in spamwords:
        matchlist = re.findall(word, eml.body, flags=re.IGNORECASE) + re.findall(word, eml.subject, flags=re.IGNORECASE)
        sc+=len(matchlist)
    
    #ratio of spam keywords to words
    wc = len(re.findall("\s", eml.body))
    print(str(sc) + "/" + str(wc) + "=" + str(sc/wc))



#ADD TIME SUSPICION
#CHANGE REP by SPAM RATIO, BLOCKED EMAILS, DATE, IP?