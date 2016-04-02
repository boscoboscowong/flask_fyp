from database import db_control

rows = db_control.list_all_image_of_panel(1)

for row in rows:
    print row.path