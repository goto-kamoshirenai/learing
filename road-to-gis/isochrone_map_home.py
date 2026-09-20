import osmnx as ox
import geopandas as gpd
import networkx as nx
from shapely.geometry import Point
import folium

# --- 1) グラフ読み込み & 投影 ---
G = ox.load_graphml("home_walk_2km.graphml")
G_proj = ox.project_graph(G)  # メートル系

# 起点（自宅, WGS84）
lat, lon = 35.549232, 139.7519519
pt_wgs84 = gpd.GeoSeries([Point(lon, lat)], crs=G.graph.get("crs", "EPSG:4326"))
pt_proj  = pt_wgs84.to_crs(G_proj.graph["crs"])
x, y = pt_proj.iloc[0].x, pt_proj.iloc[0].y
origin = ox.distance.nearest_nodes(G_proj, X=x, Y=y)

# --- 2) Dijkstra（距離: m） ---
speed_m_per_min = 80
thresh_5m  = 5  * speed_m_per_min  # 400
thresh_10m = 10 * speed_m_per_min  # 800
thresh_15m = 15 * speed_m_per_min  # 1200
lengths = nx.single_source_dijkstra_path_length(
    G_proj, source=origin, cutoff=thresh_15m, weight="length"
)

# 到達ノード集合
S5  = {n for n, d in lengths.items() if d <= thresh_5m}
S10 = {n for n, d in lengths.items() if d <= thresh_10m}
S15 = {n for n, d in lengths.items() if d <= thresh_15m}

# --- 3) エッジ由来でポリゴン化 ---
# 投影座標のGDF（m）
edges_gdf_proj = ox.graph_to_gdfs(G_proj, nodes=False, edges=True)

def iso_polygon_from_edges(reachable_nodes: set, buffer_m=10, simplify_m=3):
    """到達ノードに両端が含まれる道路エッジを抽出→buffer→union_all→Polygon（WGS84）"""
    if not reachable_nodes:
        return None

    # (u,v,key) MultiIndex の u,v が到達集合に含まれるエッジのみ採用
    def both_endpoints_reached(idx):
        try:
            u, v = idx[0], idx[1]
        except Exception:
            return False
        return (u in reachable_nodes) and (v in reachable_nodes)

    sub = edges_gdf_proj.loc[edges_gdf_proj.index.map(both_endpoints_reached)]
    if sub.empty:
        return None

    # 道路形状を太くし結合
    merged = sub.buffer(buffer_m).union_all().buffer(0).simplify(simplify_m)

    # WGS84へ変換して shapely geometry を返す
    return gpd.GeoDataFrame(geometry=[merged], crs=edges_gdf_proj.crs).to_crs(4326).iloc[0].geometry

# 細め設定
poly_5m  = iso_polygon_from_edges(S5,  buffer_m=8,  simplify_m=3)
poly_10m = iso_polygon_from_edges(S10, buffer_m=10, simplify_m=3)
poly_15m = iso_polygon_from_edges(S15, buffer_m=12, simplify_m=4)

# --- 4) Folium 可視化 ---
m = folium.Map(location=[lat, lon], zoom_start=15, tiles="cartodbpositron")

def add_poly(geom, name, color, fill_opacity=0.28):
    if geom is None:
        return
    folium.GeoJson(
        data=gpd.GeoSeries([geom], crs="EPSG:4326").to_json(),
        name=name,
        style_function=lambda x, col=color: {
            "color": col, "weight": 2, "fillOpacity": fill_opacity, "fillColor": col
        },
        tooltip=name,
    ).add_to(m)

# レイヤ順：15 → 10 → 5（下から順に）
add_poly(poly_15m, "徒歩15分圏（~1200m）", "#377eb8")
add_poly(poly_10m, "徒歩10分圏（~800m）",  "#4daf4a")
add_poly(poly_5m,  "徒歩5分圏（~400m）",   "#e41a1c")

# 起点マーカー
folium.Marker([lat, lon], icon=folium.Icon(color="red"), tooltip="起点（自宅）").add_to(m)
folium.LayerControl().add_to(m)

m.save("isochrone_map_home.html")
print("isochrone_map_home.html を出力しました。")
