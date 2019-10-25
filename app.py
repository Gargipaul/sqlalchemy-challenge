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

# Flask route
#################

@app.route("/")
def welcome():
    
    return(
        "/api/v1.0/precipitation<br/><br/>"
        "/api/v1.0/stations<br/><br/>"
        "/api/v1.0/tobs<br/><br/>"
        "/api/v1.0/startdate<br/><br/>"
        "/api/v1.0/start/end<br/>"
    )
    



# presipitation result

@app.route("/api/v1.0/precipitation")
def precipitation():
   
   session = Session(engine)
   

   prcp_data= session.query(Measurement.date, Measurement.prcp).all()

   session.close()
   
   all_data = []

   for date, prcp in prcp_data:
       prcp_dict = {}
       prcp_dict["date"] = date
       prcp_dict["prcp"] = prcp
       all_data.append(prcp_dict)
   return jsonify(all_data)



# station result

@app.route("/api/v1.0/stations")
def stations():
    

   
    station_results = session.query(Station.station).all()

    
    station_list = list(np.ravel(station_results))

    return jsonify(station_list)

# tobs result
  
@app.route("/api/v1.0/tobs")
def tobs():
    

    
    tobs_results = session.query(Measurement.tobs).all()

  
    tobs_list = list(np.ravel(tobs_results))

    return jsonify(tobs_list)

    # startdate get Min/Avg/Max temp  

@app.route("/api/v1.0/<startdate>")
def tobs_by_date(startdate):

    start_temp = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= startdate).all()

    temp = list(np.ravel(start_temp))
    

    return jsonify(temp)

# start/end date and get Min/Avg/Max temp  

@app.route("/api/v1.0/<start>/<end>")
def tobs_trip(start,end):

     
    
    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    end_date= dt.datetime.strptime(end,'%Y-%m-%d')
    last_year = dt.timedelta(days=365)
    start = start_date-last_year
    end = end_date-last_year
    
    trip_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
   
    tobs_trip = list(np.ravel(trip_data))
    
    return jsonify(tobs_trip)
    





if __name__ == "__main__":
    app.run(debug=True)