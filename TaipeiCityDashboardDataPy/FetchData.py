import orjson as json
import requests
import pandas as pd
from pprint import pprint

def get_data(url: str):
	payload = 'catagory=car&lat=25.04833&lon=121.52224&type=1'
	headers = {
	'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
	'DNT': '1',
	'sec-ch-ua-mobile': '?0',
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
	'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
	'Accept': '*/*',
	'X-Requested-With': 'XMLHttpRequest',
	'sec-ch-ua-platform': '"macOS"',
	'host': 'itaipeiparking.pma.gov.taipei',
	'Cookie': 'ASP.NET_SessionId=nz0lwjk2owgxgmxn02fzyeyy'
	}

	response = requests.request("POST", url, headers=headers, data=payload)
	response = json.loads(response.text)
	
	return response

def filter_data(data: list):
	"""
	# filter
	- address
	- carTotalNum
	- carRemainderNum
	- motorTotalNum
	- motorRemainderNum
	- payex
	- parkName
	- parkId
	- entrance(包含Lon, Lat, ~~Add~~)
	- lat
	- lon
	- fullRateLevel(層數)
	- servicetime
	- tel
	- pregnancy_First(婦幼)
	- remark(路邊車格才需要)
	"""
	
	df = pd.DataFrame(data)
	df = df[["address", "carTotalNum", "carRemainderNum", "motorTotalNum", "motorRemainderNum", "payex", "parkName", "parkId", "entrance", "lat", "lon", "fullRateLevel", "servicetime", "tel", "pregnancy_First", "remark"]]
	return df

if __name__ == "__main__":
	# pprint(get_data("https://itaipeiparking.pma.gov.taipei/MapAPI/GetAllPOIData"))
	pprint(filter_data(get_data("https://itaipeiparking.pma.gov.taipei/MapAPI/GetAllPOIData")).to_dict(orient="records")[0])