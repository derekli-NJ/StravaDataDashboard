from InfoRetriever import get_race_data, get_athlete_info
from VDOT import format_data, calculate_vdot
from Database import create_database

access_token = "2687aadf8fcd64c965937d81677ae5cc2bebc487"


athlete_info = get_athlete_info(access_token)
race_data = get_race_data(access_token)

data = format_data(athlete_info, race_data)

vdot_data = calculate_vdot(data)

create_database(vdot_data)

