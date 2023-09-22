import requests
from bs4 import BeautifulSoup
import re

def get_blog(url):
    URL = url
    res = requests.get(URL)
    soup = BeautifulSoup(res.text, "html.parser")
    final_url = soup.select_one("iframe")["src"]

    # 크롤링 가능한 블로그 URL로 변경
    BLOG_URL = "https://blog.naver.com" + final_url
    res_blog = requests.get(BLOG_URL)
    soup_blog = BeautifulSoup(res_blog.text, "html.parser")

    category = soup_blog.select_one("div.blog2_series > a.pcol2") # 카테고리
    if category is None:
        print("이 블로그는 별도의 카테고리를 구분하지 않습니다.")
    else:
        print("카테고리: ", category.text)
    title = soup_blog.select_one("span.se-fs-") # 제목
    if title is None:
        print("이 블로그는 제목이 없습니다.")
    else:
        print("제목: ", title.text)
    name = soup_blog.select_one("span.nick > a.link") # 작성자
    if name is None:
        print("이 블로그에 대한 작성자를 확인할 수 없습니다.")
    else:
        print("작성자: ", name.text)
    date = soup_blog.select_one("span.se_publishDate") # 작성일시
    if date is None:
        print("이 블로그에 대한 작성일시가 확인되지 않았습니다.")
    else:
        print("작성일시: ", date.text)
    content = soup_blog.select("span.se-fs-")
    # 블로그별 구조의 차이에 따른 추가패턴 탐색
    content_add1 = soup_blog.select("span.se-fs-19")
    content_list = []
    for i in content:
        content_list.append(i.text)
    # 추가패턴 검색 시 내용추가 진행
    # content_add(soup_blog, "span.se-fs-19", content_list)
    # content_add(soup_blog, "span.se-fs-fs30", content_list)
    # content_add(soup_blog, "span.se-fs-fs24", content_list)
    # print(re.findall("se[-_]fs.*", str(soup_blog.select_one("span"))))
    for i in soup_blog.select("span"): # 태그 패턴이 "se-fsxxxxx또는 se_fsxxxxx패턴을 모두 찾아 content_add매소드 적용"
        if not len(re.findall("(?<=class=\")se[-_]fs.*", str(i))) == 0:
            print(re.findall("(?<=class=\")se[-_]fs.*", str(i))[0].split(" ")[0])
            content_add(soup_blog, "span." + re.findall("(?<=class=\")se[-_]fs.*", str(i))[0].split(" ")[0], content_list)
    # print(soup_blog.select("span"))

    content_result = ""
    for i in content_list:
        content_result += i
    print(content_result) # 원문
    print("============================================================================================")

# 블로그별 구조의 차이에 따른 추가패턴 탐색에 대한 모델
def content_add(soup, pattern, list_content): # soup: soup_blog사용, pattern: soup.select 표현식사용, list_content: content_list사용
    add_content = soup.select(pattern)
    # 추가패턴 검색 시 내용추가 진행
    if add_content is not None:
        for i in add_content:
            list_content.append(i.text)

naver_url = "https://search.naver.com/search.naver?where=blog&query=%ED%85%8C%EC%8A%AC%EB%9D%BC&sm=tab_opt&nso=so:dd,p:from20230921to20230922"
res_naver = requests.get(naver_url)
soup_naver = BeautifulSoup(res_naver.text, "html.parser")
search_url = soup_naver.select("a.api_txt_lines")
blog_url_list = []
for i in search_url:
    blog_url_list.append(i["href"])

for i in blog_url_list:
    get_blog(i)