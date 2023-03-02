import psycopg
import lillorgid.webapp.settings

class Database():

    def __init__(self):
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = psycopg.connect(lillorgid.webapp.settings.AZURE_POSTGRES_CONNECTION_STRING,
                                 row_factory=psycopg.rows.dict_row)
        self.cursor = self.connection.cursor()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.connection.close()
