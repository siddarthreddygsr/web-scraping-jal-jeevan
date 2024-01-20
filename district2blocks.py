import requests

def dist2bl(state_code,dt_code):
    url = "https://ejalshakti.gov.in/jjmreport/JJMBlockMapView.aspx/BindBlockMap"
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-IN,en-GB;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "Content-Length": "76",
        "Content-Type": "application/json; charset=utf-8",
        "Cookie": "_ga_WQYLJRC2X1=GS1.1.1705681106.3.1.1705684768.0.0.0; _ga=GA1.1.1394336993.1705658309; ASP.NET_SessionId=hscmh2fouxqlsxnuq5p1cwe1",
        "Host": "ejalshakti.gov.in",
        "Origin": "https://ejalshakti.gov.in",
        "Referer": "https://ejalshakti.gov.in/jjmreport/JJMBlockMapView.aspx",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
        "X-Requested-With": "XMLHttpRequest",
    }
    data = {
        "Cat": "11",
        "SubCat": "11",
        "Param": "11",
        "StCode11": state_code,
        "DtCode11": dt_code
    }

    response = requests.post(url, headers=headers, json=data)
    block_data = response.json()['d']
    bl_codes = []
    try:
        name = "" + block_data[0]['Name']
    except:
        name = ""
        print(block_data)
    bl_codes.append(name)
    bl_codes.append([])
    for block in block_data:
        keyvalue = block['KeyValue']
        blcode11 = ""
        for i in keyvalue:
            if int(i) == 9:
                blcode11 += "%3A"
            else:
                blcode11 += str(int(i)+1)
        blcode11 += "1"
        bl_codes[1].append(blcode11)
    return bl_codes
# dist2bl("471","8521")
