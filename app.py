import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc

from flask import Flask, jsonify

##############
engine = create_engine(r"sqlite:///C:\Users\gargi\sqlalchemy-challenge\Resources\hawaii.sqlite")


Base = automap_base()
Base.prepare(engine, reflect=True)
measurement = Base.classes.measurement
station = Base.classes.stations
session = Session(engine)




# Flask Setup
#################
app = Flask(__name__)



# Flask Routes
##################

@app.route("/api/v1.0/precipitation")
def precipitation():
   # Create our session (link) from Python to the DB
   session = Session(engine)
   
   # Query all precipitaion
   prcp_data= session.query(measurement.date, measurement.prcp).all()

   session.close()
   # Convert list of tuples into normal list
   # Prcption = list(np.ravel(prcp_data))
   all_data = []
   for date, prcp in prcp_data:
       prcp_dict = {}
       prcp_dict["date"] = date
       prcp_dict["prcp"] = prcp
       all_data.append(prcp_dict)
   return jsonify(all_data)



# Dictionary of TOBS Data
    

@app.route("/api/v1.0/tobs")
def tobs():
   # Create our session (link) from Python to the DB
   session = Session(engine)
   
   # Query all precipitaion
   tobs_data= session.query(measurement.date, measurement.tobs).all()

   session.close()
   # Convert list of tuples into normal list
   # Prcption = list(np.ravel(prcp_data))   
   tobs_data = []
   results = session.query(measurement).filter(measurement.date > '2016-10-09').filter(measurement.date <= '2017-10-09').all()
   for data in results:
        tobs_dict = {}
        tobs_dict[data.date] = data.tobs
        tobs_data.append(tobs_dict)
   return jsonify(all_tobs)


@app.route("/api/v1.0/stations")
def stations():
    

    # Query all stations
    station_results = session.query(station.station).all()

    # Convert list of tuples into normal list
    station_list = list(np.ravel(station_results))

    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def tobs():
    

    # Query all tobs
    tobs_results = session.query(measurement.tobs).all()

    # Convert list of tuples into normal list
    tobs_list = list(np.ravel(tobs_results))

    return jsonify(tobs_list)


@app.route("/api/v1.0/<startdate>")
def tobs_by_date(startdate):
    

    return jsonify(session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= startdate).all())


@app.route("/api/v1.0/<startdate>/<enddate>")
def tobs_by_date_range(startdate, enddate):
    

    return jsonify(session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= startdate).filter(measurement.date <= enddate).all())


if __name__ == "__main__":
    app.run(debug=True)