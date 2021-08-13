# SQLAlchemy-Challenge

This analysis looks at weather and precipitation data in Hawaii from 2014-2017.  It aims to use the data to plan a trip to determine what the weather will be based on past history.

### **climate-starter.ipynb**

**Precipitation Analysis:**

An exploratory precipitation analysis was done for the last year of data.  It shows precipitation (in inches) by date.  The average rainfall is approximately 0.176 inches. 

**Station Analysis:**

There were a total of 9 stations where measurements were conducted.  This analysis determined the station with the highest number of measurements.   The most active station was USC00519281 (WAIHEE 837.5, HI US).  The minimum, maximum, and average temperatures were calculated for this station.

A histogram was created for temperature ranges for the last year for data.  The temperate mostly falls around the 75 degree range.



### app.py (Climate API)

Six different routes were created:

1. ***/* :** Homepage that lists all the routes.

2. ***/api/v1.0/precipitation* :** A dictionary with date as key and precipitation as value for dates in the last year of the dataset.

3. ***/api/v1.0/stations* :** A list of stations and their names.

4. ***/api/v1.0/tobs*:** Temperature observations for each date for the last year of data for the most active station.

5. ***/api/v1.0/yyyy-mm-dd*** **:** Queries the min, max, and avg temperatures for the date entered and every subsequent date.

6. ***/api/v1.0/yyyy-mm-dd/yyy-mm-dd***: Queries the min, max, and avg temperature for each date in between the entered date range.

   

### Temperature Analysis I

**T-Test:**

This analysis looks at temperature data for the months of June and August to see if there is a statistical significance between the two time periods.  An unpaired t-test was done.  There is no statistical significance.

### Temperature Analysis II

**Avg Temp:**

This analysis calculates average temperature between a given date range (August 2016).  It creates a bar chart of the average temperature with and includes a y error bar.

**Total Rainfall:**

This analysis calculates total rainfall per weather station for the same given time period.

