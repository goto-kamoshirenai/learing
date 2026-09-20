import osmnx as ox

# 東京駅を中心に半径2kmの徒歩ネットワークを取得
lat, lon = 35.681236, 139.767125
G = ox.graph_from_point((lat, lon), dist=2000, network_type="walk")

# ローカルに保存して再利用可能に
ox.save_graphml(G, "tokyo_walk_2km.graphml")
print("tokyo_walk_2km.graphml を保存しました。")

