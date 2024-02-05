import requests
from bs4 import BeautifulSoup
from candidate_scraper import parse, parse1
from concurrent.futures import ThreadPoolExecutor

def process_candidate(candidate_url):
    parse(url=candidate_url)

def main():
    with ThreadPoolExecutor() as executor:  # Adjust the number of workers as needed
        for district in range(2):
            response = requests.get(f"https://myneta.info/telangana2023/index.php?action=show_constituencies&state_id={district}")
            soup = BeautifulSoup(response.text, 'html.parser')

            candidate_links = soup.find_all('a', href=lambda href: href and 'candidate.php?candidate_id=' in href)

            candidate_urls = [f"https://myneta.info/telangana2023/{link['href']}" for link in candidate_links]

            # Use executor.map to process the candidate URLs in parallel
            executor.map(process_candidate, candidate_urls)

if __name__ == "__main__":
    main()
