from flask import Flask, request, make_response, jsonify
from functools import wraps
import datetime
#import time
from sense_hat import SenseHat

sense = SenseHat()


app = Flask(__name__)

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == 'pi5climate' and auth.password == 'xT75k?8GhAj#':
            return f(*args, **kwargs)
        return make_response('Could not verify your login!', 401, {'WWW-Authenticate': 'BASIC realm="Login required"'})
    return decorated

@app.route('/')
@auth_required
def index():
    return '<h1>You are logged in on index</h1>'

@app.route('/page')
@auth_required
def page():
    return '<h1>You are logged in on page</h1>'

@app.route('/climate', methods=['GET'])
@auth_required
def get_climate():
    sHumidity = str(sense.get_humidity())
    rHumidity = sHumidity[0:2]
    print("Fuktigheten är: ",rHumidity, "% relativ fuktighet")

    sPressure = str(sense.get_pressure())
    rPressure = sPressure[0:4]
    print("Trycket är: ", rPressure, "millibar")

    sTemp = str(sense.get_temperature())
    rTemp = sTemp[0:4]
    print("Temperaturen är: ",rTemp," grader")

    dt=datetime.datetime.now()

    d = dt.date()
    sD = str(d)
    print(sD)

    t = dt.time()
    sTimeLong = str(t)
    sT = sTimeLong[0:8]
    print(sT)

#    climatSensors = {"id": 1, "Datum": sD }, {"id": 2, "Tid": sT},{"id": 3, "Temperatur": rTemp }, {"id": 4, "Lufttryck": rPressure},{"id": 5, "Fuktighet": rHumidity }

#    return jsonify({'Klimat Sensors': climatSensors})
#    return jsonify(climatSensors)
    return jsonify({"id": 1, "Datum": sD }, {"id": 2, "Tid": sT},{"id": 3, "Temperatur": rTemp }, {"id": 4, "Lufttryck": rPressure},{"id": 5, "Fuktighet": rHumidity })


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5008,debug=True)

