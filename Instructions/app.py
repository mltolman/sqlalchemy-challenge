import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


# Set Up Database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#reflect an existing db into a new model

Base = automap_base()

# Reflect the table

Base.prepare(engine, reflect = True)

# Save references to the tables 

Meas = Base.classes.measurement
Station = Base.classes.station

# Flask Setup

app = Flask(__name__)

#Flask Routes

@app.route("/")
def home():
    """List all available API routs"""
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def percipitation():

    # create session
    session = Session(engine)

    """Return list of percipitation"""
    # query results
    results = session.query(Meas.date, Meas.prcp).all()

    session.close()

    percip = []

    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        percip.append(prcp_dict)

    return jsonify(percip)

@app.route("/api/v1.0/stations")
def stations():
    
    session = Session(engine)

    """Return list of all stations from dataset"""

    results = session.query(Station.station, Station.name).all()

    session.close()

    stations_list = []

    for station, name in results:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        stations_list.append(station_dict)

    return jsonify(stations_list)


@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)

    """Return dates and temps of most active sations for last year of data"""  

    results = session.query(Meas.date, Meas.tobs).filter(Meas.date >= '2016-08-23').all()

    session.close()

    tobs_list = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def calc_temps(start_date):

    session = Session(engine)

    """Return tmin, tavg, tmax for given start date"""

    

    results = session.query(func.min(Meas.tobs), func.avg(Meas.tobs), func.max(Meas.tobs))
        
    session.close()


    start_tobs_list = []

    for date, tobs in results:
        start_date = {}
        start_date['date'] = date['start']
        start_date['tmin'] = func.min(Meas.tobs)
        start_date['tavg'] = func.avg(Meas.tobs)
        start_date['tmax'] = func.max(Meas.tobs)
        start_tobs_list.append(start_date)

    return jsonify(start_tobs_list)
        

    

#    start_tobs_list = []

#    for date, tobs in results:
#        start_tobs_dict = {}
#        start_tobs_dict['date'] = date
#        start_tobs_dict['tmin'] = func.min(Meas.tobs)
#        start_tobs_dict['tavg'] = func.avg(Meas.tobs)
#        start_tobs_dict['tmax'] = func.max(Meas.tobs)
#        start_tobs_list.append(start_tobs_dict)

#    return jsonify(start_tobs_list)

if __name__ == '__main__':
    app.run(debug = True)