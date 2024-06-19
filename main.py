import sqlite3

import flask
from flask import Flask, render_template, request

from initdb.create_db import InitDb, DB_PATH

_db = InitDb()
data = _db.data

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", tables=data)


@app.route("/form/<table_name>", methods=["GET"])
def tb(table_name):
    return render_template("table_form.html", fields=data[table_name], table_name=table_name)


@app.route("/insert/<table_name>", methods=["POST"])
def insert(table_name):
    with sqlite3.connect(DB_PATH) as db:
        cursor = db.cursor()
        insert_query = []
        for field in data[table_name]:
            field_name = field['name']
            value = request.form.get(field_name)
            dtype = field['dtype']
            if dtype not in ("integer", "real"):
                insert_query.append(f"\'{value}\'")
            else:
                insert_query.append(value)
        query = f"INSERT INTO {table_name} VALUES(null, {','.join(insert_query)})"
        print("QUERY:", query)
        cursor.execute(query)
        cursor.close()
        return "200"


if __name__ == "__main__":
    app.run()
