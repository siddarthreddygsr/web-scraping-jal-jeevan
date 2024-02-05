import requests
from bs4 import BeautifulSoup
from candidate_scraper import parse,parse1
import pandas as pd
from tqdm import tqdm

dataframe = []
candidate_urls_main =  []
for district in tqdm(range(2), desc="Processing Districts", unit="district", dynamic_ncols=True, ascii=" ▖▘▝▗▚▞█", colour="GREEN"):
    response = requests.get(f"https://myneta.info/telangana2023/index.php?action=show_constituencies&state_id={district+1}")
    soup = BeautifulSoup(response.text, 'html.parser')

    candidate_links = soup.find_all('a', href=lambda href: href and 'candidate.php?candidate_id=' in href)

    candidate_ids = [link['href'].split('=')[1] for link in candidate_links]

    candidate_urls_main += [f"https://myneta.info/telangana2023/{link['href']}" for link in candidate_links]
for candidate_url in tqdm(candidate_urls_main, desc="Processing candidates", unit="candidate",  ascii=" ▖▘▝▗▚▞█", colour="RED"):
    parsed_data = parse(url=candidate_url)
    dataframe.append(parsed_data)

df = pd.DataFrame(dataframe)
df.to_csv("CANDYdeez.csv")

