import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

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
    category_list = []
    if category is None:
        category_list.append("<카테고리경로가 다르거나 카테고리가 설정되지 않음>")
    else:
        # print("카테고리: ", category.text)
        category_list.append(category.text)
    title = soup_blog.select_one("span.se-fs-") # 제목
    title_list = []
    if title is None:
        title_new = soup_blog.select_one("h3.se_textarea")
        if title_new is None:
            title_list.append("<제목경로가 다르거나 제목 설정되지 않음>")
        else:
            title_list.append(title_new.text)
    else:
        # print("제목: ", title.text)
        title_list.append(title.text)
    name = soup_blog.select_one("span.nick > a.link") # 작성자
    name_list = []
    if name is None:
        name_list.append("<작성자경로가 다르거나 작성자 불분명함>")
    else:
        # print("작성자: ", name.text)
        name_list.append(name.text)
    date = soup_blog.select_one(".se_publishDate") # 작성일시
    date_list= []
    if date is None:
        date_list.append("<작성일지경로가 다르거나 작성일지 확인 불가능>")
    else:
        # print("작성일시: ", date.text)
        date_list.append(date.text)
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
    for i in soup_blog.select("span"): # 태그 패턴이 "se-fsxxxxx또는 se_fsxxxxx패턴을 모두 찾아 content_add매소드 적용"
        find_pattern = re.findall("(?<=class=\")se[-_]fs.*", str(i))
        pattern_only = []   # 리스트 find_pattern에서의 중복 제거 후 리스트
        for value in find_pattern:
            if value not in pattern_only:
                pattern_only.append(value)
    if not len(pattern_only) == 0:
        content_add(soup_blog, "span." + pattern_only[0].split(" ")[0], content_list)

    content_result = ""
    for i in content_list:
        content_result += i
    # print(content_result) # 원문
    # print("============================================================================================")

    # dataframe형식으로 출력하기 위한 dataset
    return category_list, title_list, name_list, date_list, content_list

# 블로그별 구조의 차이에 따른 추가패턴 탐색에 대한 모델
def content_add(soup, pattern, list_content): # soup: soup_blog사용, pattern: soup.select 표현식사용, list_content: content_list사용
    add_content = soup.select(pattern)
    # 추가패턴 검색 시 내용추가 진행
    if add_content is not None:
        add_content_only = []
        for i in add_content:
            list_content.append(i.text)
        for value in list_content: # 리스트 add_content에 대한 중복 제거
            if value not in add_content_only:
                add_content_only.append(value)
        list_content = add_content

naver_url = "https://search.naver.com/search.naver?where=blog&query=%ED%85%8C%EC%8A%AC%EB%9D%BC&sm=tab_opt&nso=so:dd,p:from20230921to20230922"
res_naver = requests.get(naver_url)
soup_naver = BeautifulSoup(res_naver.text, "html.parser")
search_url = soup_naver.select("a.api_txt_lines")
blog_url_list = []
for i in search_url:
    blog_url_list.append(i["href"])

category_result = []
title_result = []
name_result = []
date_result = []
content_result = []
for i in blog_url_list:
    a, b, c, d, e = get_blog(i)
    category_result.extend(a)
    title_result.extend(b)
    name_result.extend(c)
    date_result.extend(d)
    content_result.append(e)

# dataframe 생성 및 출력
data = {"카테고리": category_result, "제목": title_result, "작성자": name_result, "작성일시": date_result, "본문": content_result}
df = pd.DataFrame(data)
print(df)