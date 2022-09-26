import json

from flask import Flask, g, request
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

def serialize_patient_prescription(record):
    return {
        'medicationCode' : record['code'],
        'medicationDescription' : record['description'],
        'prescriptionStartDate' : record['prescriptionStartDate'],
        'prescriptionEndDate' : record['prescriptionEndDate'],
        'reasonCode' : record['reasonCode'],
        'reasonDescription' : record['reasonDescription'],
        'timesDispensed' : record['timesDispensed']
    }

class PatientPrescriptions(Resource):

    def get(self, patient_id):

        def get_prescriptions_for_patient(tx, patient_id):
            return tx.run(
                """
                MATCH (p:Patient {id: $patient_id})-[:HAD]->(:Encounter)<-[r:PRESCRIBED_AT]-(m:Medication)
                RETURN m.code AS code, m.description AS description, r.prescriptionStartDate AS prescriptionStartDate, 
                r.prescriptionEndDate AS prescriptionEndDate, r.reasonCode AS reasonCode, 
                r.reasonDescription AS reasonDescription, r.timesDispensed AS timesDispensed 
                """, {'patient_id': patient_id}
            ).data()
        db = get_db()
        patient_prescriptions = db.read_transaction(get_prescriptions_for_patient, patient_id)
        return [serialize_patient_prescription(record) for record in patient_prescriptions]

class MedicationNumberOfPatients(Resource):
    
    def get(self, medication_code):

        def get_number_of_patients(tx, medication_code):
            return tx.run(
                """
                MATCH (:Medication {code: $medication_code})-[:PRESCRIBED_AT]->(:Encounter)<-[:HAD]-(p:Patient)
                RETURN count(DISTINCT p) as numPatients
                """, {'medication_code': medication_code}
            ).data()
        db = get_db()
        num_patients = db.read_transaction(get_number_of_patients, medication_code)
        return num_patients

class MedicationSequenceFrequency(Resource):

    def get(self, medication_code_1, medication_code_2):

        def get_medication_sequence_frequency(tx, medication_code_1, medication_code_2):
            return tx.run(
                """
                MATCH (m1:Medication {code: $medication_code_1})-[:PRESCRIBED_AT]->(e:Encounter)<-[:HAD]-(p:Patient)
                MATCH (e)-[:HAS_NEXT*]->(:Encounter)<-[:PRESCRIBED_AT]-(:Medication {code: $medication_code_2})
                RETURN count(DISTINCT p) AS numPatients
                """, {'medication_code_1': medication_code_1, 'medication_code_2': medication_code_2}
            ).data()
        db = get_db()
        frequency = db.read_transaction(get_medication_sequence_frequency, medication_code_1, medication_code_2)
        return frequency

api.add_resource(PatientPrescriptions, '/patient_prescriptions/<string:patient_id>')
api.add_resource(MedicationNumberOfPatients, '/num_patients_prescribed/<string:medication_code>')
api.add_resource(MedicationSequenceFrequency, '/medication_sequence_frequency/<string:medication_code_1>/<string:medication_code_2>')