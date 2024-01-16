# Import the dependencies.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text, inspect, func, and_
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///RBCDS\Starter_Code\Week 3\Challenge\Module 10\Starter_Code\Resources\hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session= Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
# Create our session (link) from Python to the DB
    session = Session(engine)

    ABC = engine.execute(text('SELECT date, prcp FROM Measurement WHERE date >= "2016-08-23"')).fetchall()

# # Save the query results as a Pandas DataFrame. Explicitly set the column names

    sql_query = pd.DataFrame(ABC, columns = ['date', 'precipitation'])
# Sort the dataframe by date
    sql_query = sql_query.sort_values('date', ascending=True)

    session.close()

    precipitation_dates = list(np.ravel(sql_query))
    return jsonify(precipitation_dates)


@app.route("/api/v1.0/stations")
def stations():
#     # Create our session (link) from Python to the DB
    session = Session(engine)

#     """Return a list of passenger data including the name, age, and sex of each passenger"""
     # Query all passengers
    Station1 = session.query(Station.station).all()

    session.close()
    All_stations = list(np.ravel(Station1))
    return jsonify(All_stations)

@app.route("/api/v1.0/tobs")
def tobs():
#     # Create our session (link) from Python to the DB
    session = Session(engine)

    MASI = engine.execute(text('SELECT date,tobs FROM Measurement WHERE date >= "2016-08-23" AND station = "USC00519281"')).fetchall()
    sql_query2 = pd.DataFrame(MASI, columns = ['date','tobs'])
    
    session.close()
    pd_stations = list(np.ravel(sql_query2))
    return jsonify(pd_stations)

@app.route("/api/v1.0/<start>")
def start(start):
#     # Create our session (link) from Python to the DB
    print("Start Date:", start)  # Debugging print statement

    # Create our session (link) from Python to the DB
    session = Session(engine)

    sel = [Measurement.date, Measurement.tobs]

    # Debugging print statement to check the generated SQL query
    print(session.query(*sel).filter(Measurement.date >= start))

    temperature_data = session.query(*sel).filter(Measurement.date >= start).all()

    # Calculate summary statistics
    min_temp = min(row[1] for row in temperature_data)
    max_temp = max(row[1] for row in temperature_data)
    avg_temp = sum(row[1] for row in temperature_data) / len(temperature_data)

    session.close()

    # Convert the result to a list of dictionaries
    result_list = [{"date": row[0], "temperature": row[1]} for row in temperature_data]

    # Include summary statistics in the response
    result_dict = {
        "temperature_data": result_list,
        "summary_statistics": {
            "min_temperature": min_temp,
            "max_temperature": max_temp,
            "avg_temperature": avg_temp
        }
    }

    return jsonify(result_dict)

@app.route("/api/v1.0/<start>/<end>")
def end(start,end):
#     # Create our session (link) from Python to the DB
    

    # Create our session (link) from Python to the DB
    session = Session(engine)

    sel = [Measurement.date, Measurement.tobs]

    temperature_data = session.query(*sel).filter(and_(Measurement.date >= start, Measurement.date <= end)).all()

    # Calculate summary statistics
    min_temp = min(row[1] for row in temperature_data)
    max_temp = max(row[1] for row in temperature_data)
    avg_temp = sum(row[1] for row in temperature_data) / len(temperature_data)

    session.close()

    # Convert the result to a list of dictionaries
    result_list = [{"date": row[0], "temperature": row[1]} for row in temperature_data]

    # Include summary statistics in the response
    result_dict = {
        "temperature_data": result_list,
        "summary_statistics": {
            "min_temperature": min_temp,
            "max_temperature": max_temp,
            "avg_temperature": avg_temp
        }
    }

    return jsonify(result_dict)




if __name__ == '__main__':
    app.run(debug=True)