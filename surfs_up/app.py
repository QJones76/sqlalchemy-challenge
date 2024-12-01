# Import the dependencies.
from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import numpy as np
import pandas as pd

#################################################
# Database Setup
#################################################
engine = create_engine('sqlite:///Resources/hawaii.sqlite')

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################

# Create a default page with all available api routes
@app.route('/')
def home():
    return(
        f'Available Routes:<br/>'
        f'/api/v1.0/precipitation <br/>'
        f'/api/v1.0/stations <br/>'
        f'/api/v1.0/tobs <br/>'
        f'/api/v1.0/start <br/>'
        f'/api/v1.0/start/end'
    )

# Create a route for for the query resutls from your precipitation analysis
# using date as the key and prcp as the value
@app.route('/api/v1.0/precipitation')
def precipitation():
    # Create a session link
    session = Session(engine)

    # Find the last year of precipitation data
    prcp_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= (pd.to_datetime(session.query(func.max(Measurement.date)).\
        scalar()) - pd.DateOffset(years=1)).strftime('%Y-%m-%d')).all()
    
    # convert to a pandas dataframe
    prcp_data_df = pd.DataFrame(prcp_data, columns=['date', 'prcp'])

    # convert to a dictionary
    prcp_data_dict = prcp_data_df.set_index('date')['prcp'].to_dict()

    # Close the session
    session.close()

    # Return jsonified data
    return jsonify(prcp_data_dict)

# Create a route that returns the list of stations from the dataset
@app.route('/api/v1.0/stations')
def stations():
    # Create a session link
    session = Session(engine)

    # Query the list of staion names
    results = session.query(Station.station).all()

    # Close the session
    session.close()

    # Convert the list of tuple into a normal list for jsonifycation
    all_stations = list(np.ravel(results))

    # Return jsonified data
    return jsonify(all_stations)


# Create a route that returns the date and the last year of tobs data for mas
@app.route('/api/v1.0/tobs')
def mas_temp_observations():
    # Create a session link
    session = Session(engine)

    # TEMPERATURE SECTION (start)
    # For just temperature data, use this section and comment out the dictionary section
    # Define mas like you did in the analysis
    mas = session.query(Measurement.station, func.count(Measurement.station)) \
    .group_by(Measurement.station) \
    .order_by(func.count(Measurement.station).desc()).first()
    mas_name = mas[0]

    # Find the mas data
    station_temp = session.query(Measurement.tobs).\
    filter(Measurement.station == f'{mas_name}').\
    filter(Measurement.date >= (pd.to_datetime(session.query(func.max(Measurement.date)).\
    scalar()) - pd.DateOffset(years=1)).strftime('%Y-%m-%d')).all()

    # Close the session
    session.close()

    # Convert the list of tuple data into a normal list for jsonifycation
    year_of_mas_temp = list(np.ravel(station_temp))

    # Return the jsonified data
    return jsonify(year_of_mas_temp)
    # TEMPERATURE SECTION (end)

    # # DICTIONARY SECTION (start)
    # # For a dictionary of temperature data, use this and comment out the temperature section 
    # # Define mas like you did in the anlysis
    # mas = session.query(Measurement.station, func.count(Measurement.station)) \
    # .group_by(Measurement.station) \
    # .order_by(func.count(Measurement.station).desc()).first()
    # mas_name = mas[0]
    
    # # Find the mas data
    # station_temp = session.query(Measurement.date, Measurement.tobs).\
    # filter(Measurement.station == f'{mas_name}').\
    # filter(Measurement.date >= (pd.to_datetime(session.query(func.max(Measurement.date)).\
    # scalar()) - pd.DateOffset(years=1)).strftime('%Y-%m-%d')).all()

    # # Convert to a dataframe
    # station_temp_df = pd.DataFrame(station_temp, columns=['date', 'tobs'])

    # # Convert to a dictionary
    # station_temp_dict = station_temp_df.set_index('date')['tobs'].to_dict()

    # # Close the session
    # session.close()

    # # Return jsonified data
    # return jsonify(station_temp_df)
    # # DICTIONARY SECTION (end)


# Create a route that returns the min, avg, and max temp for a start date
@app.route('/api/v1.0/start')
def start():
    # Ask user for a start date
    start_date = input("Enter the start date (YYYY-MM-DD): ")

    # Create a session link
    session = Session(engine)

    # Find the min, avg, and max temps for all values after the start date
    results = session.query(
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)
    ).filter(Measurement.date >= start_date).all()

    # Save the results in a dictionary for jsonifycation
    temps = {
        "start_date": start_date,
        "min_temp": results[0][0],
        "avg_temp": results[0][1],
        "max_temp": results[0][2]
    }

    # Close the session
    session.close()

    # Return jsonified data
    return jsonify(temps)

# Create a route that returns the min, avg, and max temp for a start-end date
@app.route('/api/v1.0/start/end')
def start_end():
    # Ask user for a start date
    start_date = input("Enter the start date (YYYY-MM-DD): ")

    # Ask user for a end date
    end_date = input("Enter the end date (YYYY-MM-DD): ")

    # Create a session link
    session = Session(engine)

    # Find the min, avg, and max temps for all values after the start date
    results = session.query(
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)
    ).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    # Save the results in a dictionary for jsonifycation
    temps = {
        "start_date": start_date,
        "min_temp": results[0][0],
        "avg_temp": results[0][1],
        "max_temp": results[0][2]
    }

    # Close the session
    session.close()

    # Return jsonified data
    return jsonify(temps)

if __name__ == "__main__":
    app.run(debug=True)