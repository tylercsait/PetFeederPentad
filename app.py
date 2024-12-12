from flask import Flask, request, jsonify, render_template, redirect, url_for
import db_utils
from registerpets import process_pet_input

app = Flask(__name__)

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
    with db_utils.mysql_connection() as (cursor, connection):
        cursor.execute("SELECT rfid, rfid_text, max_feedings_day, max_portions_day, portions_per_feeding FROM pets")
        pets = cursor.fetchall()
        pets = [dict(rfid=row[0], rfid_text=row[1], max_feedings_day=row[2], max_portions_day=row[3], portions_per_feeding=row[4]) for row in pets]
    return render_template('view_pets.html', pets=pets)

@app.route('/delete-pet/<rfid>', methods=['POST'])
def delete_pet(rfid):
    with db_utils.mysql_connection() as (cursor, connection):
        db_utils.delete_pet_by_rfid(cursor,rfid)
        connection.commit()
    return redirect(url_for('view_pets'))

@app.route('/view-history/<rfid>')
def view_history(rfid):
    with db_utils.mysql_connection() as (cursor, connection):
        cursor.execute(
            "SELECT date, last_time_fed, feedings_today, portions_eaten_today, leftover_portions FROM history WHERE rfid = %s",
            (rfid,))
        history = cursor.fetchall()
        history = [dict(date=row[0], last_time_fed=row[1], feedings_today=row[2], portions_eaten_today=row[3],
                        leftover_portions=row[4]) for row in history]

        cursor.execute("SELECT rfid_text FROM pets WHERE rfid = %s", (rfid,))
        pet_name_row = cursor.fetchone()
        pet_name = pet_name_row[0] if pet_name_row else "Unknown Pet"

    last_time_fed = history[-1]['last_time_fed'] if history else "N/A"
    date = history[-1]['date'] if history else "N/A"
    return render_template('view_history.html', rfid=rfid, history=history, last_time_fed=last_time_fed, date=date,
                           pet_name=pet_name)


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

    with db_utils.mysql_connection() as (cursor, connection):
        if not db_utils.check_pet_exists(cursor, rfid, "pets"):
            db_utils.add_pet(cursor, rfid, rfid_text, max_feedings_day, max_portions_day, portions_per_feeding)
        else:
            print("pet already exists")

    return jsonify({"message": "Pet information submitted successfully!"})

# Route for the Contact Us page
@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
