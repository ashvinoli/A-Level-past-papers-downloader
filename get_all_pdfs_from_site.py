import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import pathlib 
from datetime import date
import json


def download_all():
    dir_path = os.path.dirname(os.path.realpath(__file__))   
    with open("subjects.json") as f:
        data = json.load(f)
        url_header = data["site"]
        subjects = data["subjects"]
        combined_urls = [urljoin(url_header,sub) for sub in subjects]
        for url in combined_urls:
            cur_year = date.today().year
            init_year = data["init_year"]
            for year in range(init_year,cur_year+1):
                final_url = f"{url}/{year}"
                soup = BeautifulSoup(requests.get(final_url).text,"html.parser")
                folder_location = os.path.join(dir_path,final_url.split("/")[-2])
                if not os.path.exists(folder_location):
                    pathlib.Path(folder_location).mkdir(parents=True, exist_ok=True)
                all_html = soup.findAll('a')
                for links in all_html:
                    my_href = str(links.get("href"))
                    if my_href.endswith(".pdf"):
                        print("Downloading file %s"%(my_href))
                        file_name = os.path.join(folder_location,my_href)
                        if not os.path.exists(file_name):
                            my_file = open(file_name,"wb")
                            download_link = f"{final_url}/{my_href}"
                            my_file.write(requests.get(download_link).content)
                            my_file.close() 
            
                

if __name__ == "__main__":
    download_all()
    
    
