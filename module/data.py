import requests
from bs4 import BeautifulSoup
from googlesearch import search
from progressbar import *

def update1(year,inputurl):
    query = ''
    response = requests.get(inputurl)
    print(F"{year}申請入學資料更新中...")

    widgets = ['進度: ',Percentage(), ' ', Bar('#'),' ', Timer(),' ', ETA(), ' ']   
    pbar = ProgressBar(widgets=widgets)

    schoollist=[]
    response = requests.get(
        F"{inputurl}")
    soup = BeautifulSoup(response.text, "html.parser")
    result=soup.find_all("ul", class_="schools")[0]
    schools=result.find_all("li")
    for o in pbar(schools): 
        try:
            pid=o.select_one('a').get('href')
            schoolname=o.select_one("a").getText()
            query = schoolname[5:]
            schoolurl=""
            for j in search(query, stop=1):
                schoolurl=str(j)

        except:
            pass

        schoolresponse = requests.get(
            F"{inputurl}/{pid}")
        soup2 = BeautifulSoup(schoolresponse.text, "html.parser")
        result2=soup2.find_all("tr")
        resultlist2=[]
        for i in result2:
            try:
                a = i.find_all("td")
                if a !=[]:
                    代碼=a[1].select_one('a').get('href')
                    url=a[0].select_one('a').get('href')
                    科系=a[1].select_one("a").getText()
                    招收人數=a[2].getText()
                    檢定標準={
                        "國":a[3].getText(),
                        "英":a[4].getText(),
                        "數":a[5].getText(),
                        "社":a[6].getText(),
                        "自":a[7].getText(),
                        "英聽":a[8].getText()                   
                    }
                    篩選倍率={
                        "國":a[9].getText(),
                        "英":a[10].getText(),
                        "數":a[11].getText(),
                        "社":a[12].getText(),
                        "自":a[13].getText(),
                        "相加項":a[14].getText()      
                    }
                    temp={"代碼":代碼,"url":url,"科系":科系,"招收人數":招收人數,"檢定標準":檢定標準,"篩選倍率":篩選倍率}
                    resultlist2.append(temp)
            except:
                pass
        schoollist.append({"SchoolId":pid.rstrip("/"),"SchoolName":schoolname,"SchoolUrl":schoolurl,"校系分則":resultlist2})
    print(F"{year}申請入學資料更新完成")
    return schoollist


def update2(year,inputurl):
    # query = ''
    response = requests.get(inputurl)
    print(F"{year}繁星資料更新中...")
    groups=[]
    widgets = ['進度: ',Percentage(), ' ', Bar('#'),' ', Timer(),' ', ETA(), ' ']   
    response0 = requests.get(F"{inputurl}")
    soup0 = BeautifulSoup(response0.text, "html.parser")   
    result0=soup0.find_all("ul",class_="groups")[0]

    for o in (result0):
        groupurl=o.select_one('a').get('href')
        group=o.select_one('a').getText()
        print(group)
        schoollist=[]
        response = requests.get(
            F"{inputurl}/{groupurl}")
        soup = BeautifulSoup(response.text, "html.parser")
        result=soup.find_all("ul", class_="schools")[0]
        schools=result.find_all("li")
        pbar = ProgressBar(widgets=widgets)
        for o in pbar(schools): 
            try:
                
                schoolsid=o.select_one('a').get('href')[:-1]
                schoolname=o.select_one("a").getText()
                
                query = schoolname[5:]
                SchoolStarThreshold=o.select_one('p').getText()[8:]
                schoolurl=""
                # for j in search(query, stop=1):
                #     schoolurl=str(j)

            except:
                pass

            schoolresponse = requests.get(
                F"{inputurl}/{groupurl}/{schoolsid}")
            soup2 = BeautifulSoup(schoolresponse.text, "html.parser")
            result2=soup2.find_all("tr")
            resultlist2=[]
            for i in result2:
                
                try:
                    a = i.find_all("td")
                    if a !=[]:
                                   
                        代碼=a[1].select_one('a').get('href')
                        url=a[0].select_one('a').get('href')
                        科系=a[1].select_one("a").getText()
                        招收人數=a[2].getText()
                        print(F"{schoolname} : {科系}")
                        學測檢定標準={
                            "國":a[3].getText(),
                            "英":a[4].getText(),
                            "數":a[5].getText(),
                            "社":a[6].getText(),
                            "自":a[7].getText(),
                            "英聽":a[8].getText()                   
                        }
                        
                        分發比序={
                            "no1":a[9].getText(),
                            "no2":a[10].getText(),
                            "no3":a[11].getText(),
                            "no4":a[12].getText(),
                            "no5":a[13].getText(),
                            "no6":a[14].getText(),
                            "no7":a[15].getText()      
                        }
                        temp={"group":group,"學校":schoolname,"學校繁星標準":SchoolStarThreshold,"代碼":代碼,"url":url,"科系":科系,"招收人數":招收人數,"學測檢定標準":學測檢定標準,"分發比序":分發比序}
                        resultlist2.append(temp)
                except:
                    pass
            schoollist.append({"群":group,"SchoolId":schoolsid.rstrip("/"),"SchoolName":schoolname,"SchoolUrl":schoolurl,"學校繁星標準":SchoolStarThreshold,"校系分則":resultlist2})
            # print({"群":group,"SchoolId":schoolsid.rstrip("/"),"SchoolName":schoolname,"SchoolUrl":schoolurl,"學校繁星標準":SchoolStarThreshold,"校細分則":resultlist2})
        groups.append(schoollist)
    print(F"{year}繁星資料更新完成")
    return groups
# update2("110","https://university-tw.ldkrsi.men/star/")