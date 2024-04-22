from flask import Flask, request, render_template
import pickle
import sklearn

# Check scikit-learn version
if sklearn.__version__ >= "0.22.0":
    from sklearn.ensemble import RandomForestRegressor
else:
    from sklearn.ensemble import RandomForest

app = Flask(__name__)  # initializing flask app

# Load the model
with open('model', 'rb') as model_file:
    model = pickle.load(model_file)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/', methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':
        present_price = float(request.form['price'])
        car_age = int(request.form['age'])
        seller_type = request.form['seller']
        fuel_type = request.form['fuel']
        transmission_type = request.form['transmission']

        if fuel_type == 'Diesel':
            fuel_type = 1
        else:
            fuel_type = 0

        if seller_type == 'Individual':
            seller_type = 1
        else:
            seller_type = 0

        if transmission_type == 'Manual':
            transmission_type = 1
        else:
            transmission_type = 0

        prediction = model.predict([[present_price, car_age, fuel_type, seller_type, transmission_type]])
        output = round(prediction[0], 2)

        return render_template('index.html', output="{} Lakh".format(output))

if __name__ == '__main__':
    app.run(debug=True)
