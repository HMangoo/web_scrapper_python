import requests
from bs4 import BeautifulSoup # useful HTML tool 

LIMIT = 50
URL = f"https://www.indeed.com/jobs?q=python&limit={LIMIT}"  

def extract_last_pages():
  # Get website
  result = requests.get(URL)
  
  # Get HTML text
  soup = BeautifulSoup(result.text, "html.parser")
  
  # Get <div class="pagination"
  pagination = soup.find("div", {"class" : "pagination"})

  # Get all anchor in pagination
  links = pagination.find_all('a')
  
  # Get last page number
  pages_anchor = []
  for link in links[0:-1] :
    pages_anchor.append(int(link.string))
  last_page = pages_anchor[-1]

  return last_page

def extract_job(html):

  result = html.find("td", {"class": "resultContent"})
  #job title
  jobTitle = result.find("h2", {"class":"jobTitle"})
  title = jobTitle.find("span", title=True).string
  
  #companay
  company = result.find("span", {"class" : "companyName"})
  company_anchor = company.find("a")
  if company_anchor is not None:
        company = str(company_anchor.string)
  else:
        company = str(company.string)
  # remove space
  company = company.strip()
  
  #location
  location = result.find("div", {"class": "companyLocation"}).text
  """
  text는 전체 텍스트를 가져오고
  string은 내부에 태그가 있을 경우 None으로 변환함.
  """

  #link
  link = html["data-jk"] # html : class = "sponTapItem"를 가지고 있는 a tag
  
  return {
    'title': title, 
    'company': company, 
    'location': location,
    'link': f"https://www.indeed.com/jobs?q=python&limit=50&vjk={link}"
  }
  
def extract_indeed_jobs(last_page):
  jobs = []
  for page in range(last_page):
    print(f"Scrapping page {page}")
    result = requests.get(f"{URL}&start={page*LIMIT}")
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("a", {"class": "sponTapItem"})
    
    for result in results:
      job = extract_job(result)
      jobs.append(job)
      
  return jobs

def get_jobs():
  last_page = extract_last_pages()
  jobs = extract_indeed_jobs(last_page)
  return jobs




