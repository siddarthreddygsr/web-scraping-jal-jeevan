import concurrent
import requests
from bs4 import BeautifulSoup
from candidate_scraper import parse1
import pandas as pd
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

def process_district(district):
    response = requests.get(f"https://myneta.info/telangana2023/index.php?action=show_constituencies&state_id={district+1}")
    soup = BeautifulSoup(response.text, 'html.parser')

    candidate_links = soup.find_all('a', href=lambda href: href and 'candidate.php?candidate_id=' in href)

    candidate_urls = [f"https://myneta.info/telangana2023/{link['href']}" for link in candidate_links]

    return candidate_urls

def process_candidate(candidate_url):
    return parse1(url=candidate_url)

dataframe = []
processed_candidate_urls = set()
dist_cnt = 1
batch_size = 5
candidate_urls_main = []

df_og = pd.read_csv("CANDYdeez.csv")
with tqdm(total=dist_cnt, position=0, desc="Processing Districts", unit="district", dynamic_ncols=True, ascii=" ▖▘▝▗▚▞█", colour="GREEN") as progress_bar:
    for district in range(dist_cnt):
        candidate_urls = process_district(district)

        if not candidate_urls:
            progress_bar.update(100)
            break

        for url in candidate_urls:
            if url not in processed_candidate_urls:
                candidate_urls_main.append(url)
                processed_candidate_urls.add(url)

        progress_bar.update(100 / dist_cnt)
print(len(candidate_urls_main))
existing_urls = set(df_og['url'])
for url in candidate_urls_main:
    candidate_urls_main = [url for url in candidate_urls_main if url not in existing_urls]
print(len(candidate_urls_main))
# Process candidates in batches and append to the CSV after every 5 candidates
for i in range(0, len(candidate_urls_main), batch_size):
    batch_urls = candidate_urls_main[i:i+batch_size]
    
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_candidate, url) for url in batch_urls]

        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Processing candidates", unit="candidate", ascii=" ▖▘▝▗▚▞█", colour="RED"):
            parsed_data = future.result()
            dataframe.append(parsed_data)

    # Append to CSV after every batch
    if i % batch_size == 0:
        df = pd.DataFrame(dataframe)
        df.to_csv("CANDYdeez.csv", mode='a', header=(i == 0))  # Append to CSV, only write header for the first batch

# Close the progress bar
progress_bar.close()
try:
    state_name = list(existing_urls)[0].split("/")[3][:-4]
except:
    try:
        state_name = list(candidate_urls_main)[0].split("/")[3][:-4]
    except:
        state_name = "state_un"
df_main = pd.read_csv("CANDYdeez.csv")
unique_df = df_main.drop_duplicates(subset=['url'])
unique_df.to_csv(f'{state_name}.csv', index=False)