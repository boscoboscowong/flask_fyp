from database import db_connect
from database_class.panel import Panel
from database_class.panel_source import Panel_source


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
                          row['path'], row['used']))
    return panel_list


"""panel detail in booking.html"""
def get_panel_detail(pid):
    select_query = "SELECT panel.*, panel_source.*, panel_usage.used FROM panel " \
                   "INNER JOIN panel_source ON panel_source.pid=panel.pid " \
                   "INNER JOIN panel_usage ON panel_usage.pid=panel.pid " \
                   "WHERE panel_source.img_no='1'" \
                   "AND panel.pid={}".format(pid)

    panel_list = []
    for row in db_connect.execute_select(select_query):
        panel_list.append(Panel(row['pid'], row['name'], row['region'],
                          row['location'], row['latitude'], row['longitude'],
                          row['height'], row['width'], row['airtime_rate'],
                          row['pedestrain_flow'], row['cap'], row['img_no'],
                          row['path'], row['used']))
    return panel_list

"""list all image of the panel in booking.html"""
def list_all_image_of_panel(pid):
    select_query = "SELECT panel.*, panel_source.*, panel_usage.used FROM panel " \
                   "INNER JOIN panel_source ON panel_source.pid=panel.pid " \
                   "INNER JOIN panel_usage ON panel_usage.pid=panel.pid " \
                   "WHERE panel_source.pid={}".format(pid)

    panel_list =[]
    for row in db_connect.execute_select(select_query):
        panel_list.append(Panel_source(row['sid'], row['pid'], row['img_no'], row['path'])
    return panel_list