__author__ = 'xero-mac'
import db

testDB = db.ChatDB("Exia.db")

if testDB.add_new_user("xero", "7689") is False:
    print("Add user Fail")
else:
    print "Success!"