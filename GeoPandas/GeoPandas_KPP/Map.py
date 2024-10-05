import os
import geopandas as gpd
import matplotlib.pyplot as plt
import random
import ipywidgets as widgets
from IPython.display import display

# Define the directory path
folder_path = 'Dataset/world_10m_cultural/10m_cultural'

# List the shapefiles in the directory
shapefiles = [file for file in os.listdir(folder_path) if file.endswith('.shp')]

# Create a dropdown widget to select a shapefile
dropdown = widgets.Dropdown(
    options=shapefiles,
    description='Shapefile:',
    disabled=False,
)

# Create a button to plot the selected shapefile
plot_button = widgets.Button(description="Plot Map")


# Function to plot the selected shapefile
def plot_map(b):
    selected_shapefile = dropdown.value
    shapefile_path = os.path.join(folder_path, selected_shapefile)

    # Load the selected shapefile
    world = gpd.read_file(shapefile_path)

    # Create a new column with random data for coloring purposes
    world["color"] = [random.randint(0, 255) for _ in range(len(world))]

    # Plotting the map
    fig, ax = plt.subplots(figsize=(15, 10))
    world.plot(column="color", cmap="rainbow", linewidth=0.5, ax=ax, edgecolor="blue")
    ax.set_title(f"Choropleth Map of {selected_shapefile}")
    ax.axis("on")
    plt.xlabel(f"Map using {selected_shapefile}")
    plt.grid(color="green", linewidth=0.5)
    plt.show()


# Link the button to the plotting function
plot_button.on_click(plot_map)

# Display the dropdown and button in Jupyter Notebook
display(dropdown)
display(plot_button)
