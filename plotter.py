import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets import Button
import cv2
import json

# Config
map_img_path = "limgrave_map.jpeg" 
locations_file = "nightreign_landmarks.txt"
output_file = "landmarks.json"

# Load map
img = cv2.cvtColor(cv2.imread(map_img_path), cv2.COLOR_BGR2RGB)

# Load location names
with open(locations_file, "r") as f:
    locations = [line.strip() for line in f if line.strip()]

coords = {}
skipped_locations = set()
current_index = 0

# Setup plotting with more space for buttons
fig, ax = plt.subplots(figsize=(12, 8))
plt.subplots_adjust(bottom=0.15)  # Make room for buttons

ax.imshow(img)
ax.set_title(f"Location {current_index + 1}/{len(locations)}: {locations[current_index]}")

# Create button axes
ax_back = plt.axes([0.1, 0.05, 0.1, 0.04])
ax_skip = plt.axes([0.25, 0.05, 0.1, 0.04])
ax_save = plt.axes([0.4, 0.05, 0.1, 0.04])
ax_reset = plt.axes([0.55, 0.05, 0.1, 0.04])
ax_status = plt.axes([0.7, 0.05, 0.25, 0.04])

# Create buttons
back_button = Button(ax_back, 'Back')
skip_button = Button(ax_skip, 'Skip')
save_button = Button(ax_save, 'Save')
reset_button = Button(ax_reset, 'Reset Point')
status_button = Button(ax_status, 'Show Status')

# Store plotted points for visualization
plotted_points = {}

def update_title():
    """Update the title with current progress"""
    status = "PLOTTED" if locations[current_index] in coords else "SKIPPED" if locations[current_index] in skipped_locations else "PENDING"
    ax.set_title(f"Location {current_index + 1}/{len(locations)}: {locations[current_index]} [{status}]")
    fig.canvas.draw()

def clear_plotted_points():
    """Remove all plotted point markers from the display"""
    for point in plotted_points.values():
        point.remove()
    plotted_points.clear()

def show_plotted_points():
    """Display all currently plotted points"""
    clear_plotted_points()
    for loc, (x, y) in coords.items():
        # Add a red circle marker
        circle = patches.Circle((x, y), radius=5, color='red', alpha=0.7)
        ax.add_patch(circle)
        plotted_points[loc] = circle
    fig.canvas.draw()

def onclick(event):
    """Handle map clicks to place location markers"""
    global current_index
    # Only handle clicks on the main map axes, not on buttons
    if event.inaxes == ax and event.xdata is not None and event.ydata is not None:
        if current_index < len(locations):
            loc = locations[current_index]
            
            # Remove from skipped if it was previously skipped
            skipped_locations.discard(loc)
            
            # Store coordinates
            coords[loc] = (round(event.xdata, 2), round(event.ydata, 2))
            print(f"✓ {loc}: {coords[loc]}")
            print(f"Total plotted so far: {len(coords)}")
            
            # Move to next location
            advance_to_next()
            show_plotted_points()
            update_title()

def advance_to_next():
    """Move to the next unfinished location"""
    global current_index
    if current_index < len(locations) - 1:
        current_index += 1
    # Find next location that needs attention
    while (current_index < len(locations) - 1 and 
           locations[current_index] in coords):
        current_index += 1

def go_back(event):
    """Go back to previous location"""
    global current_index
    if current_index > 0:
        current_index -= 1
        update_title()
        print(f"← Back to: {locations[current_index]}")
        print(f"Current coords dict has {len(coords)} locations")

def skip_location(event):
    """Skip current location"""
    global current_index
    if current_index < len(locations):
        loc = locations[current_index]
        
        # Remove from coords if it was previously plotted
        coords.pop(loc, None)
        
        # Add to skipped set
        skipped_locations.add(loc)
        print(f"⏭ Skipped: {loc}")
        print(f"Current coords dict has {len(coords)} locations")
        
        # Move to next location
        advance_to_next()
        show_plotted_points()
        update_title()

def save_coords(event):
    """Save current coordinates to JSON file"""
    print(f"🔍 Debug - coords dictionary contains: {len(coords)} items")
    for loc, coord in coords.items():
        print(f"  {loc}: {coord}")
    
    if coords:
        with open(output_file, "w") as f:
            json.dump(coords, f, indent=2)
        print(f"💾 Saved {len(coords)} locations to {output_file}")
        print(f"📊 Status: {len(coords)} plotted, {len(skipped_locations)} skipped, {len(locations) - len(coords) - len(skipped_locations)} pending")
        
        # Verify what was actually written to file
        try:
            with open(output_file, "r") as f:
                saved_data = json.load(f)
            print(f"✅ Verified: File contains {len(saved_data)} locations")
        except Exception as e:
            print(f"❌ Error verifying save: {e}")
    else:
        print("❌ No coordinates to save")

def reset_current_point(event):
    """Reset/remove the current location's coordinates"""
    global current_index
    loc = locations[current_index]
    
    # Remove from both coords and skipped
    coords.pop(loc, None)
    skipped_locations.discard(loc)
    
    print(f"🔄 Reset: {loc}")
    show_plotted_points()
    update_title()

def show_status(event):
    """Show detailed status of all locations"""
    print("\n" + "="*50)
    print("MAPPING STATUS:")
    print("="*50)
    
    plotted = []
    skipped = []
    pending = []
    
    for i, loc in enumerate(locations):
        if loc in coords:
            plotted.append(f"{i+1:2d}. {loc}")
        elif loc in skipped_locations:
            skipped.append(f"{i+1:2d}. {loc}")
        else:
            pending.append(f"{i+1:2d}. {loc}")
    
    print(f"✅ PLOTTED ({len(plotted)}):")
    for item in plotted:
        print(f"  {item}")
    
    print(f"\n⏭  SKIPPED ({len(skipped)}):")
    for item in skipped:
        print(f"  {item}")
    
    print(f"\n⏳ PENDING ({len(pending)}):")
    for item in pending:
        print(f"  {item}")
    
    print("="*50)

# Connect event handlers
fig.canvas.mpl_connect('button_press_event', onclick)
back_button.on_clicked(go_back)
skip_button.on_clicked(skip_location)
save_button.on_clicked(save_coords)
reset_button.on_clicked(reset_current_point)
status_button.on_clicked(show_status)

# Keyboard shortcuts
def on_key_press(event):
    global current_index
    if event.key == 'left' or event.key == 'b':  # Back
        go_back(event)
    elif event.key == 'right' or event.key == 's':  # Skip
        skip_location(event)
    elif event.key == 'r':  # Reset current point
        reset_current_point(event)
    elif event.key == 'ctrl+s':  # Save
        save_coords(event)
    elif event.key == 'up':  # Go to previous location
        if current_index > 0:
            current_index -= 1
            update_title()
    elif event.key == 'down':  # Go to next location
        if current_index < len(locations) - 1:
            current_index += 1
            update_title()

fig.canvas.mpl_connect('key_press_event', on_key_press)

print("🗺️  Interactive Map Plotter")
print("=" * 40)
print("CONTROLS:")
print("• Click on map: Plot current location")
print("• Back button: Go to previous location")
print("• Skip button: Skip current location")
print("• Reset Point: Clear current location")
print("• Save button: Save coordinates to JSON")
print("• Show Status: Display progress summary")
print("\nKEYBORD SHORTCUTS:")
print("• ← or B: Back")
print("• → or S: Skip")
print("• ↑/↓: Navigate locations")
print("• R: Reset current point")
print("• Ctrl+S: Save")
print("=" * 40)

update_title()
plt.show()