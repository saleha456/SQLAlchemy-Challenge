import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc

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

	results = session.query(Measurement.date, Measurement.prcp).all()

	session.close()

	all_prcp = []

	for date, prcp in results:
		prcp_dict = {}
		prcp_dict["date"] = date
		prcp_dict["precipitation"] = prcp

		all_prcp.append(prcp_dict)

	return jsonify(all_prcp)




@app.route("/api/v1.0/tobs")
def temp():
    session = Session(engine)

    # Get most recent date
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    
    # Convert day, month, and year to int
    most_recent_date_list = most_recent_date.split('-',3)
    day = int(most_recent_date_list[2])
    month = int(most_recent_date_list[1])
    year = int(most_recent_date_list[0])

    # Get date from one year prior
    twelvemonthsprior = dt.date(year, month, day) - dt.timedelta(days=365)



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

	startdate = dt.strptime(start,"%Y-%m-%d")
	



	session = Session(engine)

	results = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
	group_by(Measurement.date).\
	filter(Measurement.date >= startdate).all()

	session.close()

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
def startendrange(start):
	startdate = dt.strptime(start,"%Y-%m-%d")
	enddate = dt.strptime(end, "%Y-%m-%d")

	session = Session(engine)

	results = session.query(Measurement.date, func.min(Measurement.tobs),func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
	group_by(Measurement.date).\
	filter(Measurement.date >= startdate).\
	filter(Measurement.date <= enddate).all()

	session.close()

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