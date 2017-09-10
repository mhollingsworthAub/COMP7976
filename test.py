import urllib.request
siteHtml = urllib.request.urlopen("http://www.auburn.edu").read()
output = open("output.txt", "w")
output.write(siteHtml.decode("utf-8"))
output.flush()
output.close()
#test commit from code