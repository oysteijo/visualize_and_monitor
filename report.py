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

    def __init__(self, database=None, fields=None):
        if not database:
            database = "reporter.db"

        self.database   = database
        self.connection = sqlite3.connect(self.database)
        self.cursor     = self.connection.cursor()
        if fields:
            self.set_fields(fields)

    def set_fields(self, fields):
        integer_indicators = ["epoch", "step", "fold"]

        int_fields = set() 
        for f in fields:
            if any([ii in f for ii in integer_indicators]):
                int_fields.add(f)

        #print(int_fields)

        float_fields = set(fields) - int_fields
        #print(float_fields)

        create_str = """create table if not exists {}(
            id INTEGER PRIMARY KEY,
            date DATETIME,
            description TEXT,
            {})""".format( TABLENAME, ", ".join([ f+ " INTEGER\n" for f in int_fields] ))
        print(create_str)


        # self.cursor.execute("""create table if not exists training_log(

    def write(self, values ):
        columns = ", ".join(values.keys())
        #columns += ", date"
        placeholders = ":"+", :".join(values.keys())
        #placeholders += ", :", datetime.now()
        query = 'INSERT INTO %s (%s) VALUES (%s)' % (TABLENAME, columns, placeholders)
        print( query )
        #cur.execute(query, values)
        #con.commit()

if __name__ == "__main__":
    reporter = Reporter(fields=["epoch", "score", "steps", "bigsteps", "foldepoch"])
    reporter.write({"epoch": 2, "score": 4.0})

