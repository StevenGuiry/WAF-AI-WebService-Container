from crypt import methods
from flask import Flask, request, render_template
#from flask_cors import CORS
import numpy as np
import pickle
import logging
import json

logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

model = None

def create_app():
    app = Flask(__name__)
    #CORS(app)

    with open('xgb_model.pkl', 'rb') as f:
        model = pickle.load(f)


    @app.route("/")
    def index():
        return render_template('WAF-AI.html')

    @app.route('/predict', methods=['POST'])
    def get_prediction():
        if request.method == 'POST':
            data = request.get_json()
            data = json.dumps(data)
            single_q = data.count("'")
            double_q = data.count("\"")
            slash = data.count("/")
            dot = data.count(".")
            if single_q == 0 & double_q > 2:
                no_quote = 1
            else:
                no_quote = 0
            data = [single_q, dot, slash, no_quote]
            app.logger.info(str(data))
            data = np.array(data)[np.newaxis, :]
            prediction = model.predict(data)
        if prediction[0] == 0:
            return "Good"
        else:
            return "Bad"
    
    return app

    #     @app.route('/predict', methods=['POST'])
    # def get_prediction():
    #     if request.method == 'POST':
    #         data = request.get_json()
    #         data = np.array(data)[np.newaxis, :]
    #         prediction = model.predict(data)
    #     return str(prediction[0])