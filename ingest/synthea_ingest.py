import os 
import json

from neo4j import GraphDatabase
from ingest_queries import synthea_queries
from synthea_schema import schema_statements


class SyntheaDataIngester:

    def __init__(self, neo4j_conf, queries, schema):
        self.driver = GraphDatabase.driver(neo4j_conf["url"], auth = (neo4j_conf["user"], neo4j_conf["password"]))
        self.batch_size = neo4j_conf.get("batch_size")
        self.database = neo4j_conf.get("database")
        self.queries = queries
        self.schema = schema
        self.cwd = os.path.abspath(os.path.dirname(__file__))

    def create_indexes(self):
        with self.driver.session(database=self.database) as session:
            for statement in self.schema:
                session.run(statement)


    def batch_data_load(self):
        ingest_query = """
        LOAD CSV WITH HEADERS FROM '{file}' AS row
        CALL {{
            WITH row
            {query_body}
        }} IN TRANSACTIONS OF {batch_size} ROWS
        """

        for file, query_dict in self.queries.items():
            file_path = "file:///data-1000/csv/" + file
            print("Processing: ", file_path)
            for query in query_dict.get("nodes", []):
                query_args = {"file": file_path, "query_body": query, "batch_size": self.batch_size}
                node_query = ingest_query.format(**query_args)
                with self.driver.session(database=self.database) as session:
                    session.run(node_query)
            print("Finished Writing Nodes")
            
            for query in query_dict.get("relationships", []):
                query_args = {"file": file_path, "query_body": query, "batch_size": self.batch_size}
                relationship_query = ingest_query.format(**query_args)
                with self.driver.session(database=self.database) as session:
                    session.run(relationship_query)
            print("Finished writing rels.")

    def close(self):
        self.driver.close()


def main():
    f = open('neo4j_conf.json')
    neo4j_conf = json.load(f)
    f.close()
    ingester = SyntheaDataIngester(neo4j_conf, synthea_queries, schema_statements)
    ingester.create_indexes()
    ingester.batch_data_load()
    ingester.close()


if __name__ == "__main__":
    main()