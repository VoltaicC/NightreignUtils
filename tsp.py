import json, math
import networkx as nx
import matplotlib.pyplot as plt
from PIL import Image

#Config
landmarks_file = "landmarks.json"
map_file = "images/maps/limgrave_map.jpeg"

with open(landmarks_file, "r") as f:
    coords = json.load(f)

# Jail + bird nodes
jails = ["Northwest of Lake", "Murkwater Terminus", "Stormhill", "Highroad", "East of Lake", "Mistwood", "Northeast Tunnel Entrance"]
bird_paths = [
    ("BirdStart1","BirdEnd1"),
    ("BirdStart2","BirdEnd2"),
    ("BirdStart3","BirdEnd3"),
    ("BirdStart4","BirdEnd4"),
    ("BirdStart5","BirdEnd5"),
    ("BirdStart6","BirdEnd6"),
]

nodes = jails + [n for pair in bird_paths for n in pair]

def distance(a, b):
    (x1, y1), (x2, y2) = coords[a], coords[b]
    return math.hypot(x2 - x1, y2 - y1)

# Graph
G = nx.Graph()
for a in nodes:
    for b in nodes:
        if a != b:
            G.add_edge(a, b, weight=distance(a, b))

# Bird shortcuts
for start, end in bird_paths:
    G.add_edge(start, end, weight=1)  # cheap one-shot edge

# Solve TSP
tsp_path = nx.approximation.traveling_salesman_problem(
    G.subgraph(nodes),
    nodes=jails,
    weight="weight",
    cycle=False,
    method=nx.approximation.greedy_tsp
)

print("Approx Route:", " -> ".join(tsp_path))

#Draw
img = Image.open(map_file)
plt.figure(figsize=(10,10))
plt.imshow(img)

# Draw bird paths
for start, end in bird_paths:
    sx, sy = coords[start]
    ex, ey = coords[end]
    plt.plot([sx, ex], [sy, ey], "cyan", linestyle="--", linewidth=1.5, alpha=0.6)
    plt.scatter([sx, ex], [sy, ey], c="cyan", s=50, marker="^")

# Draw route with arrows + numbers
px, py = [], []
for node in tsp_path:
    if node in coords:
        x, y = coords[node]
        px.append(x); py.append(y)

plt.plot(px, py, color="yellow", linewidth=3, alpha=0.9, zorder=3)

# Add arrows + step numbers
for i, node in enumerate(tsp_path):
    if node in coords:
        x, y = coords[node]
        plt.scatter(x, y, c="red" if node.startswith("Jail") else "orange", s=100, zorder=4)
        plt.text(x+15, y+15, str(i+1), color="black", fontsize=10, weight="bold",
                 bbox=dict(facecolor="white", edgecolor="none", alpha=0.6, pad=1))

# Add direction arrows
for i in range(len(px)-1):
    plt.arrow(px[i], py[i], px[i+1]-px[i], py[i+1]-py[i],
              head_width=40, head_length=40, fc="yellow", ec="yellow",
              alpha=0.7, length_includes_head=True)

plt.title("Shortest Jail Route with Bird Shortcuts", fontsize=16, color="white", pad=20)
plt.show()
