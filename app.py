from flask import Flask, jsonify

prcp = []


stations = []

temp = []

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
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"



@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the date and precipitation data as json"""
     return jsonify(prcp)



@app.route("/api/v1.0/stations")
def stations():
    """Return the justice league data as json"""

    return jsonify(stations)



@app.route("/api/v1.0/tobs")
def temp():
    """Return the justice league data as json"""

    return jsonify(temp)



@app.route("/api/v1.0/<start>")
def startrange():
    """Return the justice league data as json"""

    return jsonify(temp)



@app.route("/api/v1.0/<start>/<end>")
def startendrange():
    """Return the justice league data as json"""

    return jsonify(temp)




if __name__ == "__main__":
    app.run(debug=True)