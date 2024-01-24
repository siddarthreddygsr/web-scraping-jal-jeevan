import requests

def fetch_village_data(state_code, dt_code, vil_code):
    url = "https://ejalshakti.gov.in/jjmreport/JJMVillage_Profile.aspx/BindSchemeInfo"

    payload = {
        "stcode": state_code,
        "dtcode": dt_code,
        "cat": "11",
        "subcat": "11",
        "param": "11",
        "VillageId": vil_code
    }

    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Origin": "https://ejalshakti.gov.in",
        "Referer": "https://ejalshakti.gov.in/jjmreport/JJMVillage_Profile.aspx",
        "X-Requested-With": "XMLHttpRequest",
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for bad response status
        return response.json()  # Assuming the response is JSON, adjust accordingly if it's different
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
