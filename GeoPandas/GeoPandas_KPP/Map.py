import os
import geopandas as gpd
import folium
from folium import LayerControl
import ipywidgets as widgets
from IPython.display import display, clear_output

# Define the directory path for shapefiles
folder_path = 'Dataset/world_10m_cultural/10m_cultural'

# List shapefiles in the directory
shapefiles = [file for file in os.listdir(folder_path) if file.endswith('.shp')]

# Base map options with attribution
base_maps = {
    'OpenStreetMap': ('OpenStreetMap', '© OpenStreetMap contributors'),
    'Stamen Terrain': (
    'Stamen Terrain', 'Map tiles by Stamen Design, CC BY 3.0 — Map data © OpenStreetMap contributors'),
    'Stamen Toner': ('Stamen Toner', 'Map tiles by Stamen Design, CC BY 3.0 — Map data © OpenStreetMap contributors'),
    'Stamen Watercolor': (
    'Stamen Watercolor', 'Map tiles by Stamen Design, CC BY 3.0 — Map data © OpenStreetMap contributors'),
    'CartoDB Positron': ('CartoDB Positron', '© OpenStreetMap contributors & CartoDB'),
    'CartoDB Dark Matter': ('CartoDB Dark Matter', '© OpenStreetMap contributors & CartoDB'),
}

# Dropdown for base map selection
base_map_dropdown = widgets.Dropdown(
    options=list(base_maps.keys()),
    description='Base Map:',
    disabled=False,
)

# Widgets to select and organize shapefiles
available_list = widgets.SelectMultiple(
    options=shapefiles,
    description='Available Shapefiles:',
    disabled=False,
    rows=10,
)

selected_list = widgets.SelectMultiple(
    options=[],
    description='Selected Shapefiles:',
    disabled=False,
    rows=10,
)

# Buttons for adding/removing shapefiles
add_button = widgets.Button(description="Add →")
remove_button = widgets.Button(description="← Remove")
up_button = widgets.Button(description="↑ Move Up")
down_button = widgets.Button(description="↓ Move Down")

# Button to plot the map
plot_button = widgets.Button(description="Plot Map")

# Output widget for the dynamic map
output = widgets.Output()


# Function to add shapefiles to the selected list
def add_shapefiles(b):
    current_selected = list(selected_list.options)
    new_selected = list(available_list.value)
    selected_list.options = current_selected + new_selected


# Function to remove shapefiles from the selected list
def remove_shapefiles(b):
    current_selected = list(selected_list.options)
    to_remove = list(selected_list.value)
    selected_list.options = [f for f in current_selected if f not in to_remove]


# Function to move shapefiles up in the selected list
def move_up(b):
    current_selected = list(selected_list.options)
    selected_items = list(selected_list.value)

    for item in selected_items:
        idx = current_selected.index(item)
        if idx > 0:
            current_selected[idx], current_selected[idx - 1] = current_selected[idx - 1], current_selected[idx]

    selected_list.options = current_selected


# Function to move shapefiles down in the selected list
def move_down(b):
    current_selected = list(selected_list.options)
    selected_items = list(selected_list.value)

    for item in reversed(selected_items):
        idx = current_selected.index(item)
        if idx < len(current_selected) - 1:
            current_selected[idx], current_selected[idx + 1] = current_selected[idx + 1], current_selected[idx]

    selected_list.options = current_selected


# Function to plot the selected shapefiles on the selected base map
def plot_dynamic_map(b):
    with output:
        clear_output(wait=True)

        # Get selected base map and shapefiles
        selected_base_map_key = base_map_dropdown.value
        selected_base_map, attribution = base_maps[selected_base_map_key]
        selected_shapefiles = selected_list.options

        # Initialize folium map with the selected base map and attribution
        m = folium.Map(location=[0, 0], zoom_start=2, tiles=selected_base_map, attr=attribution)

        # Iterate through selected shapefiles and add them to the folium map
        for selected_shapefile in selected_shapefiles:
            shapefile_path = os.path.join(folder_path, selected_shapefile)

            # Load the shapefile
            gdf = gpd.read_file(shapefile_path)

            # Check if the GeoDataFrame has a CRS
            if gdf.crs is None:
                # If no CRS, set it to EPSG:4326 (default for folium)
                gdf.set_crs("EPSG:4326", inplace=True)
            else:
                # If it has a CRS, transform it to EPSG:4326
                gdf = gdf.to_crs("EPSG:4326")

            # Convert the GeoDataFrame to GeoJSON and add it to the map
            folium.GeoJson(gdf).add_to(m)

        # Display the dynamic map with layer controls
        LayerControl().add_to(m)

        # Render the map
        display(m)


# Link buttons to their respective functions
add_button.on_click(add_shapefiles)
remove_button.on_click(remove_shapefiles)
up_button.on_click(move_up)
down_button.on_click(move_down)
plot_button.on_click(plot_dynamic_map)

# Layout for controls
controls = widgets.HBox([
    widgets.VBox([available_list, add_button, remove_button, up_button, down_button]),
    selected_list,
    base_map_dropdown
])

# Display the widgets and the output
display(controls)
display(plot_button)
display(output)
