import sqlite3
from datetime import datetime

TABLENAME = "training_log"

class Reporter(object):
    """
        Reporter class to be used in the training algorithm.

        reporter = Reporter()
        reporter.write({"epoch": epoch,
                        "fold" : fold,
                        "description": "New loss func",
                        "val_loss": validation_loss,
                        "train_loss": train_loss
                        })
    """

    def __init__(self, database="reporter.db"):
        self.database   = database
        self.connection = sqlite3.connect(self.database)
        self.cursor     = self.connection.cursor()
        self.table_created = self._check_table()

    def _check_table(self):
        try:
            self.cursor.execute("""
                SELECT COUNT(*)
                FROM information_schema.tables
                WHERE table_name = '{0}'
                """.format(TABLENAME.replace('\'', '\'\'')))
            return self.cursor.fetchone()[0] == 1
        except:
            return False

    def _create_table(self, values):
        d = { str: "TEXT", float: "FLOAT", int: "INTEGER" }
        create_str = """create table if not exists {}(
            id INTEGER PRIMARY KEY
            ,d1 INT  -- Date Stored in unixtime (seconds since 1st.Jan.1970) 
            """.format(TABLENAME)
        for k,v in values.items():
            create_str += "\n      ,{} {}".format(str(k), d[type(v)] )
        create_str += ")"

        self.cursor.execute( create_str )
        self.connection.commit()
        self.table_created = True

    def write(self, values ):
        if not self.table_created:
            self._create_table(values)

        columns = ", ".join(values.keys())
        placeholders = ":"+", :".join(values.keys())
        query = """INSERT INTO {} (d1, {}) VALUES (strftime('%s', 'now'), {})""".format(TABLENAME, columns, placeholders)
        self.cursor.execute(query, values)
        self.connection.commit()

if __name__ == "__main__":
    reporter = Reporter()
    reporter.write({
        "description": "new loss function",
        "epoch"      : 2,
        "score"      : 4.0
    })


