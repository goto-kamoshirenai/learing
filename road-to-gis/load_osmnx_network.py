import osmnx as ox

# 保存済みGraphMLファイルを読み込み（オフライン実行可能）
G = ox.load_graphml("tokyo_walk_2km.graphml")

print(f"グラフを読み込みました。ノード数: {len(G)}")
