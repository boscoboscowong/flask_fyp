from flask import Flask, render_template, request, session, url_for, redirect, abort
from werkzeug.utils import secure_filename
import os
import time
from database import db_connect
from database import db_control


app = Flask(__name__)


@app.route('/')
def login():
    return render_template('pages/login.html',
                           title='Login')


@app.route('/checking', methods=['POST'])
def check():
    if request.method == 'POST':
        username_form = request.form['username']
        pwd_form = request.form['pwd']
        row = db_control.check_user_login(username_form, pwd_form)

        if row['num'] == 1:
            session['username'] = request.form['username']
            session['uid'] = db_control.get_user_uid(session['username'])
            return redirect(url_for('quickstart'))

    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/quickstart')
def quickstart():
    if 'username' not in session:
        abort(403)

    return render_template('pages/quickstart.html',
                           title='Quickstart',
                           panel_list=db_control.get_panel_detail_by_region())


@app.route('/quicksearch')
def quicksearch():
    if 'username' not in session:
        abort(403)

    return render_template('pages/quicksearch.html',
                           title='Quicksearch')


@app.route('/location')
def location():
    if 'username' not in session:
        abort(403)

    return render_template('pages/location.html',
                           title='Location',
                           panel_list=db_control.get_panel_detail_by_region())


@app.route('/booking', methods=['GET'])
def booking():
    if 'username' not in session:
        abort(403)

    if request.method == 'GET':
        pid = request.args.get('pid')
        return render_template('pages/booking.html',
                               title='Booking',
                               pid=pid,
                               panel_list_by_pid=db_control.get_panel_detail(pid),
                               panel_all_image=db_control.list_all_image_of_panel(pid),
                               panel_other_choice=db_control.get_panel_detail_by_region())


@app.route('/payment', methods=['POST'])
def payment():
    if 'username' not in session:
        abort(403)

    if request.method == 'POST':
        pid = request.form['pid']
        session['pid'] = pid
        session['date_from'] = request.form['date_from']
        session['date_to'] = request.form['date_to']
        session['file_type'] = request.form['file_type']

        prefix_path = 'C:\\PyCharm\\flask_fyp\\static\\file_source'

        f = request.files['file']
        file_path = os.path.join(prefix_path, secure_filename(f.filename))
        session['file_path'] = f.save(file_path)


        return render_template('pages/payment.html',
                               title='Payment',
                               panel_list_by_pid=db_control.get_panel_detail(pid),
                               panel_all_image=db_control.list_all_image_of_panel(pid))

@app.route('/confirm')
def confirm():
    db_control.insert_booking_detail(session['pid'], session['uid'], session['date_from'], session['date_to'])
    session['bid'] = db_control.get_booking_bid(session['pid'], session['uid'][0]['uid'])
    db_control.insert_file_source(session['bid'], session['file_type'], session['file_path'])
    return redirect(url_for('quickstart'))

@app.route('/detail')
def detail():
    if 'username' not in session:
        abort(403)

    return render_template('pages/detail.html',
                           title='Detail')


@app.route('/register')
def register():
    return render_template('pages/register.html',
                           title='Register')


@app.route('/doregister', methods=['POST'])
def do_register():
    if request.method == 'POST':
        db_control.insert_a_row_to_login_table(request.form['username'], request.form['pwd'],
                                               request.form['company_name'], request.form['email'],
                                               request.form['tel'])
        return redirect(url_for('success_register'))


@app.route('/success_register')
def success_register():
    time.sleep(2)
    return redirect(url_for('login'))


@app.route('/profile')
def profile():
    if 'username' not in session:
        abort(403)

    return render_template('pages/profile.html',
                           title='Profile',
                           user_profile=db_control.get_user_detail(session['username']))


if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run()
