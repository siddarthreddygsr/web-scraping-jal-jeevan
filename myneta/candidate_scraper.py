from bs4 import BeautifulSoup
import requests
import re
import pdb
import json
from pprint import pprint

proxies = {
        'http':"http://20.111.54.16:8123"
    }

def cases_table(soup):
    try:
        cases_table_rows = soup.find('table', attrs={'id':'cases'}).find_all('tr')
        cases_meta_data = [cell.text for cell in cases_table_rows[0].find_all('td')]
        cases_json_data = []
        for row in cases_table_rows[1:]:
            row_data = {}
            flag = 0
            edge_cases = 0
            for cell in row.find_all('td'):
                try:
                    row_data[cases_meta_data[flag]] = cell.text.replace('\xa0', ' ')
                    flag += 1
                except:
                    edge_cases += 1
            if bool(row_data):
                cases_json_data.append(row_data)
        cases_data = json.dumps(cases_json_data)
    except:
        cases_data = "No data available on site"
    return cases_data


def parse(url, proxy_flag):
    if proxy_flag:
        response = requests.get(url, proxies=proxies)
    else:
        response = requests.get(url)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    cand_dict = {}
    
    try:
        w3_panel = soup.find_all(class_="w3-panel")[2]
        cand_dict["state"] = url.split("/")[3][:-4]
        cand_dict["year"] = url.split("/")[3][-4:]
        cand_dict["name"] = w3_panel.find("h2").get_text(strip=True)
        cand_dict["constituency"] = w3_panel.find("h5").get_text(strip=True)
        cand_dict["district"] = re.findall(r'\((.*?)\)', cand_dict["constituency"])[-1]
        cand_dict["so_do_wo"] = w3_panel.find_all("div")[3].get_text(strip=True).split(":")[-1]
        cand_dict["age"] = w3_panel.find_all("div")[4].get_text(strip=True).replace('Age:', '').strip()
        cand_dict["party"] = w3_panel.find_all('div')[1].find('div').get_text(strip=True).replace('Part:','').split(":")[-1]
        cand_dict["url"] = url
        it_table_rows = soup.find('table', attrs={'id':'income_tax'}).find_all('tr')
        meta_data = [cell.text for cell in it_table_rows[0].find_all('th')]
        json_data = []
        for row in it_table_rows:
            row_data = {}
            flag = 0
            for cell in row.find_all('td'):
                row_data[meta_data[flag]] = cell.text.replace('\xa0', ' ')
                flag += 1
            if bool(row_data):
                json_data.append(row_data)
        cand_dict["income_tax_data"] = json.dumps(json_data)
        cand_dict["cases_data"] = cases_table(soup)
        cand_dict["self_prof"] = w3_panel.find('p').find('b', string='Self Profession:').next_sibling.strip()
        cand_dict["spouse_prof"] = w3_panel.find('p').find('b', string='Spouse Profession:').next_sibling.strip().replace("\n","")
        w3_red = soup.find_all(class_ = "w3-red")
        if len(w3_red) == 0:
            cand_dict["criminal_cases"] = '0'
        else:
            cand_dict["criminal_cases"] = soup.find_all(class_ = "w3-red")[0].find("span").get_text(strip = True)
        cand_dict["education"] = soup.find_all(class_ = "w3-panel")[4].find_all(class_ = "w3-panel")[2].get_text(strip = True).replace("Educational DetailsCategory:","").replace(",",".").strip()
        cand_dict["assets"], cand_dict["liabilities"] = [value.get_text(strip = True).replace('\xa0', ' ') for value in soup.find_all(class_="w3-table")[0].find_all('b')]
    except:
        print(f"{url}\n{url}\n{url}\n{url}\n{url}\n")
    return cand_dict
# print(parse("https://myneta.info/telangana2023/candidate.php?candidate_id=309"))



# pprint(table1("https://myneta.info/telangana2023/candidate.php?candidate_id=453"))
