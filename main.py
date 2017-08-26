from flask import Flask, render_template
from flask_restful import Resource, Api, reqparse
from flask_api import status

from edge_util_api import EdgeUtilApi
from edge_config_api import EdgeConfigApi
import sys

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fogos'
api = Api(app)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# List of REST APIs
api.add_resource(EdgeUtilApi, '/qos_interpreter.json')
api.add_resource(EdgeConfigApi, '/join.json')

if __name__ == '__main__':
    if(len(sys.argv) == 1):
        app.run(debug=True, host='0.0.0.0', port=9090)
    else:
        try:
            server_port = int(sys.argv[1])
            app.run(debug=True, host='0.0.0.0', port=server_port)
        except:
            print('[Error] Invalid port number! Pleack check the port number you typed: ', sys.argv[1])

