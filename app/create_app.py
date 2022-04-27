from crypt import methods
from flask import Flask, request, render_template
#from flask_cors import CORS
import numpy as np
import pickle

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
            data = np.array(data)[np.newaxis, :]
            prediction = model.predict(data)
        return str(prediction[0])
    
    return app