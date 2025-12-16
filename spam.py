import os, re


class EmailData:
    def __init__(self, sender_name, sender_email, date, body):
        self.sender_name = sender_name
        self.sender_email = sender_email
        self.date = date
        self.body = body
        self.rep = 0

    def __str__(self):
        return f"{self.sender_name}\n{self.sender_email}\n{self.date}\n{self.body}\n\n"
    


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


    while curLine.split(":")[0] != "From":
        curLine = eml.readline()

    idx = curLine.index("<")
    name = curLine[6:idx-1]

    sender = curLine[idx+1:len(curLine)-2]

    
    num = aggregate.index("Content-Type")
    print(num)

    #put data in object
    emailData.append(EmailData(name, sender, date, "test"))

    eml.close()

#print emldata
for eml in emailData:
    print(eml)

