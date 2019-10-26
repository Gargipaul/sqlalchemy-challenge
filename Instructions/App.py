import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc
import os
from flask import Flask, jsonify

#######################################################
print(os.path)
engine = create_engine('sqlite:///Resources/hawaii.sqlite')


Base = automap_base()


Base.prepare(engine, reflect=True)


Measurement = Base.classes.measurement

Station = Base.classes.station


session = Session(engine)

#################
# Flask Setup
#################

app = Flask(__name__)



#################
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
    


#######################
# precipitation result
#######################

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
       session.close()
   return jsonify(all_data)



#################
# station result
#################

@app.route("/api/v1.0/stations")
def stations():
    

   
    station_results = session.query(Station.station).all()

    session.close()
    station_list = list(np.ravel(station_results))

    return jsonify(station_list)


################
# tobs result
################


@app.route("/api/v1.0/tobs")
def tobs():
    

    
    tobs_results = session.query(Measurement.tobs).all()

    session.close()
    tobs_list = list(np.ravel(tobs_results))

    return jsonify(tobs_list)


################################
# startdate get Min/Avg/Max temp  
################################


@app.route("/api/v1.0/<startdate>")
def tobs_by_date(startdate):

    start_temp = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs).\
    filter(Measurement.date >= startdate)).all()

    session.close()

    temp = list(np.ravel(start_temp))
    

    return jsonify(temp)


#########################################
# start/end date and get Min/Avg/Max temp  
#########################################


@app.route("/api/v1.0/<start>/<end>")
def tobs_trip(start,end):

     
    
    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    end_date= dt.datetime.strptime(end,'%Y-%m-%d')
    start = start_date
    end = end_date
    
    trip_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()
    tobs_trip = list(np.ravel(trip_data))
    
    return jsonify(tobs_trip)
    





if __name__ == "__main__":
    app.run(debug=True)