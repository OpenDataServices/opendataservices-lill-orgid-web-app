from flask import Flask, render_template
import psycopg
import lillorgid.webapp.settings

app = Flask(__name__)

@app.route("/")
def home():
    return render_template(
        'home.html'
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

