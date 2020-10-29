import os, sys
from flask import Flask, render_template, redirect, request, jsonify 
import json
import mean_group_d as mg


# ----------------------
# $$$$$$$ FLASK $$$$$$$$
# ----------------------

app = Flask(__name__)  # init

@app.route("/")  # Default path
def default():
    mensaje = " <h1> API Grupo D  (GET) </h1> <p> Para obtener TOKEN    /get/token?id=</p>    Para obtener DF     /get/df/?tok= "
    return mensaje

# ----------------------
# $$$$$$$ FLASK GET $$$$$$$$
# ----------------------

@app.route('/get/token', methods=['GET'])
def token():
    if 'id' in request.args:
        group = str(request.args['id'])
    if group == "D128": 
        dnis = (55114370 * 3406313 * 51928335)
        result = "D" + str(dnis)
        return {'token': result}
    else:
        return "Error: Invalid group. El id debe ser D128" + "<br>" + "<br>" + str(request.args)

@app.route('/get/df', methods=['GET'])
def api_df():
    token_id = None
    if 'tok' in request.args:
        token_id = str(request.args['tok'])
    if token_id == 'D9748859183511168646350':           #Si el token es válido
        url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"       #obtener los datos actualizados
        country_l =["PRT", "VEN", "TUR", "GBR", "ESP"]  # lista de paises grupo D
        resp =  mg.t_d_mean (url, country_l)            # Obtener la media diaria de total_deaths para esos países
        return resp
    else:
        return "Error: Invalid Token" + "<br>" + "<br>" + str(request.args)

# ----------------------
# $$$$$$$ MAIN $$$$$$$$
# ----------------------

def main():

    print("STARTING PROCESS")
    print(os.path.dirname(__file__))
    
    # Get the settings fullpath
    settings_file = os.path.dirname(__file__) + "/settings.json"
    # Load json from file 
    with open(settings_file, "r") as json_file_readed:
        json_readed = json.load(json_file_readed)
    
    # Load variables from jsons
    SERVER_RUNNING = json_readed["server_running"]
    
    if SERVER_RUNNING:
        DEBUG = json_readed["debug"]
        HOST = json_readed["host"]
        PORT_NUM = json_readed["port"]
        app.run(debug=DEBUG, host=HOST, port=PORT_NUM)
    else:
        print("Server settings.json doesn't allow to start server. " + "Please, allow it to run it.")
            
if __name__ == "__main__":
    main()