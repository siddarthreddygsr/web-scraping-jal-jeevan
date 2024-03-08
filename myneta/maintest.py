#just data


# import requests
# from bs4 import BeautifulSoup

# # Function to scrape data for a single candidate
# def scrape_candidate_data(candidate_url):
#     response = requests.get(candidate_url)
#     soup = BeautifulSoup(response.text, 'html.parser')

#     cand_dict = {}
#     cand_dict["name"] = soup.find_all(class_="w3-panel")[2].find("h2").get_text(strip=True)
#     cand_dict["constituency"] = soup.find_all(class_="w3-panel")[2].find("h5").get_text(strip=True)
#     cand_dict["so_do_wo"] = soup.find_all(class_="w3-panel")[2].find_all("div")[3].get_text(strip=True).split(":")[-1]
#     cand_dict["age"] = soup.find_all(class_="w3-panel")[2].find_all("div")[4].get_text(strip=True).replace('Age:', '').strip()
#     cand_dict["party"] = soup.find_all(class_="w3-panel")[2].find_all('div')[1].find('div').get_text(strip=True).replace('Part:','').split(":")[-1]
#     #cand_dict["assets"], cand_dict["liabilities"] = [value.get_text(strip=True).replace('\xa0', ' ') for value in soup.find_all(class_="w3-table")[0].find_all('b')]
#      # Extract assets and liabilities with default values
#     assets_liabilities = [value.get_text(strip=True).replace('\xa0', ' ') for value in soup.find_all(class_="w3-table")[0].find_all('b')]
#     cand_dict["assets"] = assets_liabilities[0] if len(assets_liabilities) >= 1 else None
#     cand_dict["liabilities"] = assets_liabilities[1] if len(assets_liabilities) >= 2 else None
#     return cand_dict

# # Main script
# dist_cnt = 100

# for district in range(dist_cnt):
#     district_url = f"https://myneta.info/telangana2023/index.php?action=show_constituencies&state_id={district+1}"
#     response_district = requests.get(district_url)
#     soup_district = BeautifulSoup(response_district.text, 'html.parser')

#     candidate_links = soup_district.find_all('a', href=lambda href: href and 'candidate.php?candidate_id=' in href)

#     for link in candidate_links:
#         candidate_url = f"https://myneta.info/telangana2023/{link['href']}"
#         candidate_data = scrape_candidate_data(candidate_url)
#         print(f"Data for Candidate from {district+1} district:", candidate_data)
#         # You can save or process the data as needed


#DATA INTO CSV
import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

# Function to scrape data for a single candidate
def scrape_candidate_data(candidate_url):
    response = requests.get(candidate_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    cand_dict = {}
    cand_dict["name"] = soup.find_all(class_="w3-panel")[2].find("h2").get_text(strip=True)
    cand_dict["constituency"] = soup.find_all(class_="w3-panel")[2].find("h5").get_text(strip=True)
    cand_dict["so_do_wo"] = soup.find_all(class_="w3-panel")[2].find_all("div")[3].get_text(strip=True).split(":")[-1]
    cand_dict["age"] = soup.find_all(class_="w3-panel")[2].find_all("div")[4].get_text(strip=True).replace('Age:', '').strip()
    cand_dict["party"] = soup.find_all(class_="w3-panel")[2].find_all('div')[1].find('div').get_text(strip=True).replace('Part:','').split(":")[-1]
    #cand_dict["assets"], cand_dict["liabilities"] = [value.get_text(strip=True).replace('\xa0', ' ') for value in soup.find_all(class_="w3-table")[0].find_all('b')]
    # Extract assets and liabilities with default values
    assets_liabilities = [value.get_text(strip=True).replace('\xa0', ' ') for value in soup.find_all(class_="w3-table")[0].find_all('b')]
    cand_dict["assets"] = assets_liabilities[0] if len(assets_liabilities) >= 1 else None
    cand_dict["liabilities"] = assets_liabilities[1] if len(assets_liabilities) >= 2 else None
    return cand_dict

# Main script
dist_cnt = 100
output_filename = "output_myneta.csv"

# Initialize an empty DataFrame to store data
all_data_df = pd.DataFrame()

for district in range(dist_cnt):
    district_url = f"https://myneta.info/Rajasthan2023/index.php?action=show_constituencies&state_id={district+1}"
    response_district = requests.get(district_url)
    soup_district = BeautifulSoup(response_district.text, 'html.parser')

    candidate_links = soup_district.find_all('a', href=lambda href: href and 'candidate.php?candidate_id=' in href)

    district_data_list = []

    for link in candidate_links:
        candidate_url = f"https://myneta.info/Rajasthan2023/{link['href']}"
        candidate_data = scrape_candidate_data(candidate_url)
        print(f"Data for Candidate from {district+1} district:", candidate_data)
        district_data_list.append(candidate_data)

    # Create a DataFrame for the district data
    district_df = pd.DataFrame(district_data_list)
    all_data_df = pd.concat([all_data_df, district_df], ignore_index=True)

    # Save the DataFrame to CSV after processing each district
    all_data_df.to_csv(output_filename, index=False)

# Save the final DataFrame to CSV after processing all districts
all_data_df.to_csv(output_filename, index=False)


#DATA INTO CSV RESUME FUNCTION

# import requests
# from bs4 import BeautifulSoup
# import pandas as pd
# import csv
# import os

# # Function to scrape data for a single candidate
# def scrape_candidate_data(candidate_url):
#     response = requests.get(candidate_url)
#     soup = BeautifulSoup(response.text, 'html.parser')

#     cand_dict = {}
#     cand_dict["name"] = soup.find_all(class_="w3-panel")[2].find("h2").get_text(strip=True)
#     cand_dict["constituency"] = soup.find_all(class_="w3-panel")[2].find("h5").get_text(strip=True)
#     cand_dict["so_do_wo"] = soup.find_all(class_="w3-panel")[2].find_all("div")[3].get_text(strip=True).split(":")[-1]
#     cand_dict["age"] = soup.find_all(class_="w3-panel")[2].find_all("div")[4].get_text(strip=True).replace('Age:', '').strip()
#     cand_dict["party"] = soup.find_all(class_="w3-panel")[2].find_all('div')[1].find('div').get_text(strip=True).replace('Part:','').split(":")[-1]
#     #cand_dict["assets"], cand_dict["liabilities"] = [value.get_text(strip=True).replace('\xa0', ' ') for value in soup.find_all(class_="w3-table")[0].find_all('b')]
#     # Extract assets and liabilities with default values
#     assets_liabilities = [value.get_text(strip=True).replace('\xa0', ' ') for value in soup.find_all(class_="w3-table")[0].find_all('b')]
#     cand_dict["assets"] = assets_liabilities[0] if len(assets_liabilities) >= 1 else None
#     cand_dict["liabilities"] = assets_liabilities[1] if len(assets_liabilities) >= 2 else None
#     return cand_dict

# # Function to load or create progress information
# def load_progress_info():
#     progress_file = "progress_info.txt"
#     if os.path.exists(progress_file):
#         with open(progress_file, "r") as file:
#             last_scraped_candidate_id = int(file.read())
#         return last_scraped_candidate_id
#     else:
#         return 0

# # Function to save progress information
# def save_progress_info(candidate_id):
#     progress_file = "progress_info.txt"
#     with open(progress_file, "w") as file:
#         file.write(str(candidate_id))

# # Main script
# dist_cnt = 100
# output_filename = "output.csv"

# # Load the last scraped candidate ID
# last_scraped_candidate_id = load_progress_info()

# # Initialize an empty DataFrame to store data
# all_data_df = pd.DataFrame()

# for district in range(dist_cnt):
#     district_url = f"https://myneta.info/telangana2023/index.php?action=show_constituencies&state_id={district+1}"
#     response_district = requests.get(district_url)
#     soup_district = BeautifulSoup(response_district.text, 'html.parser')

#     candidate_links = soup_district.find_all('a', href=lambda href: href and 'candidate.php?candidate_id=' in href)

#     district_data_list = []

#     for link in candidate_links:
#         candidate_id = int(link['href'].split('=')[1])
#         if candidate_id <= last_scraped_candidate_id:
#             print(f"Already scraped Candidate ID {candidate_id}. Skipping...")
#             continue

#         candidate_url = f"https://myneta.info/telangana2023/{link['href']}"
#         candidate_data = scrape_candidate_data(candidate_url)
#         print(f"Data for Candidate ID {candidate_id} from {district+1} district:", candidate_data)
#         district_data_list.append(candidate_data)

#     # Create a DataFrame for the district data
#     district_df = pd.DataFrame(district_data_list)
#     all_data_df = pd.concat([all_data_df, district_df], ignore_index=True)

#     # Save the DataFrame to CSV after processing each district
#     all_data_df.to_csv(output_filename, index=False)

#     # Update the last scraped candidate ID
#     if district_data_list:
#         last_scraped_candidate_id = max(candidate_id for candidate_id in (int(link['href'].split('=')[1]) for link in candidate_links))



# # Save the final DataFrame to CSV after processing all districts
# all_data_df.to_csv(output_filename, index=False)

# # Save the last scraped candidate ID for resuming next time
# save_progress_info(last_scraped_candidate_id)
