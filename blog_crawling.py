import requests
from bs4 import BeautifulSoup

URL = "https://blog.naver.com/PostView.naver?blogId=aaa4815926&logNo=223217855620"
res = requests.get(URL)
soup = BeautifulSoup(res.text, "html.parser")

category = soup.select_one("div.blog2_series > a.pcol2") # 카테고리
print("카테고리: ", category.text)
title = soup.select_one("span.se-fs-") # 제목
print("제목: ", title.text)
name = soup.select_one("span.nick > a.link") # 작성자
print("작성자: ", name.text)
date = soup.select_one("span.se_publishDate") # 작성일시
print("작성일시: ", date.text)
content = soup.select("span.se-fs-")
content_list = []
for i in content:
    content_list.append(i.text)
content_result = ""
for i in content_list:
    content_result += i
print(content_result) # 원문