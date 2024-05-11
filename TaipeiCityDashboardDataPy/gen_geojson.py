import pandas as pd
import json

def csv_to_geojson(csv_file):
    """
    Convert a CSV file with addr, lon, and lat columns into a GeoJSON format.

    Parameters:
    - csv_file (str): Path to the CSV file.

    Returns:
    - str: A string representation of the GeoJSON.
    """
    # 讀取 CSV 文件
    df = pd.read_csv(csv_file)
    
	# 將Lat, Lon取到小數點後4位
    df['Lat'] = df['Lat'].apply(lambda x: round(x, 4))
    df['Lon'] = df['Lon'].apply(lambda x: round(x, 4))

    # 構建 GeoJSON 結構
    geojson = {
        "type": "FeatureCollection",
        "crs": {
            "type": "name",
            "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}
        },
        "features": []
    }

    # 填充 features
    for _, row in df.iterrows():
        feature = {
            "type": "Feature",
            "properties": {"addr": row['Addr']},
            "geometry": {
                "type": "Point",
                "coordinates": [row['Lat'], row['Lon']]
            }
        }
        geojson['features'].append(feature)

    # 將 GeoJSON 對象儲存為檔案
    filename = csv_file.replace(".csv", ".geojson")
    with open(filename, "w") as f:
        json.dump(geojson, f)

# 示例使用
if __name__ == "__main__":
    # CSV 文件路徑
    csv_path = ["./FireSafety.csv", "./FireDifficultAreas.csv", "./EarthquakeManagedBuildings.csv"]  # 更改此路徑以指向您的 CSV 文件

    # 生成 GeoJSON
    for path in csv_path:
        csv_to_geojson(path)
