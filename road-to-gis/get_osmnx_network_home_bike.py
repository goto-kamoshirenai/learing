import osmnx as ox

# 東京駅を中心に半径2kmの徒歩ネットワークを取得
lat, lon = 35.549232, 139.7519519
G = ox.graph_from_point((lat, lon), dist=5000, network_type="bike")

# ローカルに保存して再利用可能に
ox.save_graphml(G, "home_bike_2km.graphml")
print("home_bike_2km.graphml を保存しました。")

