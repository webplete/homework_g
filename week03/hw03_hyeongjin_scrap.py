import requests
from bs4 import BeautifulSoup

# 타겟 URL을 읽어서 HTML를 받아오고,
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20200713', headers=headers)

# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
# soup이라는 변수에 "파싱 용이해진 html"이 담긴 상태가 됨
soup = BeautifulSoup(data.text, 'html.parser')

# 지니뮤직의 1~50위 곡의 정보를 스크래핑
# 순위, 제목, 가수 스크래핑
# [0:2].strip() 은 크롤링된 값 문자열을 0번째부터 2째자리까지 자르기

chart_lists = soup.select('#body-content > div.newest-list > div > table > tbody > tr')

for chart_list in chart_lists:
    rank = chart_list.select_one('td.number').text[0:2].strip()
    title = chart_list.select_one('td.info > a').text.strip()
    artist = chart_list.select_one('td.info > a.artist.ellipsis').text.strip()
    print(rank, title, artist, sep=" - ")
    # 순위, 제목, 가수가 sep "-" 을 통해 구분된다.

