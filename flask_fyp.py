from flask import Flask, render_template, request, session, url_for, redirect, abort, jsonify
from werkzeug.utils import secure_filename
import time, os, csv
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
            db_control.update_1_to_user_freq(session['uid'][0]['uid'])
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
                           panel_list=db_control.get_panel_detail_by_region_limit_9())


@app.route('/quicksearch', methods=['POST'])
def quicksearch():
    if 'username' not in session:
        abort(403)

    if request.method == 'POST':
        session['region'] = request.form['region']
        session['date_from'] = request.form['date_from']
        session['date_to'] = request.form['date_to']
        session['mode'] = request.form['mode']
        session['min_price'] = request.form['min_price']
        session['max_price'] = request.form['max_price']

    return render_template('pages/quicksearch.html',
                           title='Quicksearch',
                           suitable_panel=db_control.get_all_panel_by_preference(session['region'], session['mode'], session['date_from'],
                                                                                 session['date_to'], session['min_price'], session['max_price']))


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
                               panel_other_choice=db_control.get_panel_detail_by_region_limit_3(),
                               list_all_booking=db_control.get_all_booking_of_panel(pid))


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

        prefix_path = 'C:\\\\PyCharm\\\\flask_fyp\\\\static\\\\file_source\\\\'

        f = request.files['file_path']
        session['file_path'] = f.filename
        file_path = os.path.join(prefix_path, secure_filename(f.filename))
        f.save(file_path)

        return render_template('pages/payment.html',
                               title='Payment',
                               panel_list_by_pid=db_control.get_panel_detail(pid),
                               panel_all_image=db_control.list_all_image_of_panel(pid),
                               demo_display=db_control.get_all_file_of_panel(pid, session['date_from'],
                                                                             session['date_to']))


@app.route('/simulation', methods=['POST'])
def simulation():
    pid = session['pid']
    rows = db_control.get_all_file_of_panel(pid, session['date_from'], session['date_to'])
    results = {idx: rows[idx]['file_path'] for idx in range(0, len(rows))}
    return jsonify(results)


@app.route('/confirm')
def confirm():
    db_control.insert_booking_detail_and_file_source(session['pid'], session['uid'][0]['uid'], session['date_from'],
                                                     session['date_to'], session['pid'], session['file_type'],
                                                     session['file_path'])
    db_control.update_1_to_panel_usage(session['pid'])

    return redirect(url_for('quickstart'))


@app.route('/detail')
def detail():
    if 'username' not in session:
        abort(403)

    return render_template('pages/detail.html',
                            title='Detail',
                            booking_detail=db_control.get_all_booking_detail(session['uid'][0]['uid']))


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


@app.route('/supplier')
def supplier():
    if 'username' not in session:
        abort(403)

    return render_template('pages/supplier.html',
                           title='Supplier')


@app.route('/panel_upload', methods=['POST'])
def panelupload():
    panel_name = request.form['panel_name']
    region = request.form['region']
    location = request.form['location']
    latitude = request.form['latitude']
    longitude = request.form['longitude']
    height = request.form['height']
    width = request.form['width']
    airtime_rate = request.form['airtime_rate']
    pedestrian_flow = request.form['pedestrain_flow']
    business_mode = request.form['mode']

    if business_mode == 'sole':
        cap = 1
    elif business_mode == '1-5':
        cap = 5
    else:
        cap = 10

    f1 = request.files['file_path_1']
    f2 = request.files['file_path_2']

    prefix_path = 'C:\\\\PyCharm\\\\flask_fyp\\\\static\\\\img\\\\'

    session['file_path_1'] = f1.filename
    session['file_path_2'] = f2.filename

    file_path_1 = os.path.join(prefix_path, secure_filename(f1.filename))
    file_path_2 = os.path.join(prefix_path, secure_filename(f2.filename))

    f1.save(file_path_1)
    f2.save(file_path_2)

    db_control.insert_panel_detail(panel_name, region, location, latitude, longitude, height, width, airtime_rate,
                                   pedestrian_flow, business_mode, cap, session['file_path_1'], session['file_path_2'])

    return redirect(url_for('quickstart'))


@app.route('/csv')
def csv_upload():

    return render_template('pages/csv.html',
                           title='CSV Upload')


@app.route('/readcsv', methods=['POST'])
def read_csv():
    f = request.files['csv']

    prefix_path = 'C:\\\\PyCharm\\\\flask_fyp\\\\static\\\\csv\\\\'

    session['csv'] = f.filename
    file_path = os.path.join(prefix_path, secure_filename(f.filename))
    f.save(file_path)

    with open(file_path, 'rb') as inFile:
        reader = csv.reader(inFile)
        for row in reader:
            db_control.insert_panel_detail((",".join(row)))

    return redirect(url_for('quickstart'))


if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run()
