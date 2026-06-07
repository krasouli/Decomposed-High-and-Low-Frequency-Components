import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
import fiona
import rasterio
from matplotlib.lines import Line2D
import os
import numpy as np
import pandas as pd
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

# Paths
shapefile_dir = 'ir_shp2'
elev_file = os.path.join(shapefile_dir, 'IRN_alt.tif')
land_cover_file = os.path.join(shapefile_dir, 'IRN_cov.tif')

# List all available layers
layers = fiona.listlayers(shapefile_dir)

# Identify possible water body layers by name (adjust as needed)
water_keywords = ['water', 'lake', 'sea', 'river', 'reservoir', 'wetland']
water_layers = [layer for layer in layers if any(wk in layer.lower() for wk in water_keywords)]

# Load the elevation raster data
with rasterio.open(elev_file) as src:
    elevation = src.read(1)
    elevation_extent = [src.bounds.left, src.bounds.right, src.bounds.bottom, src.bounds.top]

# Limit elevation values to the range [-100, 7000]
elevation = np.clip(elevation, 0, 4000)

# Load the land cover raster data
with rasterio.open(land_cover_file) as lc_src:
    land_cover = lc_src.read(1)
    land_cover_extent = [lc_src.bounds.left, lc_src.bounds.right, lc_src.bounds.bottom, lc_src.bounds.top]

# Inspect unique values to determine water class (uncomment to check)
# print(np.unique(land_cover))

# Set the land cover class value(s) for water bodies (update as needed)
water_classes = [20]  # <-- Replace with correct value(s) for water in your data

# Create a mask for water bodies
water_mask = np.isin(land_cover, water_classes)

# Weather station coordinates (latitude, longitude)
stations = {
    'Tehran': (35.715298, 51.404343),
    'Semnan': (35.183, 54.417),
    'Mashhad': (36.310699, 59.599457),
    'Arak': (34.08, 49.7),
    'Bandar Anzali': (37.463909, 49.479862),
    'Rasht': (37.280834, 49.583057)
}

# Create a GeoDataFrame for the stations
station_points = [Point(lon, lat) for lat, lon in stations.values()]
stations_gdf = gpd.GeoDataFrame({'City': list(stations.keys())}, geometry=station_points, crs='EPSG:4326')

# Create plot
fig, ax = plt.subplots(figsize=(12, 12))

# Plot elevation raster
img = ax.imshow(elevation, extent=elevation_extent, cmap='terrain', alpha=0.5, zorder=0, vmin=0, vmax=4000)

# Overlay water bodies from land cover raster
ax.imshow(np.where(water_mask, 1, np.nan), extent=land_cover_extent, cmap='Blues', alpha=0.5, zorder=1)

# Plot each province layer (all layers except water)
for layer in layers:
    if layer not in water_layers:
        gdf = gpd.read_file(shapefile_dir, layer=layer)
        gdf.plot(ax=ax, edgecolor='black', facecolor='none', linewidth=1, zorder=2)

# Plot water body layers with blue fill (vector layers, if any)
for water_layer in water_layers:
    water_gdf = gpd.read_file(shapefile_dir, layer=water_layer)
    water_gdf.plot(ax=ax, color='lightblue', edgecolor='blue', alpha=0.7, linewidth=0.5, zorder=3)

# Plot weather stations
stations_gdf.plot(ax=ax, color='red', markersize=80, zorder=4)
# Custom label offsets for Rasht and Bandar Anzali to avoid overlap
label_offsets = {
    'Tehran': (0.2, 0),
    'Semnan': (0.2, 0),
    'Mashhad': (0.2, 0),
    'Arak': (0.2, 0),
    'Bandar Anzali': (0.5, -0.3),  # Move label right and down
    'Rasht': (-1.0, 0.3),          # Move label left and up
}

for city, point in zip(stations_gdf['City'], stations_gdf.geometry):
    dx, dy = label_offsets.get(city, (0.2, 0))
    ax.text(point.x + dx, point.y + dy, city, fontsize=12, weight='bold', zorder=5)

#for x, y, label in zip(stations_gdf.geometry.x, stations_gdf.geometry.y, stations_gdf['City']):
#    ax.text(x + 0.2, y, label, fontsize=12, weight='bold', zorder=5)

# Add color bar for elevation
cbar = fig.colorbar(img, ax=ax, fraction=0.036, pad=0.04)
cbar.set_label('Elevation (m.a.s.l)')

# Add legend for water bodies and weather stations
legend_elements = [
    Line2D([0], [0], marker='o', color='w', label='Water Bodies',
           markerfacecolor='lightblue', markeredgecolor='blue', markersize=15),
    Line2D([0], [0], marker='o', color='w', label='Weather Stations',
           markerfacecolor='red', markeredgecolor='k', markersize=15)
]
ax.legend(handles=legend_elements, loc='upper right')

#ax.set_title('Iran Provinces, International Water Bodies, Topography, and 6 Weather Stations')
ax.set_xlabel('Longitude  (°E)', fontsize=15)
ax.set_ylabel('Latitude  (°N)', fontsize=15)
ax.set_xlim(43, 65)
ax.set_ylim(23, 40)



# Monthly data for six stations
months = list(range(1, 13))
stations_data = {
    'Semnan': {
        'p': [15.643125, 19.9734375, 21.4078125, 18.6265625, 13.076875, 4.1421875, 2.99, 2.178125, 2.5190625, 5.6178125, 11.045, 15.37],
        't': [4.048286344, 6.690155313, 12.0321525, 18.39801563, 24.23386875, 29.83625, 32.2822625, 30.91109063, 26.6225, 19.54708438, 11.31687719, 5.659374688]
    },
    'Mashhad': {
        'p': [24.523125, 35.7625, 52.1946875, 37.46375, 31.18625, 5.685625, 1.600625, 0.7975, 2.57375, 7.4846875, 16.8128125, 20.70875],
        't': [2.745463469, 4.734109813, 9.452315625, 15.4979125, 21.19264063, 26.51030625, 28.50333125, 26.69263125, 22.01885625, 15.3517125, 8.8946875, 4.562903438]
    },
    'Tehran': {
        'p': [31.92294118, 33.12882353, 41.01088235, 33.75, 13.42764706, 2.035588235, 2.415294118, 1.560882353, 0.913636364, 12.94294118, 28.75852941, 33.76294118],
        't': [5.119848676, 7.162588324, 11.87926176, 17.77234, 23.19294412, 28.64757647, 31.13955147, 30.32505294, 26.3475, 19.85551912, 12.10167618, 7.003506897]
    },
    'Arak': {
        'p': [35.01294118, 36.72911765, 55.77529412, 51.93323529, 24.77588235, 3.208823529, 1.284117647, 1.580909091, 1.616470588, 16.68117647, 38.21735294, 39.535],
        't': [0, 2.716592697, 8.040339485, 13.49646147, 18.57727956, 24.37129412, 27.74355588, 26.71072727, 22.13466765, 15.70284382, 8.083535412, 3.190979897]
    },
    'Rasht': {
        'p': [125.3250606, 124.0678788, 104.9738788, 66.86975758, 40.85127273, 36.43472727, 50.933, 65.7970303, 151.6025758, 193.5752424, 195.9522121, 140.2088182],
        't': [7.128228739, 7.154969398, 9.843190616, 14.11966667, 19.57927468, 23.87631313, 25.74513196, 25.76094917, 22.41705612, 17.97095503, 12.654, 9.086653959]
    },
    'Bandar Anzali': {
        'p': [167.4223881, 122.8059701, 110.8298507, 58.49701493, 43.4119403, 52.69701493, 49.07910448, 115.2283582, 268.3238806, 334.3940299, 308.0227273, 210.7939394],
        't': [7.3, 7.1, 8.9, 13.5, 18.8, 23.4, 26, 25.8, 22.6, 18.3, 13.6, 9.7]
    }
}

# Add inset climograph subplot
axins = inset_axes(
    ax,
    width="40%", height="40%",
    bbox_to_anchor=(0.05, 0.05, 1.0, 1.35),  # Shift right (x0) and up (y0)
    bbox_transform=ax.transAxes,
    loc='lower left',
    borderpad=2
    )

import numpy as np

colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown']

for i, (station, data) in enumerate(stations_data.items()):
    c = colors[i % len(colors)]

    # Monthly temperature-precipitation line
    axins.plot(
        data['t'],
        data['p'],
        marker='s',
        label=station,
        color=c
    )

    # Annual values: mean temperature and total precipitation
    t_ann = np.mean(data['t'])
    p_ann = np.sum(data['p'])

    # Add annual point in the same color
    axins.scatter(
        t_ann,
        p_ann,
        color=c,
        s=90,
        edgecolor='black',
        zorder=5
    )

# Axes and styling
axins.set_xlabel('Air Temperature (°C)', fontsize=10)
axins.set_ylabel('Precipitation (mm)', fontsize=10)
axins.set_title('Monthly Climograph', fontsize=11)
axins.grid(True, linestyle='--', alpha=0.5)

# Plot limits
axins.set_xlim(-2, 34)
axins.set_ylim(0, 1855)

# Example De Martonne classification lines
T_line = np.linspace(-2, 34, 300)

I_arid = 10
P_arid = I_arid * (T_line + 10)
axins.plot(T_line, P_arid, color='black', linestyle='-', linewidth=1.8,
        label='De Martonne = 10: Arid')

I_humid = 28
P_humid = I_humid * (T_line + 10)
axins.plot(T_line, P_humid, color='black', linestyle=':', linewidth=1.8,
        label='De Martonne = 28: Humid')

axins.legend(fontsize=8, loc='upper left', frameon=True)
fig.text(0.94, 0.92, '(a)', ha='left', va='top', fontsize=16, fontweight='bold')

plt.draw()
plt.tight_layout()


#colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown']
#for i, (station, data) in enumerate(stations_data.items()):
#    # Plot temperature (x) vs precipitation (y) for each station
#    axins.plot(data['t'], data['p'], marker='o', label=station, color=colors[i])
#
#axins.set_xlabel('Air Temperature (°C)', fontsize=10)
#axins.set_ylabel('Precipitation (mm)', fontsize=10)
#axins.set_title('Monthly Climograph', fontsize=11)
#axins.grid(True, linestyle='--', alpha=0.5)
#axins.axhline(y=135, color='black', linestyle='--', linewidth=2,label='Aridity Threshold')
#axins.legend(fontsize=8, loc='upper left', frameon=True)
#fig.text(0.94, 0.92, '(a)', ha='left', va='top', fontsize=16, fontweight='bold')
#
#plt.draw()
#
#plt.tight_layout()

# Save the figure as a TIFF file
plt.savefig('iran_map_with_elevation_and_water_bodies2.tiff', dpi=300, format='tiff')

plt.show()
