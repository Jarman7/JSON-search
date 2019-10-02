import re

def main():
    searchParameters = findParameters()
    print(searchParameters)
    searchFile(searchParameters)


def findParameters():
    searchParameters = []
    returnParameters = {}
    f = open("Config.txt", "r")
    for i in range(10):
        line = f.readline()
        if len(re.findall("Search [0-9]+:", line)) > 0:
            searchTermWithNewline = re.sub("Search [0-9]+:", "", line)
            searchTerm = re.sub("\n", "", searchTermWithNewline)
            if len(searchTerm) > 0:
                searchParameters.append(searchTerm)

        elif len(re.findall("Filename:", line)) > 0:
            filenameWithNewline = re.sub("Filename:", "", line)
            filename = re.sub("\n", "", filenameWithNewline)
            if len(filename) > 0:
                returnParameters["filename"] = filename
    f.close()
    returnParameters["parameters"] = searchParameters
    return returnParameters

def searchFile(searchParameters):
    searchParametersList = searchParameters["parameters"]
    numOfSearchParameters = len(searchParametersList)
    r = open(searchParameters["filename"], "r")
    w = open("Output.txt", "w")
    line = r.readline()
    record = []
    while line:
        counter = 0
        while counter < numOfSearchParameters:
            if len(re.findall("( )*"+searchParametersList[counter], line)) > 0:
                searchTermName = re.sub(":(?s).*", "", searchParametersList[counter])
                searchTermWithNewline = re.sub("( )*"+searchTermName+":( )*", "", line)
                searchTerm = re.sub("\n", "", searchTermWithNewline)

                if len(re.findall("\([0-9]*\)", searchTerm)) > 0:
                    numberOfAdditionalTerms = int(searchTerm[1:-1])
                    searchTerm = ""
                    for i in range(numberOfAdditionalTerms):
                        line = r.readline()
                        searchTerm += re.sub("( )*", "",line) + ", "
                        searchTerm = re.sub("\n", "", searchTerm)

                if counter == numOfSearchParameters - 1 and searchTerm:
                    record.append(searchTerm+"\n")
                    if len(record) == numOfSearchParameters:
                        w.write(convertRecordToString(record))
                        record = []
                    else:
                        record = []

                elif searchTerm and counter == 0:
                    record = [searchTerm]

                elif searchTerm:
                    record.append(searchTerm+", ")


            counter += 1
        line = r.readline()

def convertRecordToString(record):
    returnString = ""
    for item in record:
        returnString += item

    returnString = returnString[:-1]+"\n"
    return returnString

if __name__ == "__main__":
    main()