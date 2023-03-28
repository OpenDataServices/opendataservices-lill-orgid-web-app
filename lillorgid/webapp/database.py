import lillorgid.webapp.settings as settings
import requests
import json

class Database():

    def __init__(self):
        pass

    def query_lists(self, query):
        url = settings.SOLR_URL + "/" + settings.SOLR_LISTS_CORE + "/select"
        r = requests.get(url, data=query, auth=requests.auth.HTTPBasicAuth(settings.SOLR_USERNAME, settings.SOLR_PASSWORD),)
        r.raise_for_status()
        return r.json()

    def query_data(self, query):
        url = settings.SOLR_URL + "/" + settings.SOLR_DATA_CORE + "/select"
        r = requests.get(url, data=query, auth=requests.auth.HTTPBasicAuth(settings.SOLR_USERNAME, settings.SOLR_PASSWORD),)
        r.raise_for_status()
        return r.json()
