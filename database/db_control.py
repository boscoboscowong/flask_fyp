from database import db_connect
from database_class.panel import Panel


"""panel detail in location.html"""
def get_panel_detail_by_region_HKI():
    SELECT_QUERY="SELECT panel.*, panel_source.path, panel_usage.used FROM panel" \
                 "INNER JOIN panel_usage " \
                 "ON panel.pid=panel_source.pid=panel_usage.pid" \
                 "WHERE pane_source.img_no='1'" \
                 "AND panel.region='HKI'"
    panel_list=[]
    for row in db_connect.execute_select(SELECT_QUERY):
        panel_list.append(Panel(row['pid']), row['name'], row['region'],
                          row['location'], row['latitude'], row['longitude'],
                          row['height'], row['width'], row['airtime_rate'],
                          row['pedestrain_flow'], row['cap'], row['used'],row['path'])
        return panel_list

"""panel detail in booking.html"""
