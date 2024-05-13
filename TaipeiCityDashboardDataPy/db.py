import sqlalchemy
import pandas as pd
import orjson as json
import requests

def addr2WGS84(addr: str) -> tuple:
	"""
		地址轉換經緯度
	"""
	url = f"https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/findAddressCandidates?singleLine={addr}&f=json"
	data = requests.get(url).json()
	if data["candidates"]:
		return data["candidates"][0]["location"]["x"], data["candidates"][0]["location"]["y"]
	else:
		return None

class Database:
	def __init__(self, dbname: str, user: str, password: str, host: str, port: str):
		self.dbname = dbname
		self.user = user
		self.password = password
		self.host = host
		self.port = port
		self.connection = None

	def connect(self):
		try:
			conn_str = f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}"
			self.connection = sqlalchemy.create_engine(conn_str)
		except Exception as e:
			print(e)

	def disconnect(self):
		try:
			self.cursor.close()
			self.connection.close()
			print("Connection closed successfully")
		except Exception as e:
			print(e)

	def execute(self, query: str):
		try:
			self.cursor.execute(query)
			self.connection.commit()
			print("Query executed successfully")
		except Exception as e:
			print(e)

	def fetch(self, query: str):
		try:
			self.cursor.execute(query)
			data = self.cursor.fetchall()
			print("Data fetched successfully")
			return data
		except Exception as e:
			print(e)

	def fetch_df(self, query: str):
		try:
			df = pd.read_sql_query(query, self.connection)
			print("Data fetched successfully")
			return df
		except Exception as e:
			print(e)

if __name__ == "__main__":

	dashboard = Database(dbname="dashboard", user="postgres", password="11111111", host="localhost", port="5433")
	manager = Database(dbname="dashboardmanager", user="postgres", password="11111111", host="localhost", port="5432")

	dashboard.connect()
	manager.connect()
	
	# read ods
	df = pd.read_excel("./113年臺北市可供避難收容處所一覽表-1130305更新上傳.ods", engine="odf")
	#df Addr = 縣市,鄉鎮,村里,門牌 連起來
	df["Addr"] = df["縣市"] + df["鄉鎮"] + df["村里"] + df["門牌"]
	df['Lat'] = None
	df['Lon'] = None
	for i in df.index:
		lat, lon = addr2WGS84(df.loc[i, "Addr"])
		df.loc[i, "Lat"] = lat
		df.loc[i, "Lon"] = lon
	df.to_csv("evacuation_shelter.csv", index=False)

	# df.to_sql("evacuation_shelter", dashboard.connection, if_exists="replace", index=False)

	# df = pd.read_csv("./臺北市急救責任醫院名冊.csv", encoding="big5")
	# df.drop(columns=["行政區"], inplace=True)
	# df.rename(columns={"醫院名稱": "Name", "地址": "Addr", "電話": "Tel"}, inplace=True)
	# df["lat"] = None
	# df["lon"] = None
	# for i in df.index:
	# 	lat, lon = addr2WGS84(df.loc[i, "Addr"])
	# 	df.loc[i, "lat"] = lat
	# 	df.loc[i, "lon"] = lon
	# print(df)
	# df.to_sql("hospital", dashboard.connection, if_exists="replace", index=False)