synthea_queries = {
    "patients.csv" : {
        "nodes":("""
        MERGE (p:Patient {id: row.Id})
        ON CREATE SET p.birthDate = datetime(row.BIRTHDATE),
        p.deathDate = row.deathDate,
        p.ssn = row.SSN,
        p.passportNumber = row.PASSPORT,
        p.namePrefix = row.PREFIX,
        p.firstName = row.FIRST,
        p.lastName = row.LAST,
        p.nameSuffix = row.SUFFIX,
        p.maidenName = row.MAIDEN,
        p.maritalStatus = row.MARITAL,
        p.race = row.RACE,
        p.ethnicity = row.ETHNICITY,
        p.gender = row.GENDER,
        p.birthPlace = row.BIRTHPLACE,
        p.address = row.ADDRESS,
        p.city = row.CITY,
        p.state = row.STATE,
        p.county = row.COUNTY,
        p.zip = row.ZIP,
        p.lat = row.LAT,
        p.long = row.LONG,
        p.healthcareExpenses = row.HEALTHCARE_EXPENSES,
        p.healthcareCoverage = row.HEALTHCARE_COVERAGE
        ON MATCH SET p.birthDate = datetime(row.BIRTHDATE),
        p.deathDate = row.deathDate,
        p.ssn = row.SSN,
        p.passportNumber = row.PASSPORT,
        p.namePrefix = row.PREFIX,
        p.firstName = row.FIRST,
        p.lastName = row.LAST,
        p.nameSuffix = row.SUFFIX,
        p.maidenName = row.MAIDEN,
        p.maritalStatus = row.MARITAL,
        p.race = row.RACE,
        p.ethnicity = row.ETHNICITY,
        p.gender = row.GENDER,
        p.birthPlace = row.BIRTHPLACE,
        p.address = row.ADDRESS,
        p.city = row.CITY,
        p.state = row.STATE,
        p.county = row.COUNTY,
        p.zip = row.ZIP,
        p.lat = row.LAT,
        p.long = row.LONG,
        p.healthcareExpenses = row.HEALTHCARE_EXPENSES,
        p.healthcareCoverage = row.HEALTHCARE_COVERAGE
        """,)
    },
    "encounters.csv" : {
        "nodes": (
            """
            MERGE (e:Encounter {id: row.Id})
            ON CREATE SET 
            e.startDateTime = datetime(row.START),
            e.endDateTime = row.STOP,
            e.encounterClass = row.ENCOUNTERCLASS,
            e.code = row.CODE,
            e.description = row.DESCRIPTION,
            e.baseEncounterCost = row.BASE_ENCOUNTER_COST,
            e.totalClaimCost = row.TOTAL_CLAIM_COST,
            e.payerCoveragAmount = row.PAYER_COVERAGE,
            e.reasonCode = row.REASONCODE,
            e.reasonDescription = row.REASONDESCRIPTION
            ON MATCH SET
            e.startDateTime = datetime(row.START),
            e.endDateTime = row.STOP,
            e.encounterClass = row.ENCOUNTERCLASS,
            e.code = row.CODE,
            e.description = row.DESCRIPTION,
            e.baseEncounterCost = row.BASE_ENCOUNTER_COST,
            e.totalClaimCost = row.TOTAL_CLAIM_COST,
            e.payerCoveragAmount = row.PAYER_COVERAGE,
            e.reasonCode = row.REASONCODE,
            e.reasonDescription = row.REASONDESCRIPTION

            MERGE (p:Patient {id: row.PATIENT})

            MERGE (o:Organization {id: row.ORGANIZATION})

            MERGE (pyr:Payer {id: row.PAYER})

            MERGE (pvdr:Provider {id: row.PROVIDER})
            """,
        ),
        "relationships" : (
            """
            MATCH (e:Encounter {id: row.Id})
            MATCH (p:Patient {id: row.PATIENT})
            MERGE (p)-[:HAD]->(e)
            
            WITH e, row
            MATCH (o:Organization {id: row.ORGANIZATION})
            MERGE (e)-[:AT]->(o)

            WITH e, row
            MATCH (pyr:Payer {id: row.PAYER})
            MERGE (e)-[:PAID_FOR_BY]->(pyr)

            WITH e, row
            MATCH (pvdr:Provider {id: row.PROVIDER})
            MERGE (e)-[:WITH]->(pvdr)
            """,
        )
    },
    "allergies.csv": {
        "nodes" : (
            """
            MERGE (a:Allergy {code: row.CODE})
            ON CREATE SET
            a.diagnoseDate = row.START,
            a.endDate = row.STOP,
            a.system = row.SYSTEM,
            a.description = row.DESCRIPTION,
            a.type = row.TYPE,
            a.category = row.CATEGORY,
            a.reaction1 = row.REACTION1,
            a.description1 = row.DESCRIPTION1,
            a.severity1 = row.SEVERITY1,
            a.reaction2 = row.REACTION2,
            a.description2 = row.DESCRIPTION2,
            a.severity2 = row.SEVERITY2
            ON MATCH SET 
            a.diagnoseDate = row.START,
            a.endDate = row.STOP,
            a.system = row.SYSTEM,
            a.description = row.DESCRIPTION,
            a.type = row.TYPE,
            a.category = row.CATEGORY,
            a.reaction1 = row.REACTION1,
            a.description1 = row.DESCRIPTION1,
            a.severity1 = row.SEVERITY1,
            a.reaction2 = row.REACTION2,
            a.description2 = row.DESCRIPTION2,
            a.severity2 = row.SEVERITY2

            MERGE (e:Encounter {id: row.ENCOUNTER})
            """,
        ),
        "relationships" : (
            """
            MATCH (a:Allergy {code: row.CODE})
            MATCH (e:Encounter {id: row.ENCOUNTER})
            MERGE (a)-[:DISCOVERED_AT]->(e)
            """,
        )
    },
    "careplans.csv" : {
        "nodes" : (
            """
            MERGE (c:CarePlan {id: row.Id})
            ON CREATE SET
            c.startDate = row.START,
            c.stopDate = row.STOP,
            c.code = row.CODE,
            c.description = row.DESCRIPTION,
            c.reasonCode = row.REASONCODE,
            c.reasonDescription = row.REASONDESCRIPTION
            ON MATCH SET
            c.startDate = row.START,
            c.stopDate = row.STOP,
            c.code = row.CODE,
            c.description = row.DESCRIPTION,
            c.reasonCode = row.REASONCODE,
            c.reasonDescription = row.REASONDESCRIPTION

            MERGE (e:Encounter {id: row.ENCOUNTER})
            """,
        ),
        "relationships" : (
            """
            MATCH (c:CarePlan {id: row.Id})
            MATCH (e:Encounter {id: row.ENCOUNTER})
            MERGE (c)-[:CREATED_AT]->(e)
            """,
        ),
    },
    "claims.csv" : {
        "nodes" : (
            """
            MERGE (c:Claim {id: row.Id})
            ON CREATE SET
            c.department = row.DEPARTMENTID,
            c.diagnosis1 = row.DIAGNOSIS1,
            c.diagnosis2 = row.DIAGNOSIS2,
            c.diagnosis3 = row.DIAGNOSIS3,
            c.diagnosis4 = row.DIAGNOSIS4,
            c.diagnosis5 = row.DIAGNOSIS5,
            c.diagnosis6 = row.DIAGNOSIS6,
            c.diagnosis7 = row.DIAGNOSIS7,
            c.diagnosis8 = row.DIAGNOSIS8,
            c.currentIllnessDate = row.CURRENTILLNESSDATE,
            c.serviceDate = row.SERVICEDATE,
            c.status1 = row.STATUS1,
            c.status2 = row.STATUS2,
            c.statusP = row.STATUSP,
            c.outstanding1 = row.OUTSTANDING1,
            c.outstanding2 = row.OUTSTANDING2,
            c.outstandingP = row.OUTSTANDINGP,
            c.lastBilledDate1 = row.LASTBILLEDDATE1,
            c.lastBilledDate2 = row.LASTBILLEDDATE2,
            c.lastBilledDateP = row.LASTBILLEDDATEP,
            c.healthcareClaimTypeID1 = row.HEALTHCARECLAIMTYPEID1,
            c.healthcareClaimTypeID2 = row.HEALTHCARECLAIMTYPEID2
            ON MATCH SET 
            c.department = row.DEPARTMENTID,
            c.diagnosis1 = row.DIAGNOSIS1,
            c.diagnosis2 = row.DIAGNOSIS2,
            c.diagnosis3 = row.DIAGNOSIS3,
            c.diagnosis4 = row.DIAGNOSIS4,
            c.diagnosis5 = row.DIAGNOSIS5,
            c.diagnosis6 = row.DIAGNOSIS6,
            c.diagnosis7 = row.DIAGNOSIS7,
            c.diagnosis8 = row.DIAGNOSIS8,
            c.currentIllnessDate = row.CURRENTILLNESSDATE,
            c.serviceDate = row.SERVICEDATE,
            c.status1 = row.STATUS1,
            c.status2 = row.STATUS2,
            c.statusP = row.STATUSP,
            c.outstanding1 = row.OUTSTANDING1,
            c.outstanding2 = row.OUTSTANDING2,
            c.outstandingP = row.OUTSTANDINGP,
            c.lastBilledDate1 = row.LASTBILLEDDATE1,
            c.lastBilledDate2 = row.LASTBILLEDDATE2,
            c.lastBilledDateP = row.LASTBILLEDDATEP,
            c.healthcareClaimTypeID1 = row.HEALTHCARECLAIMTYPEID1,
            c.healthcareClaimTypeID2 = row.HEALTHCARECLAIMTYPEID2

            MERGE (e:Encounter {id: row.APPOINTMENTID})

            MERGE (p1:Payer {id: row.PRIMARYPATIENTINSURANCEID})

            MERGE (p2:Payer {id: row.SECONDARYPATIENTINSURANCEID})
            """,
        ),
        "relationships": (
            """
            MATCH (c:Claim {id: row.Id})
            MATCH (e:Encounter {id: row.APPOINTMENTID})
            MERGE (c)-[:MADE_FOR]->(e)

            WITH c, row
            MATCH (p1:Payer {id: row.PRIMARYPATIENTINSURANCEID})
            MERGE (c)-[:HAS_PRIMARY]->(p1)

            WITH c, row
            MATCH (p2:Payer {id: row.PRIMARYPATIENTINSURANCEID})
            MERGE (c)-[:HAS_SECONDARY]->(p2)
            """,
        ),
    },
    "conditions.csv" : {
            "nodes" : (
                """
                MERGE (c:Condition {code: row.CODE})
                ON CREATE SET
                c.description = row.DESCRIPTION
                ON MATCH SET
                c.description = row.DESCRIPTION

                MERGE (e:Encounter {id: row.ENCOUNTER})
                """,
            ),
            "relationships" : (
                """
                MATCH (e:Encounter {id: row.ENCOUNTER})
                MATCH (c:Condition {code: row.CODE})
                MERGE (c)-[r:DIAGNOSED_AT]->(e)
                ON CREATE SET
                r.diagnoseDate = row.START,
                r.resolveDate = row.STOP
                ON MATCH SET
                r.diagnoseDate = row.START,
                r.resolveDate = row.STOP
                """,
            )
    },
    "devices.csv" : {
            "nodes" : (
                """
                MERGE (d:Device {code: row.CODE})
                ON CREATE SET
                d.description = row.DESCRIPTION,
                d.udi = row.UDI
                ON MATCH SET
                d.description = row.DESCRIPTION,
                d.udi = row.UDI

                MERGE (e:Encounter {id: row.ENCOUNTER})
                """,
            ),
            "relationships" : (
                """
                MATCH (d:Device {code: row.CODE})
                MATCH (e:Encounter {id: row.ENCOUNTER})
                MERGE (d)-[r:ASSOCIATED_AT]->(e)
                ON CREATE SET
                r.startDate = row.START,
                r.endDate = row.STOP
                ON MATCH SET
                r.startDate = row.START,
                r.endDate = row.STOP
                """,
            )
    },
    "imaging_studies.csv" : {
            "nodes" : (
                """
                MERGE (i:ImagingStudy {id: row.Id})
                ON CREATE SET
                i.date = row.DATE,
                i.seriesUID = row.SERIES_UID,
                i.bodySiteCode = row.BODYSITE_CODE,
                i.bodySiteDescription = row.BODYSITE_DESCRIPTION,
                i.modalityCode = row.MODALITY_CODE,
                i.modalityDescription = row.MODALITY_DESCRIPTION,
                i.instanceUID = row.INSTANCE_UID,
                i.sopCode = row.SOP_CODE,
                i.sopDescription = row.SOP_DESCRIPTION,
                i.procedureCode = row.PROCEDURE_CODE
                ON MATCH SET
                i.date = row.DATE,
                i.seriesUID = row.SERIES_UID,
                i.bodySiteCode = row.BODYSITE_CODE,
                i.bodySiteDescription = row.BODYSITE_DESCRIPTION,
                i.modalityCode = row.MODALITY_CODE,
                i.modalityDescription = row.MODALITY_DESCRIPTION,
                i.instanceUID = row.INSTANCE_UID,
                i.sopCode = row.SOP_CODE,
                i.sopDescription = row.SOP_DESCRIPTION,
                i.procedureCode = row.PROCEDURE_CODE

                MERGE (e:Encounter {id: row.ENCOUNTER})
                """,
            ),
            "relationships": (
                """
                MATCH (i:ImagingStudy {id: row.Id})
                MATCH (e:Encounter {id: row.ENCOUNTER})
                MERGE (i)-[:CONDUCTED_AT]->(e)
                """,
            )
    },
    "immunizations.csv" : {
            "nodes" : (
                """
                MERGE (i:Immunization {code: row.CODE})
                ON CREATE SET
                i.description = row.DESCRIPTION
                ON MATCH SET
                i.description = row.DESCRIPTION

                MERGE (e:Encounter {id: row.ENCOUNTER})
                """,
            ),
            "relationships" : (
                """
                MATCH (i:Immunization {code: row.CODE})
                MATCH (e:Encounter {id: row.ENCOUNTER})
                MERGE (i)-[r:ADMINISTERED_AT]->(e)
                ON CREATE SET
                r.date = row.DATE,
                r.cost = row.COST
                ON MATCH SET
                r.date = row.DATE,
                r.cost = row.COST
                """,
            )
    },
    "medications.csv" : {
        "nodes" : (
            """
            MERGE (m:Medication {code: row.CODE})
            ON CREATE SET 
            m.description = row.DESCRIPTION
            ON MATCH SET
            m.description = row.DESCRIPTION

            MERGE (e:Encounter {id: row.ENCOUNTER})

            MERGE (pyr:Payer {id: row.PAYER})
            """,
        ),
        "relationships" : (
            """
            MATCH (m:Medication {code: row.CODE})
            MATCH (e:Encounter {id: row.ENCOUNTER})
            MERGE (m)-[r:PRESCRIBED_AT]->(e)
            ON CREATE SET 
            r.prescriptionStartDate = row.START,
            r.prescriptionEndDate = row.STOP,
            r.reasonCode = row.REASONCODE,
            r.reasonDescription = row.REASONDESCRIPTION,
            r.timesDispensed = row.DISPENSES
            ON MATCH SET 
            r.prescriptionStartDate = row.START,
            r.prescriptionEndDate = row.STOP,
            r.reasonCode = row.REASONCODE,
            r.reasonDescription = row.REASONDESCRIPTION,
            r.timesDispensed = row.DISPENSES

            WITH m, row

            MATCH (pyr:Payer {id: row.PAYER})
            MERGE (m)-[r2:PAID_FOR_BY]->(pyr)
            ON CREATE SET
            r2.baseCost = row.BASE_COST,
            r2.payerCoverage = row.PAYER_COVERAGE,
            r2.totalCost = row.TOTALCOST
            ON MATCH SET
            r2.baseCost = row.BASE_COST,
            r2.payerCoverage = row.PAYER_COVERAGE,
            r2.totalCost = row.TOTALCOST
            """,
        )
    },
    "organizations.csv" : {
        "nodes" : (
            """
            MERGE (o:Organization {id: row.Id})
            ON CREATE SET 
            o.name = row.NAME,
            o.address = row.ADDRESS,
            o.city = row.CITY,
            o.state = row.STATE,
            o.zip = row.ZIP,
            o.lat = row.LAT,
            o.lon = row.LON,
            o.phone = row.PHONE,
            o.revenue = row.REVENUE,
            o.utilization = row.UTILIZATION
            ON MATCH SET
            o.name = row.NAME,
            o.address = row.ADDRESS,
            o.city = row.CITY,
            o.state = row.STATE,
            o.zip = row.ZIP,
            o.lat = row.LAT,
            o.lon = row.LON,
            o.phone = row.PHONE,
            o.revenue = row.REVENUE,
            o.utilization = row.UTILIZATION
            """,
        ),
    },
    "payer_transitions.csv" : {
        "nodes" : (
            """
            MERGE (i:InsuranceCoveragePeriod {patient: row.PATIENT, payer: row.PAYER, startYear: row.START_YEAR, endYear: row.END_YEAR})
            ON CREATE SET
            i.memberId = row.MEMBERID,
            i.ownership = row.OWNERSHIP,
            i.ownerName = row.OWNERNAME
            ON MATCH SET
            i.memberId = row.MEMBERID,
            i.ownership = row.OWNERSHIP,
            i.ownerName = row.OWNERNAME

            MERGE (p:Patient {id: row.PATIENT})
            MERGE (pyr:Payer {id: row.PAYER})
            WITH row WHERE row.SECONDARY_PAYER IS NOT NULL
            MERGE (spyr:Payer {id: row.SECONDARY_PAYER})
            """,
        ),
        "relationships" : (
            """
            MATCH (i:InsuranceCoveragePeriod {patient: row.PATIENT, payer: row.Payer, startYear: row.START_YEAR, endYear: row.END_YEAR})
            MATCH (p:Patient {id: row.PATIENT})
            MERGE (p)-[:INSURED_DURING]->(i)

            WITH i, row
            MATCH (p1:Payer {id: row.PAYER})
            MERGE (i)-[:WITH_PAYER]->(p1)

            WITH i, row
            MATCH (p2:Payer {id: row.SECONDARY_PAYER})
            MERGE (i)-[:WITH_SECONDARY_PAYER]->(p2)
            """,
        )
    }, 
    "payers.csv" : {
        "nodes" : (
            """
            MERGE (p:Payer {id: row.Id})
            ON CREATE SET
            p.name = row.NAME, 
            p.address = row.ADDRESS,
            p.city = row.CITY,
            p.stateHeadquarters = row.STATE_HEADQUARTERED,
            p.zip = row.ZIP,
            p.phone = row.PHONE,
            p.amountCovered = row.AMOUNT_COVERED,
            p.amountUncovered = row.AMOUNT_UNCOVERED,
            p.revenue = row.REVENUE,
            p.numCoveredEncounters = row.COVERED_ENCOUNTERS,
            p.numUncoveredEncounters = row.UNCOVERED_ENCOUNTERS,
            p.numCoveredMedications = row.COVERED_MEDICATIONS,
            p.numUncoveredMedications = row.UNCOVERED_MEDICATIONS,
            p.numCoveredProcedures = row.COVERED_PROCEDURES,
            p.numUncoveredProcedures = row.UNCOVERED_PROCEDURES,
            p.numCoveredImmunizations = row.COVERED_IMMUNIZATIONS,
            p.numUncoveredImmunizations = row.UNCOVERED_IMMUNIZATIONS,
            p.numUniqueCustomers = row.UNIQUE_CUSTOMERS,
            p.avgQOLS = row.QOLS_AVG,
            p.memberMonths = row.MEMBER_MONTHS
            ON MATCH SET
            p.name = row.NAME, 
            p.address = row.ADDRESS,
            p.city = row.CITY,
            p.stateHeadquarters = row.STATE_HEADQUARTERED,
            p.zip = row.ZIP,
            p.phone = row.PHONE,
            p.amountCovered = row.AMOUNT_COVERED,
            p.amountUncovered = row.AMOUNT_UNCOVERED,
            p.revenue = row.REVENUE,
            p.numCoveredEncounters = row.COVERED_ENCOUNTERS,
            p.numUncoveredEncounters = row.UNCOVERED_ENCOUNTERS,
            p.numCoveredMedications = row.COVERED_MEDICATIONS,
            p.numUncoveredMedications = row.UNCOVERED_MEDICATIONS,
            p.numCoveredProcedures = row.COVERED_PROCEDURES,
            p.numUncoveredProcedures = row.UNCOVERED_PROCEDURES,
            p.numCoveredImmunizations = row.COVERED_IMMUNIZATIONS,
            p.numUncoveredImmunizations = row.UNCOVERED_IMMUNIZATIONS,
            p.numUniqueCustomers = row.UNIQUE_CUSTOMERS,
            p.avgQOLS = row.QOLS_AVG,
            p.memberMonths = row.MEMBER_MONTHS
            """,
        )
    },
    "procedures.csv" : {
        "nodes" : (
            """
            MERGE (p:Procedure {code: row.CODE})
            ON CREATE SET
            p.description = row.DESCRIPTION
            ON MATCH SET
            p.description = row.DESCRIPTION

            MERGE (e:Encounter {id: row.ENCOUNTER})
            """,
        ),
        "relationships" : (
            """
            MATCH (p:Procedure {code: row.CODE})
            MATCH (e:Encounter {id: row.ENCOUNTER})
            MERGE (p)-[r:PERFORMED_AT]->(e)
            ON CREATE SET
            r.startDateTime = row.START,
            r.stopDateTime = row.STOP,
            r.reasonCode = row.REASONCODE,
            r.reasonDescription = row.REASONDESCRIPTION,
            r.baseCost = row.BASE_COST
            ON MATCH SET 
            r.startDateTime = row.START,
            r.stopDateTime = row.STOP,
            r.reasonCode = row.REASONCODE,
            r.reasonDescription = row.REASONDESCRIPTION,
            r.baseCost = row.BASE_COST
            """,
        )
    },
    "providers.csv" : {
        "nodes" : (
            """
            MERGE (p:Provider {id: row.Id})
            ON CREATE SET
            p.name = row.NAME,
            p.gender = row.GENDER,
            p.specialty = row.SPECIALTY,
            p.address = row.ADDRESS,
            p.city = row.CITY, 
            p.state = row.STATE,
            p.zip = row.ZIP,
            p.lat = row.LAT,
            p.lon = row.LON,
            p.utilization = row.UTILIZATION
            ON MATCH SET 
            p.name = row.NAME,
            p.gender = row.GENDER,
            p.specialty = row.SPECIALTY,
            p.address = row.ADDRESS,
            p.city = row.CITY, 
            p.state = row.STATE,
            p.zip = row.ZIP,
            p.lat = row.LAT,
            p.lon = row.LON,
            p.utilization = row.UTILIZATION

            MERGE (o:Organization {id: row.ORGANIZATION})
            """,
        ),
        "relationships" : (
            """
            MATCH (p:Provider {id: row.Id})
            MATCH (o:Organization {id: row.ORGANIZATION})
            MERGE (p)-[:EMPLOYED_BY]->(o)
            """,
        )
    },
    "supplies.csv" : {
        "nodes" : {
            """
            MERGE (s:Supply {code: row.CODE})
            ON CREATE SET
            s.description = row.DESCRIPTION
            ON MATCH SET
            s.description = row.DESCRIPTION

            MERGE (e:Encounter {id: row.ENCOUNTER})
            """,
        },
        "relationships" : {
            """
            MATCH (s:Supply {code: row.CODE})
            MATCH (e:Encounter {id: row.ENCOUNTER})
            MERGE (s)-[r:USED_AT]->(e)
            ON CREATE SET
            r.useDate = row.DATE,
            r.quantity = row.QUANTITY
            ON MATCH SET
            r.useDate = row.DATE,
            r.quantity = row.QUANTITY
            """,
        }
    }
}