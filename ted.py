import util
import os
from os import path
import pandas as pd
import numpy as np
if __name__ == '__main__':
    # ids, titles, paths are what should be written.
    ids, titles = util.navigator()
    paths = []
    written = path.join(path.curdir,'data')
    # 일단 data라는 폴더가 없으면 data라는 폴더를 생성한다.
    try :
        os.mkdir(path.join(path.curdir,'data'))
    except:
        "folder exists"
    for i in range(len(ids)):
        #print title
        print(titles[i])
        # 일단 subtitle 받아주기
        subtitle = util.subttoText(ids[i])

        # 그 다음에, context manager(with)를 사용하여 data 폴더 안에 title.txt의 글 파일을 만든다.
        # Q file alreay exists 의 경우에는 어덯게 처리되지?
        path_tmp = path.join(written,(title[i]+".txt"))
        with open(path_tmp,"w") as p:
            p.write(subtitle)
        # 해당 path를 하나의 리스트(paths)에 저장하여, ids, titles, paths 를 csv 파일
        paths.append(path_tmp)

    df = pd.DataFrame({
    'ids':ids,
    'titles':titles,
    'paths':paths
    })
# 많은 데이터가 유실된다. 특정 ted에 들어가면 해당 body가 json load를 할 때 전혀 값이 들어오지 않는다.
# 너무 빠르고 많은 request 때문인가?
