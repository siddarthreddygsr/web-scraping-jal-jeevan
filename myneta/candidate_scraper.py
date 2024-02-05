from bs4 import BeautifulSoup
import requests
import re

def parse(url):
    response = requests.get(url)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    cand_dict = {}
    cand_dict["name"] = soup.find_all(class_="w3-panel")[2].find("h2").get_text(strip=True)
    cand_dict["constituency"] = soup.find_all(class_="w3-panel")[2].find("h5").get_text(strip=True)
    cand_dict["district"] = re.findall(r'\((.*?)\)', cand_dict["constituency"])[-1]
    cand_dict["so_do_wo"] = soup.find_all(class_="w3-panel")[2].find_all("div")[3].get_text(strip=True).split(":")[-1]
    cand_dict["age"] = soup.find_all(class_="w3-panel")[2].find_all("div")[4].get_text(strip=True).replace('Age:', '').strip()
    cand_dict["party"] = soup.find_all(class_="w3-panel")[2].find_all('div')[1].find('div').get_text(strip=True).replace('Part:','').split(":")[-1]
    cand_dict["assets"], cand_dict["liabilities"] = [value.get_text(strip = True).replace('\xa0', ' ') for value in soup.find_all(class_="w3-table")[0].find_all('b')]
    # print(soup.find_all(class_="w3-table")[0].find_all('b'))
    print(cand_dict)


def parse1(url):
    response = requests.get(url)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    cand_dict = {}
    
    w3_panel = soup.find_all(class_="w3-panel")[2]
    cand_dict["state"] = url.split("/")[3][:-4]
    cand_dict["year"] = url.split("/")[3][-4:]
    cand_dict["name"] = w3_panel.find("h2").get_text(strip=True)
    cand_dict["constituency"] = w3_panel.find("h5").get_text(strip=True)
    cand_dict["district"] = re.findall(r'\((.*?)\)', cand_dict["constituency"])[-1]
    cand_dict["so_do_wo"] = w3_panel.find_all("div")[3].get_text(strip=True).split(":")[-1]
    cand_dict["age"] = w3_panel.find_all("div")[4].get_text(strip=True).replace('Age:', '').strip()
    cand_dict["party"] = w3_panel.find_all('div')[1].find('div').get_text(strip=True).replace('Part:','').split(":")[-1]

    cand_dict["assets"], cand_dict["liabilities"] = [value.get_text(strip = True).replace('\xa0', ' ') for value in soup.find_all(class_="w3-table")[0].find_all('b')]
    cand_dict["self_prof"] = w3_panel.find('p').find('b', string='Self Profession:').next_sibling.strip()
    cand_dict["spouse_prof"] = w3_panel.find('p').find('b', string='Spouse Profession:').next_sibling.strip().replace("\n","")
    w3_red = soup.find_all(class_ = "w3-red")
    if len(w3_red) == 0:
        cand_dict["criminal_cases"] = '0'
    else:
        cand_dict["criminal_cases"] = soup.find_all(class_ = "w3-red")[0].find("span").get_text(strip = True)
    cand_dict["education"] = soup.find_all(class_ = "w3-panel")[4].find_all(class_ = "w3-panel")[2].get_text(strip = True).replace("Educational DetailsCategory:","").replace(",",".").strip()

    return cand_dict
# print(parse1("https://myneta.info/telangana2023/candidate.php?candidate_id=309"))

# state,year,constituency,ac_no,district,sub_region,reservations,candidate_name,party,party_eci,url,winner,gender,age,so_do,address,profession,spouse_profession,criminal_cases,serious_criminal_cases,education,assets,liabilities,net_assets,filed_itr,declared_pan,recontest_url,recontest_assets_this,recontest_assets_last,recontest_assets_change,recontest_remarks