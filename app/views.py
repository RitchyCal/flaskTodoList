from flask import g, abort, render_template, redirect, url_for
from app import app
from rethinkdb import RethinkDB
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from .forms import TaskForm


# rethink config
RDB_HOST =  'localhost'
RDB_PORT = 28015
TODO_DB = 'todo'
r = RethinkDB()

@app.route("/", methods = ['GET', 'POST'])
def index():
    form = TaskForm()
    if form.validate_on_submit():
        r.table('todos').insert({"name": form.label.data}).run(g.rdb_conn)
        return redirect(url_for('index'))
    selection = list(r.table('todos').run(g.rdb_conn))
    return render_template('index.html', form=form, tasks=selection)

# db setup; only run once
def dbSetup():
    connection = r.connect(host=RDB_HOST, port=RDB_PORT)
    try:
        r.db_create(TODO_DB).run(connection)
        r.db(TODO_DB).table_create('todos').run(connection)
        print ('Database setup completed')
    except RqlRuntimeError:
        print ('Database already exists.')
    finally:
        connection.close()
dbSetup()

# open connection before each request
@app.before_request
def before_request():
    try:
        g.rdb_conn = r.connect(host=RDB_HOST, port=RDB_PORT, db=TODO_DB)
    except RqlDriverError:
        abort(503, "Database connection could be established.")

# close the connection after each request
@app.teardown_request
def teardown_request(exception):
    try:
        g.rdb_conn.close()
    except AttributeError:
        pass