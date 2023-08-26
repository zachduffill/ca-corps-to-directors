import requests
from bs4 import BeautifulSoup    

corpFilename = "corporations.txt"
# The filename of the .txt containing corporation names, seperated line-by-line

def getDirectorsFromCorp(corpName):
    url = "https://ised-isde.canada.ca/cc/lgcy/fdrlCrpSrch.html?"
    postData = f"_pageFlowMap=&_page=&V_SEARCH.docsStart=1&V_SEARCH.baseURL=fdrlCrpSrch.html&V_SEARCH.command=search&corpName={corpName}&corpNumber=&busNumber=&corpProvince=&corpStatus=&corpAct=&buttonNext=Search"
    postHeaders = {"Origin": "https://ised-isde.canada.ca","Content-Type": "application/x-www-form-urlencoded","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7","Sec-Fetch-Site": "same-origin","Sec-Fetch-Mode": "navigate","Sec-Fetch-User": "?1","Sec-Fetch-Dest": "document","Referer": "https://ised-isde.canada.ca/cc/lgcy/fdrlCrpSrch.html"}

    page = requests.post(url, postData,headers=postHeaders)
    soup = BeautifulSoup(page.content, "html.parser")
    firstCorp = soup.find(attrs={"class":"col-md-11"})

    if firstCorp == None:
        print(f"Could not find {corpName}")
        return None
    else:
        page = requests.get("https://ised-isde.canada.ca/cc/lgcy/"+firstCorp.findChild().findChild()["href"])
        soup = BeautifulSoup(page.content, "html.parser")
        directors = soup.find_all(attrs={"class":"full-width pad-bttm-md list-inline-block"})

        list = []
        for d in directors:
            list.append(d.get_text(separator=" ").strip().replace("  "," ").replace("  "," ").split("\n \n\t\t\t\t\t\t\t\t\t\t\t"))
        return list


corpFile = open(corpFilename, "r")
corps = corpFile.readlines()
corpFile.close()

csv = open("directors.csv", "w")
for corp in corps:
    directors = getDirectorsFromCorp(corp)
    for d in directors:
        csv.write(corp.strip()+","+",".join(d)+"\n")
        print(corp.strip()+" "+" ".join(d))