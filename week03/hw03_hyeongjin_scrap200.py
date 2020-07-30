import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta

# 스크래핑 할 대상 사이트의 서버에 크롤러가 아닌 일반 유저 인것처럼 정보를 보내는 형식 requests 모듈과 header, User-Agent 활용
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

# 반복문을 통해 지니뮤직 1~200위 차트의 순위 정보를 크롤링 한다.(페이지를 자동으로 넘겨가며 크롤링. range 함수사용)
# range 함수는 연속된 숫자(정수)를 만들어준다. 1, 5의 경우 마지막 5는 포함되지 않는다.
# 뮤직차트 1위에서 200위까지가 총 4페이지 이기 때문에 range 함수를 1, 5 입력할 경우 4페이지 까지 생성한다.
# range 값은 가져오는 url뒤 마지막 pg= 뒤 숫자에 입력된다. (str 을 이용하여 숫자값을 입력한다.)

for i in range(1, 5):
    data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&ymd=20200728&hh=23&rtm=N&pg=' + str(i),
                        headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    for i in soup.select('#body-content > div.newest-list > div > table > tbody > tr'):
        rank = i.select_one('td.number').text[0:3].strip()
        title = i.select_one('td.info > a').text.strip()
        artist = i.select_one('td.info > a.artist.ellipsis').text.strip()

        print(rank, title, artist, sep=" - ")
        # sep "-" 구분자를 통해 순위 - 제목 - 가수 형태로 각 항목값 사이에 - 가 구분자로 입력된다.

        db.chart_lists.insert_one({
            'rank': rank,
            'title': title,
            'artist': artist
        })

