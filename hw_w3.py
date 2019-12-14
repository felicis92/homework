import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.

# URL을 읽어서 HTML를 받아오고,
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20190908', headers=headers)

# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
soup = BeautifulSoup(data.text, 'html.parser')


musics = soup.select('#body-content > div.newest-list > div > table > tbody > tr')

# [소영] 제목이랑 가수명이 어딨는지 copy select를 해보았습니다
#body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.title.ellipsis
#body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.artist.ellipsis
# a.title.ellipsis 랑 a.artist.ellipsis 에 각각 들어있는 것 같으니 태그를 걸어주면 될 것 같습니다.

rank = 1
for music in musics:
    a_tag = music.select_one('td.info > a.title.ellipsis')
    b_tag = music.select_one('td.info > a.artist.ellipsis')

    if a_tag is not None:
        # a_tag에 뭐가 있으면 = 제목에 어떤 값이 있으면 rank, net_title, singer를 print하는 반복문 생성
        title = a_tag.text.strip()
        singer = b_tag.text
        doc = {
            'rank' : rank,
            'title' : title,
            'singer' : singer
            }
        db.musics.insert_one(doc)
        rank += 1