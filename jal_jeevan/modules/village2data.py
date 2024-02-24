import requests

def vil_d(
        state_code,
        dt_code,
        vil_code,
        proxies={'http':"http://143.110.232.177:80"}
          ):
    url = "https://ejalshakti.gov.in/jjmreport/JJMVillage_Profile.aspx/Bind_Fhtc_info"
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-IN,en-GB;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "Content-Length": "76",
        "Content-Type": "application/json; charset=utf-8",
        "Cookie": "_ga_WQYLJRC2X1=GS1.1.1706117075.6.1.1706117086.0.0.0; ASP.NET_SessionId=hgnliqs5jkzjbugnypsa0by4; _ga=GA1.1.1394336993.1705658309",
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
    response = requests.post(url, headers=headers, json=data,proxies=proxies)
    service_level_data = response.json()['d'][0]['ServiceLevel']
    return service_level_data
