import requests

def bl2vl(state_code,dt_code,bl_code):
    url = "https://ejalshakti.gov.in/jjmreport/JJMVillageMapView.aspx/BindvillageMap"
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
        "Cat":"11",
        "SubCat":"11",
        "Param":"11",
        "StCode11":state_code,
        "DtCode11":dt_code,
        "lgd_BlockId":bl_code
    }
    response = requests.post(url, headers=headers, json=data)
    village_data = response.json()['d']
    village_codes = []
    village_codes.append(village_data[0]['Name'])
    village_codes.append([])
    for village in village_data:
        # print(f'Name: {i["Name"]},KeyID: {i["KeyId"]}, KeyValue: {i["KeyValue"]}')
        vil_code = village['KeyId']
        vil_encode = ""
        for i in vil_code:
            if int(i) == 9:
                vil_encode += "%3A"
            else:
                vil_encode += str(int(i)+1)
        vil_encode += "1"
        village_codes[1].append(vil_encode)
    return village_codes
# print(bl2vl("471",'8521','63%3A11'))