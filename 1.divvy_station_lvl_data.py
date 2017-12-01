import pandas as pd

df = pd.read_csv("Divvy_Trips.csv",
                index_col = "TRIP ID", usecols = ["TRIP ID", "FROM STATION ID", "FROM LATITUDE", "FROM LONGITUDE"])

df = df.rename(columns = {"FROM STATION ID": "fromstationid", "FROM LATITUDE":"fromlatitude", \
                "FROM LONGITUDE":"fromlongitude"})
station_df = df.drop_duplicates(["fromstationid"], keep = "last")
station_df.to_csv("station_loc_id.csv")
