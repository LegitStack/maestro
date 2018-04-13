import os.path
import manage_db

if not os.path.isfile('../db/testing.db'):
    db = manage_db.Database_Connection('testing')
    db.create_tables()
    db.insert_sdr('B',1)
