import requests
from bs4 import BeautifulSoup
from candidate_scraper import parse
import pandas as pd
from tqdm import tqdm

dataframe = []
candidate_urls_main =  []
progress_bar = tqdm(total=50, position=0, desc="Processing Districts", unit="district", dynamic_ncols=True, ascii=" ▖▘▝▗▚▞█", colour="GREEN")
dist_cnt = 100
progress_made = 0
for district in range(dist_cnt):
    response = requests.get(f"https://myneta.info/telangana2023/index.php?action=show_constituencies&state_id={district+1}")
    soup = BeautifulSoup(response.text, 'html.parser')

    candidate_links = soup.find_all('a', href=lambda href: href and 'candidate.php?candidate_id=' in href)

    candidate_ids = [link['href'].split('=')[1] for link in candidate_links]

    candidate_urls = [f"https://myneta.info/telangana2023/{link['href']}" for link in candidate_links]
    
    if len(candidate_urls) == 0:
        progress_bar.update(100-progress_made)
        break
    else:
        candidate_urls_main += candidate_urls
    progress_made += 100/dist_cnt
    progress_bar.update(100/dist_cnt)
progress_bar.close()

for candidate_url in tqdm(candidate_urls_main, desc="Processing candidates", unit="candidate",  ascii=" ▖▘▝▗▚▞█", colour="RED"):
    parsed_data = parse(url=candidate_url)
    # print(parsed_data)
    dataframe.append(parsed_data)

df = pd.DataFrame(dataframe)
df.to_csv("Telangana_2023.csv")