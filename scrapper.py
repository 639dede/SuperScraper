import requests
from bs4 import BeautifulSoup

LIMIT = 50

def get_last_page(url):
    result = requests.get(url)

    soup = BeautifulSoup(result.text, "html.parser")

    pagination = soup.find("div", {"class": "pagination"})

    links = pagination.find_all("a")

    links = links[:-1]
    pages = []

    for link in links:
        pages.append(int(link.string))

    max_page = pages[-1]
    return max_page


def extract_job(soup):
  t = str(soup.select_one("span[title]").string)
  c_n = str(soup.find("span", {"class": "companyName"}).string)
  c_l = str(soup.find("div", {"class": "companyLocation"}).string)
  j_i = soup["data-jk"]
  return {
      'title':
      t,
      'company':
      c_n,
      'location':
      c_l,
      'link':
      f"https://kr.indeed.com/%EC%B1%84%EC%9A%A9%EB%B3%B4%EA%B8%B0?jk={j_i}&vjs=3"
  }


def extract_jobs(last_page, url):
    jobs = []
    for page in range(last_page):
      print(f"Scrapping page {page}..")
      result = requests.get(f"{url}&start={page*LIMIT}")
      soup = BeautifulSoup(result.text, "html.parser")
      results = soup.find_all("a", {"class": "tapItem"})
      for result in results:
          job = extract_job(result)
          jobs.append(job)
    return jobs





def get_jobs(word):
  url = f"https://kr.indeed.com/%EC%B7%A8%EC%97%85?as_and={word}&as_phr=&as_any=&as_not=&as_ttl=&as_cmp=&jt=all&st=&salary=&radius=25&fromage=any&limit={LIMIT}"
  last_page=get_last_page(url)
  jobs=extract_jobs(last_page, url)
  return jobs
