import orjson as json
import requests
import pandas as pd
import re
from pprint import pprint
from itertools import count
from urllib.parse import unquote

class DataFetcher():
	"""
		取得API資料或是檔案資料

		Args:
			name (str): 資料名稱
			url (str): 資料來源
			method (str): 請求方法
			headers (dict): 請求標頭
			params (dict): 請求參數
	"""
	def __init__(self, name: str, url: str = "", method: str = "", headers: dict = {}, params: dict = {}) -> None:
		self.name = name
		self.url = url
		self.json_data = None
		self.method = method
		self.headers = headers
		self.params = params
	
	def get_data(self):
		if self.method == "GET":
			self.json_data = requests.get(self.url, params=self.params).json()
		elif self.method == "POST":
			self.json_data = requests.post(self.url, data=self.params).json()
		elif self.method == "DOWNLOAD":
			self._download_file()
		else:
			raise ValueError("Invalid Method")
	
	def get_filname_from_content_disposition(self, cd: str):
		if not cd: return None
		
		fname = re.findall('filename="(.+)"', cd)
		if len(fname) == 0: return None
		return unquote(fname[0])

	def _download_file(self):
		self.json_data = requests.get(self.url, headers=self.headers, stream=True)
		fname = self.get_filname_from_content_disposition(self.json_data.headers.get('Content-Disposition'))

		with open(f"{fname}", "wb") as f:
			for chunk in self.json_data.iter_content(chunk_size=1024):
				f.write(chunk)
		print(f"File {fname} downloaded successfully")


if __name__ == "__main__":
	# 災害應變避難所
	evacuation_shelter = DataFetcher(
		name="EvacuationShelter",
		url="https://data.taipei/api/frontstage/tpeod/dataset/resource.download?rid=9def0ac0-ad65-4f34-a8a6-aeba704c70d4",
		method="DOWNLOAD",
	)
	evacuation_shelter.get_data()

	# 災害通報(tel)
	disaster_notifications = DataFetcher(
		name="DisasterNotifications",
		url="https://data.taipei/api/dataset/a9ff987d-3552-443f-8aed-3be10aac0a9d/resource/29fa440a-221c-4c64-98eb-509188431064/download",
		method="DOWNLOAD",
	)
	disaster_notifications.get_data()

	# 防災學校
	disaster_prevention_school = DataFetcher(
		name="DisasterPreventionSchool",
		url="https://data.taipei/api/dataset/6f8e0610-2c32-4148-b746-25fe17ce3fd0/resource/9fcab730-09a2-4b14-b157-282fd8bca1fe/download",
		method="DOWNLOAD",
	)
	disaster_prevention_school.get_data()

	# 急救責任醫院
	emergency_hospital = DataFetcher(
		name="EmergencyHospital",
		url="	https://data.taipei/api/dataset/b747394c-9e67-4b1d-8d1e-bc64f143d06a/resource/3a4930ba-474f-497b-8916-4e9d342f5035/download",
		method="DOWNLOAD",
	)
	emergency_hospital.get_data()