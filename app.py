from flask import Flask, request, render_template, redirect, url_for
import db_utils

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('test.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        rfid = request.form['rfid']
        rfid_text = request.form['rfid_text']
        max_feedings_day = int(request.form['max_feedings_day'])
        max_portions_day = int(request.form['max_portions_day'])
        portions_per_feeding = int(request.form['portions_per_feeding'])

        # Insert into MySQL database
        with db_utils.mysql_connection() as cursor:
            db_utils.add_pet(cursor, rfid, rfid_text, max_feedings_day, max_portions_day, portions_per_feeding)

        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
