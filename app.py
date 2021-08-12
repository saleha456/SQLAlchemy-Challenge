import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc
import datetime as dtt
from datetime import datetime as dt
from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)


Measurement = Base.classes.measurement
Station = Base.classes.station



# Flask Setup
app = Flask(__name__)


# Flask Routes

@app.route("/")
def home():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/yyyy-mm-dd<br/>"
        f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd<br/>")



@app.route("/api/v1.0/stations")
def stations():
    # Return Station data as JSON

    session = Session(engine)

    results = session.query(Station.station, Station.name).all()

    session.close()

    all_stations = []

    for station, stationname in results:

    	station_dict = {}
    	station_dict["station"] = station
    	station_dict["name"] = stationname

    	all_stations.append(station_dict)


    return jsonify(all_stations)


@app.route("/api/v1.0/precipitation")
def precipitation():
	
	session = Session(engine)

	# Get most recent date and the date from one year prior
	max_date_str = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
	max_date = dt.strptime(max_date_str, "%Y-%m-%d")
	max_date_ly = max_date - dtt.timedelta(days=365)


	#Query precipitation results for last year of data
	results = session.query(Measurement.date, Measurement.prcp).\
	filter(Measurement.date > max_date_ly).all()


	session.close()


	dates = []
	prcps = []

	for date, prcp in results:
		dates.append(date)
		prcps.append(prcp)

	prcp_dict = dict(zip(dates, prcps))

	return jsonify(prcp_dict)




@app.route("/api/v1.0/tobs")
def temp():
    session = Session(engine)

    # Get most recent date
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    most_recent_date = dt.strptime(most_recent_date, "%Y-%m-%d")
   

    # Get date from one year prior
    twelvemonthsprior = most_recent_date - dtt.timedelta(days=365)



    # Get most active station info
    most_active_station = session.query(Measurement.station, func.count(Measurement.station)).\
    		group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first()

    stationid = most_active_station[0]

    # Query temperature results for last year of data for the most active station
    results = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
    		filter(Measurement.station == stationid).\
    		filter(Measurement.date > twelvemonthsprior).all()

	# Close session
    session.close()

    all_tobs = []

    for station, date, tobs in results:

    	tobs_dict = {}
    	tobs_dict["station"] = station
    	tobs_dict["date"] = date
    	tobs_dict["temp"] = tobs

    	all_tobs.append(tobs_dict)

    return jsonify(all_tobs)



@app.route("/api/v1.0/<start>")
def startrange(start):

	# Get start date
	startdate = dt.strptime(start,"%Y-%m-%d")
	startdate = startdate - dtt.timedelta(days=1)
	

	# Create sesson and query results
	session = Session(engine)

	results = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
	group_by(Measurement.date).\
	filter(Measurement.date > startdate).all()


	# Find min and max dates from measurement data
	max_date_str = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
	max_date = dt.strptime(max_date_str,"%Y-%m-%d")
	min_date_str = session.query(Measurement.date).order_by(Measurement.date.asc()).first()[0]
	min_date = dt.strptime(min_date_str,"%Y-%m-%d")

	session.close()

	# Message if date outside range
	if (startdate < min_date or startdate > max_date) == True:
		return f"Please enter a date between {min_date_str} and {max_date_str}."


	# Store data into a dictionary
	all_tobs = []

	for date, mintemp, maxtemp, avgtemp in results:
		tobs_dict = {}
		tobs_dict["date"] = date
		tobs_dict["minimumtemp"] = mintemp
		tobs_dict["maximumtemp"] = maxtemp
		tobs_dict["avgtemp"] = round(avgtemp,2)

		all_tobs.append(tobs_dict)


	return jsonify(all_tobs)  

@app.route("/api/v1.0/<start>/<end>")
def startendrange(start=None, end=None):

	# Get start and end dates as variables
	startdate = dt.strptime(start,"%Y-%m-%d")
	startdate = startdate - dtt.timedelta(days=1)
	enddate = dt.strptime(end, "%Y-%m-%d")

	# Create session and query results
	session = Session(engine)

	results = session.query(Measurement.date, func.min(Measurement.tobs),func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
	group_by(Measurement.date).\
	filter(Measurement.date >= startdate).\
	filter(Measurement.date <= enddate).all()

	# Find min and max dates from measurement data
	max_date_str = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
	max_date = dt.strptime(max_date_str, "%Y-%m-%d")
	min_date_str = session.query(Measurement.date).order_by(Measurement.date.asc()).first()[0]
	min_date = dt.strptime(min_date_str, "%Y-%m-%d")


	session.close()


	# Message if date outside range
	if (startdate < min_date or startdate > max_date or enddate < min_date or enddate > max_date) == True:
		return f"Please enter a date range between {min_date_str} and {max_date_str}."



	# Store data as a dictionary
	all_tobs = []

	for date, mintemp, maxtemp, avgtemp in results:
		tobs_dict = {}
		tobs_dict["date"] = date
		tobs_dict["minimumtemp"] = mintemp
		tobs_dict["maximumtemp"] = maxtemp
		tobs_dict["avgtemp"] = round(avgtemp,2)

		all_tobs.append(tobs_dict)

	return jsonify(all_tobs)




if __name__ == "__main__":
    app.run(debug=True)