from database import db_control

row = db_control.check_user_login("johnlee", "johnlee")
print row['num']