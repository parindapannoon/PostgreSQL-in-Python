import psycopg2
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
import numpy as np

# Database connection parameters
host = "localhost"
dbname = "xxx"
user = "xxx"
password = "xxx"
port = 5432

# Create a connection to the database
conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password, port=port)

# SQL query for layers
sql_fire = "SELECT * FROM aoi2014firepoints;"
sql_lulc = "SELECT * FROM lulc2017esribkk;"
sql_bor = "SELECT * FROM district;"
cursor = conn.cursor()
cursor.execute(sql_fire)
print(cursor.fetchall())
# Read data into a GeoDataFrame
gdf_fire = gpd.read_postgis(sql_fire, conn, geom_col='geom')
gdf_lulc = gpd.read_postgis(sql_lulc, conn, geom_col='geom')
gdf_bor = gpd.read_postgis(sql_bor, conn, geom_col='geom')

# Check if CRS is set for the GeoDataFrame, if not, set it to a default CRS (EPSG:4326)
if gdf_fire.crs is None:
    gdf_fire.set_crs(epsg=4326, inplace=True)
if gdf_lulc.crs is None:
    gdf_lulc.set_crs(epsg=4326, inplace=True)
if gdf_bor.crs is None:
    gdf_bor.set_crs(epsg=4326, inplace=True)

# Plot the GeoDataFrame with a basemap
fig, ax = plt.subplots(figsize=(14, 9))
gdf_fire.plot(ax=ax, marker='o', color='red', markersize=3)
gdf_bor.plot(ax=ax, alpha=0.7, color='none', edgecolor='purple')
gdf_lulc.plot(ax=ax, alpha=0.6, column='lulc', cmap='tab20b')

# Print the CRS and bounds
print("aoi2014firepoints CRS:", gdf_fire.crs.to_string())
print("aoi2014firepoints Bounds:", gdf_fire.total_bounds)

# Set the extent for contextily based on the combined bounds of both layers
xmin_lulc, ymin_lulc, xmax_lulc, ymax_lulc = gdf_lulc.total_bounds
xmin_fire, ymin_fire, xmax_fire, ymax_fire = gdf_fire.total_bounds
xmin_bor, ymin_bor, xmax_bor, ymax_bor = gdf_bor.total_bounds

xmin = min(xmin_lulc, xmin_fire, xmin_bor)
ymin = min(ymin_lulc, ymin_fire, ymin_bor)
xmax = max(xmax_lulc, xmax_fire, xmax_bor)
ymax = max(ymax_lulc, ymax_fire, ymax_bor)

# Calculate zoom level
lat_length = ymax - ymin
zoom_lat = int(np.ceil(np.log2(360 * 2.0 / lat_length)))

ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)

# Add a basemap
try:
    ctx.add_basemap(ax, crs=gdf_fire.crs.to_string(), source=ctx.providers.CartoDB.Positron, zoom=zoom_lat)
except Exception as e:
    print(f"Error adding basemap: {e}")
conn.close()

plt.title("Active fire spots and Districts of Bangkok")
plt.show()