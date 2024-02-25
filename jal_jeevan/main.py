import requests
import pandas as pd
from modules.district2blocks import dist2bl
from modules.block2village import bl2vl
from modules.village2data import vil_d
import pdb
from tqdm import tqdm


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
        'http':"http://20.111.54.16:8123"
    }
data = {
    "StCode": state_code,
    "Name": "1"
}

response = requests.post(url, headers=headers, json=data,
                         proxies=proxies
                         )

json_response = response.json()
data = json_response['d']
for i in data:
    keyvalue = i['KeyValue']
    dist_name = i['KeyName']

    dtcode11 = ""
    for i in keyvalue:
        if int(i) == 9:
            dtcode11 += "%3A"
        else:
            dtcode11 += str(int(i)+1)
    dtcode11 += "1"
    info_dict = {
            "state_name" : "Andhra Pradesh",
            "district_name" : dist_name,
        }
    block_info_arr = dist2bl(state_code=state_code, 
                             dt_code=dtcode11, 
                             proxies=proxies,
                             info_dict=info_dict)
    for block_code_dict in block_info_arr:
        block_code = block_code_dict['blcode11']
        block_name = block_code_dict['block_name']
        blocks_df = pd.read_csv("block.csv")
        blocks_dframe = []
        if block_code in blocks_df['Block_id'].values:
            print('block completed in prev iteration')
            continue
        df = pd.read_csv("output.csv")
        dataframe = []
        vil_dict_arr = bl2vl(state_code,dtcode11,block_code, info_dict=block_code_dict,
                         proxies=proxies
                         )
        for village in tqdm(vil_dict_arr, desc="Processing Villages", unit="village"):
            final_info_dict = village.copy()
            service_level = vil_d(state_code, dtcode11, village['vil_encode'],proxies=proxies)
            final_info_dict['service_level'] = service_level
            # pdb.set_trace()
            dataframe.append(final_info_dict)
        blocks_dframe.append({
            'Block_name': block_name,
            'Block_id': block_code
        })
        blocks_df_new = pd.DataFrame(blocks_dframe)
        blocks_df_save = pd.concat([blocks_df,blocks_df_new], ignore_index=True)
        blocks_df_save.to_csv('block.csv', index=False)
        df_new = pd.DataFrame(dataframe)
        df_save = pd.concat([df, df_new], ignore_index=True)
        df_save.to_csv('output.csv', index=False)


