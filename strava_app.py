from info_retriever import get_race_data, get_athlete_info
from vdot import format_data, calculate_vdot
from database import create_database, update_database, query_database
from plot import plot
import os.path
from os import path

access_token = "7449d7e1d2e8c7f48919c058e19f117af563ed2a"


athlete_info = get_athlete_info(access_token)
race_data = get_race_data(access_token)

data = format_data(athlete_info, race_data)

vdot_data = calculate_vdot(data)

if (path.exists("race.db")):
    update_database(vdot_data)
else:
    create_database(vdot_data)

queried_data = query_database()
print(queried_data)

plot(queried_data)
