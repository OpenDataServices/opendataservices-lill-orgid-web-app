from flask import Flask, render_template, abort
import psycopg
import lillorgid.webapp.settings

app = Flask(__name__)

@app.route("/")
def home():
    return render_template(
        'home.html'
    )


@app.route("/list")
def list():
    connection = psycopg.connect(lillorgid.webapp.settings.AZURE_POSTGRES_CONNECTION_STRING,
                                 row_factory=psycopg.rows.dict_row)
    with connection.cursor() as cur:
        res = cur.execute(
            "select * from list order by id",
            []
        )
        lists = [r for r in res.fetchall()]

    connection.close()

    return render_template(
        'lists.html',
        lists=lists
    )

@app.route('/list/<id>')
def list_index(id):
    connection = psycopg.connect(lillorgid.webapp.settings.AZURE_POSTGRES_CONNECTION_STRING,
                                 row_factory=psycopg.rows.dict_row)
    with connection.cursor()    as cur:
        res = cur.execute(
            "select * from list where id=%s",
            [id]
        )
        list = res.fetchone()

    connection.close()

    if not list:
        abort(404)

    return render_template(
        'list/index.html',
        list=list
    )

@app.route("/data-standard/iati")
def data_standard_iati():
    return __data_standard('iati')


@app.route("/data-standard/ocds")
def data_standard_ocds():
    return __data_standard('ocds')



def __data_standard(data_standard):
    connection = psycopg.connect(lillorgid.webapp.settings.AZURE_POSTGRES_CONNECTION_STRING, row_factory=psycopg.rows.dict_row)
    with connection.cursor() as cur:
        res = cur.execute(
            "select list, count(*) from data where data_standard=%s group by list",
            [data_standard]
        )
        lists = [{"list": r['list'], "count": r['count']} for r in res.fetchall()]

    connection.close()


    return render_template(
        'data_standard/'+data_standard+'.html',
        lists=lists
    )

