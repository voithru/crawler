from bs4 import BeautifulSoup as BS
import requests
import pandas as pd
import numpy as np
import json
from urllib.parse import urljoin

# import re
def subttoText(id):
    """
    TED 영어 자막을 받아와 string으로 내보내는 함수.
    input -
        id : str or int. 각 영상마다의 고유번호를 받아온다.['__INITIAL_DATA__']['talks'][0]['id']에 있다.
    output -
        result : str. 전체 스크립트를 하나의 str로 리턴한다. (applause)등의 것들이 써있다.
    """
    url = 'http://www.ted.com/talks/subtitles/id/{}/lang/en'.format(str(id))
    bs = BS(requests.get(url).text,'lxml')
    jsonfile = json.loads(bs.select('p')[0].text)['captions']
    result = ''
    for i in jsonfile:
        result = result + ' ' + i['content']
    result = result.replace('\n',' ').strip()
    result = result.replace('-',' ')
    result = result.replace('  ',' ')
    result = result.replace('"','')
    """
    p = re.compile('\(.*?\)')
    lis = p.findall(result)
    for i in list(set(lis)):
        result = result.replace(i,'')
    """
    return result


def navigator():
    """
    http://new.ted.com/talks/browse 를 전부 돌아다니며 각 영상의 ids, title을 return 하는 함수.
    같은 인덱스로 묶여있다.
    input -
    output -
        resultIds : list. 총 id들. type of element - int
        resultTitles : list. 총 title 들. type of element - str
    """
    BASEURL = 'http://new.ted.com/talks/browse'
    PAGEURL = 'http://new.ted.com/talks/browse?page={}' #.format(int) 로 접근.
    resultIds = []
    resultTitles = []
    # maximum page 계산
    max_pages = BS(requests.get(BASEURL).text,'lxml').select('div.pagination a.pagination__item')[-1].text


    # 이제 돌아다니며 url로 접근
    for i in range(int(max_pages)):
        bs = BS(requests.get(PAGEURL.format(i+1)).text,'lxml').select('div.row div.media__image a')
        for pgs in bs:
            try:
                added_url = urljoin(BASEURL,pgs['href'])
                title = pgs['href'].replace('/talks/','')
                idbs = BS(requests.get(added_url).text,'lxml')
                json_data = idbs.select('div.talks-main script')
                json_data = json_data[-1].text
                json_data = ' '.join(json_data.split(',', 1)[1].split(')')[:-1])
                json_data = json.loads(json_data)
                ids = int(json_data['__INITIAL_DATA__']['talks'][0]['id'])
                resultIds.append(ids)
                resultTitles.append(title)
                print("navigating, %s", title)
            except:
                print(json_data)

    return resultIds, resultTitles
