import pandas as pd
import json

def determine_color(difficulty_level):
    color_map = {
        1: "#248188",
        2: "#F65658"
    }
    return color_map.get(difficulty_level, "#000000")  # Default color if no match

def csv_to_geojson(csv_file):
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
            "properties": {
                "addr": row['Addr'],
                "difficulty_level": row['DifficultyLevel'],
                "color": determine_color(row['DifficultyLevel'])  # Assign color based on difficulty level
            },
            "geometry": {
                "type": "Point",
                "coordinates": [row['Lat'], row['Lon']]
            }
        }
        geojson['features'].append(feature)

    # 將 GeoJSON 對象儲存為檔案
    filename = csv_file.replace(".csv", ".geojson")
    with open(filename, "w") as f:
        json.dump(geojson, f, ensure_ascii=False, indent=4)

# 示例使用
if __name__ == "__main__":
    csv_path = "./FireDifficultAreas.csv"
    csv_to_geojson(csv_path)
