import urllib.request
from bs4 import BeautifulSoup as bs
import os.path

htmlSource = os.getcwd() + "/htmlSource/" #directory to store all the html source text files
maxDepth = 2 

def findChildren(link, depth): #This will find all child URLS (in 'a' elements) from link
    depth += 1

    if depth > maxDepth:
        return False
    try:
        fileName = htmlSource + link.replace("/", "_").replace(":", "_")
        if os.path.exists(fileName + ".txt"):
            print("found file " + fileName + ".txt")
            return True

        print("Processing " + link)
        siteHtml = urllib.request.urlopen(link).read()        
        
        output = open(fileName + ".txt", "w")
        output.write(siteHtml.decode("utf-8"))
        output.flush()
        output.close()

        soup = bs(siteHtml.decode("utf-8"), "html.parser")


        for link in soup.find_all("a"):
            if(link.get("href") is not None):
                if "http://" in link.get("href"): 
                    findChildren(link.get("href"), depth)
    except:
        return False       

def makeGram(directory):
    for fileName in os.listdir(directory):
        unigram = open(directory + fileName.replace(".txt", ".count"), 'w')
        counter = [0] * 95
        fileContents = open(directory + fileName, "r").read()
        for char in fileContents:
            if ord(char) > 31 and ord(char) < 127:  
                counter[ord(char) - 32 ] += 1

        s = str(counter[0])
        for i in range (1, 94):
            s = s + "," + str(counter[i])
        unigram.write(s)
        unigram.flush()
        unigram.close()

if os.path.exists(htmlSource) is False:
    os.makedirs(htmlSource)

findChildren("http://www.auburn.edu", 0)
makeGram(htmlSource)
