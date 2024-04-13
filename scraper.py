import requests 
from bs4 import BeautifulSoup
import csv

all_jobs=[]

def scrape_page(url):
  r = requests.get(url,
      headers={
          "User-Agent":
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
      })
  r.encoding = 'utf-8'  # 응답 객체의 인코딩을 'utf-8'로 설정
  
  soup = BeautifulSoup(r.content, 'html.parser')
  jobs = soup.find("ul", class_="line-dot").find_all("li", class_="cont-right")
  
  for job in jobs:
    company = job.find("div", class_="txt").find("span").text
    url = job.find("div", class_="link").find("a")["href"]
    title = job.find("div", class_="link").find("a").text.strip()
    date = job.find("p", class_="date").text[1:-1].strip("마감")
    money = job.find("div", class_="cp-info").find_all("span")[3].text.strip().strip('"')

    if money.startswith("근무지"):
       money = "협상"

    job_data = {
      "company" :company,
      "title" :title,
      "money" :money,
      "date" :date,
      "url" : f"https://www.work.go.kr{url}"
    }
    all_jobs.append(job_data)

  
    

def get_pages(keyword):
  r = requests.get(f"https://www.work.go.kr/wnSearch/unifSrch.do?regDateStdt=&regDateEndt=&colName=tb_workinfo&srchDateSelected=all&sortField=RANK&sortOrderBy=DESC&pageIndex=1&tabName=tb_workinfo&dtlSearch=&query={keyword}&radio_period=on",
      headers={
          "User-Agent":
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
      })
  r.encoding = 'utf-8' 
  
  soup = BeautifulSoup(r.content, 'html.parser')
  page_number = len(soup.find("nav", class_="pagination").find_all("a"))+1

  if page_number>6:
    page_number = 6

  for x in range(1, page_number):
    url = f"https://www.work.go.kr/wnSearch/unifSrch.do?regDateStdt=&regDateEndt=&colName=tb_workinfo&srchDateSelected=all&sortField=RANK&sortOrderBy=DESC&pageIndex={x}&tabName=tb_workinfo&dtlSearch=&query={keyword}&radio_period=on"
    scrape_page(url)

  return all_jobs


def save_to_file(file_name,jobs):
    file = open(f"{file_name}.csv", mode="w", encoding="utf-8-sig", newline="")
    writter = csv.writer(file)
    writter.writerow(["기업", "공고", "연봉","모집기간", "링크"])

    for job in jobs:
        writter.writerow(job.values())

    file.close()