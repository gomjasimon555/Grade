from flask import Flask, jsonify, request,send_file
from flask_pymongo import PyMongo
from flask_cors import CORS  # Import CORS
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Configure MongoDB URI
app.config['MONGO_URI'] = 'mongodb://localhost:27017/gradepredictionsystem'

# Initialize PyMongo
mongo = PyMongo(app)

# Configure CORS before creating the app instance
CORS(app)

loaded_random_forest_model = pickle.load(open("models/random_forest_model.pkl", "rb"))
loaded_decision_tree_model = pickle.load(open("models/decision_tree_model.pkl", "rb"))

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/get', methods=['GET'])
def get_documents():
    # Retrieve data from a collection
    documents = list(mongo.db.collection_name.find())
    return jsonify({'documents': documents})


@app.route('/viewgrade', methods=['POST'])
def view_details():
    entered_data = request.get_json()
    print("entered_data:", entered_data)

    grade = mongo.db.details.find_one({'name': entered_data['name'], 'symbol': entered_data['symbol']})

    if grade:
        grade['_id'] = str(grade['_id'])
        return jsonify(grade)
    else:
        # Invalid credentials
        return jsonify({'message': 'Invalid name or symbol'}), 401



@app.route('/adddetails', methods=['POST'])
def add_details():
    entered_data = request.get_json()
    print("entered_data:", entered_data)
    name = entered_data['name']
    symbol=entered_data['symbol']
    assignment=entered_data['assignment']
    attendance=entered_data['attendance']
    firstterm=entered_data['firstterm']
    secondterm=entered_data['secondterm']
    # Assuming you have new data in the same format as your training data
    new_data = pd.DataFrame(np.array([assignment, attendance, firstterm, secondterm]).reshape(1,-1),
                            columns=['Assignment', 'Attendance', 'first_term', 'second_term'])
    

    
    # Make predictions on the new data
    predicted_class_from_random_forest_model = loaded_random_forest_model.predict(new_data)
    predicted_class_from_decision_tree_model = loaded_decision_tree_model.predict(new_data)

    # Define the Encoded_class DataFrame to map class labels to grades
    Encoded_class = pd.DataFrame({'Grade': ["A", "A+", "B", "B+", "C", "C+", "D", "D+", "E", "F"],
                                'Encoded': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]})

    # Map the predicted class to its corresponding grade using the Encoded_class DataFrame
    predicted_grade_from_random_forest_model = Encoded_class[Encoded_class["Encoded"] == predicted_class_from_random_forest_model[0]]["Grade"].item()
    predicted_grade_from_decision_tree_model = Encoded_class[Encoded_class["Encoded"] == predicted_class_from_decision_tree_model[0]]["Grade"].item()

    print(f"Predicted Grade From Random Forest : {predicted_grade_from_random_forest_model}")
    print(f"Predicted Grade From Decision Tree : {predicted_grade_from_decision_tree_model}")

    entered_data['predicted_grade_from_random_forest_model'] = predicted_grade_from_random_forest_model
    entered_data['predicted_grade_from_decision_tree_model'] = predicted_grade_from_decision_tree_model

    full_marks = 400;
    assignment_actual = float(entered_data['assignment'])
    attendance_actual = float(entered_data['attendance'])
    firstterm_actual = float(entered_data['firstterm'])
    secondterm_actual = float(entered_data['secondterm'])

    obtained_marks = assignment_actual+ attendance_actual +firstterm_actual + secondterm_actual;
    average_marks = obtained_marks/full_marks;
    entered_data['average_marks'] = average_marks


    # Mapping of grade ranges to actual grades
    grade_mapping = {
        (0.9, 1.01): 'A+',
        (0.8, 0.9): 'A',
        (0.7, 0.8): 'B+',
        (0.6, 0.7): 'B',
        (0.5, 0.6): 'C+',
        (0.4, 0.5): 'C',
        (0.3, 0.4): 'D+',
        (0.2, 0.3): 'D',
        (0.1, 0.2): 'E',
        (0.0, 0.1): 'F'
    }

    # Initialize grade as None
    grade = None

    # Map average_marks to grades
    for range_, g in grade_mapping.items():
        if range_[0] <= average_marks < range_[1]:
            grade = g
            break
    entered_data['actual_grade'] = grade
    print("Obtained Grade:",grade)
    print("Obtained Average Mark:",average_marks)


    # Insert data into a collection
    mongo.db.details.insert_one(entered_data)
    return jsonify({'message': 'Data added successful'})
  

@app.route('/signup', methods=['POST'])
def signup():
    data = {
        'email': 'admin@gmail.com',
        'password': 'admin@gmail.com'
    }
    # Insert data into a collection
    mongo.db.admin.insert_one(data)
    return jsonify({'message': 'Signup successful'})

@app.route('/login', methods=['POST'])
def login():
    # Get the login credentials from the request
    login_data = request.get_json()
    print("login_data:", login_data)

    # Find the user in the collection
    user = mongo.db.admin.find_one({'email': login_data['email'], 'password': login_data['password']})

    if user:
        # Successful login
        return jsonify({'message': 'Login successful'})
    else:
        # Invalid credentials
        return jsonify({'message': 'Invalid email or password'}), 401


@app.route('/generate_plot', methods=['GET'])
def generate_plot():
    # Generate the plot using matplotlib
    plt.plot([1, 2, 3], [4, 5, 6])  # Example plot data

    # Save the plot image to a BytesIO object
    image_stream = io.BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)

    # Encode the image as base64
    encoded_image = base64.b64encode(image_stream.read()).decode('utf-8')

    # Return the base64 encoded image as JSON response
    return jsonify({'image': encoded_image})


if __name__ == '__main__':
    app.run(debug=True)
