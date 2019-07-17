import matplotlib.dates
import matplotlib.pyplot as plt, mpld3
from mpldatacursor import datacursor
from mpld3 import plugins

from datetime import datetime


def plot(data):
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
  display: block;
  background-color: #ffffff;
}
"""
    #plt.style.use('seaborn-poster') #sets the size of the charts
    plt.style.use('ggplot')
    x_axis = []
    y_axis = []


    label = []

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

    mpld3.show()





