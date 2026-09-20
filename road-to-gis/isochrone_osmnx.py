import osmnx as ox
import networkx as nx
import geopandas as gpd
from shapely.geometry import Point

# 1. GraphMLを読み込み
print("[1/5] GraphMLを読み込んでいます...")
G = ox.load_graphml("tokyo_walk_2km.graphml")
print("      完了")

print("[2/5] 座標系を変換しています...")
G_proj = ox.project_graph(G)  # メートル単位に変換

# 2. 東京駅の座標（WGS84）
lat, lon = 35.681236, 139.767125

# WGS84のポイントを作成
pt_wgs84 = gpd.GeoSeries([Point(lon, lat)], crs=G.graph["crs"])  # EPSG:4326想定
# 投影座標系へ変換
pt_proj = pt_wgs84.to_crs(G_proj.graph["crs"])
x, y = pt_proj.iloc[0].x, pt_proj.iloc[0].y
print("      完了")

# 3. 最近傍ノードを取得（scipy使用）
print("[3/5] 最近傍ノードを探索しています...")
origin = ox.distance.nearest_nodes(G_proj, X=x, Y=y)
print(f"起点ノード: {origin}")

# 4. Dijkstra法による最短距離計算
print("[4/5] Dijkstra法で到達可能範囲を計算しています...")
speed_m_per_min = 80
max_minutes = 15
max_dist_m = speed_m_per_min * max_minutes

lengths = nx.single_source_dijkstra_path_length(
    G_proj, source=origin, cutoff=max_dist_m, weight="length"
)

print(f"      完了: {len(lengths)}ノード")

# 5. 到達圏の距離ごとにノードを抽出
print("[5/5] 時間別にノードを分類しています...")
thresh_5m  = 5 * 80
thresh_10m = 10 * 80
thresh_15m = 15 * 80

nodes_5m  = [n for n, d in lengths.items() if d <= thresh_5m]
nodes_10m = [n for n, d in lengths.items() if d <= thresh_10m]
nodes_15m = [n for n, d in lengths.items() if d <= thresh_15m]
print("      完了")
print(f"5分={len(nodes_5m)} 10分={len(nodes_10m)} 15分={len(nodes_15m)}")


# ---- 結果 ----
# python isochrone_osmnx.py                                                     
# 起点ノード: 12802523328
# 計算ノード数: 3932
# 5分=778 10分=2009 15分=3932
