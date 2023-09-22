import requests
from bs4 import BeautifulSoup
import re

# 검색 키워드와 검색 기간에 따른 기사제목, 네이버뉴스 URL이 있는 경우 URL 검색
def Tesla_keyword_page(p):
    page = str(10 * p - 9)
    title_list = []
    naver_url_list = []
    for i in range(1, 10 * p - 9 + 1, 10):
        URL = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=테슬라&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=92&mynews=0&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:r,p:all,a:all&start=" + str(i)
        headers = {'User-Agent':'Mozilla/5.0'}
        res = requests.get(URL, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")

        title = soup.select("a.news_tit")
        naver_url = soup.select("div.info_group")
        for i in title:
            title_list.append(i.text)
        for i in naver_url:
            if len(i.select("a")) == 2:
                naver_url_list.append(i.select("a")[1]["href"])
            else:
                naver_url_list.append("네이버 뉴스기사 URL없음")
    return title_list, naver_url_list

title, url = Tesla_keyword_page(9)
for i in range(len(title)):
    print("기사제목: ", title[i])
    print("네이버 기사 URL: ", url[i])
    print("=============================================================================")