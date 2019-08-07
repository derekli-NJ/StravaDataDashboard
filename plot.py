import matplotlib.dates
import matplotlib.pyplot as plt, mpld3
import matplotlib.ticker as ticker
from mpldatacursor import datacursor
from mpld3 import plugins
import numpy as np
from numpy.polynomial.polynomial import polyfit

from datetime import datetime


def plot_vdot_race(data):
    #CSS element for the tooltip label
    css = """
div
{
  font-family: Avenir, Helvetica, sans-serif;
  border: 1px solid black;
  padding-left: 5px;
  padding-right: 5px;
  text-align: center;
  color: #000000;
  background-color: #ffffff;
}
"""
    #plt.style.use('seaborn-poster') #sets the size of the charts
    plt.style.use('ggplot')
    x_axis = []
    y_axis = []


    label = []
    #print (data)
    for key in data:
        label.append("Race: " + str(data[key][1]) + "<br/>" + "VDOT: " + str(data[key][3]))

        y_axis.append(data[key][3])
        datetime_obj = datetime.strptime(data[key][4], '%Y-%m-%d %H:%M:%S+00:00')
        x_axis.append(datetime_obj)

    dates = matplotlib.dates.date2num(x_axis)

    fig, ax = plt.subplots()

    plt.xlabel("Race dates", fontsize = 20)
    plt.ylabel("VDOT Scores", fontsize = 20)
    plt.title("VDOT Score Over Time", fontsize = 25)

    line = plt.plot_date(dates, y_axis, linestyle = 'solid', marker = '.', markersize = 14)

    plugins.clear(fig)  # clear all plugins from the figure 

    tooltip = plugins.PointHTMLTooltip(line[0], label, 
                                       hoffset = -60, voffset = -70, css = css)

    plugins.connect(fig, plugins.Reset(), plugins.BoxZoom(), plugins.Zoom(), tooltip)

    return mpld3.fig_to_html(fig)

def plot_beats_per_mile(data):
    #divide meters by this factor to get in terms of miles
    convert_meters_to_miles = 1609.344

    #plt.style.use('seaborn-poster') #sets the size of the charts
    plt.style.use('ggplot')
    
    #Data is dictionary mapping id to (activity_name, start_date_local, average_hr, distance, total_elevation_gain)

    data_by_week = {}

    for key in data:
        datetime_obj = datetime.strptime(data[key][1], '%Y-%m-%d %H:%M:%S')
        year_week_val = datetime_obj.isocalendar()[:-1]

        if year_week_val not in data_by_week:
            #Storing average_hr, distance, total_elevation_gain
            data_by_week[year_week_val] = [(data[key][2], data[key][3], data[key][4])]
        else:
            data_by_week[year_week_val].append((data[key][2], data[key][3], data[key][4]))

    x_axis = []
    x_label = []
    y_axis = []
    for key in data_by_week:
        print (key)
        total_hr_each_week = 0
        distance_week = 0
        for activity in data_by_week[key]:
            total_hr_each_week += activity[0] * (activity[1] / convert_meters_to_miles)
            distance_week += activity[1] / convert_meters_to_miles
        avg_hr_per_mile = total_hr_each_week / distance_week

        x_label.append(str(key[0]) + "-" + str(key[1]))
        x_axis.append(key[0] * 52 + key[1])
        y_axis.append(avg_hr_per_mile)
        total_hr_each_week = 0
        distance_week = 0
    

    fig, ax = plt.subplots()

    plt.xlabel("Weeks", fontsize = 20)
    plt.ylabel("Average Heartrate Per Mile", fontsize = 20)
    plt.title("Average Heartrate Per Mile Sorted by Week", fontsize = 25)

    line = plt.plot(x_axis, y_axis, linestyle = 'solid', marker = '.', markersize = 14)

    x = np.asarray(x_axis)
    y = np.asarray(y_axis)

    b, m = polyfit(x, y, 1)
    #Plots regression line
    plt.plot(x, b + m * x, linestyle = 'solid')


    plugins.clear(fig)  # clear all plugins from the figure 

    #tooltip = plugins.PointHTMLTooltip(line[0], label, 
                                       #hoffset = -60, voffset = -70, css = css)

    plugins.connect(fig, plugins.Reset(), plugins.BoxZoom(), plugins.Zoom())

    return mpld3.fig_to_html(fig)

