import sqlite3

##### HELPER FUNCTIONS #####
def find_existing_id(cursor):
    existing_id = set()
    for id_val in cursor:
       existing_id.add(id_val[0]) 
    return (existing_id)
#####


def create_database(vdot_data, run_hr_data):
    sql_create_race_table= """ CREATE TABLE IF NOT EXISTS race(
                                         id integer PRIMARY KEY,
                                         activity_name text,
                                         distance real,
                                         time text,
                                         vdot real,
                                         date text
                                     ); """

    sql_create_hr_data_table= """ CREATE TABLE IF NOT EXISTS hr_data(
                                         id integer PRIMARY KEY,
                                         activity_name text,
                                         start_date_local text,
                                         average_hr real,
                                         distance real,
                                         total_elevation_gain real
                                     ); """
    connection = sqlite3.connect("run.db")
    cursor = connection.cursor()

    #Create tables in run.db
    cursor.execute(sql_create_race_table)
    cursor.execute(sql_create_hr_data_table)

    sql_formatted_data = []
    
    for key in vdot_data:
        #Choosing to use the rounded value entered into vdot calculator (decide if I want to use the exact value later)
        sql_formatted_data.append((key, vdot_data[key][1]['entered']['distance'], vdot_data[key][0].name, vdot_data[key][1]['entered']['time'], vdot_data[key][1]['vdot'], str(vdot_data[key][0].start_date)))

    cursor.executemany('''INSERT INTO race(id, activity_name, distance, time, vdot, date) VALUES(?, ?, ?, ?, ?, ?)''', sql_formatted_data)


    hr_sql_data = []
    for activity in run_hr_data:
        hr_sql_data.append((activity.id, activity.name, str(activity.start_date_local), float(activity.average_heartrate), float(activity.distance), float(activity.total_elevation_gain)))

    cursor.executemany('''INSERT INTO hr_data(id, activity_name, start_date_local, average_hr, distance, total_elevation_gain) VALUES( ?, ?, ?, ?, ?, ?)''', hr_sql_data)

    connection.commit()
    connection.close()

def update_database(vdot_data):
    connection = sqlite3.connect("run.db")
    cursor = connection.execute("SELECT id from race")
    existing_id = find_existing_id(cursor) 
    curs = connection.cursor()
    for key in vdot_data:
        if int(key) not in existing_id:
            curs.execute('''INSERT INTO race(id, activity_name, distance, time, vdot, date) VALUES(?, ?, ?, ?, ?, ?)''',  (key, vdot_data[key][1]['entered']['distance'], vdot_data[key][0].name, vdot_data[key][1]['entered']['time'], vdot_data[key][1]['vdot'], str(vdot_data[key][0].start_date)))

    connection.commit()
    connection.close()

def update_hr_database(run_hr_data):
    connection = sqlite3.connect("run.db")

    cursor = connection.execute("SELECT id from hr_data")

    curs = connection.cursor()
    existing_id = find_existing_id(cursor)
    for activity in run_hr_data:
        if activity.id not in existing_id:
            curs.execute('''INSERT INTO hr_data(id, activity_name, start_date_local, average_hr, distance, total_elevation_gain) VALUES( ?, ?, ?, ?, ?, ?)''', (activity.id, activity.name, str(activity.start_date_local), float(activity.average_heartrate), float(activity.distance), float(activity.total_elevation_gain)))
        else:
            '''
            Since run_hr_data is in reverse chronological order we can assume
            that if an id already exists every following id has already been 
            logged in the databases creation
            '''
            break

def query_race_data():
    connection = sqlite3.connect("run.db")

    cursor = connection.execute("SELECT id, activity_name, distance, time, vdot, date from race")

    race_data = []
    for row in cursor:
        race_data.append((row[0], (row[1], row[2], row[3], row[4], row[5])))

    return (dict(race_data))

def query_hr_data():
    connection = sqlite3.connect("run.db")

    cursor = connection.execute("SELECT id, activity_name, start_date_local, average_hr, distance, total_elevation_gain from hr_data")

    hr_data = []
    for row in cursor:
        hr_data.append((row[0], (row[1], row[2], row[3], row[4], row[5])))

    return (dict(hr_data))
