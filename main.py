import alba_co_kr
from save import save_to_file

links_names = alba_co_kr.get_brand_urls()
for link_name in links_names:
    jobs = alba_co_kr.start(link_name["link"])
    save_to_file(link_name["name"], jobs)
