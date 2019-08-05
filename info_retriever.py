from stravalib import Client

def get_activity_data(access_token):
    client = Client(access_token)

    activity_stats = client.get_athlete_stats()

    run_count = activity_stats.all_run_totals.count
    bike_count = activity_stats.all_ride_totals.count
    swim_count = activity_stats.all_swim_totals.count

    total_count = run_count + bike_count + swim_count 

    all_activities = client.get_activities()

    count = 0
    run_activities = []
    swim_activities = []
    bike_activities = []
    for activity in all_activities:
        if (activity.type == "Run"):
            run_activities.append(activity) 
        if (activity.type == "Swim"):
            swim_activities.append(activity)
        if (activity.type == "Ride"):
            bike_activities.append(activity)
    return ({"Runs": run_activities, "Swims" : swim_activities, "Rides": bike_activities})

def get_run_race_data(run_activities):
    races = []
    for activity in run_activities:
        if (str(activity.workout_type) == "1"):
            races.append(activity)
    return races

def get_run_hr_data(run_activities):
    runs_hr_data = []
    for activity in run_activities:
        if (activity.has_heartrate):
            runs_hr_data.append(activity)
    return runs_hr_data


def get_athlete_info(access_token): 
    client = Client(access_token)
    curr_athlete = client.get_athlete() # Get current athlete details
    return curr_athlete


