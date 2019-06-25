from InfoRetriever import get_race_data, get_athlete_info
from VDOT import enter_data, read_vdot


access_token = "Your access token here"


athlete_info = get_athlete_info(access_token)
race_data = get_race_data(access_token)

enter_data(athlete_info, race_data)

