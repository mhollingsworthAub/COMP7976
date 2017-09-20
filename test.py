import urllib.request
from bs4 import BeautifulSoup as bs
import os.path
import time
from multiprocessing.dummy import Pool as ThreadPool, Process, Queue
pool = ThreadPool(8) 


htmlSource = os.getcwd() + "/htmlSource/" #directory to store all the html source text files
maxDepth = 3
now = time.time()

class Find:

    def findChildren(self, link, depth): #This will find all child URLS (in 'a' elements) from link
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

            rawHTML = bs(siteHtml.decode("utf-8"), "html.parser")

            
            for childLink in rawHTML.find_all("a"):
                if(childLink.get("href") is not None):
                    
                    #print("**" + childLink.get("href")[0:2] + "**\n")
                    if "http://" in childLink.get("href"): 
                        self.findChildren(childLink.get("href"), depth)
                    elif childLink.get("href")[0:2] == "//":
                        var = childLink.get("href")
                        self.findChildren("http:" + childLink.get("href"), depth)
                    elif not "https://" in childLink.get("href"):
                        l = childLink.get("href")
                        if l[0] == '/':
                            l = l[1:]
                        self.findChildren(link[:link.rfind('/') + 1] + l, depth)
        except:
            return False       
 

    def makeGram(self, directory):
        for fileName in os.listdir(directory):
            unigram = open(directory + fileName.replace(".txt", ".vec"), 'w')
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

    def makeVec(self, fileName):
        unigram = open(htmlSource + fileName.replace(".txt", ".vec"), 'w')
        counter = [0] * 95
        fileContents = open(htmlSource + fileName, "r").read()
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
f = Find()
f.findChildren("http://about.ask.com/", 0)

#f.findChildren(ld)
#f.makeGram(htmlSource)
print("Starting vec")
pool.map(f.makeVec, os.listdir(htmlSource))
pool.close()
pool.join()

print(time.time() - now)