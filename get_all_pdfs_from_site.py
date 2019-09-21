import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import re
import pathlib #this library lets mkdir word recursively, default mkdir could only crease folders to one level up

url = "http://onlineexamhelp.com/past-papers/cambridge-international-a-as-level"
def form_dic():
    global url
    my_dict = {}
    soup = BeautifulSoup(requests.get(url).text,"html.parser")
    all_html = soup.findAll('a')
    level = 1
    for _ in all_html:
        my_href = _.get("href").split('/')[-1]
        if re.match("^\d+",my_href):
            my_dict[level] = my_href
            level+=1
    return my_dict 

def download_papers(my_sub):
    global url
    complete_url = url+"/"+my_sub
    soup = BeautifulSoup(requests.get(complete_url).text,"html.parser")
    all_html = soup.findAll('a')
    available_years = []
    for _ in all_html:
        my_href = _.get("href").split('/')[-1]
        if re.match("^\d+.*\d$",my_href):
            av_year = my_href.split("-")[-1]
            available_years.append(av_year)                         
            sub_name = my_href
            sub_name = sub_name[:len(my_href)-4]
    print("Avalilable Years:" + ",".join(available_years))
    start_year = int(input("Please enter the start year:"))
    end_year = int(input("Please enter the ending year:"))
    fragments = my_sub.split("-")

    for year in range(start_year,end_year+1):
        sub = sub_name + str(year)        
        folder_location = "E:\\past_papers\\" + fragments[1]+"\\"+str(year)
        if not os.path.exists(folder_location):
            pathlib.Path(folder_location).mkdir(parents=True, exist_ok=True)
        complete_url = url+"/"+my_sub+"/"+sub
        print(complete_url)
        response = requests.get(complete_url)
        soup= BeautifulSoup(response.text, "html.parser")     
        for link in soup.select("a[href$='.pdf']"):
            #Name the pdf files using the last portion of each link which are unique in this case
            filename = os.path.join(folder_location,link['href'].split('/')[-1])
            with open(filename, 'wb') as f:
                print("Current file:"+ filename)
                f.write(requests.get(urljoin(url,link['href'])).content)

if __name__ == "__main__":
    my_dic = form_dic()
    for _ in my_dic:
        print(str(_)+"->"+my_dic[_])
    print("\n\n")
    print("Select the number of subject:")
    number = input()
    download_papers(my_dic[int(number)])
    
    
