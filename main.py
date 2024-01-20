import requests
from district2blocks import dist2bl
from block2village import bl2vl
from village2data import vil_d

url = "https://ejalshakti.gov.in/jjmreport/JJMIndia.aspx/JJM_StateDistrictSearch"
state_code = "471"
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

response = requests.post(url, headers=headers, json=data)

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
        village_codes = bl2vl(state_code,dtcode11,block_code)
        for village in village_codes[1]:
            print(f"block_name: {bl_codes[0]}, villaage name: {village_codes[0]} Service level:{vil_d(state_code,dtcode11,village)}")
