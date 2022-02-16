from flask import Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
import create_db

import sqlite3#
import json

app = Flask(__name__)
CORS(app)

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Python Tech Test API"
    }
)
app.register_blueprint(swaggerui_blueprint)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# TODO - you will need to implement the other endpoints
# GET /api/person/{id} - get person with given id
# POST /api/people - create 1 person
# PUT /api/person/{id} - Update a person with the given id
# DELETE /api/person/{id} - Delete a person with a given id

# UPDATE received via email 14/2/22
# Instructions amended as follows:
# GET /api/people/{id} - get person with given id
# POST /api/people - create 1 person
# PUT /api/people/{id} - Update a person with the given id
# DELETE /api/people/{id} - Delete a person with a given id

# jm comments
# I understand the app is using a React Form and JSON data
# but cannot seem to get that data to pull into app.py for insertion on test.db
# I attempted using json.loads() and json.dumps() but cannot seem to retrieve this data for insertion
# I have left my coding below to demonstrate understanding of form data, HTTP requests and SQL CRUD
# I can get the app to run but not the below app.routes() unfortunately

@app.route("/api/people", methods=["GET"])
def getall_people():
    conn = sqlite3.connect('test.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_people = cur.execute('SELECT * FROM Person;').fetchall()

    return jsonify(all_people)


@app.route("/api/people/{id}", methods=["GET, PUT, DELETE"])
def person():
    conn = sqlite3.connect('test.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    p = None

    if request.method == "GET":
        cur.execute("SELECT * FROM Person WHERE id=?", (id,)).fetchone()
        rows = cur.fetchall()
        for row in rows:
            p = row
        if p is not None:
            return jsonify(p), 200
        else:
            return "Something went wrong", 404

    if request.method == "PUT":
        update = """ UPDATE Person SET firstName = ?,lastName = ?, enabled = ? , authorised = ?
                WHERE id = ? """

        firstName = request.form["firstName"]
        lastName = request.form["lastname"]
        enabled = {True, False}
        authorised = {True, False}

        updated_person = {
          "id": id,
          "firstName": firstName,
          "lastName": lastName,
          "enabled": enabled,
          "authorised": authorised
        }

        conn.execute(update, (firstName, lastName, enabled, authorised, id))
        conn.commit()
        return jsonify(updated_person)

    if request.method == "DELETE":
        delete = """ DELETE FROM Person WHERE id=? """
        conn.execute(delete, (id,))
        conn.commit()

        return "Person deleted.", 200


@app.route("/api/people", methods=["POST"])
def create_person():
    conn = sqlite3.connect('test.db')
    cur = conn.cursor()
    conn.row_factory = dict_factory

    if request.method == "POST":
        firstName = request.form["firstName"]
        lastName = request.form["lastName"]
        enabled = {True, False}
        authorised = {True, False}
        create_p = """INSERT INTO Person (firstName, lastName, enabled, authorised) VALUES (?, ?, ?, ?) """
        cp = cur.execute(create_p, [firstName, lastName, enabled, authorised])
        conn.commit()
        return jsonify(cp)


if __name__ == '__main__':
    app.run()
