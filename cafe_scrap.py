# -*- coding: utf-8 -*-
"""

 - 특정 기간 범위의 게시물 수집
 
"""

import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

file = open("C:/jmkim/Scrap_NaverCafe/naver_cafe4.txt","w",encoding='utf-8')

#HTTP 요청시 서버에 애플리케이션에 대한 정보를 넘겨주기 위한 변수
headers = {
    'Host' : 'openapi.naver.com',
    'User-Agent' : 'curl/7.49.1',
    'Accept' : '*/*',
    'Content-Type' : 'application/xml',
    'X-Naver-Client-Id' : 'zPsjitdQzWyDJ_YJyciS',
    'X-Naver-Client-Secret' : 'KhaK6x18Hi'
    } 


defaultURL = 'https://openapi.naver.com/v1/search/cafearticle.xml?' 
sort = '&sort=date'       # 정렬 옵션: sim (유사도순), date (날짜순)
start1 = '&start='        # 검색 시작 위치로 최대 1000까지 가능
start2 = str(1)
display = '&display=100'  # 10(기본값), 100(최대)
query = '&query='+urllib.parse.quote_plus('청첩장 샘플 | 후기') 

#query = '&query='+urllib.parse.quote_plus(str(input("검색어: "))) 
#검색어라는 문구를 출력하여 사용자에게 단어를 문자열로 입력받은 후
# quote_plus 함수를 이용해서 단어를 인코딩(url에 한글입력 가능)


fullURL = defaultURL + sort + start1 + start2 + display + query
print(fullURL)

#http 요청을 하기 전 헤더 정보를 이용해 request 객체를 생성. urllib 모듈에서 헤더 정보를 서버에 전달시 사용하는 대표적인 방법
req = urllib.request.Request(fullURL, headers=headers) 

#생성된 request 객체를 urlopen 함수의 인수에 전달하여 헤더 정보를 포함하여 서버에게 http 요청을 하게됨. 
f = urllib.request.urlopen(req) 

#서버로부터 받은 데이터를 읽음.
resultXML = f.read( )

#읽어들인 xml 데이터를 이용하여 원하는 데이터를 가져오기 위한 뷰티풀 수프 객체를 생성 
xmlsoup = BeautifulSoup(resultXML,'html.parser')

# item 태그를 모두 가져와 저장
items = xmlsoup.find_all('item')
print(xmlsoup.find('total').get_text(strip=True))
print(xmlsoup.find('lastbuilddate').get_text(strip=True))

# <channel><title>Naver Open API - cafearticle ::'청첩장 샘플'</title>
# <link/>http://search.naver.com
# <description>Naver Search Result</description>
# <lastbuilddate>Tue, 26 Dec 2017 14:09:18 +0900</lastbuilddate>
# <total>59007</total><start>1</start><display>100</display>



#for 문을 이용하여 title, url을 공백 제거한 다음 텍스트 파일에 write.
for item in items :
     file.write('카페제목 : ' + item.title.get_text(strip=True) + '||')
     file.write('URL : ' + item.contents[2] + '||')
#     file.write('카페내용 : ' + item.description.get_text(strip=True) + '\n')

# 읽을 페이지 수 : total // 100 + 1
pages = int(xmlsoup.find('total').get_text(strip=True)) // 100 + 1    
     
for page in range(2, pages) :
    start2 = str(1)
    fullURL = defaultURL + sort + start1 + start2 + display + query
    
    req = urllib.request.Request(fullURL, headers=headers) 
    f = urllib.request.urlopen(req) 
    resultXML = f.read( )
    xmlsoup = BeautifulSoup(resultXML,'html.parser')
    items = xmlsoup.find_all('item')

    for item in items :
        file.write('카페제목 : ' + item.title.get_text(strip=True) + '||')
        file.write('URL : ' + item.contents[2] + '||')

file.close( )

#텍스트 파일 저장 후 종료


