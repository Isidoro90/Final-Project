#Final-Project
This is the repository for the final project of Isidoro Garcia and Umer Naeem 

## **The determinants of DIVVY bike use**

The usage of alternative transportation means like DIVVY bikes has increased steadily in recent years. As a result, it’s important to for the DIVVY system to have a nourished network of stations, so that users are able to use DIVVY without station constraints. In this project, we aim to identify the factors that DIVVY bikes’ demand by station. To do this, we estimate the probability of using a DIVVY at the station level and regress it to weather, geographical and socio-economic factors. In the end, this factor regression results could be useful to identify the most important factors of DIVVY demand and to assess whether a new station location is a good idea or not.
We believe that the following factors are the most important for DIVVY bikes demand: 
	Distance from origin to destination station, since biking involves physical effort. 
	Weather
	Crime rate in the trip’s area. 
	Time
	Income, since DIVVY bikes’ prices are somehow high. 
	Age of the potential user
	Gender
To assemble this dataset, we need to merge and join datasets from different sources. 
Data 
We merge data from the DIVVY trips (Trip Level), Station shapefile, Census tract shapefile, Income (Tract Level) and Crime (Tract Level). 
First, we combine geo databases in to the same file using fromstationid. Each census tract has n≥0 station within it. Plotting the stations in the city, we got the following: 

![Tracts](https://github.com/Isidoro90/Final-Project/edit/master/chicago_tract.png)
![Stations](https://github.com/Isidoro90/Final-Project/edit/master/divvy_stations.png)
![Stations_Tract_merge](https://github.com/Isidoro90/Final-Project/edit/master/stations_in_tracts.png)


Afterwards, we merge this dataset with the DIVVY trips database, using again fromstationid. With this database, that is at trip level, we calculate the probability of using a DIVVY by station and month. 

![probability_distribution](https://github.com/Isidoro90/Final-Project/edit/master/probability_histogram.png)


Afterwards, we collapse to the station and month level. This gives us 6,016 observations (555 stations, 12 months per station). This database is now a panel of stations, that will enable us to calculate DIVVY demand drivers with a fixed effects model. 

![Trips_vs_Month](https://github.com/Isidoro90/Final-Project/edit/master/scatter_prob_month.png)


Finally, we merge this database with income at the census tract level and crime levels from Chicago area using census tract id.

### **Data**
**DIVVY TRIPS**
We downloaded data for all the DIVVY bike trips in Chicago during 2016. This trip level database that includes: type of user, gender, age, location of the starting station, location of the final station and start and end times of the trips. 
	We used the location to estimate the distance per trip and the start and end times to estimate the duration per trip.
	We calculate the month by manipulating the start and end time variables. 
	We calculated the probability of using a bike in the i station in month t. 
	We estimated the 3-time buckets for the users: overnights (from 1 am to 6 am), office_early (from 7 am to 15 pm), office afternoon (from 16 to 19 hours) and nighters (from 20 to 24 hours). It’s worth saying that we decided these bins to better represent the DIVVY usage during daytime. 
 
![Distribution_of_trips_dayhour](https://github.com/Isidoro90/Final-Project/edit/master/start_time_graph.png)
 
**INCOME LEVEL DATA**
In this dataset, we divided the income in three buckets: Low, Medium and High income using 30th and 60th percentiles, respectively. 
CRIME DATA 
For this dataset, we estimated the crime level in 2 buckets: High Crime tract (iff Crime level at that tract is higher than the median crime level at Chicago). 

![Crimes_Map](https://github.com/Isidoro90/Final-Project/edit/master/chicago_crimes.png)

**Panel Regression Analysis**
Using this panel dataset, we run the following regression:

**Pr⁡(Using DIVVY at station i)_it=α+μ_t+Xβ+(u_i+ϵ_t)**

Where α is constant, μ is a constant per month (fixed effect by month), β are the parameters to estimate. 
X is matrix of n times t rows and 9 rows: 

med_income_tract
high_income_tract
pct_male
avg_age
avg_duration
high_crime_tract
office_early
office_afternoon
nighters

It is worth noting that we didn’t include fixed effects by station because income and crime data are at tract level only and thus they don’t have variation at the station month level. 

**RESULTS**
 
Looking at the table we find the following significant results: 

![regression_results](https://github.com/Isidoro90/Final-Project/edit/master/regression_results.PNG)

Medium income households are, on average, 0.7 base points more likely to use DIVVY bikes than low income households. Furthermore, High income households are, on average, 0.02 percentage points more likely to use DIVVY bikes than low income households. This result is very intuitive. It means that DIVVY bikes Engel curve, i.e. the demand of DIVVY bikes against income, is increasing, but at decreasing rates. This means that as income increases, from being low income to medium income, people start using more DIVVY bikes, but as income increases further, and perhaps people are able to afford luxury cars, the increase in DIVVY is lower compared to the medium income case. 
There are no significant differences in the use of DIVVY bikes by gender. 
The results on distance are also as expected. If the trip is 1 % farer, the probability of using a DIVVY bike decreases by 0.1 base points. This means that user consider the distance when they are deciding whether to use DIVVY bikes, as biking is a physical activity. 
Regarding crime rates, the results show a positive correlation between the crime and the probability of using DIVVY bikes. This sounds intuitive if we look at it from the crime perspective. If a criminal is considering the best place to rob, he might consider bikers as a more vulnerable population, compared to people that go by car. Consequently, the results show that if tract we the station is located has higher crime rates are associated with more DIVVY bike usage. 
Finally, we run the model with month fixed effects. This controls for weather conditions indirectly, as there a clear hike in DIVVY bikes usage during months with high temperatures. DIVVY bikes are highly demanded from April to October. This changes the intercept of different months with respect to January, our omitted month. 

![Residuals_vs_Predicted](https://github.com/Isidoro90/Final-Project/edit/master/resid_fitt_graph.png)

**Outlier analysis** 
Looking at the distribution of the probability of DIVVY usage by station, we notice that it has a lot of skewnees. Moreover, that are a significant number of stations that are considered outliers. Normally this will call for estimating the model without them. However, in this case this is no convenient for two reasons: 1 because the outliers are a considerable number and because this observations reflect the concentration of stations that are located in the loop of Chicago. 
   
 
As we can see, the linear prediction does very well for stations were the model predicted a positive probability of using DIVVY bikes and not so good for stations that are not used a lot. This suggests that some stations are not supposed to be there, according to our model. 

**Conclusions**
In this project we estimated the probability of using DIVVY bikes in Chicago with socio-economic factor that can affect it. This estimation is very useful as it can be a rule of thumb on where to put a new station in the city. Our results show that the stations with very high demand are well captured in our estimation. However, our estimation points that stations with very low demand should be there and perhaps reallocate where the socio-economics characteristics forecast a better spot. 
