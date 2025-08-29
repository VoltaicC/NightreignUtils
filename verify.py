import matplotlib.pyplot as plt
import cv2
import json

# Config
map_img_path = "limgrave_map.jpeg"      
landmarks_file = "landmarks.json"       

# Load map image
img = cv2.cvtColor(cv2.imread(map_img_path), cv2.COLOR_BGR2RGB)

# Load landmarks with coordinates
with open(landmarks_file, "r") as f:
    coords = json.load(f)

fig, ax = plt.subplots(figsize=(12, 12))
ax.imshow(img)
ax.set_title("Landmark Verification", fontsize=16)

# Plot each point
for name, (x, y) in coords.items():
    ax.plot(x, y, "ro", markersize=4)  # red dot
    ax.text(x+10, y+10, name, fontsize=6, color="yellow", 
            bbox=dict(facecolor="black", alpha=0.4, edgecolor="none", pad=1))

plt.show()
