import requests
import pdb

def dist2bl(state_code,dt_code,info_dict,proxies={'http':"http://143.110.232.177:80"}):
    url = "https://ejalshakti.gov.in/jjmreport/JJMBlockMapView.aspx/BindBlockMap"
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
        "Cat": "11",
        "SubCat": "11",
        "Param": "11",
        "StCode11": state_code,
        "DtCode11": dt_code
    }
    response = requests.post(url, headers=headers, json=data,proxies=proxies)
    block_data = response.json()['d']
    info_dict_arr = []
    for block in block_data:
        keyvalue = block['KeyValue']
        blcode11 = ""
        for i in keyvalue:
            if int(i) == 9:
                blcode11 += "%3A"
            else:
                blcode11 += str(int(i)+1)
        blcode11 += "1"
        current_info_dict = info_dict.copy()
        current_info_dict['block_name'] = block['Name']
        current_info_dict['blcode11'] = blcode11

        info_dict_arr.append(current_info_dict)
    return info_dict_arr
# dist2bl("471","8521")
