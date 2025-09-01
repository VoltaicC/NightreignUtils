import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import cv2
import json

#Config
map_img_path = "images/maps/limgrave_map.jpeg"
icon_path = "images/icons/evergaol.png"
landmarks_file = "landmarks.json"
mapping_file = "evergaol_mapping.json"

target_evergaols = {
    "Northwest of Lake",
    "Murkwater Terminus",
    "Stormhill",
    "Highroad",
    "East of Lake",
    "Mistwood",
    "Northeast Tunnel Entrance"
}

#Load assets
img = cv2.cvtColor(cv2.imread(map_img_path), cv2.COLOR_BGR2RGB)

#Load and resize icon for OffsetImage (scale factor controls size)
icon_rgba = cv2.imread(icon_path, cv2.IMREAD_UNCHANGED)
icon_rgba = cv2.cvtColor(icon_rgba, cv2.COLOR_BGRA2RGBA)

with open(landmarks_file, "r") as f:
    coords = json.load(f)

with open(mapping_file, "r") as f:
    mapping = json.load(f)

#Global state just starting with gladius default on map 0
current_map_id = 0
nightlord = "Gladius"
shifting_earth = "default"

fig, ax = plt.subplots(figsize=(12, 12))
plt.subplots_adjust(bottom=0.2)

def draw_map():
    ax.clear()
    ax.imshow(img)
    ax.set_title(f"Evergaols for Map ID {current_map_id}", fontsize=16)

    key = f"{current_map_id}.0-{nightlord}-Default"
    gaols_for_map = mapping.get(key, {})

    for name, (x, y) in coords.items():
        if name not in target_evergaols:
            continue

        # Create a small icon marker
        imagebox = OffsetImage(icon_rgba, zoom=0.2)  # adjust zoom as needed
        ab = AnnotationBbox(imagebox, (x, y), frameon=False)
        ax.add_artist(ab)

        # Label
        label = gaols_for_map.get(name, "Unknown")
        ax.text(x+20, y, f"{name}\n{label}",
                fontsize=7, color="yellow",
                bbox=dict(facecolor="black", alpha=0.5, edgecolor="none", pad=1))

    fig.canvas.draw_idle()

def next_map(event):
    global current_map_id
    current_map_id += 1
    draw_map()

axnext = plt.axes([0.4, 0.05, 0.2, 0.075])
bnext = Button(axnext, "Next Map")
bnext.on_clicked(next_map)

draw_map()
plt.show()
