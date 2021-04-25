import os
import webbrowser

# change name and directory of created html file, directory to your documentation, and directory
# to preferred browser
htmlName = "C:/Users/macie/Documents/Documentation/documentation.html"
dir = "C:/Users/macie/Documents/Documentation"
edgePath = "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"


# creates .html file and writes basic html template
def startFile():
    file = open(htmlName, 'w')
    file.write("<!DOCTYPE html>\n")
    file.write("<html>\n")
    file.write("<head>\n")
    file.write("<title>Electronic documentation</title>\n")
    file.write("</head>\n")
    file.write("<body>\n")
    file.write("<ul>\n")
    return file


# writes basic template and closes .html file
def closeFile():
    file.write("</ul>\n")
    file.write("</body>\n")
    file.write("</html>\n")

#starts html list with 'name' header
def startList(name):
    file.write("<p></p> <li><ul><h><b>" + name + "</b></h>\n")

#closes list
def closeList():
    file.write("</ul></li>\n")

#adds pdf file to a list
def addItem(directory, doc):
    buffer = "<li><a href=\"" + getAddress(directory, doc) + "\" target = \"_blank\">" + doc[:-4]
    file.write(buffer + "</a></li>\n")

def getAddress(directory, doc):
    result = directory + '/' + doc
    if os.name == "nt":
        result = result.replace('/', '\\')
    return result

def addDescripion(descLines, doc):
    for line in descLines:
        index = line.find(doc)
        if index > -1:
            file.write(line[index + len(doc):] + "<p></p>")
            return 1
    return 0


#main recursive function
def rek(dir):
    result = list(os.walk(dir))[0]
    if result[1]:
        for subDir in result[1]:
            startList(subDir)
            rek(dir + '/' + subDir)
            closeList()
    else:
        if not result[2]:
            addItem(result[0], "empty.pdf")
        description = 0
        descriptionFound = 0
        for doc in result[2]:
            if doc == "description.txt":
                descriptionFound = 1
                descriptionFile = open(getAddress(result[0], doc), 'r+')
                description = descriptionFile.readlines()
                break
        if not descriptionFound:
            descriptionFile = open(getAddress(result[0], "description.txt"), 'w')
            description = ("none", "none")
        for doc in result[2]:
            if doc[-3:] == "pdf":
                addItem(result[0], doc)
                if description:
                    if not addDescripion(description, doc[:-4]):
                        descriptionFile.write(doc[:-4] + '\n')
        descriptionFile.close()


file = startFile()
rek(dir)
closeFile()
webbrowser.register('edge', None, webbrowser.BackgroundBrowser(edgePath))
webbrowser.get('edge').open_new_tab(htmlName)
