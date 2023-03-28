from flask import Flask, render_template, abort, jsonify
from lillorgid.webapp.database import Database

app = Flask(__name__)

@app.route("/")
def home():
    return render_template(
        'home.html'
    )


API1_LIST_ID_USES_JSON_PATH = "/api1/list/<listid>/id/<orgid>/uses.json"


@app.route('/api1/openapi.json')
def api1_openapi_json():

    return jsonify({
        "openapi": "3.1.0",
        "info": {
            "title": "Lill Org Id API",
            "version": "1.0"
        },
        "paths": {
            API1_LIST_ID_USES_JSON_PATH: {
                "summary": "Gets all uses of an Org-Id",
                "description": "Gets all uses of an Org-Id across all data standards.",
                "get": {

                }
            }
        }
    })


@app.route("/list")
def list():
    db = Database()
    data = db.query_lists({'q':'*:*','start':0, 'rows':100000, 'sort':'id asc'})

    return render_template(
        'lists.html',
        lists=data.get('response', {}).get('docs', [])
    )

@app.route('/list/<id>')
def list_index(id):

    db = Database()
    # TODO escaping?  And in other places
    data = db.query_lists({'q':'id:'+id})

    return render_template(
        'list/index.html',
        list=data.get('response', {}).get('docs', []).pop()
    )


@app.route('/list/<id>/data-standard')
def list_data_standards(id):

    db = Database()

    data = db.query_lists({'q':'id:'+id})

    data2 = db.query_data({'q':'list_s:'+id,'facet.field':'datastandard_s', 'facet.mincount':1, 'facet':'true', 'rows':1})
    data2_facet_data = data2.get('facet_counts', {}).get('facet_fields',{}).get('datastandard_s',[])
    data_standards = []
    for i in range(0, len(data2_facet_data)-1,2):
        data_standards.append({"data_standard": data2_facet_data[i], "count": data2_facet_data[i+1]} )

    return render_template(
        'list/data-standards.html',
        list=data.get('response', {}).get('docs', []).pop(),
        data_standards=data_standards
    )

@app.route('/list/<id>/id')
def list_ids(id):

    db = Database()

    data = db.query_lists({'q':'id:'+id})

    data2 = db.query_data({'q':'list_s:'+id,'facet.field':'id_s', 'facet.mincount':1, 'facet':'true', 'rows':1})
    data2_facet_data = data2.get('facet_counts', {}).get('facet_fields',{}).get('id_s',[])
    ids = []
    for i in range(0, len(data2_facet_data)-1,2):
        ids.append({"id": data2_facet_data[i], "count": data2_facet_data[i+1]} )

    return render_template(
        'list/ids.html',
        list=data.get('response', {}).get('docs', []).pop(),
        ids=ids
    )

@app.route('/list/<listid>/id/<orgid>')
def list_id(listid, orgid):

    db = Database()

    data = db.query_lists({'q':'id:'+listid})

    data2 = db.query_data({'q':'list_s:'+listid+ "  id_s:"+orgid,'q.op':'AND', 'rows':100000000})

    return render_template(
        'list/id/index.html',
        list=data.get('response', {}).get('docs', []).pop(),
        ids=data2.get('response', {}).get('docs', []),
    )


@app.route(API1_LIST_ID_USES_JSON_PATH)
def api1_list_id_uses_json(listid, orgid):

    db = Database()

    data2 = db.query_data({'q':'list_s:'+listid+ "  id_s:"+orgid,'q.op':'AND', 'rows':100000000})

    out = []
    for row in data2.get('response', {}).get('docs', []):
        o = {
            'datastandard': row['datastandard_s'],
            'name': row['name_s']
        }
        out.append(o)

    return jsonify({"data":out})

@app.route("/data-standard/<data_standard>")
def data_standard(data_standard):


    db = Database()
    data2 = db.query_data({'q':'datastandard_s:'+data_standard,'facet.field':'list_s', 'facet.mincount':1, 'facet':'true', 'rows':1})
    data2_facet_data = data2.get('facet_counts', {}).get('facet_fields',{}).get('list_s',[])
    lists = []
    for i in range(0, len(data2_facet_data)-1,2):
        lists.append({"list": data2_facet_data[i], "count": data2_facet_data[i+1]} )

    return render_template(
        'data_standard/'+data_standard+'.html',
        data_standard=data_standard,
        lists=lists
    )


@app.route("/data-standard/<data_standard>/list/<list_id>")
def data_standard_list(data_standard, list_id):

    db = Database()

    data = db.query_lists({'q':'id:'+list_id})

    # TODO        abort(404) and in other places

    return render_template(
        'data_standard/list/index.html',
        data_standard=data_standard,
        list=data.get('response', {}).get('docs', []).pop(),
    )


@app.route("/data-standard/<data_standard>/list/<list_id>/id")
def data_standard_list_id(data_standard, list_id):

    db = Database()

    data = db.query_lists({'q':'id:'+list_id})

    # TODO        abort(404) and in other places

    data2 = db.query_data({'q':'list_s:'+list_id+ ' datastandard_s:'+data_standard,'q.op':'AND','facet.field':'id_s', 'facet.mincount':1, 'facet':'true', 'rows':1})
    data2_facet_data = data2.get('facet_counts', {}).get('facet_fields',{}).get('id_s',[])
    ids = []
    for i in range(0, len(data2_facet_data)-1,2):
        ids.append({"id": data2_facet_data[i], "count": data2_facet_data[i+1]} )

    return render_template(
        'data_standard/list/ids.html',
        data_standard=data_standard,
        list=data.get('response', {}).get('docs', []).pop(),
        ids=ids
    )
