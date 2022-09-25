import json

from flask import Flask, g
from flask_cors import CORS
from flask_json import FlaskJSON, json_response
from flask_restful import Api, Resource, reqparse

from neo4j import GraphDatabase, basic_auth

app = Flask(__name__)
api = Api(app)

CORS(app)
FlaskJSON(app)

@api.representation('application/json')
def output_json(data, code, headers=None):
    return json_response(data_=data, headers_=headers, status_=code)

f = open('neo4j_conf.json')
neo4j_conf = json.load(f)
f.close()
driver = GraphDatabase.driver(neo4j_conf["url"], auth=basic_auth(neo4j_conf["user"], neo4j_conf["password"]))

def get_db():
    if not hasattr(g, 'neo4j_db'):
        g.neo4j_db = driver.session()
    return g.neo4j_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'neo4j_db'):
        g.neo4j_db.close()

