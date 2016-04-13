from database import db_connect
from database_class.panel import Panel
from database_class.panel_source import Panel_source
from database_class.user import User


"""check user login in login.html"""
def check_user_login(username, pwd):
    select_query = "SELECT COUNT(*) as num FROM login " \
                   "WHERE username= '{}'" \
                   "AND pwd='{}'".format(username, pwd)

    return db_connect.verify_user_login(select_query)


"""user uid in login.html"""
def get_user_uid(username):
    select_query = "SELECT login.uid FROM login " \
                   "WHERE username='{}'".format(username)

    return db_connect.execute_select(select_query)


"""upload register data in register.html"""
def insert_a_row_to_login_table(username, pwd, company_name, email, tel):
    insert_query = "INSERT INTO login (username, pwd, company_name, email, tel) " \
                   "VALUE ('{}', '{}', '{}', '{}', '{}');" \
                   "INSERT INTO user_freq(uid, freq) " \
                   "VALUES(LAST_INSERT_ID(), 0)".format(username, pwd, company_name, email, tel)

    return db_connect.execute_insert(insert_query)


"""user detail in profile.html"""
def get_user_detail(username):
    select_query = "SELECT login.*, user_freq.freq FROM login " \
                   "INNER JOIN user_freq ON login.uid=user_freq.uid " \
                   "WHERE login.username='{}'".format(username)

    user_list = []
    for row in db_connect.execute_select(select_query):
        user_list.append(User(row['uid'], row['username'], row['pwd'], row['company_name'],
                              row['email'], row['tel'], row['freq']))

    return user_list


"""panel detail in location.html"""
def get_panel_detail_by_region():
    select_query = "SELECT panel.*, panel_source.*, panel_usage.used FROM panel " \
                   "INNER JOIN panel_source ON panel_source.pid=panel.pid " \
                   "INNER JOIN panel_usage ON panel_usage.pid=panel.pid " \
                   "WHERE panel_source.img_no='1'" \
                   "ORDER BY panel.region"

    panel_list = []
    for row in db_connect.execute_select(select_query):
        panel_list.append(Panel(row['pid'], row['name'], row['region'],
                                row['location'], row['latitude'], row['longitude'],
                                row['height'], row['width'], row['airtime_rate'],
                                row['pedestrain_flow'], row['mode'], row['cap'], row['img_no'],
                                row['panel_path'], row['used']))

    return panel_list


"""panel detail in booking.html"""
def get_panel_detail(pid):
    select_query = "SELECT panel.*, panel_source.*, panel_usage.used FROM panel " \
                   "INNER JOIN panel_source ON panel_source.pid=panel.pid " \
                   "INNER JOIN panel_usage ON panel_usage.pid=panel.pid " \
                   "WHERE panel_source.img_no='1'" \
                   "AND panel.pid='{}'".format(pid)

    panel_list = []
    for row in db_connect.execute_select(select_query):
        panel_list.append(Panel(row['pid'], row['name'], row['region'],
                                row['location'], row['latitude'], row['longitude'],
                                row['height'], row['width'], row['airtime_rate'],
                                row['pedestrain_flow'], row['mode'], row['cap'], row['img_no'],
                                row['panel_path'], row['used']))

    return panel_list


"""list all image of a panel in booking.html"""
def list_all_image_of_panel(pid):
    select_query = "SELECT panel_source.* FROM panel_source WHERE panel_source.pid = '{}'".format(pid)

    panel_list = []
    for row in db_connect.execute_select(select_query):
        panel_list.append(Panel_source(row['sid'], row['pid'], row['img_no'], row['panel_path']))

    return panel_list


"""list all booking of selected panel in booking.html"""
def get_all_booking_of_panel(pid):
    select_query = "SELECT booking.*, login.company_name FROM login " \
                   "INNER JOIN booking ON booking.uid=login.uid " \
                   "WHERE booking.pid='{}' " \
                   "ORDER BY booking.date_from".format(pid)

    return db_connect.execute_select(select_query)


"""only show 3 panel detail in quickstart.html"""
def get_panel_detail_by_region_limit_3():
    select_query = "SELECT panel.*, panel_source.*, panel_usage.used FROM panel " \
                   "INNER JOIN panel_source ON panel_source.pid=panel.pid " \
                   "INNER JOIN panel_usage ON panel_usage.pid=panel.pid " \
                   "WHERE panel_source.img_no='1'" \
                   "ORDER BY panel.region " \
                   "LIMIT 3"

    panel_list = []
    for row in db_connect.execute_select(select_query):
        panel_list.append(Panel(row['pid'], row['name'], row['region'],
                                row['location'], row['latitude'], row['longitude'],
                                row['height'], row['width'], row['airtime_rate'],
                                row['pedestrain_flow'], row['mode'], row['cap'], row['img_no'],
                                row['panel_path'], row['used']))

    return panel_list


"""demo display in payment.html"""
def get_all_file_of_panel(pid, date_from, date_to):
    select_query = "SELECT booking.*, file_source.file_path FROM booking " \
                   "INNER JOIN file_source ON file_source.pid=booking.pid " \
                   "AND file_source.bid=booking.bid " \
                   "WHERE booking.pid='{}' " \
                   "AND booking.date_from>=concat('{}', '-01') " \
                   "AND booking.date_to<=concat('{}', '-01')".format(pid, date_from, date_to)
    return db_connect.execute_select(select_query)


"""upload booking detail and file_source in payment.html"""
def insert_booking_detail_and_file_source(pid, uid, date_from, date_to, file_pid, file_type, file_path):
    insert_query = "INSERT INTO booking (pid, uid, date_from, date_to) " \
                   "VALUE ('{}', '{}', concat('{}','-01'), concat('{}', '-01')); " \
                   "INSERT INTO file_source (bid, pid, file_type, file_path) " \
                   "VALUE(LAST_INSERT_ID(), '{}', '{}', '{}') ".format(pid, uid, date_from,
                                                                       date_to, file_pid, file_type, file_path)

    return db_connect.execute_insert(insert_query)


"""+1 to the panel_usage in payment.html"""
def update_1_to_panel_usage(pid):
    update_query = "UPDATE panel_usage " \
                   "SET used = used+1 " \
                   "WHERE panel_usage.pid='{}'".format(pid)

    return db_connect.execute_update(update_query)


"""+1 to the user_freq in login.html"""
def update_1_to_user_freq(uid):
    update_query = "UPDATE user_freq " \
                   "SET freq = freq+1 " \
                   "WHERE user_freq.uid='{}'".format(uid)

    return db_connect.execute_update(update_query)


"""upload panel detail in supplier.html"""
def insert_panel_detail(panel_name, region, location, latitude, longitude, height,
                        width, airtime_rate, pedestrain_flow, mode, cap, file_path_1, file_path_2):
    insert_query = "INSERT INTO panel(name, region, location, latitude, " \
                   "longitude, height, width, airtime_rate, pedestrain_flow, mode, cap) " \
                   "VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}'); " \
                   "SET @last_insert_pid = LAST_INSERT_ID();" \
                   "INSERT INTO panel_source(pid, img_no, panel_path) " \
                   "VALUES (@last_insert_pid, 1, '{}'), " \
                   "(@last_insert_pid, 2, '{}'); " \
                   "INSERT INTO panel_usage(pid, used) " \
                   "VALUES(@last_insert_pid, 0)".format(panel_name, region, location, latitude,
                                                        longitude, height, width, airtime_rate, pedestrain_flow,
                                                        mode, cap, file_path_1, file_path_2)

    return db_connect.execute_insert(insert_query)


"""get all booking detail in detail.html"""
def get_all_booking_detail(uid):
    select_query = "SELECT booking.*, panel.*, panel_source.* FROM booking " \
                   "INNER JOIN panel ON booking.pid=panel.pid " \
                   "INNER JOIN panel_source ON panel_source.pid=booking.pid " \
                   "WHERE panel_source.img_no='1' " \
                   "AND booking.uid='{}' " \
                   "ORDER BY booking.date_from".format(uid)

    return db_connect.execute_select(select_query)


"""only show 9 panel detail in quickstart.html"""
def get_panel_detail_by_region_limit_9():
    select_query = "SELECT panel.*, panel_source.*, panel_usage.used FROM panel " \
                   "INNER JOIN panel_source ON panel_source.pid=panel.pid " \
                   "INNER JOIN panel_usage ON panel_usage.pid=panel.pid " \
                   "WHERE panel_source.img_no='1'" \
                   "ORDER BY panel.region " \
                   "LIMIT 9"

    panel_list = []
    for row in db_connect.execute_select(select_query):
        panel_list.append(Panel(row['pid'], row['name'], row['region'],
                                row['location'], row['latitude'], row['longitude'],
                                row['height'], row['width'], row['airtime_rate'],
                                row['pedestrain_flow'], row['mode'], row['cap'], row['img_no'],
                                row['panel_path'], row['used']))

    return panel_list


"""get all suitable panel in quicksearch.html"""
def get_all_panel_by_preference(region, mode, date_from, date_to, min_price, max_price):
    select_query = "SELECT panel.*, panel_source.*, panel_usage.used, booking.* FROM panel " \
                   "INNER JOIN panel_source ON panel_source.pid=panel.pid " \
                   "INNER JOIN panel_usage ON panel_usage.pid=panel.pid " \
                   "INNER JOIN booking ON booking.pid=panel.pid " \
                   "WHERE panel_source.img_no='1'" \
                   "AND panel.region='{}' " \
                   "AND mode='{}' " \
                   "AND booking.date_from>=concat('{}', '-01') " \
                   "AND booking.date_to<=concat('{}', '-01') " \
                   "AND panel.airtime_rate BETWEEN '{}' AND '{}' " \
                   "GROUP BY panel.pid". format(region, mode, date_from, date_to, min_price, max_price)

    return db_connect.execute_select(select_query)
