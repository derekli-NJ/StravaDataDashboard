import sqlite3

def create_database(vdot_data):
    sql_create_race_table= """ CREATE TABLE IF NOT EXISTS race(
                                         id integer PRIMARY KEY,
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
        sql_formatted_data.append((key, vdot_data[key][1]['entered']['distance'], vdot_data[key][1]['entered']['time'], vdot_data[key][1]['vdot'], str(vdot_data[key][0].start_date)))

    cursor.executemany('''INSERT INTO race(id, distance, time, vdot, date) VALUES(?, ?, ?, ?, ?)''', sql_formatted_data)

    connection.commit()
    connection.close()

