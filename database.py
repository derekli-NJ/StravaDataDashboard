import sqlite3

def create_database(vdot_data):
    sql_create_race_table= """ CREATE TABLE IF NOT EXISTS race(
                                         id integer PRIMARY KEY,
                                         race_name text,
                                         distance real,
                                         time text,
                                         vdot real,
                                         date text
                                     ); """

    connection = sqlite3.connect("race.db")
    cursor = connection.cursor()
    cursor.execute(sql_create_race_table)

    sql_formatted_data = []
    
    for key in vdot_data:
        #Choosing to use the rounded value entered into vdot calculator (decide if I want to use the exact value later)
        sql_formatted_data.append((key, vdot_data[key][1]['entered']['distance'], vdot_data[key][0].name, vdot_data[key][1]['entered']['time'], vdot_data[key][1]['vdot'], str(vdot_data[key][0].start_date)))

    cursor.executemany('''INSERT INTO race(id, race_name, distance, time, vdot, date) VALUES(?, ?, ?, ?, ?, ?)''', sql_formatted_data)

    connection.commit()
    connection.close()

def update_database(vdot_data):
    
    connection = sqlite3.connect("race.db")

    cursor = connection.execute("SELECT id from race")

    existing_id = set()
    for id_val in cursor:
       existing_id.add(id_val[0]) 

    print (existing_id)
    curs = connection.cursor()
    for key in vdot_data:
        if int(key) not in existing_id:
            curs.execute('''INSERT INTO race(id, race_name, distance, time, vdot, date) VALUES(?, ?, ?, ?, ?)''',  (key, vdot_data[key][1]['entered']['distance'], vdot_data[key][0].name, vdot_data[key][1]['entered']['time'], vdot_data[key][1]['vdot'], str(vdot_data[key][0].start_date)))

    connection.commit()
    connection.close()


def query_database():
    connection = sqlite3.connect("race.db")

    cursor = connection.execute("SELECT id, race_name, distance, time, vdot, date from race")

    race_data = []
    for row in cursor:
        race_data.append((row[0], (row[1], row[2], row[3], row[4], row[5])))

    return (dict(race_data))


