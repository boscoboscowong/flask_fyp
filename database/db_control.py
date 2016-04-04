from database import db_connect
from database_class.panel import Panel
from database_class.panel_source import Panel_source
from database_class.user import User


"""check user login in login.html"""
def check_user_login(username, pwd):
    select_query = "SELECT COUNT(*) as num FROM login " \
                   "WHERE username= '{}'"\
                   "AND pwd='{}'".format(username, pwd)
    return db_connect.verify_user_login(select_query)


"""user uid in login.html"""
def get_user_uid(username):
    select_query = "SELECT login.uid FROM login " \
                   "WHERE username='{}'".format(username)
    return db_connect.execute_select(select_query)


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
                                row['pedestrain_flow'], row['cap'], row['img_no'],
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
                                row['pedestrain_flow'], row['cap'], row['img_no'],
                                row['panel_path'], row['used']))
    return panel_list


"""list all image of a panel in booking.html"""
def list_all_image_of_panel(pid):
    select_query = "SELECT panel_source.* FROM panel_source WHERE panel_source.pid = '{}'".format(pid)

    panel_list = []
    for row in db_connect.execute_select(select_query):
        panel_list.append(Panel_source(row['sid'], row['pid'], row['img_no'], row['panel_path']))

    return panel_list


"""upload booking detail and file_source in pyament.html"""
def insert_booking_detail_and_file_source(pid, uid, date_from, date_to, file_type, file_path):
    insert_query = "INSERT INTO booking (pid, uid, date_from, date_to) " \
                   "VALUE ('{}', '{}', '{}', '{}'); "\
                   "INSERT INTO file_source (bid, file_type, file_path) " \
                   "VALUE(LAST_INSERT_ID(), '{}', '{}')".format(pid, uid, date_from, date_to, file_type, file_path)
    print insert_query
    return db_connect.execute_insert(insert_query)


"""upload register in register.html"""
def insert_a_row_to_login_table(username, pwd, company_name, email, tel):
    insert_query = "INSERT INTO login (username, pwd, company_name, email, tel) " \
                   "VALUE ('{}', '{}', '{}', '{}', '{}')".format(username, pwd, company_name, email, tel)
    return db_connect.execute_insert(insert_query)


"""user detail in profile.html"""
def get_user_detail(username):
    select_query = "SELECT login.*, user_frequency.frequency FROM login " \
                   "INNER JOIN user_frequency ON login.uid=user_frequency.uid " \
                   "WHERE login.username='{}'".format(username)

    user_list = []
    for row in db_connect.execute_select(select_query):
        user_list.append(User(row['uid'], row['username'], row['pwd'], row['company_name'],
                              row['email'], row['tel'], row['frequency']))

    return user_list



