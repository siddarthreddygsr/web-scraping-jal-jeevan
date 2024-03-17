import requests
from bs4 import BeautifulSoup
from candidate_scraper import parse
import pandas as pd
from tqdm import tqdm
import pdb

dataframe = []
candidate_urls_main =  []
csv_filename = "Telangana_2023.csv"
save_frequency = 1

### STEP 1: go through all the districts and aquire all candidate ID's and generate URL's
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

### STEP 2: Cleaning check if the file exists and if so then remove the URL's which have already been scraped from the current list
try:
    old_df = pd.read_csv(csv_filename)
    urls_list = old_df['url'].tolist()
    remaininng_urls = list(set(candidate_urls_main) - set(urls_list))
    removed_count = len(candidate_urls_main) - len(remaininng_urls)
    print(f"\nFound {removed_count} URL's which were already scraped")
    print(f"Removing {removed_count} URL's from list.\n")
except:
    remaininng_urls = candidate_urls_main
    print("\nFILE NOT DETECTED...")
    print("MAKE SURE THE PATH IS CORRECT IF IT EXISTS!!!")
    print("IF IT'S CORRECT AND YOU DON'T HAVE A CHECKPOINT FILE.\nYOU ARE GOOD GO A NEW FILE WILL BE GENERATED\n")

### Step 3: JUST SCRAPE THE REMAINING OFCC
for i, candidate_url in enumerate(tqdm(remaininng_urls, desc="Processing candidates", unit="candidate",  ascii=" ▖▘▝▗▚▞█", colour="RED"), 1):
    parsed_data = parse(url=candidate_url)
    dataframe.append(parsed_data)
    if i % save_frequency == 0:
        df = pd.DataFrame(dataframe)
        if old_df is not None:
            df = pd.concat([old_df,df], ignore_index=True)
            df.to_csv(csv_filename, index=False) 

df = pd.DataFrame(dataframe)
df.to_csv(csv_filename)