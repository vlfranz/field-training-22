schema_statements = (
    """CREATE CONSTRAINT patient_id IF NOT EXISTS FOR (p:Patient) REQUIRE (p.id) IS NODE KEY;""",
    """CREATE CONSTRAINT encounter_id IF NOT EXISTS FOR (e:Encounter) REQUIRE (e.id) IS NODE KEY;"""
)