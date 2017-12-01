import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point
import numpy as np
from geopy.distance import vincenty
import pandas as pd
import datetime as dt

## Preparing the crime data
crime_df = pd.read_csv("python_merged_crime.csv",
                 usecols = ["id", "geoid_new"])

crime_df["crimes_per_tract"] = crime_df.groupby("geoid_new").transform("count")
small_df = crime_df.drop_duplicates(subset = "geoid_new", keep = "last")

small_df["high_crime_tract"] = np.where(small_df["crimes_per_tract"] > small_df.crimes_per_tract.quantile(.5), 1, 0)
# ## Preparing the station merged data
station_df = pd.read_csv("python_merged_stations.csv", usecols = ["geoid_new", "fromstationid"])
merged_inner_crime = pd.merge(left = station_df, right = small_df, how = "inner", left_on = "geoid_new", right_on = "geoid_new")

## Merge with Demographic data to get income
income_df = pd.read_csv("CHICAGO TRACT.csv", usecols = ["GIDTR", "Med_HHD_Inc_ACS_09_13"])
income_df["Med_HHD_Inc_ACS_09_13"] = income_df["Med_HHD_Inc_ACS_09_13"].replace('[\$,]', '', regex=True).astype(float)
income_df["low_income_tract"] = np.where(income_df["Med_HHD_Inc_ACS_09_13"] \
         <= income_df.Med_HHD_Inc_ACS_09_13.quantile(.3), 1, 0)
income_df["med_income_tract"] = np.where((income_df["Med_HHD_Inc_ACS_09_13"] \
        > income_df.Med_HHD_Inc_ACS_09_13.quantile(.3)) & (income_df["Med_HHD_Inc_ACS_09_13"] \
        <= income_df.Med_HHD_Inc_ACS_09_13.quantile(.6)), 1, 0)
income_df["high_income_tract"] = np.where(income_df["Med_HHD_Inc_ACS_09_13"] \
         > income_df.Med_HHD_Inc_ACS_09_13.quantile(.6), 1, 0)

merged_income = pd.merge(left = merged_inner_crime, right = income_df, how = "inner", left_on = "geoid_new", right_on = "GIDTR")

## Preparing the trips data
trips_df = pd.read_csv("Divvy_Trips.csv", usecols = ["FROM STATION ID", "TRIP ID", "START TIME", \
            "GENDER", "BIRTH YEAR", "TRIP DURATION", "FROM LONGITUDE", "FROM LATITUDE", "TO LONGITUDE", "TO LATITUDE"])

## Geting Month
trips_df["month"] = trips_df["START TIME"].astype(str).str[:2]
trips_df["time"] = trips_df["START TIME"].astype(str).str[11:]
trips_df["24_hrs"] = pd.to_datetime(trips_df["time"]).dt.strftime('%H:%M:%S')
trips_df["hour"] = trips_df["24_hrs"].astype(str).str[:2]

## Creating hour categories
trips_df["overnight"] = np.where((trips_df["hour"].astype(int) >= 0) & (trips_df["hour"].astype(int) <= 6), 1,0)
trips_df["office_early"] = np.where((trips_df["hour"].astype(int) >= 7) & (trips_df["hour"].astype(int) <= 15),1 ,0)
trips_df["office_afternoon"] = np.where((trips_df["hour"].astype(int) >= 16) & (trips_df["hour"].astype(int) <= 19),1,0)
trips_df["nighters"] = np.where((trips_df["hour"].astype(int) >= 20) & (trips_df["hour"].astype(int) <= 23),1,0)

overnight = trips_df.groupby(["FROM STATION ID", "month"], as_index=False).agg({"overnight": "mean"})
office_early = trips_df.groupby(["FROM STATION ID", "month"], as_index=False).agg({"office_early": "mean"})
office_afternoon = trips_df.groupby(["FROM STATION ID", "month"], as_index=False).agg({"office_afternoon": "mean"})
nighters = trips_df.groupby(["FROM STATION ID", "month"], as_index=False).agg({"nighters": "mean"})

t1 = pd.merge(overnight, office_early, on = ["FROM STATION ID", "month"])
t2 = pd.merge(t1, office_afternoon, on = ["FROM STATION ID", "month"])
t3 = pd.merge(t2, nighters, on = ["FROM STATION ID", "month"])

## Average DURATION
def haversine_np(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)

    All args must be of equal length.

    """
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2

    c = 2 * np.arcsin(np.sqrt(a))
    miles = 6367 * c * 0.621371
    return miles
df = trips_df.rename(columns={'FROM LONGITUDE':"lon1",'TO LONGITUDE':"lon2",'FROM LATITUDE':"lat1",'TO LATITUDE':"lat2"})
miles = haversine_np(df['lon1'],df['lat1'],df['lon2'],df['lat2'])
miles = miles.to_frame(name = "miles")
trips_df["miles"] = miles["miles"]
avg_distance = trips_df.groupby(["FROM STATION ID", "month"], as_index=False).agg({"miles": "mean"})

## Estimating GENDER
trips_df["male"] = np.where(trips_df["GENDER"] == "Male", 1, 0)
pct_male = trips_df.groupby(["FROM STATION ID", "month"], as_index=False).agg({"male": "mean"})
## Average DURATION
avg_duration = trips_df.groupby(["FROM STATION ID", "month"], as_index=False).agg({"TRIP DURATION": "mean"})
## Average Age
trips_df["age"] = 2017 - trips_df["BIRTH YEAR"]
avg_age = trips_df.groupby(["FROM STATION ID", "month"], as_index=False).agg({"age": "mean"})
## Trip Probability per station
trips_per_station = (trips_df.groupby(["FROM STATION ID", "month"], as_index = False).size()/trips_df.shape[0]).reset_index()
trips_per_station = trips_per_station.rename(columns = {0:"probability"})

## Merging created variables
merge1 = pd.merge(pct_male, avg_duration, on = ["FROM STATION ID", "month"])
merge2 = pd.merge(merge1, avg_age, on = ["FROM STATION ID", "month"])
merge3 = pd.merge(merge2, trips_per_station, on = ["FROM STATION ID", "month"])
merge4 = pd.merge(merge3, avg_distance, on = ["FROM STATION ID", "month"])
merge5 = pd.merge(t3, merge4, on = ["FROM STATION ID", "month"])

final_merge = pd.merge(left = merged_income, right = merge5, how = "inner", left_on = "fromstationid", right_on = "FROM STATION ID")
final_merge.to_csv("mega_data.csv")
