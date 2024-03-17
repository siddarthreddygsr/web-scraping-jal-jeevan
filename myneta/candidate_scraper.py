from bs4 import BeautifulSoup
import requests
import re
import pdb
import json

def parse(url):
    response = requests.get(url)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    cand_dict = {}
    
    try:
        w3_panel = soup.find_all(class_="w3-panel")[2]
        cand_dict["id"] = url.split("=")[-1]
        cand_dict["state"] = url.split("/")[3][:-4]
        cand_dict["year"] = url.split("/")[3][-4:]
        cand_dict["name"] = w3_panel.find("h2").get_text(strip=True)
        cand_dict["constituency"] = w3_panel.find("h5").get_text(strip=True)
        cand_dict["district"] = re.findall(r'\((.*?)\)', cand_dict["constituency"])[-1]
        cand_dict["so_do_wo"] = w3_panel.find_all("div")[3].get_text(strip=True).split(":")[-1]
        cand_dict["age"] = w3_panel.find_all("div")[4].get_text(strip=True).replace('Age:', '').strip()
        cand_dict["party"] = w3_panel.find_all('div')[1].find('div').get_text(strip=True).replace('Part:','').split(":")[-1]
        cand_dict["url"] = url
        cand_dict["self_prof"] = w3_panel.find('p').find('b', string='Self Profession:').next_sibling.strip()
        cand_dict["spouse_prof"] = w3_panel.find('p').find('b', string='Spouse Profession:').next_sibling.strip().replace("\n","")
        w3_red = soup.find_all(class_ = "w3-red")
        if len(w3_red) == 0:
            cand_dict["criminal_cases"] = '0'
        else:
            cand_dict["criminal_cases"] = soup.find_all(class_ = "w3-red")[0].find("span").get_text(strip = True)
        cand_dict["education"] = soup.find_all(class_ = "w3-panel")[4].find_all(class_ = "w3-panel")[2].get_text(strip = True).replace("Educational DetailsCategory:","").replace(",",".").strip()
        cand_dict["assets"], cand_dict["liabilities"] = [value.get_text(strip = True).replace('\xa0', ' ') for value in soup.find_all(class_="w3-table")[0].find_all('b')]
        # pdb.set_trace()
    except:
        assets_liabilities = [value.get_text(strip=True).replace('\xa0', ' ') for value in soup.find_all(class_="w3-table")[0].find_all('b')]
        cand_dict["assets"] = assets_liabilities[1] if len(assets_liabilities) >= 1 else None
        cand_dict["liabilities"] = assets_liabilities[3] if len(assets_liabilities) >= 2 else None
        # print(f"{url}\n{url}\n{url}\n{url}\n{url}\n")
    return cand_dict
# print(parse("https://myneta.info/telangana2023/candidate.php?candidate_id=309"))

# def table1(url):
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, 'html.parser')
#     table_rows = soup.find('table', attrs={'id':'income_tax'}).find_all('tr')
#     meta_data = [cell.text for cell in table_rows[0].find_all('th')]
#     json_data = []
#     for row in table_rows:
#         row_data = {}
#         flag = 0
#         for cell in row.find_all('td'):
#             row_data[meta_data[flag]] = cell.text.replace('\xa0', ' ')
#             flag += 1
#         if bool(row_data):
#             json_data.append(row_data)
#     income_tax_data = json.dumps(json_data)
#     return income_tax_data


# print(table1("https://myneta.info/telangana2023/candidate.php?candidate_id=309"))