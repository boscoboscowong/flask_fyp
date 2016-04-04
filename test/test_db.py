from database import db_control

for row in db_control.get_booking_bid(1, 1):
    print row['bid']
