import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc

from flask import Flask, jsonify

##############
engine = create_engine(r'sqlite:///C:\Users\gargi\sqlalchemy-challenge\Instructions\Resources\hawaii.sqlite')


Base = automap_base()


Base.prepare(engine, reflect=True)


Measurement = Base.classes.measurement

Station = Base.classes.station


session = Session(engine)


# Flask Setup
#################
app = Flask(__name__)

@app.route("/")
def welcome():
    
    return ("Welcome to Hawaii")
    





@app.route("/api/v1.0/precipitation")
def precipitation():
   
   session = Session(engine)
   

   prcp_data= session.query(Measurement.date, Measurement.prcp).all()
   print(prcp_data)
   session.close()
   
   all_data = []

   for date, prcp in prcp_data:
       prcp_dict = {}
       prcp_dict["date"] = date
       prcp_dict["prcp"] = prcp
       all_data.append(prcp_dict)
   return jsonify(all_data)


@app.route("/api/v1.0/precipitation")
def precip():


    
    all_tobs = []
    results = session.query(Measurement).filter(Measurement.date > '2016-10-09').filter(Measurement.date <= '2017-10-09').all()
    for data in results:
        tobs_dict = {}
        tobs_dict[data.date] = data.tobs
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)


@app.route("/api/v1.0/stations")
def stations():
    

   
    station_results = session.query(Station.station).all()

    
    station_list = list(np.ravel(station_results))

    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def tobs():
    

    
    tobs_results = session.query(Measurement.tobs).all()

  
    tobs_list = list(np.ravel(tobs_results))

    return jsonify(tobs_list)


@app.route("/api/v1.0/<startdate>")
def tobs_by_date(startdate):
    start_temp = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= startdate).all()

    temp = list(np.ravel(start_temp))
    

    return jsonify(temp)

@app.route("/api/v1.0/<startdate>/<enddate>")
def tobs_by_date_range(startdate, enddate):
    start_end = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= startdate).filter(Measurement.date <= enddate).all()
    new = list(np.ravel(start_end))
    
    return jsonify(new)



if __name__ == "__main__":
    app.run(debug=True)