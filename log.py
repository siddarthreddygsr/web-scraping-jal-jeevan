import requests
import pandas as pd
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from district2blocks import dist2bl
from block2village import bl2vl
from village2data import vil_d


logging.basicConfig(filename='web_scraping_log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_village(state_code, dtcode11, bl_codes, village, village_codes):
    try:
        service_level = vil_d(state_code, dtcode11, village[1])
        logging.info(f"Processed: State_name: Maharashtra, district_name: {bl_codes[0]}, block_name: {village_codes[0]}, village_name: {village[0]}, Service level: {service_level}")
        return {
            'State_name': "Maharashtra",
            'district_name': bl_codes[0],
            'block_name': village_codes[0],
            'village_name': village[0],
            'service_level': service_level
        }
    except Exception as e:
        logging.error(f"Error processing village {village[0]}: {str(e)}")
        return None

url = "https://ejalshakti.gov.in/jjmreport/JJMIndia.aspx/JJM_StateDistrictSearch"
state_code = "381"
headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-IN,en-GB;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Content-Type": "application/json; charset=utf-8",
    "Cookie": "_ga_WQYLJRC2X1=GS1.1.1705681106.3.1.1705681170.0.0.0; _ga=GA1.1.1394336993.1705658309; ASP.NET_SessionId=hscmh2fouxqlsxnuq5p1cwe1",
    "Host": "ejalshakti.gov.in",
    "Origin": "https://ejalshakti.gov.in",
    "Referer": "https://ejalshakti.gov.in/jjmreport/JJMIndia.aspx",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "X-Requested-With": "XMLHttpRequest",
}

data = {
    "StCode": state_code,
    "Name": "1"
}

proxies = {
    'http': "http://138.197.102.119:80"
}

try:
    response = requests.post(url, headers=headers, json=data, proxies=proxies)
    response.raise_for_status()
    json_response = response.json()
    data = json_response['d']

    dataframe = []

    def process_data(i):
        keyvalue = i['KeyValue']
        dtcode11 = "".join("%3A" if int(c) == 9 else str(int(c) + 1) for c in keyvalue) + "1"
        bl_codes = dist2bl(state_code=state_code, dt_code=dtcode11)
        results = []
        with ThreadPoolExecutor() as executor:
            for block_code in bl_codes[1]:
                village_codes = bl2vl(state_code, dtcode11, block_code)
                for village in village_codes[1]:
                    results.append(executor.submit(process_village, state_code, dtcode11, bl_codes, village, village_codes))

        
        for future in as_completed(results):
            result = future.result()
            if result:
                dataframe.append(result)

    
    with ThreadPoolExecutor() as executor:
        executor.map(process_data, data)

    
    df = pd.DataFrame(dataframe)

    
    df.to_csv('output.csv', index=False)

except requests.exceptions.RequestException as e:
    logging.error(f"Request failed: {str(e)}")
except Exception as e:
    logging.error(f"Unexpected error: {str(e)}")
