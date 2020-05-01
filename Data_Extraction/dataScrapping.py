import re
from bs4 import BeautifulSoup
import urllib.request
from pymongo import MongoClient
import json
import time
from datetime import datetime

client = MongoClient('mongodb://karthi:secret@54.234.91.148/myDB')
# client = MongoClient(port=27017)
db = client['myDB']
bookDataDoc = db.bookData
fileDataDoc = db.fileData
# home_pageURL = urllib.request.Request("http://www.gutenberg.org/wiki/Gutenberg:Offline_Catalogs")

def readFile(fileName):
    print(fileName)
    f = open(fileName, "r+" )
    content = f.read()
    f.close()
    return  content

file_list = ["1996","1997","1998","1999","2000","2001","2002","2003","2004","2005","2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016","2017","2018","2019","2020"]
#

file_mongo_list = []
nameList = []
bookList = []
listIterator = 0
for each_file in file_list:
    if each_file is not None:
        file_dict = {}
        file_dict["name"] = each_file
        now = datetime.now()
        current_time = now.strftime("%d/%m/%Y %H:%M:%S")
        file_dict["start"] = current_time
        page = readFile(each_file)
        soup = BeautifulSoup(page, 'html.parser')
        pageContent = soup.text
        searchObj = re.search("ETEXT NO.|EBOOK NO.",pageContent)
        if searchObj is not None and searchObj.start() is not None:
            lastIndex = 0
            if pageContent.rfind("EBOOK NO.") > 1:
                lastIndex = pageContent.rfind("EBOOK NO.") + 9
            else:
                lastIndex = pageContent.rfind("ETEXT NO.") + 9
            listContent = pageContent[lastIndex:].splitlines()
            #listContent = pageContent[searchObj.end():].splitlines()
            for eachList in listContent:
                try:
                    if eachList is not None and not eachList.strip() == '':
                        #find all occurences of space and iterate in the reverse direction to find the last occ
                        #the above idea is not used
                        # lastWordOcc = re.findall("[a-zA-Z]",eachList)[-1]
                        # titleAuthor = eachList[:eachList.rfind(lastWordOcc)+1]

                        lastSpaceOcc = eachList.rfind(re.findall("\s",eachList)[-1])
                        #ignoreNum = True
                        titleAuthor = eachList
                        # print("before")
                        # print(titleAuthor)
                        if lastSpaceOcc > 1 and eachList[lastSpaceOcc-1] == " ":
                            while True:
                                if not eachList[lastSpaceOcc] == " ":
                                    break
                                lastSpaceOcc = lastSpaceOcc - 1
                            titleAuthor = eachList[:lastSpaceOcc+1]
                        # print("after")
                        # charIter = 0
                        # prevChar = ""
                        # for eachChar in titleAuthor:
                        #     if eachChar == " " and prevChar == " ":
                        #         titleAuthor = titleAuthor[:charIter-1]
                        #     prevChar = eachChar
                        #     charIter = charIter + 1
                        # print(titleAuthor)
                        if titleAuthor[0] == " ":
                            titleAuthor = prevValue + titleAuthor
                            listIterator = listIterator - 1
                            del nameList[listIterator]
                        nameList.append(titleAuthor)
                        listIterator = listIterator + 1
                        prevValue = titleAuthor
                except:
                    pass
            # iterate nameList and
            for eachBook in nameList:
                book_dict = {}
                if eachBook.find(" by ") > 1:
                    book_dict["Title"] = eachBook[:eachBook.find(" by ") - 1]
                    author = eachBook[eachBook.find(" by ") + 4:]
                    if author.find("[") > 1:
                        author = author[: author.find("[") - 1]
                    if author.find("\xa0") > 1:
                        author = author[: author.find("\xa0")]
                    book_dict["Author"] = author
                else:
                    book_dict["Title"] = eachBook
                bookList.append(book_dict)
        now = datetime.now()
        current_time = now.strftime("%d/%m/%Y %H:%M:%S")
        file_dict["end_time"] = current_time
        file_mongo_list.append(file_dict)
    time.sleep(300)

                #print(titleAuthor)
# print(bookList)
# print(file_mongo_list)
bookDataDoc.insert_many(bookList)
fileDataDoc.insert_many(file_dict)
