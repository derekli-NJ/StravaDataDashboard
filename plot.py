import matplotlib.dates
import matplotlib.pyplot as plt, mpld3

from datetime import datetime


def plot(data):
    #plt.style.use('seaborn-poster') #sets the size of the charts
    plt.style.use('ggplot')
    x_axis = []
    y_axis = []

    for key in data:
        y_axis.append(data[key][2])
        datetime_obj = datetime.strptime(data[key][3], '%Y-%m-%d %H:%M:%S+00:00')
        print (type(datetime_obj))
        x_axis.append(datetime_obj)

    dates = matplotlib.dates.date2num(x_axis)

    fig = plt.figure()

    plt.xlabel("Race dates", fontsize = 20)
    plt.ylabel("VDOT Scores", fontsize = 20)
    plt.title("VDOT Score Over Time", fontsize = 25)

    plt.plot_date(dates, y_axis)



    #plt.plot([3,1,4,1,5], 'ks-', mec='w', mew=5, ms=20)
    mpld3.show()
