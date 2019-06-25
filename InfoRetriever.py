from stravalib import Client



def get_race_data(access_token):
    client = Client(access_token)
    print(client.get_athlete()) # Get current athlete details

#activity = client.get_activity(1972530211)
#print (activity)

#race = client.get_running_races(2018)



#for i in range(10):
        #print (next(race))

    activity_stats = client.get_athlete_stats()

    run_count = activity_stats.all_run_totals.count
    bike_count = activity_stats.all_ride_totals.count
    swim_count = activity_stats.all_swim_totals.count

    total_count = run_count + bike_count + swim_count 

    all_activities = client.get_activities()

    count = 0
    races = []
    while count < run_count:
        activity = next(all_activities)
        if (activity.manual):
            count += 1
        if (str(activity.type) != "Run"):
            continue
        count += 1
        if (str(activity.workout_type) == "1" and str(activity.type) == "Run"):
            #print(str(activity.name) + " and " + str(activity.workout_type))
            races.append(activity)
    return races
#for activity in client.get_activities(after = "2010-01-01T00:00:00Z",  limit=5):
        #print ("type = " + activity.type)


def get_athlete_info(access_token): 
    client = Client(access_token)
    curr_athlete = client.get_athlete() # Get current athlete details
    return curr_athlete







