import matplotlib.pyplot as plt
import cv2
import json

#Congif
map_img_path = "limgrave_map.jpeg" 
locations_file = "nightreign_landmarks.txt"
output_file = "landmarks.json"

# Load map
img = cv2.cvtColor(cv2.imread(map_img_path), cv2.COLOR_BGR2RGB)

# Load location names
with open(locations_file, "r") as f:
    locations = [line.strip() for line in f if line.strip()]

coords = {}

# Setup plotting
fig, ax = plt.subplots()
ax.imshow(img)
ax.set_title("Click on: " + locations[0])
index = [0]  # Mutable index

def onclick(event):
    if event.xdata is not None and event.ydata is not None:
        loc = locations[index[0]]
        coords[loc] = (round(event.xdata, 2), round(event.ydata, 2))
        print(f"{loc}: {coords[loc]}")
        index[0] += 1

        if index[0] < len(locations):
            ax.set_title("Click on: " + locations[index[0]])
            fig.canvas.draw()
        else:
            print("✅ All locations mapped! Saving to JSON...")
            with open(output_file, "w") as f:
                json.dump(coords, f, indent=2)
            plt.close(fig)

# Connect the click event
fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()
