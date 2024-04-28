import psycopg2
import pandas as pd
import orjson as json
from FetchData import get_final_data
class Database:
	def __init__(self, dbname: str, user: str, password: str, host: str, port: str):
		self.dbname = dbname
		self.user = user
		self.password = password
		self.host = host
		self.port = port

	def connect(self):
		try:
			self.connection = psycopg2.connect(
				dbname=self.dbname,
				user=self.user,
				password=self.password,
				host=self.host,
				port=self.port
			)
			self.cursor = self.connection.cursor()
			print(f"Connection established successfully with {self.dbname} database")
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
	
	data = get_final_data()

	# 把 data insert進去PostgreSQL public.city_parking_info
	for i in range(len(data)):
		# 使用 .loc 或 .iloc 獲取對應的值
		address = data.loc[i, 'address']
		carTotalNum = data.loc[i, 'carTotalNum']
		carRemainderNum = data.loc[i, 'carRemainderNum']
		motorTotalNum = data.loc[i, 'motorTotalNum']
		motorRemainderNum = data.loc[i, 'motorRemainderNum']
		payex = data.loc[i, 'payex']
		parkName = data.loc[i, 'parkName']
		parkId = data.loc[i, 'parkId']
		entrance_json = data.loc[i, 'entrance']
		
		# 處理entrance為None的情況
		if entrance_json is None:
			lat = data.loc[i, 'lat']
			lon = data.loc[i, 'lon']
		else:
			entrance_list = json.loads(entrance_json)
			entrance_address = entrance_list[0].get('Add')
			lat = entrance_list[0].get('Lat')
			lon = entrance_list[0].get('Lon')
		servicetime = data.loc[i, 'servicetime']
		tel = data.loc[i, 'tel']
		pregnancy_First = data.loc[i, 'pregnancy_First']
		remark = data.loc[i, 'remark']
		_type = data.loc[i, 'Type']

		query = f"""
		INSERT INTO public.city_parking_info ("address", "carTotalNum", "carRemainderNum", "motorTotalNum", "motorRemainderNum", "payex", "parkName", "parkId", "entrance_address", "lat", "lon", "servicetime", "tel", "pregnancy_First", "remark", "type")
		VALUES ('{address}', {carTotalNum}, {carRemainderNum}, {motorTotalNum}, {motorRemainderNum}, '{payex}', '{parkName}', '{parkId}', '{entrance_address}', {lat}, {lon}, '{servicetime}', '{tel}', {pregnancy_First}, '{remark}', '{_type}');
		"""

		dashboard.execute(query)
