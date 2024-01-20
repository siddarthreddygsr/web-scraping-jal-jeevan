import requests

def vil_d(state_code,dt_code,vil_code):
    url = "https://ejalshakti.gov.in/jjmreport/JJMVillage_Profile.aspx/Bind_Fhtc_info"
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
        "StCode11":state_code,
        "DtCode11":dt_code,
        "VillCode":vil_code,
        "Cat":"11",
        "SubCat":"11",
        "Param":"11"
    }

    response = requests.post(url, headers=headers, json=data)
    service_level_data = response.json()['d'][0]['ServiceLevel']
    return service_level_data
# vil_d(1,1)
