from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
import db_utils
from registerpets import process_pet_input

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Route for the register pets page
@app.route('/register')
def register():
    return render_template('register.html')

# Default route for the directory page (index.html)
@app.route('/')
def index():
    return render_template('index.html')

# Route for viewing all registered pets
@app.route('/view-pets')
def view_pets():
    with db_utils.mysql_connection() as cursor:
        cursor.execute("SELECT rfid, rfid_text, max_feedings_day, max_portions_day, portions_per_feeding FROM pets")
        pets = cursor.fetchall()
        pets = [dict(rfid=row[0], rfid_text=row[1], max_feedings_day=row[2], max_portions_day=row[3], portions_per_feeding=row[4]) for row in pets]
    return render_template('view_pets.html', pets=pets)

# Route for viewing history of a pet by RFID
@app.route('/view-history/<rfid>')
def view_history(rfid):
    with db_utils.mysql_connection() as cursor:
        cursor.execute("SELECT date, last_time_fed, feedings_today, portions_eaten_today, leftover_portions FROM history WHERE rfid = %s", (rfid,))
        history = cursor.fetchall()
        history = [dict(date=row[0], last_time_fed=row[1], feedings_today=row[2], portions_eaten_today=row[3], leftover_portions=row[4]) for row in history]
    return render_template('view_history.html', rfid=rfid, history=history)

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
            socketio.emit('new_pet', {'message': f'New pet registered: {rfid_text}'}, namespace='/notifications')
        else:
            print("Pet already exists")

    return jsonify({"message": "Pet information submitted successfully!"})

@socketio.on('connect', namespace='/notifications')
def connect():
    print("Client connected")

@socketio.on('disconnect', namespace='/notifications')
def disconnect():
    print("Client disconnected")

def send_notification(message):
    with app.app_context():
        print(f'Sending notification: {message}')
        socketio.emit('notify', {'message': message}, namespace='/notifications')
        print("Notification emitted")  # Log after emitting

if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)