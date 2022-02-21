import requests
from bs4 import BeautifulSoup
import math

URL = "http://www.alba.co.kr/"


def get_brand_urls():
    alba = requests.get(URL)

    # Get HTML text
    soup = BeautifulSoup(alba.text, "html.parser")

    super_brand = soup.find("div", {"id": "MainSuperBrand"})
    brands = super_brand.find_all("a", {"class": "goodsBox-info"})

    brand_links = []
    for brand in brands:
        link = str(brand["href"])
        name = brand.find("span", {"class":"company"}).string

        link_name = {
          'link':link,
          'name':name
        }
        brand_links.append(link_name)
    return brand_links


def get_last_page(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    page = soup.find("div", {"id": "NormalInfo"}).find_all(
        "script", {"type": "text/javascript"})[-2].text
    number_of_page = float(page.split(",")[1])/float(page.split(",")[2])
    return math.ceil(number_of_page)


def extranct_job_info(info):
    # place
    place = info.find("td", {"class": "local"}).text.replace("\xa0", " ")
    # title
    title = info.find("td", {"class": "title"}).find(
        "span", {"class": "title"}).string
    # time
    time = info.find("td", {"class": "data"}).find("span").string
    # pay
    pay = info.find("td", {"class": "pay"}).text
    # date
    date = info.find("td", {"class": "regDate"}).text

    return {
        'place': place,
        'title': title,
        'time': time,
        'pay': pay,
        'date': date
    }


def extract_url_info(url="", pages=1):
    all_info = []
    print(f"Scrapping url : {url}")
    print(f"number of page : {pages}")
    for page in range(pages):
      print(f"Scrapping page {page+1}")
      alba = requests.get(f"{url}?page={page+1}&pagesize=50")
      soup = BeautifulSoup(alba.text, "html.parser")
      page_info = soup.find("div", {"id": "NormalInfo"}).find(
          "tbody").find_all("tr")
      page_info = page_info[0::2]

      for info in page_info:
          job = extranct_job_info(info)
          all_info.append(job)

    return all_info


def start(url):
    last_page = get_last_page(url)
    jobs = extract_url_info(url, last_page)
    return jobs
