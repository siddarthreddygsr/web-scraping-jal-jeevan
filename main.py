import requests
import pandas as pd
from modules.district2blocks import dist2bl
from modules.block2village import bl2vl
from modules.village2data import vil_d


url = "https://ejalshakti.gov.in/jjmreport/JJMIndia.aspx/JJM_StateDistrictSearch"
state_code = "481"
headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-IN,en-GB;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Content-Type": "application/json; charset=utf-8",
    "Cookie": "_ga_WQYLJRC2X1=GS1.1.1706117075.6.1.1706117086.0.0.0; ASP.NET_SessionId=hgnliqs5jkzjbugnypsa0by4; _ga=GA1.1.1394336993.1705658309",
    "Host": "ejalshakti.gov.in",
    "Origin": "https://ejalshakti.gov.in",
    "Referer": "https://ejalshakti.gov.in/jjmreport/JJMIndia.aspx",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "X-Requested-With": "XMLHttpRequest",
}
proxies = {
        'http':"http://138.197.102.119:80"
    }
data = {
    "StCode": state_code,
    "Name": "1"
}

response = requests.post(url, headers=headers, json=data,proxies=proxies)

json_response = response.json()
data = json_response['d']
for i in data:
    keyvalue = i['KeyValue']
    dtcode11 = ""
    for i in keyvalue:
        if int(i) == 9:
            dtcode11 += "%3A"
        else:
            dtcode11 += str(int(i)+1)
    dtcode11 += "1"
    bl_codes = dist2bl(state_code=state_code, dt_code=dtcode11)
    for block_code in bl_codes[1]:
        blocks_df = pd.read_csv("block.csv")
        blocks_dframe = []
        if block_code in blocks_df['Block_id'].values:
            print('block completed in prev iteration')
            continue
        df = pd.read_csv("output.csv")
        dataframe = []
        village_codes = bl2vl(state_code,dtcode11,block_code)
        for village in village_codes[1]:
            if village[1] in df['village_code'].values:
                print("village scanned skipping..")
            else:
                print(f"State_name: Andhra Pradesh, district_name: {bl_codes[0]}, block_name: {village_codes[0]}, village_name: {village[0]}, village_code: {village[1]} ,Service level:{vil_d(state_code,dtcode11,village[1])}")
            dataframe.append({
                'State_name':"Andhra Pradesh",
                'district_name': bl_codes[0],
                'block_name': village_codes[0],
                'village_name': village[0],
                'village_code':village[1],
                'service_level': vil_d(state_code, dtcode11, village[1])
            })
        blocks_dframe.append({
            'Block_name': village_codes[0],
            'Block_id': block_code
        })
        blocks_df_new = pd.DataFrame(blocks_dframe)
        blocks_df_save = pd.concat([blocks_df,blocks_df_new], ignore_index=True)
        blocks_df_save.to_csv('block.csv', index=False)
        df_new = pd.DataFrame(dataframe)
        df_save = pd.concat([df, df_new], ignore_index=True)
        df_save.to_csv('output.csv', index=False)

