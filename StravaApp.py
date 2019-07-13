from InfoRetriever import get_race_data, get_athlete_info
from VDOT import format_data, read_vdot, create_database, calculate_vdot


access_token = "40966e55980680825230ee14e355ce2c05672b20"


athlete_info = get_athlete_info(access_token)
race_data = get_race_data(access_token)

data = format_data(athlete_info, race_data)

calculate_vdot(data)

create_database(data)

