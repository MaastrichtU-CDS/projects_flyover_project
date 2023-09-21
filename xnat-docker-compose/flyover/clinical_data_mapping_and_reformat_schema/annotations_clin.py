import requests
import sys

# fetch data name
if len(sys.argv) > 1 and isinstance(sys.argv[1], str):
    filename = sys.argv[1]
else:
    filename = input("Please provide the filename of the CSV file that was triplified (without .csv extension):\n")

# ensure it does not have .csv in its name
if ".csv" in filename:
    filename = filename[:filename.rfind(".csv")]


endpoint = "http://rdf-store:7200/repositories/userRepo/statements"

#query to add new classes - (Neoplasm and Radiotherapy) and unit classes for clinical data
queryneoplasm = f"""
PREFIX db: <http://data.local/rdf/ontology/>
PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
PREFIX lidicom: <https://johanvansoest.nl/ontologies/LinkedDicom/>
PREFIX roo: <http://www.cancerdata.org/roo/>
PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
INSERT
    {{

    GRAPH <http://annotations_clin/>
    {{

     db:{filename}.years rdf:type owl:Class.

     db:{filename}.years rdfs:label "Years".

     db:{filename}.days rdf:type owl:Class.

     db:{filename}.days rdfs:label "Days".

     db:{filename}.Gray rdf:type owl:Class.

     db:{filename}.Gray rdfs:label "Gy".

     db:{filename}.radiotherapyClass rdf:type owl:Class.

     db:{filename}.radiotherapyClass dbo:table db:{filename}.

     db:{filename}.neoplasmClass rdf:type owl:Class.

     db:{filename}.neoplasmClass dbo:table db:{filename}.

     ?patient dbo:has_column ?neoplasm, ?radiotherapy.

     ?neoplasm rdf:type db:{filename}.neoplasmClass.

     ?radiotherapy rdf:type db:{filename}.radiotherapyClass.

}}
}}
where
{{
    BIND(IRI(CONCAT(str(?patient), "/neoplasm")) as ?neoplasm).

    BIND(IRI(CONCAT(str(?patient), "/radiotherapy")) as ?radiotherapy).

    ?patient rdf:type db:{filename}.

}}
"""

#query for new predicates and equivalencies from NCIT and ROO for radiomic data
queryequiv = f"""

PREFIX db: <http://data.local/rdf/ontology/>
PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
PREFIX lidicom: <https://johanvansoest.nl/ontologies/LinkedDicom/>
PREFIX roo: <http://www.cancerdata.org/roo/>
PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
INSERT
    {{
    GRAPH <http://annotations_clin/>
    {{

     #replace the predicate dbo:has_column for each table row instance --> column instance with new predicates

     ?clinical roo:P100061 ?patientID.   #has_identifier

     ?clinical roo:P100018 ?gender.      #has_biological_sex

     ?clinical roo:P100000 ?age.

     ?age roo:P100027 db:{filename}.years.

     ?clinical roo:P100022 ?hpv.         #has_finding

     #?clinical roo:P100214 ?asa.         #has_measurement

     #?clinical roo:P100218 ?whostatus.   #has_WHO_status

     ?clinical roo:P100029 ?neoplasm.

     ?neoplasm roo:P100244 ?tstage.      #has_T_stage

     ?neoplasm roo:P100242 ?nstage.      #has_N_stage

     ?neoplasm roo:P100241 ?mstage.      #has_M_stage

     ?neoplasm roo:P100219 ?ajcc.        #has_AJCC_stage

     ?neoplasm roo:P100202 ?tumour.      #tumourSite

     ?neoplasm roo:P10032 ?metastasis.   #has_metastasis

     ?neoplasm roo:P100022 ?regionalrecurrence, ?regionalrecurrencedays, ?metastasisdays.  #has_finding

    #?localrecurrencedays roo:P100027 db:{filename}.days.

     ?regionalrecurrencedays roo:P100027 db:{filename}.days.

     ?metastasisdays roo:P100027 db:{filename}.days.

     ?clinical roo:P100403 ?radiotherapy. #treated_by

     ?radiotherapy roo:P100027 ?rttotaldays. #has_unit

     ?rttotaldays roo:P100027 db:{filename}.days.

     #?radiotherapy roo:P100023 ?graytotaldose. #has_dose

     #?graytotaldose roo:P100027 db:{filename}.Gray.

     #?radiotherapy roo:P100214 ?graydoseperfraction.   #has_dose_per_fraction

     #?graydoseperfraction roo:P100027 db:{filename}.Gray.

     #?radiotherapy roo:P100224 ?rtfractions. #has_fraction_count

     ?clinical roo:P100403 ?surgery.     #treated_by

     ?clinical roo:P100028 ?survival.    #has_vital_status

     ?clinical roo:P100026 ?overallsurvivaldays.

     ?overallsurvivaldays roo:P100027 db:{filename}.days.

     ?clinical roo:P100231 ?chemo.        #chemo_administered


     #set new equivalencies for the classes

     db:{filename} owl:equivalentClass ncit:C16960.

     db:{filename}.Patient_\# owl:equivalentClass ncit:C25364.

     db:{filename}.Sex owl:equivalentClass ncit:C28421.

     db:{filename}.Age owl:equivalentClass roo:C100003.

     db:{filename}.HPV_status owl:equivalentClass ncit:C14226.

     #db:{filename}.pretreat_hb_in_mmolperlitre owl:equivalentClass roo:asaScore.

     #db:{filename}.performance_status_ecog owl:equivalentClass ncit:C105721.

     db:{filename}.T-stage owl:equivalentClass ncit:C48885.

     db:{filename}.N-stage owl:equivalentClass ncit:C48884.

     db:{filename}.M-stage owl:equivalentClass ncit:C48883.

     db:{filename}.TNM_group_stage owl:equivalentClass ncit:C38027.

     db:{filename}.Surgery owl:equivalentClass ncit:C17173.

     db:{filename}.Primary_Site owl:equivalentClass ncit:C3263.

     #db:{filename}.event_recurrence_metastatic_free_survival owl:equivalentClass roo:eventrecurrence.

     #db:{filename}.recurrence_metastatic_free_survival_in_days owl:equivalentClass roo:eventrecurrencedays.

     #db:{filename}.event_local_recurrence owl:equivalentClass roo:localrecurrence.

     #db:{filename}.local_recurrence_in_days owl:equivalentClass roo:localrecurrencedays.

     db:{filename}.Locoregional owl:equivalentClass roo:regionalrecurrence.

     db:{filename}.Time_diagnosis_to_LR_\(days\) owl:equivalentClass roo:regionalrecurrencedays.

     db:{filename}.Distant owl:equivalentClass ncit:C19151.

     db:{filename}.Time_diagnosis_to_DM_\(days\) owl:equivalentClass roo:metastasisdays.

     db:{filename}.Death owl:equivalentClass ncit:C25717.

     db:{filename}.Time_diagnosis_to_Death_\(days\) owl:equivalentClass roo:overallsurvivaldays.

     db:{filename}.Therapy owl:equivalentClass ncit:C15632.

     db:{filename}.Time_diagnosis_to_end_treatment_\(days\) owl:equivalentClass roo:rttotaldays.

     #db:{filename}.radiotherapy_refgydose_total_highriskgtv owl:equivalentClass roo:graytotaldose.

     #db:{filename}.radiotherapy_refgydose_perfraction_highriskgtv owl:equivalentClass roo:graydoseperfraction.

     #db:{filename}.radiotherapy_number_fractions_highriskgtv owl:equivalentClass roo:rttotalfraction.

     db:{filename}.years owl:equivalentClass ncit:C29848.

     db:{filename}.days owl:equivalentClass ncit:C25301.

     db:{filename}.Gray owl:equivalentClass ncit:C18063.

     db:{filename}.neoplasmClass owl:equivalentClass ncit:C3262.

     db:{filename}.radiotherapyClass owl:equivalentClass ncit:C15313.

     dbo:has_value owl:sameAs roo:P100042.    #has_value

     dbo:has_unit owl:sameAs roo:P100047.    #has_value

     dbo:cell_of rdf:type owl:ObjectProperty;
                 owl:inverseOf dbo:has_cell.

    }}
    }}

    where

    {{

    ?clinical rdf:type db:{filename}.

    ?clinical dbo:has_column ?patientID, ?gender, ?age, ?tumour, ?hpv, ?tstage, ?nstage, ?mstage, ?ajcc, ?surgery, ?chemo, ?rttotaldays, ?survival, ?overallsurvivaldays, ?metastasis, ?metastasisdays, ?neoplasm, ?radiotherapy, ?regionalrecurrence, ?regionalrecurrencedays.

    ?patientID rdf:type db:{filename}.Patient_\#.

    ?neoplasm rdf:type db:{filename}.neoplasmClass.

    ?radiotherapy rdf:type db:{filename}.radiotherapyClass.

    ?gender rdf:type db:{filename}.Sex.

    ?age rdf:type db:{filename}.Age.

    ?tumour rdf:type db:{filename}.Primary_Site.

    #?whostatus rdf:type db:{filename}.performance_status_ecog.

    ?hpv rdf:type db:{filename}.HPV_status.

    ?tstage rdf:type db:{filename}.T-stage.

    ?nstage rdf:type db:{filename}.N-stage.

    ?mstage rdf:type db:{filename}.M-stage.

    ?ajcc rdf:type db:{filename}.TNM_group_stage.

    #?asa rdf:type db:{filename}.pretreat_hb_in_mmolperlitre.

    ?surgery rdf:type db:{filename}.Surgery.

    ?chemo rdf:type db:{filename}.Therapy.

    ?rttotaldays rdf:type db:{filename}.Time_diagnosis_to_end_treatment_\(days\).

    #?graytotaldose rdf:type db:{filename}.radiotherapy_refgydose_total_highriskgtv.

    #?graydoseperfraction rdf:type db:{filename}.radiotherapy_refgydose_perfraction_highriskgtv.

    #?rtfractions rdf:type db:{filename}.radiotherapy_number_fractions_highriskgtv.

    ?survival rdf:type db:{filename}.Death.

    ?overallsurvivaldays rdf:type db:{filename}.Time_diagnosis_to_Death_\(days\).

    #?eventrecurrence rdf:type db:{filename}.event_recurrence_metastatic_free_survival.

    #?eventrecurrencedays rdf:type db:{filename}.recurrence_metastatic_free_survival_in_days.

    #?localrecurrence rdf:type db:{filename}.event_local_recurrence.

    #?localrecurrencedays rdf:type db:{filename}.local_recurrence_in_days.

    ?regionalrecurrence rdf:type db:{filename}.Locoregional.

    ?regionalrecurrencedays rdf:type db:{filename}.Time_diagnosis_to_LR_\(days\).

    ?metastasis rdf:type db:{filename}.Distant.

    ?metastasisdays rdf:type db:{filename}.Time_diagnosis_to_DM_\(days\).

    }}

"""

#query to replace empty cells of HPV column with "Unknown"
queryUnknown = f"""
PREFIX db: <http://data.local/rdf/ontology/>
PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
PREFIX lidicom: <https://johanvansoest.nl/ontologies/LinkedDicom/>
PREFIX roo: <http://www.cancerdata.org/roo/>
PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
INSERT
    {{

    GRAPH <http://annotations_clin/>
    {{
       ?hpvv dbo:has_cell ?hpvcell.
       ?hpvcell dbo:has_value "Unknown".
    }}
    }}
        WHERE {{
            ?patient roo:P100022 ?hpvv.
            FILTER NOT EXISTS {{?hpvv dbo:has_cell ?hpvcell}}.
            BIND(IRI(CONCAT(str(?hpvv), "/value")) as ?hpvcell).
    }}
    """

#call this function to run a query on your endpoint
def runQuery(endpoint, query):
    annotationResponse = requests.post(endpoint,
                                   data="update=" + query,
                                   headers={
                                       "Content-Type": "application/x-www-form-urlencoded",
                                       # "Accept": "application/json"
                                   })
    output = annotationResponse.status_code

    if output == 204:
        print("Mapping added successfully")
    else:
        print("Mapping incorrect")


runQuery(endpoint, queryneoplasm)
runQuery(endpoint, queryequiv)
runQuery(endpoint, queryUnknown)

#addmapping function to map the categorical values to its semantical code for clinical data
def addMapping(localTerm, targetClass, superClass):
    queryval = """
            PREFIX db: <http://data.local/rdf/ontology/>
            PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
            PREFIX lidicom: <https://johanvansoest.nl/ontologies/LinkedDicom/>
            PREFIX roo: <http://www.cancerdata.org/roo/>
            PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            INSERT
                {
                 GRAPH <http://annotations_clin/> {
                    ?term rdf:type owl:Class ;
                     owl:equivalentClass [ owl:intersectionOf
                                                    ( [ rdf:type owl:Restriction ;
                                                        owl:onProperty dbo:cell_of ;
                                                        owl:someValuesFrom ?superClass;
                                                      ]
                                                      [ rdf:type owl:Restriction ;
                                                        owl:onProperty dbo:has_value ;
                                                        owl:hasValue ?localValue;
                                                      ]
                                                    ) ;
                                 rdf:type owl:Class
                               ] ;
                     rdfs:subClassOf ?superClass .
                }
            } WHERE {
                BIND(<%s> AS ?term).
                BIND(<%s> AS ?superClass).
                BIND("%s"^^xsd:string AS ?localValue).
            }
            """ % (targetClass, superClass, localTerm)

    annotationResponse = requests.post(endpoint,
                                       data="update=" + queryval,
                                       headers={
                                           "Content-Type": "application/x-www-form-urlencoded"
                                       })
    output = annotationResponse.status_code

    if output == 204:
        print("Mapping added successfully")
    else:
        print("Mapping incorrect")


# T stage
addMapping("Tx", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48737",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48885")
addMapping("T1", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48720",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48885")
addMapping("T2", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48724",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48885")
addMapping("T3", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48728",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48885")
addMapping("T4", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48732",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48885")
addMapping("T4a", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48732",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48885")
addMapping("T4b", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48732",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48885")

# N stage
addMapping("N0", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48705",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48884")
addMapping("N1", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48706",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48884")
addMapping("N2", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48786",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48884")
addMapping("N2a", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48786",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48884")
addMapping("N2b", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48786",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48884")
addMapping("N2c", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48786",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48884")
addMapping("N3", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48714",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48884")
addMapping("N3b", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48714",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48884")

# M stage
addMapping("M0", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48699",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48883")
addMapping("Mx", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48704",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48883")

# gender
addMapping("F", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C16576",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28421")
addMapping("M", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C20197",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28421")

# survival
addMapping("1", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28554",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C25717")
addMapping("0", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C37987",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C25717")
# 0=alive
# 1=dead

# tumorlocation
addMapping("Oropharynx", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12762",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C3263")
addMapping("Larynx", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12420",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C3263")
addMapping("Hypopharynx", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12246",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C3263")
addMapping("Nasopharynx", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12423",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C3263")
addMapping("unknown", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C00000",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C3263")

# hpv
addMapping("%2B", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C128839",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C14226")
addMapping("-", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C131488",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C14226")
addMapping("N/A", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C10000",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C14226")

# ajcc
addMapping("N/A", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C00000",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping("stage I", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27966",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping("Stade I", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27966",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping("stage I", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27966",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")

addMapping("Stade II", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28054",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping("stage II", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28054",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping("StageII", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28054",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping("Stage II", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28054",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping("stage IIB", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28054",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping("Stage IIB", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28054",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")

addMapping("stage III", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27970",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping("Stade III", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27970",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping("Stage III", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27970",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")

addMapping("Stage IV", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27971",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping("stage IV", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27971",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")

addMapping("Stade IVA", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27971",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping("Stage IVA", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27971",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping("stage IVA", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27971",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping("stage IVB", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27971",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping("Stade IVB", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27971",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")

# chemo
addMapping("chemo radiation", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C94626",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C15632")
addMapping("radiation", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C15313",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C15632")
