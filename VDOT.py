import openpyxl
from units import unit
import units.predefined


def enter_data(athlete_info, race_data):
    srcfile = openpyxl.load_workbook('test.xlsm',read_only=False, keep_vba= True)#to open the excel sheet and if it has macros

    sheetname = srcfile.get_sheet_by_name('Daniels Tables')#get sheetname from the file

    print ("Hi " + str(athlete_info.firstname) + " thanks for choosing our service!")


    if (athlete_info.sex == "M"):
        print ("Adding height into correct place")
        sheetname['C2'] = "72" # My height hardcoded (could have user enter it)
    elif (athlete_info.sex == "F"):
        sheetname['C2'] = "64" #Average Female Height
    else:
        sheetname['C2'] = "69" # Assume is a man if no sex listed

    if (athlete_info.dateofbirth != None):
        sheetname['E2'] = athlete_info.dateofbirth # Birthdate
    else:
        print ("Prompt user for birthdate")

    if (athlete_info.weight != None): 
        sheetname['C3'] = athlete_info.weight # Weight
    else:
        print ("Prompt user for weight")

    if (athlete_info.max_heartrate != None):
        sheetname['E3'] = athlete_info.max_heartrate# HRmax
    else:
        print ("Prompt user for heart rate max")


    meter = unit('m')


    race_distances = { "5k" : meter(5000), "8k" : meter(8000), "10k" : meter(10000), "12k" : meter(12000), "15k" : meter(15000), "1/2 Mar" : meter(21097.5), "Marathon" : meter(42195)}
    
    filled_distance = False
    for race in race_distances:
        if (abs(race_distances[race] - race_data[0].distance) < 0.1 * race_distances[race]):   
            sheetname['E6'] = race #Enter distance (need to edit S5 if Custom)
            filled_distance = True
    if (not filled_distance):
        sheetname['E6'] = "Custom" 
        sheetname['S5'] = race_data[0].distance
    

    sheetname['G6'] = str('3:25:24') #Edits the race time

    sheetname.cell(row=20,column=22).value = "something" #write to row 1,col 1 explicitly, this type of writing is useful to write something in loops

    srcfile.save('test.xlsm')#save it as a new file, the original file is untouched and here I am saving it as xlsm(m here denotes macros).


def read_vdot():
    print ("Filler")#Read from I/J 6 to get VDOT score
