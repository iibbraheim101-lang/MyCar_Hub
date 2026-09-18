from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# الاتصال بقاعدة البيانات
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# إنشاء الجدول لو ماهو موجود
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            car_model TEXT NOT NULL,
            plate_number TEXT NOT NULL,
            mileage INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# تشغيل إنشاء الجدول أول ما يشتغل البرنامج
init_db()

@app.route('/')
def home():
    conn = get_db_connection()
    cars = conn.execute('SELECT * FROM cars').fetchall()
    conn.close()
    return render_template('index.html', cars=cars)

@app.route('/add', methods=('POST',))
def add_car():
    car_model = request.form['car_model']
    plate_number = request.form['plate_number']
    mileage = request.form['mileage']
    
    conn = get_db_connection()
    conn.execute('INSERT INTO cars (car_model, plate_number, mileage) VALUES (?, ?, ?)',
                 (car_model, plate_number, mileage))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)