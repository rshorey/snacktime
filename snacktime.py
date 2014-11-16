# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing

# configuration
DATABASE = '/tmp/snacks.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

# a useful method for connecting to the DB
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])
    

#initialize database
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

#methods for connecting to and disconnecting from db before/after requests
@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/')
def show_snacks():
    cur = g.db.execute('select name, type, date, cost from snacks order by date desc')
    snacks = [dict(name=row[0], type=row[1], date=row[2], cost=row[3]) for row in cur.fetchall()]
    return render_template('show_snacks.html', snacks=snacks)
            
@app.route('/add', methods=['POST'])
def add_snacks():
    g.db.execute('insert into snacks (name, type, date, cost) values (?, ?, ?, ?)',
                 [request.form['name'], request.form['type'], request.form['date'], request.form['cost']])
    g.db.commit()
    flash('New snack was successfully added')
    return redirect(url_for('show_snacks'))


#fire up the server
if __name__ == '__main__':
    app.run()