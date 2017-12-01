import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point
import numpy as np

import pandas as pd

tract_df = gpd.read_file("geo_export_add04ab2-b26d-4df6-97be-d04944b3a133.shp")

station_df = pd.read_csv("station_loc_id.csv")
geometry = [Point(xy) for xy in zip(station_df.fromlongitude, station_df.fromlatitude)]
station_coords = gpd.GeoDataFrame(station_df, crs = {'init': 'epsg:4269'}, geometry=geometry)

located_stations = gpd.sjoin(station_coords, tract_df, how = 'left', op = 'within')
located_stations= located_stations[np.isfinite(located_stations['geoid_new'])]
located_stations.to_csv("python_merged_stations.csv")

## Graphing stations by tracts
stations_by_tract = located_stations.groupby("geoid_new").count()
stations_by_tract = stations_by_tract[["index_right"]].rename(columns = {"index_right": "Stations"})

mapped_stations = pd.merge(tract_df, stations_by_tract, how = "inner", left_on = "geoid_new", right_index = True)
mapped_stations.plot(column = "Stations", k = 9, linewidth = 0)
plt.title("Stations in tracts")
plt.show()
plt.savefig("stations_in_tract.png")
