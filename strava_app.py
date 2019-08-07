from flask import Flask, render_template, json, request, redirect, url_for, jsonify
from threading import Lock
import strava_data, config, json
from stravalib import Client


lock = Lock()

app = Flask(__name__)
app.config.from_envvar('APP_SETTINGS')

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
def login():
    c = Client()
    url = c.authorization_url(client_id=app.config['STRAVA_CLIENT_ID'],
                              redirect_uri=url_for('.logged_in', _external=True),
                              approval_prompt='auto')
    return render_template('login.html', authorize_url = url)

@app.route("/strava-oauth")
def logged_in():
    """
    Method called by Strava (redirect) that includes parameters.
    - state
    - code
    - error
    """
    error = request.args.get('error')
    state = request.args.get('state')
    if error:
        return render_template('login_error.html', error=error)
    else:
        code = request.args.get('code')
        client = Client()
        access_token = client.exchange_code_for_token(client_id=app.config['STRAVA_CLIENT_ID'],
                                                      client_secret=app.config['STRAVA_CLIENT_SECRET'],
                                                      code=code)
        print (config.access_token)
        config.access_token = access_token['access_token']
        config.refresh_token = access_token['refresh_token']
        config.expires_at = access_token['expires_at']
        print ("HERE")
        print (access_token)
        print (config.access_token)
        # Probably here you'd want to store this somewhere -- e.g. in a database.
        strava_athlete = client.get_athlete()

        return render_template('index.html')


@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/query', methods = ['POST'])
def query():
    data = json.loads(request.data)
    return draw_fig(data["plot_type"])

if __name__ == '__main__':
    app.run(debug = True, host = 'localhost', port = 8000)
