import orjson as json
import requests
import pandas as pd
from pprint import pprint
from itertools import count

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

def assign_park_ids(df):
    # 分類停車場和路邊車格
    df['Type'] = df['carTotalNum'].apply(lambda x: 'PL' if x > 0 else 'PS')

    # 生成唯一的 parkId
    pl_counter = count(1)
    ps_counter = count(1)
    
    def generate_id(row):
        if row['Type'] == 'PL':
            return f"PL{next(pl_counter):03d}"
        else:
            return f"PS{next(ps_counter):03d}"
    
    df['parkId'] = df.apply(generate_id, axis=1)
    return df

def get_final_data():
	data = get_data("https://itaipeiparking.pma.gov.taipei/MapAPI/GetAllPOIData")
	data = filter_data(data)
	data = assign_park_ids(data)
	
	return data

if __name__ == "__main__":
	data = get_data("https://itaipeiparking.pma.gov.taipei/MapAPI/GetAllPOIData")
	data = filter_data(data)
	data = assign_park_ids(data)
      
	data.to_csv("data.csv", index=False)
	pprint(data)