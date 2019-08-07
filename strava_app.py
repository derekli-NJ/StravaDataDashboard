from flask import Flask, render_template, json, request
import json
from threading import Lock
import strava_data

lock = Lock()

app = Flask(__name__)


def draw_fig(fig_type):
    """Returns html equivalent of matplotlib figure
    Parameters
    ----------
    fig_type: string, type of figure
    Returns
    --------
    d3 representation of figure
    """

    with lock:
        data = strava_data.setup()
        if fig_type == "hr_per_mile":
            return strava_data.plot_beats_per_mile_fig(data[fig_type])
        elif fig_type == "vdot_race":
            return strava_data.plot_vdot_race_fig(data[fig_type])
        else:
            raise 


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/query', methods = ['POST'])
def query():
    data = json.loads(request.data)
    return draw_fig(data["plot_type"])

if __name__ == '__main__':
    app.run(debug = True, host = 'localhost', port = 8000)
