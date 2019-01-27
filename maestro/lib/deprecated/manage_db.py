'''
this module creates a database. it was created before, designed after the Tcl
verison. this will be replaced by pandas dataframes and if we need to save it
for long term persistence between sessions we'll save it out to pickels or
something. (for now anyway.)
'''

import sqlite3 as lite
import sys


class Database_Connection(object):
    def __init__(self, name: str = 'database', path: str = '../../database/'):
        self.name = name
        self.con = None
        self.cur = None
        self.path = path
        try:
            self.con = lite.connect(self.path + name + '.db')
            self.cur = self.con.cursor()
            self.cur.execute('SELECT SQLITE_VERSION()')
            data = self.cur.fetchone()
            print("SQLite version: %s" % data)
        except lite.Error(e):
            print("Error %s:" % e.args[0])
            sys.exit(1)
        #finally:
        #    if con:
        #        con.close()

    def get_name(self):
        return self.name

    def create_tables(self):
        self.cur.execute("CREATE TABLE sdr(node INTEGER PRIMARY KEY AUTOINCREMENT, input CHAR, ix INTEGER)")
        self.cur.execute("CREATE TABLE acts(node INTEGER PRIMARY KEY AUTOINCREMENT, input CHAR, ix INTEGER, notes CHAR)")
        self.cur.execute("CREATE TABLE states(old CHAR, act CHAR, new CHAR)")
        #return self.cur.lastrowid

    def insert_sdr(self, input, ix):
        con = lite.connect(self.path + self.name + '.db')
        with con:
            cur = con.cursor()
            cur.execute("INSERT INTO sdr (input,ix) VALUES('{input}',{ix})".format(input=input, ix=ix))
        return cur.lastrowid

    def insert_acts(self, input, ix, notes=''):
        con = lite.connect(self.path + self.name + '.db')
        with con:
            cur = con.cursor()
            cur.execute("INSERT INTO acts (input,ix,notes) VALUES('{input}',{ix},'{notes}')".format(input=input, ix=ix, notes=notes))
        return cur.lastrowid


    def insert_states(self, old_state, action, new_state):
        con = lite.connect(self.path + self.name + '.db')
        with con:
            cur = con.cursor()
            cur.execute("INSERT INTO states(old,act,new) VALUES('{old}','{act}','{new}')".format(old=old_state, act=action, new=new_state))
        return cur.lastrowid

    def select_sdr_node(self, input, ix):
        self.cur.execute("SELECT node FROM sdr WHERE input='{input}' AND ix={ix}".format(input=input, ix=ix))
        return self.cur.fetchall()

    def select_sdr_input(self, node):
        self.cur.execute("SELECT input FROM sdr WHERE node={node}".format(node=node))
        return self.cur.fetchall()

    def select_sdr_input_ix(self, node):
        self.cur.execute("SELECT input,ix FROM sdr WHERE node={node}".format(node=node))
        return self.cur.fetchall()

    def select_state(self, old, new):
        self.cur.execute("SELECT act FROM states WHERE old='{old}' and new='{new}'".format(old=old,new=new))
        return self.cur.fetchall()


    def get_lastrowid(self):
        return self.cur.lastrowid
