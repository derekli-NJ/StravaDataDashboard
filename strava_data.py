from info_retriever import get_activity_data, get_athlete_info, get_run_race_data, get_run_hr_data
from vdot import format_data, calculate_vdot
from database import create_database, update_database, update_hr_database, query_race_data, query_hr_data
from plot import plot_vdot_race, plot_beats_per_mile
import os.path, config
from os import path

def setup():
    access_token = config.access_token

    athlete_info = get_athlete_info(access_token)
    activity_data = get_activity_data(access_token)

    run_data = activity_data["Runs"]
    swim_data = activity_data["Swims"]
    bike_data = activity_data["Rides"]

    race_data = get_run_race_data(run_data)
    run_hr_data = get_run_hr_data(run_data) 

    formatted_race_data = format_data(athlete_info, race_data)

    vdot_data = calculate_vdot(formatted_race_data)

    if (path.exists("run.db")):
        update_database(vdot_data)
        update_hr_database(run_hr_data)
    else:
        create_database(vdot_data, run_hr_data)

    queried_race_data = query_race_data()
    queried_hr_data = query_hr_data()


    calorie_count = activity_data["Calorie_Count"]
    print (calorie_count)
    return {"hr_per_mile" : queried_hr_data, "vdot_race" : queried_race_data, "calorie_count" : calorie_count}

def plot_vdot_race_fig(data):
    return plot_vdot_race(data)

def plot_beats_per_mile_fig(data):
    return plot_beats_per_mile(data)


