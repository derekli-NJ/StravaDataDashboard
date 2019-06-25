import openpyxl


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

    print (athlete_info.weight, athlete_info.max_heartrate)
    sheetname['C3'] # Weight
    sheetname['E3'] # HRmax



    sheetname['G6'] = str('3:25:24') #Edits the race time
    sheetname['E6'] #Enter distance (need to edit S5 if Custom)

    sheetname.cell(row=20,column=22).value = "something" #write to row 1,col 1 explicitly, this type of writing is useful to write something in loops

    srcfile.save('test.xlsm')#save it as a new file, the original file is untouched and here I am saving it as xlsm(m here denotes macros).


def read_vdot():
    print ("Filler")#Read from I/J 6 to get VDOT score
