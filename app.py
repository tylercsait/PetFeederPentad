from flask import Flask, request, jsonify, render_template, redirect, url_for
import db_utils
from registerpets import process_pet_input

app = Flask(__name__)

# Route for the SmartFeeder page
@app.route('/register')
def register():
    return render_template('register.html')

# Default route for the directory page (now index.html)
@app.route('/')
def index():
    return render_template('index.html')

# Route for another page
@app.route('/another-page')
def another_page():
    return render_template('another_page.html')

@app.route('/api/pets', methods=['POST'])
def api_pets():
    data = request.json
    rfid = data['rfid']
    rfid_text = data['rfid_text']
    max_feedings_day = int(data['max_feedings_day'])
    portions_per_feeding = int(data['portions_per_feeding'])
    max_portions_day = max_feedings_day * portions_per_feeding

    with db_utils.mysql_connection() as cursor:
        if not db_utils.check_pet_exists(cursor, rfid, "pets"):
            db_utils.add_pet(cursor, rfid, rfid_text, max_feedings_day, max_portions_day, portions_per_feeding)
        else:
            print("pet already exists")

    return jsonify({"message": "Pet information submitted successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
