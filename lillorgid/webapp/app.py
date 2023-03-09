from flask import Flask, render_template, abort
import psycopg
import lillorgid.webapp.settings
from lillorgid.webapp.database import Database

app = Flask(__name__)

@app.route("/")
def home():
    return render_template(
        'home.html'
    )


@app.route("/list")
def list():
    with Database() as db:
        res = db.cursor.execute(
            "select * from list order by id",
            []
        )
        lists = [r for r in res.fetchall()]


    return render_template(
        'lists.html',
        lists=lists
    )

@app.route('/list/<id>')
def list_index(id):
    with Database() as db:
        res = db.cursor.execute(
            "select * from list where id=%s",
            [id]
        )
        list = res.fetchone()

        if not list:
            abort(404)

    return render_template(
        'list/index.html',
        list=list
    )


@app.route('/list/<id>/data-standard')
def list_data_standards(id):
    with Database() as db:
        res = db.cursor.execute(
            "select * from list where id=%s",
            [id]
        )
        list = res.fetchone()

        if not list:
            abort(404)

        res = db.cursor.execute(
            "select data_standard, count(*) from data where list=%s group by data_standard",
            [id]
        )
        data_standards = [{"data_standard": r['data_standard'], "count": r['count']} for r in res.fetchall()]


    return render_template(
        'list/data-standards.html',
        list=list,
        data_standards=data_standards
    )

@app.route('/list/<id>/id')
def list_ids(id):
    with Database() as db:
        res = db.cursor.execute(
            "select * from list where id=%s",
            [id]
        )
        list = res.fetchone()

        if not list:
            abort(404)

        res = db.cursor.execute(
            "select id, count(*) from data where list=%s group by id order by id asc",
            [id]
        )
        ids = [{"id": r['id'], "count": r['count']} for r in res.fetchall()]


    return render_template(
        'list/ids.html',
        list=list,
        ids=ids
    )

@app.route('/list/<listid>/id/<orgid>')
def list_id(listid, orgid):
    print(orgid)
    with Database() as db:
        res = db.cursor.execute(
            "select * from list where id=%s",
            [listid]
        )
        list = res.fetchone()

        if not list:
            abort(404)

        res = db.cursor.execute(
            "select * from data where list=%s and id=%s",
            [listid, orgid]
        )
        ids = [r for r in res.fetchall()]

        if not ids:
            abort(404)


    return render_template(
        'list/id/index.html',
        list=list,
        ids=ids
    )


@app.route("/data-standard/<data_standard>")
def data_standard(data_standard):
    with Database() as db:
        res = db.cursor.execute(
            "select list, count(*) from data where data_standard=%s group by list",
            [data_standard]
        )
        lists = [{"list": r['list'], "count": r['count']} for r in res.fetchall()]

    return render_template(
        'data_standard/'+data_standard+'.html',
        lists=lists
    )

