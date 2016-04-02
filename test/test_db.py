from database import db_control

rows = db_control.get_panel_detail_by_region()

for row in rows:
    print row.path