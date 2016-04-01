from flask import Flask, render_template
from database import db_connect
from database import db_control


app = Flask(__name__)


@app.route('/')
def quickstart():
    return render_template('pages/quickstart.html',
                           title='Quickstart',
                           )

@app.route('/quicksearch')
def quicksearch():
    return render_template('pages/quicksearch.html',
                           title='Quicksearch')

@app.route('/location')
def location():
    return render_template('pages/location.html',
                           title='Location')

@app.route('/booking')
def booking():
    return render_template('pages/booking.html',
                           title='Booking')

@app.route('/payment')
def payment():
    return render_template('pages/payment.html',
                           title='Payment')

@app.route('/detail')
def detail():
    return render_template('pages/detail.html',
                           title='Detail')

@app.route('/login')
def login():
    return render_template('pages/login.html',
                           title='Login')

@app.route('/register')
def register():
    return render_template('pages/register.html',
                           title='Register')

@app.route('/profile')
def profile():
    return render_template('pages/profile.html',
                           title='Profile')


if __name__ == '__main__':
    app.debug = True
    app.run()
