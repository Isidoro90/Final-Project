import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point
import numpy as np

import pandas as pd

tract_df = gpd.read_file("geo_export_add04ab2-b26d-4df6-97be-d04944b3a133.shp")

crime_df = pd.read_csv("Crimes_2016_clean_short.csv")
geometry = [Point(xy) for xy in zip(crime_df.longitude, crime_df.latitude)]
crime_coords = gpd.GeoDataFrame(crime_df, crs = {'init': 'epsg:4269'}, geometry=geometry)

located_crime = gpd.sjoin(crime_coords, tract_df, how = 'left', op = 'within')
located_crime= located_crime[np.isfinite(located_crime['geoid_new'])]
located_crime.to_csv("python_merged_crime.csv")

## Graphing stations by tracts
crimes_by_tract = located_crime.groupby("geoid_new").count()
crimes_by_tract = crimes_by_tract[["index_right"]].rename(columns = {"index_right": "Crimes"})

mapped_crimes = pd.merge(tract_df, crimes_by_tract, how = "inner", left_on = "geoid_new", right_index = True)
mapped_crimes.plot(column = "Crimes", k = 9, linewidth = 0)
plt.title("Crimes in tracts")
plt.show()
plt.savefig("crimes_in_tract.png")
